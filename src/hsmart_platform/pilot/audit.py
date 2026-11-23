"""Per-tenant hash-linked audit records (tamper-evident pilot, not WORM storage)."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import AuditEvent, Tenant

GENESIS = "0" * 64


def canonical_json(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def append_audit(
    session: Session,
    *,
    tenant_id: str,
    actor: str,
    action: str,
    resource: str,
    outcome: str,
    reason_code: str,
    payload_sha256: str,
    correlation_id: str | None = None,
) -> AuditEvent:
    # The tenant-row lock serializes sequence allocation on PostgreSQL.
    tenant = session.scalar(select(Tenant).where(Tenant.id == tenant_id).with_for_update())
    if tenant is None:
        raise ValueError("tenant_not_found")
    previous = session.scalar(
        select(AuditEvent).where(AuditEvent.tenant_id == tenant_id).order_by(AuditEvent.sequence.desc()).limit(1)
    )
    sequence = 1 if previous is None else previous.sequence + 1
    previous_hash = GENESIS if previous is None else previous.event_hash
    occurred_at = datetime.now(timezone.utc)
    body = {
        "tenant_id": tenant_id,
        "sequence": sequence,
        "actor": actor,
        "action": action,
        "resource": resource,
        "outcome": outcome,
        "reason_code": reason_code,
        "correlation_id": correlation_id or str(uuid.uuid4()),
        "payload_sha256": payload_sha256,
        "previous_hash": previous_hash,
        "occurred_at": occurred_at.isoformat(),
    }
    event_hash = hashlib.sha256(bytes.fromhex(previous_hash) + canonical_json(body)).hexdigest()
    event_body = {**body, "occurred_at": occurred_at}
    event = AuditEvent(**event_body, event_hash=event_hash)
    session.add(event)
    session.flush()
    return event


def verify_audit_chain(session: Session, tenant_id: str) -> bool:
    events = session.scalars(
        select(AuditEvent).where(AuditEvent.tenant_id == tenant_id).order_by(AuditEvent.sequence.asc())
    ).all()
    previous_hash = GENESIS
    for expected_sequence, event in enumerate(events, start=1):
        occurred_at = event.occurred_at
        if occurred_at.tzinfo is None:
            occurred_at = occurred_at.replace(tzinfo=timezone.utc)
        body = {
            "tenant_id": event.tenant_id,
            "sequence": event.sequence,
            "actor": event.actor,
            "action": event.action,
            "resource": event.resource,
            "outcome": event.outcome,
            "reason_code": event.reason_code,
            "correlation_id": event.correlation_id,
            "payload_sha256": event.payload_sha256,
            "previous_hash": event.previous_hash,
            "occurred_at": occurred_at.isoformat(),
        }
        expected_hash = hashlib.sha256(bytes.fromhex(previous_hash) + canonical_json(body)).hexdigest()
        if event.sequence != expected_sequence or event.previous_hash != previous_hash or event.event_hash != expected_hash:
            return False
        previous_hash = event.event_hash
    return True
