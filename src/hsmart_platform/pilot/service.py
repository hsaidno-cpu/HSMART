"""Registry, entitlement and synchronous invocation service for the local pilot."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Capability, CapabilityGrant, CapabilityVersion, Installation, Invocation
from ..settings import Settings
from .audit import append_audit
from .auth import Principal, require_scope
from .errors import AuthorizationError, ConflictError, PilotError
from .runtime import execute


def _digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def grant_capability(
    session: Session,
    *,
    tenant_id: str,
    capability_key: str,
    subject: str,
    permission: str,
    granted_by: str,
    evidence_ref: str,
    expires_at: datetime | None = None,
) -> CapabilityGrant:
    capability = session.scalar(
        select(Capability).where(
            Capability.tenant_id == tenant_id,
            Capability.capability_key == capability_key,
            Capability.status == "ACTIVE",
        )
    )
    if capability is None:
        raise PilotError("capability_not_found", 404)
    if permission not in {"capability.invoke", "capability.read", "registry.manage"}:
        raise PilotError("unsupported_grant_permission", 422)
    if not evidence_ref.strip():
        raise PilotError("grant_evidence_required", 422)
    grant = CapabilityGrant(
        tenant_id=tenant_id,
        capability_id=capability.id,
        subject=subject,
        permission=permission,
        granted_by=granted_by,
        evidence_ref=evidence_ref,
        expires_at=expires_at,
    )
    session.add(grant)
    session.flush()
    append_audit(
        session,
        tenant_id=tenant_id,
        actor=granted_by,
        action="ENTITLEMENT_GRANT_CREATED",
        resource=capability_key,
        outcome="ALLOW",
        reason_code="EXPLICIT_GRANT",
        payload_sha256=_digest({"subject": subject, "permission": permission, "evidence_ref": evidence_ref}),
    )
    session.commit()
    return grant


def _has_grant(session: Session, principal: Principal, capability: Capability, permission: str) -> bool:
    now = datetime.now(timezone.utc)
    grants = session.scalars(
        select(CapabilityGrant).where(
            CapabilityGrant.tenant_id == principal.tenant_id,
            CapabilityGrant.capability_id == capability.id,
            CapabilityGrant.subject == principal.subject,
            CapabilityGrant.permission == permission,
            CapabilityGrant.revoked_at.is_(None),
        )
    ).all()
    for grant in grants:
        expiry = grant.expires_at
        if expiry is not None:
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if expiry <= now:
                continue
        return True
    return False


def list_capabilities(session: Session, principal: Principal) -> list[dict[str, Any]]:
    require_scope(principal, "capability.read")
    rows = session.execute(
        select(Capability, CapabilityVersion)
        .join(CapabilityVersion, CapabilityVersion.capability_id == Capability.id)
        .where(
            Capability.tenant_id == principal.tenant_id,
            Capability.status == "ACTIVE",
            CapabilityVersion.status == "PUBLISHED",
            CapabilityVersion.rights_status == "CLEARED",
        )
        .order_by(Capability.capability_key, CapabilityVersion.version)
    ).all()
    result = []
    for capability, version in rows:
        if _has_grant(session, principal, capability, "capability.read") or _has_grant(
            session, principal, capability, "capability.invoke"
        ):
            result.append({
                "capability_id": capability.capability_key,
                "version": version.version,
                "display_name": capability.display_name,
                "entrypoint": version.entrypoint,
                "artifact_sha256": version.artifact_sha256,
            })
    return result


def _deny_invocation(
    session: Session,
    principal: Principal,
    *,
    capability_key: str,
    reason_code: str,
    payload_sha256: str,
) -> None:
    append_audit(
        session,
        tenant_id=principal.tenant_id,
        actor=principal.subject,
        action="CAPABILITY_INVOCATION_DENIED",
        resource=capability_key,
        outcome="DENY",
        reason_code=reason_code,
        payload_sha256=payload_sha256,
    )
    session.commit()
    raise AuthorizationError(reason_code)


def invoke_capability(
    session: Session,
    settings: Settings,
    principal: Principal,
    *,
    capability_key: str,
    version: str,
    payload: dict[str, Any],
    idempotency_key: str,
    host_id: str | None = None,
) -> dict[str, Any]:
    actual_host = host_id or settings.pilot_host_id
    request_digest = _digest({
        "capability_id": capability_key,
        "version": version,
        "payload": payload,
        "host_id": actual_host,
    })
    if "capability.invoke" not in principal.scopes:
        _deny_invocation(
            session, principal, capability_key=capability_key,
            reason_code="required_scope_missing", payload_sha256=request_digest,
        )
    if not idempotency_key or len(idempotency_key) > 200:
        raise PilotError("valid_idempotency_key_required", 422)
    if not isinstance(payload, dict):
        raise PilotError("payload_must_be_object", 422)

    capability = session.scalar(
        select(Capability).where(
            Capability.tenant_id == principal.tenant_id,
            Capability.capability_key == capability_key,
            Capability.status == "ACTIVE",
        )
    )
    if capability is None:
        raise PilotError("capability_not_found", 404)
    version_record = session.scalar(
        select(CapabilityVersion).where(
            CapabilityVersion.capability_id == capability.id,
            CapabilityVersion.version == version,
        )
    )
    if version_record is None or version_record.status != "PUBLISHED":
        raise PilotError("capability_version_not_published", 404)
    if version_record.rights_status != "CLEARED" or not version_record.rights_evidence_ref:
        _deny_invocation(
            session, principal, capability_key=capability_key,
            reason_code="distribution_rights_not_cleared", payload_sha256=request_digest,
        )
    if not _has_grant(session, principal, capability, "capability.invoke"):
        _deny_invocation(
            session, principal, capability_key=capability_key,
            reason_code="capability_entitlement_missing", payload_sha256=request_digest,
        )
    installation = session.scalar(
        select(Installation).where(
            Installation.tenant_id == principal.tenant_id,
            Installation.capability_version_id == version_record.id,
            Installation.host_id == actual_host,
            Installation.state == "ACTIVE",
            Installation.package_digest == version_record.artifact_sha256,
        )
    )
    if installation is None:
        _deny_invocation(
            session, principal, capability_key=capability_key,
            reason_code="capability_not_active_on_host", payload_sha256=request_digest,
        )

    # Replays are returned only after current scope, rights, entitlement and installation
    # state have been checked. Revocation must take effect even for prior idempotent requests.
    existing = session.scalar(
        select(Invocation).where(
            Invocation.tenant_id == principal.tenant_id,
            Invocation.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        if existing.request_sha256 != request_digest:
            raise ConflictError("idempotency_key_reused_with_different_request")
        if existing.status != "COMPLETED" or existing.result is None:
            raise ConflictError("invocation_not_complete")
        return {
            "invocation_id": existing.id,
            "status": existing.status,
            "result": existing.result,
            "trace_id": existing.trace_id,
            "idempotent_replay": True,
        }

    invocation = Invocation(
        tenant_id=principal.tenant_id,
        capability_version_id=version_record.id,
        subject=principal.subject,
        host_id=actual_host,
        idempotency_key=idempotency_key,
        request_sha256=request_digest,
        status="RUNNING",
        trace_id=str(uuid.uuid4()),
    )
    session.add(invocation)
    session.flush()
    try:
        result = execute(version_record.entrypoint, payload)
        invocation.result = result
        invocation.status = "COMPLETED"
        invocation.completed_at = datetime.now(timezone.utc)
        append_audit(
            session,
            tenant_id=principal.tenant_id,
            actor=principal.subject,
            action="CAPABILITY_INVOKED",
            resource=f"{capability_key}@{version}",
            outcome="ALLOW",
            reason_code="ENTITLEMENT_AND_HOST_VERIFIED",
            payload_sha256=request_digest,
            correlation_id=invocation.trace_id,
        )
        session.commit()
    except Exception:
        session.rollback()
        raise
    return {
        "invocation_id": invocation.id,
        "status": invocation.status,
        "result": result,
        "trace_id": invocation.trace_id,
        "idempotent_replay": False,
    }
