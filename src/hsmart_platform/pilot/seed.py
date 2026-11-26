"""Small deterministic tenant bootstrap helper for the local pilot."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Tenant


def ensure_tenant(session: Session, slug: str, display_name: str) -> Tenant:
    tenant = session.scalar(select(Tenant).where(Tenant.slug == slug))
    if tenant is None:
        tenant = Tenant(slug=slug, display_name=display_name, status="active")
        session.add(tenant)
        session.flush()
    return tenant
