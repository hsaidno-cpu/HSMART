"""Add the KM2 local registry, entitlement, installer and audit pilot.

Revision ID: 0002_registry_installer_pilot
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_registry_installer_pilot"
down_revision = "0001_platform_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "capabilities",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("capability_key", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("publisher_id", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("tenant_id", "capability_key", name="uq_capability_tenant_key"),
    )
    op.create_index("ix_capability_tenant_status", "capabilities", ["tenant_id", "status"])
    op.create_table(
        "capability_versions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("capability_id", sa.String(length=36), sa.ForeignKey("capabilities.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("version", sa.String(length=80), nullable=False),
        sa.Column("entrypoint", sa.String(length=160), nullable=False),
        sa.Column("manifest", sa.JSON(), nullable=False),
        sa.Column("artifact_sha256", sa.String(length=64), nullable=False),
        sa.Column("artifact_path", sa.Text(), nullable=False),
        sa.Column("signer_key_id", sa.String(length=120), nullable=False),
        sa.Column("signature_b64", sa.Text(), nullable=False),
        sa.Column("license_id", sa.String(length=120), nullable=False),
        sa.Column("rights_status", sa.String(length=24), nullable=False),
        sa.Column("rights_evidence_ref", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("capability_id", "version", name="uq_capability_version"),
    )
    op.create_index("ix_capability_version_status", "capability_versions", ["capability_id", "status"])
    op.create_table(
        "capability_grants",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("capability_id", sa.String(length=36), sa.ForeignKey("capabilities.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("subject", sa.String(length=240), nullable=False),
        sa.Column("permission", sa.String(length=80), nullable=False),
        sa.Column("granted_by", sa.String(length=240), nullable=False),
        sa.Column("evidence_ref", sa.Text(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_capability_grant_subject", "capability_grants", ["tenant_id", "subject", "capability_id", "permission"])
    op.create_table(
        "installations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("capability_version_id", sa.String(length=36), sa.ForeignKey("capability_versions.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("host_id", sa.String(length=160), nullable=False),
        sa.Column("package_digest", sa.String(length=64), nullable=False),
        sa.Column("installed_path", sa.Text(), nullable=False),
        sa.Column("state", sa.String(length=24), nullable=False),
        sa.Column("installed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("disabled_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("tenant_id", "capability_version_id", "host_id", name="uq_installation_tenant_version_host"),
    )
    op.create_index("ix_installation_tenant_state", "installations", ["tenant_id", "state"])
    op.create_table(
        "invocations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("capability_version_id", sa.String(length=36), sa.ForeignKey("capability_versions.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("subject", sa.String(length=240), nullable=False),
        sa.Column("host_id", sa.String(length=160), nullable=False),
        sa.Column("idempotency_key", sa.String(length=200), nullable=False),
        sa.Column("request_sha256", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("result", sa.JSON(), nullable=True),
        sa.Column("trace_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("tenant_id", "idempotency_key", name="uq_invocation_tenant_idempotency"),
    )
    op.create_index("ix_invocation_tenant_created", "invocations", ["tenant_id", "created_at"])
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("actor", sa.String(length=240), nullable=False),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("resource", sa.String(length=240), nullable=False),
        sa.Column("outcome", sa.String(length=24), nullable=False),
        sa.Column("reason_code", sa.String(length=120), nullable=False),
        sa.Column("correlation_id", sa.String(length=36), nullable=False),
        sa.Column("payload_sha256", sa.String(length=64), nullable=False),
        sa.Column("previous_hash", sa.String(length=64), nullable=False),
        sa.Column("event_hash", sa.String(length=64), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("tenant_id", "sequence", name="uq_audit_tenant_sequence"),
    )
    op.create_index("ix_audit_tenant_time", "audit_events", ["tenant_id", "occurred_at"])


def downgrade() -> None:
    op.drop_index("ix_audit_tenant_time", table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index("ix_invocation_tenant_created", table_name="invocations")
    op.drop_table("invocations")
    op.drop_index("ix_installation_tenant_state", table_name="installations")
    op.drop_table("installations")
    op.drop_index("ix_capability_grant_subject", table_name="capability_grants")
    op.drop_table("capability_grants")
    op.drop_index("ix_capability_version_status", table_name="capability_versions")
    op.drop_table("capability_versions")
    op.drop_index("ix_capability_tenant_status", table_name="capabilities")
    op.drop_table("capabilities")
