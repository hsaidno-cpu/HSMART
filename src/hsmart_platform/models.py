"""Platform persistence models. Schema changes are Alembic-owned."""
from __future__ import annotations

from datetime import datetime, timezone
import uuid

from sqlalchemy import DateTime, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = (UniqueConstraint("slug", name="uq_tenants_slug"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    outbox_messages: Mapped[list["OutboxMessage"]] = relationship(back_populates="tenant")


class OutboxMessage(Base):
    __tablename__ = "outbox_messages"
    __table_args__ = (
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_outbox_tenant_idempotency_key"),
        Index("ix_outbox_status_available", "status", "available_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False)
    topic: Mapped[str] = mapped_column(String(120), nullable=False)
    aggregate_id: Mapped[str] = mapped_column(String(120), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="pending")
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    tenant: Mapped[Tenant] = relationship(back_populates="outbox_messages")


class Capability(Base):
    __tablename__ = "capabilities"
    __table_args__ = (
        UniqueConstraint("tenant_id", "capability_key", name="uq_capability_tenant_key"),
        Index("ix_capability_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False)
    capability_key: Mapped[str] = mapped_column(String(120), nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    publisher_id: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class CapabilityVersion(Base):
    __tablename__ = "capability_versions"
    __table_args__ = (
        UniqueConstraint("capability_id", "version", name="uq_capability_version"),
        Index("ix_capability_version_status", "capability_id", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    capability_id: Mapped[str] = mapped_column(ForeignKey("capabilities.id", ondelete="RESTRICT"), nullable=False)
    version: Mapped[str] = mapped_column(String(80), nullable=False)
    entrypoint: Mapped[str] = mapped_column(String(160), nullable=False)
    manifest: Mapped[dict] = mapped_column(JSON, nullable=False)
    artifact_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    artifact_path: Mapped[str] = mapped_column(Text, nullable=False)
    signer_key_id: Mapped[str] = mapped_column(String(120), nullable=False)
    signature_b64: Mapped[str] = mapped_column(Text, nullable=False)
    license_id: Mapped[str] = mapped_column(String(120), nullable=False)
    rights_status: Mapped[str] = mapped_column(String(24), nullable=False)
    rights_evidence_ref: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="PUBLISHED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class CapabilityGrant(Base):
    __tablename__ = "capability_grants"
    __table_args__ = (
        Index("ix_capability_grant_subject", "tenant_id", "subject", "capability_id", "permission"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False)
    capability_id: Mapped[str] = mapped_column(ForeignKey("capabilities.id", ondelete="RESTRICT"), nullable=False)
    subject: Mapped[str] = mapped_column(String(240), nullable=False)
    permission: Mapped[str] = mapped_column(String(80), nullable=False)
    granted_by: Mapped[str] = mapped_column(String(240), nullable=False)
    evidence_ref: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class Installation(Base):
    __tablename__ = "installations"
    __table_args__ = (
        UniqueConstraint("tenant_id", "capability_version_id", "host_id", name="uq_installation_tenant_version_host"),
        Index("ix_installation_tenant_state", "tenant_id", "state"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False)
    capability_version_id: Mapped[str] = mapped_column(ForeignKey("capability_versions.id", ondelete="RESTRICT"), nullable=False)
    host_id: Mapped[str] = mapped_column(String(160), nullable=False)
    package_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    installed_path: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str] = mapped_column(String(24), nullable=False, default="INSTALLED")
    installed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    disabled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Invocation(Base):
    __tablename__ = "invocations"
    __table_args__ = (
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_invocation_tenant_idempotency"),
        Index("ix_invocation_tenant_created", "tenant_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False)
    capability_version_id: Mapped[str] = mapped_column(ForeignKey("capability_versions.id", ondelete="RESTRICT"), nullable=False)
    subject: Mapped[str] = mapped_column(String(240), nullable=False)
    host_id: Mapped[str] = mapped_column(String(160), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(200), nullable=False)
    request_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACCEPTED")
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    trace_id: Mapped[str] = mapped_column(String(36), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    __table_args__ = (
        UniqueConstraint("tenant_id", "sequence", name="uq_audit_tenant_sequence"),
        Index("ix_audit_tenant_time", "tenant_id", "occurred_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    actor: Mapped[str] = mapped_column(String(240), nullable=False)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    resource: Mapped[str] = mapped_column(String(240), nullable=False)
    outcome: Mapped[str] = mapped_column(String(24), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(120), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(36), nullable=False)
    payload_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    event_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
