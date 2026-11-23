"""REST API for the HSMART first-party local pilot."""
from __future__ import annotations

from collections.abc import Generator
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Capability
from .auth import Principal, authenticate_token, require_scope
from .errors import PilotError
from .service import grant_capability, invoke_capability, list_capabilities, revoke_capability_grant

router = APIRouter(prefix="/v1", tags=["KM2 Pilot"])


def get_db(request: Request) -> Generator[Session, None, None]:
    session = request.app.state.session_factory()
    try:
        yield session
    finally:
        session.close()


def get_principal(request: Request, authorization: str | None = Header(default=None)) -> Principal:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="bearer_token_required")
    try:
        return authenticate_token(authorization[7:].strip(), request.app.state.settings)
    except PilotError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.code) from exc


class InvokeRequest(BaseModel):
    capability_id: str = Field(min_length=1, max_length=120)
    version: str = Field(min_length=1, max_length=80)
    payload: dict[str, Any]
    host_id: str | None = Field(default=None, max_length=160)


class GrantRequest(BaseModel):
    capability_id: str = Field(min_length=1, max_length=120)
    subject: str = Field(min_length=1, max_length=240)
    permission: str
    evidence_ref: str = Field(min_length=1, max_length=2000)
    expires_at: datetime | None = None


@router.get("/capabilities")
def discover_capabilities(
    principal: Principal = Depends(get_principal),
    session: Session = Depends(get_db),
):
    try:
        return {"items": list_capabilities(session, principal)}
    except PilotError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.code) from exc


@router.post("/invoke")
def invoke(
    request: Request,
    body: InvokeRequest,
    idempotency_key: str = Header(alias="Idempotency-Key", min_length=8, max_length=200),
    principal: Principal = Depends(get_principal),
    session: Session = Depends(get_db),
):
    try:
        return invoke_capability(
            session, request.app.state.settings, principal,
            capability_key=body.capability_id, version=body.version,
            payload=body.payload, idempotency_key=idempotency_key, host_id=body.host_id,
        )
    except PilotError as exc:
        session.rollback()
        raise HTTPException(status_code=exc.status_code, detail=exc.code) from exc


@router.post("/registry/grants", status_code=201)
def create_grant(
    body: GrantRequest,
    principal: Principal = Depends(get_principal),
    session: Session = Depends(get_db),
):
    try:
        require_scope(principal, "entitlement.grant")
        capability = session.scalar(
            select(Capability).where(
                Capability.tenant_id == principal.tenant_id,
                Capability.capability_key == body.capability_id,
            )
        )
        if capability is None:
            raise PilotError("capability_not_found", 404)
        grant = grant_capability(
            session,
            tenant_id=principal.tenant_id,
            capability_key=body.capability_id,
            subject=body.subject,
            permission=body.permission,
            granted_by=principal.subject,
            evidence_ref=body.evidence_ref,
            expires_at=body.expires_at,
        )
        return {"grant_id": grant.id, "status": "ACTIVE"}
    except PilotError as exc:
        session.rollback()
        raise HTTPException(status_code=exc.status_code, detail=exc.code) from exc

 
class RevokeGrantRequest(BaseModel):
    evidence_ref: str = Field(min_length=1, max_length=2000)


@router.post("/registry/grants/{grant_id}/revoke")
def revoke_grant(
    grant_id: str,
    body: RevokeGrantRequest,
    principal: Principal = Depends(get_principal),
    session: Session = Depends(get_db),
):
    try:
        require_scope(principal, "entitlement.grant")
        grant = revoke_capability_grant(
            session,
            tenant_id=principal.tenant_id,
            grant_id=grant_id,
            revoked_by=principal.subject,
            evidence_ref=body.evidence_ref,
        )
        return {"grant_id": grant.id, "status": "REVOKED" if grant.revoked_at else "ACTIVE"}
    except PilotError as exc:
        session.rollback()
        raise HTTPException(status_code=exc.status_code, detail=exc.code) from exc
