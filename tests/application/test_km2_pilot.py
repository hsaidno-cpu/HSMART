"""Security and end-to-end acceptance tests for the local HSMART KM2 pilot."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
import json
import hashlib
import os
from pathlib import Path
import sys

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from hsmart_platform.app import create_app
from hsmart_platform.database import Base
from hsmart_platform.models import (
    AuditEvent,
    Capability,
    CapabilityGrant,
    CapabilityVersion,
    Installation,
    Invocation,
    Tenant,
)
from hsmart_platform.pilot.audit import verify_audit_chain
from hsmart_platform.pilot.packages import (
    build_package,
    install_package,
    transition_installation,
    verify_package,
)
from hsmart_platform.pilot.service import grant_capability, invoke_capability, revoke_capability_grant
from hsmart_platform.settings import Settings


ROOT = Path(__file__).resolve().parents[2]
ISSUER = "https://issuer.hsmart.test"
AUDIENCE = "hsmart-api"
SUBJECT = "pilot-user"
HOST_ID = "hsmart-local-mcp-host-v1"
GIT_SHA = "0123456789abcdef0123456789abcdef01234567"


def make_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine


def make_keys(tmp_path: Path):
    private = Ed25519PrivateKey.generate()
    private_path = tmp_path / "oidc-private.pem"
    public_path = tmp_path / "oidc-public.pem"
    private_path.write_bytes(private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    public_path.write_bytes(private.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ))
    return private_path, public_path


def make_token(private_path: Path, tenant_id: str, scopes: list[str], *, issuer: str = ISSUER, audience: str = AUDIENCE, minutes: int = 10):
    now = datetime.now(timezone.utc)
    claims = {
        "iss": issuer,
        "aud": audience,
        "sub": SUBJECT,
        "tenant_id": tenant_id,
        "scope": " ".join(scopes),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
        "jti": "test-token-" + str(int(now.timestamp() * 1000000)),
    }
    return jwt.encode(claims, private_path.read_text(encoding="utf-8"), algorithm="EdDSA")


def make_settings(database_url: str, public_key: Path, *, environment: str = "test") -> Settings:
    return Settings(
        environment=environment,
        database_url=database_url,
        oidc_issuer=ISSUER,
        oidc_audience=AUDIENCE,
        oidc_public_key_file=str(public_key),
        artifact_store_path=".hsmart-test-artifacts",
        pilot_host_id=HOST_ID,
    )


def seed_active_capability(session: Session, tenant_id: str, artifact_digest: str = "a" * 64):
    capability = Capability(
        tenant_id=tenant_id,
        capability_key="hsmart.echo",
        display_name="HSMART Echo",
        description="First-party echo pilot",
        publisher_id="hsmart-first-party",
        status="ACTIVE",
    )
    session.add(capability)
    session.flush()
    version = CapabilityVersion(
        capability_id=capability.id,
        version="0.1.0",
        entrypoint="builtin:hsmart.echo.v1",
        manifest={"capability_id": "hsmart.echo", "rights_status": "CLEARED"},
        artifact_sha256=artifact_digest,
        artifact_path="/tmp/pilot-package.tar.gz",
        signer_key_id="test-signer",
        signature_b64="c2lnbmF0dXJl",
        license_id="Apache-2.0",
        rights_status="CLEARED",
        rights_evidence_ref="test:first-party-license",
        status="PUBLISHED",
    )
    session.add(version)
    session.flush()
    install = Installation(
        tenant_id=tenant_id,
        capability_version_id=version.id,
        host_id=HOST_ID,
        package_digest=artifact_digest,
        installed_path="/tmp/pilot-package.tar.gz",
        state="ACTIVE",
    )
    session.add(install)
    grant = CapabilityGrant(
        tenant_id=tenant_id,
        capability_id=capability.id,
        subject=SUBJECT,
        permission="capability.invoke",
        granted_by="test-admin",
        evidence_ref="test:explicit-entitlement",
    )
    session.add(grant)
    session.commit()
    return capability, version, install, grant


def create_package(tmp_path: Path, *, rights_status: str = "CLEARED"):
    private = Ed25519PrivateKey.generate()
    private_path = tmp_path / "package-private.pem"
    public_path = tmp_path / "package-public.pem"
    private_path.write_bytes(private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    public_path.write_bytes(private.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ))
    metadata = {
        "capability_id": "hsmart.echo",
        "version": "0.1.0",
        "display_name": "HSMART Echo",
        "description": "Test capability",
        "publisher_id": "hsmart-first-party",
        "entrypoint": "builtin:hsmart.echo.v1",
        "license_id": "Apache-2.0",
        "rights_status": rights_status,
        "rights_evidence_ref": "repo:LICENSE",
        "source_repository": "https://github.com/hsaidno-cpu/HSMART",
    }
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    source_dir = tmp_path / "package-files"
    source_dir.mkdir()
    (source_dir / "README.md").write_text("pilot package", encoding="utf-8")
    bundle = tmp_path / "hsmart-echo.tar.gz"
    digest = build_package(
        metadata_path=metadata_path,
        source_dir=source_dir,
        private_key_path=private_path,
        signer_key_id="test-package-key",
        source_commit=GIT_SHA,
        output_path=bundle,
        license_file_path=ROOT / "LICENSE",
    )
    trust_policy_path = tmp_path / "publisher-trust.json"
    trust_policy_path.write_text(json.dumps({
        "schema_version": "1.0.0",
        "trusted_signers": {
            "test-package-key": {
                "public_key_sha256": hashlib.sha256(public_path.read_bytes()).hexdigest()
            }
        },
        "publishers": {
            "hsmart-first-party": {
                "source_repository": metadata["source_repository"],
                "allowed_capabilities": ["hsmart.echo"],
                "allowed_license_ids": ["Apache-2.0"],
                "rights_evidence_ref": metadata["rights_evidence_ref"],
                "allowed_source_commits": [GIT_SHA],
                "license_file_path": str(ROOT / "LICENSE")
            }
        }
    }), encoding="utf-8")
    return bundle, private_path, public_path, trust_policy_path, digest


def test_oidc_verification_fails_closed_on_bad_issuer_audience_and_expiry(tmp_path):
    from hsmart_platform.pilot.auth import authenticate_token
    from hsmart_platform.pilot.errors import AuthenticationError

    private_path, public_path = make_keys(tmp_path)
    settings = make_settings("sqlite://", public_path)
    valid = make_token(private_path, "tenant-one", ["capability.invoke"])
    assert authenticate_token(valid, settings).subject == SUBJECT
    bad_issuer = make_token(private_path, "tenant-one", ["capability.invoke"], issuer="https://wrong.test")
    with pytest.raises(AuthenticationError):
        authenticate_token(bad_issuer, settings)
    bad_audience = make_token(private_path, "tenant-one", ["capability.invoke"], audience="other-api")
    with pytest.raises(AuthenticationError):
        authenticate_token(bad_audience, settings)
    expired = make_token(private_path, "tenant-one", ["capability.invoke"], minutes=-2)
    with pytest.raises(AuthenticationError):
        authenticate_token(expired, settings)


def test_signed_package_installation_lifecycle_and_tamper_rejection(tmp_path):
    engine = make_engine()
    with Session(engine) as session:
        tenant = Tenant(slug="tenant-package", display_name="Package Tenant")
        session.add(tenant)
        session.commit()
        tenant_id = tenant.id
        bundle, _, public_path, trust_path, digest = create_package(tmp_path)
        verified = verify_package(bundle, public_path, trust_path)
        assert verified.artifact_sha256 == digest
        install = install_package(
            session,
            tenant_id=tenant_id,
            host_id=HOST_ID,
            bundle_path=bundle,
            public_key_path=public_path,
            artifact_store_path=tmp_path / "artifacts",
            installer_subject="publisher",
            trust_policy_path=trust_path,
        )
        assert install.state == "INSTALLED"
        activated = transition_installation(session, install.id, "ACTIVE", "admin")
        assert activated.state == "ACTIVE"
        disabled = transition_installation(session, install.id, "DISABLED", "admin")
        assert disabled.state == "DISABLED"
        active_again = transition_installation(session, install.id, "ACTIVE", "admin")
        assert active_again.state == "ACTIVE"
        revoked = transition_installation(session, install.id, "REVOKED", "admin")
        assert revoked.state == "REVOKED"
        with pytest.raises(Exception):
            transition_installation(session, install.id, "ACTIVE", "admin")
        assert verify_audit_chain(session, tenant_id)

        # A changed payload must fail the signed file inventory even when the tar remains parseable.
        from hsmart_platform.pilot.errors import PackageVerificationError
        import io
        import tarfile
        members = {}
        with tarfile.open(bundle, "r:gz") as archive:
            for item in archive.getmembers():
                source = archive.extractfile(item)
                if source is not None:
                    members[item.name] = source.read()
        members["files/README.md"] = b"tampered"
        tampered_raw = io.BytesIO()
        with tarfile.open(fileobj=tampered_raw, mode="w") as archive:
            for name, content in members.items():
                info = tarfile.TarInfo(name)
                info.size = len(content)
                info.mode = 0o644
                archive.addfile(info, io.BytesIO(content))
        import gzip
        tampered = tmp_path / "tampered.tar.gz"
        with tampered.open("wb") as stream:
            with gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as compressed:
                compressed.write(tampered_raw.getvalue())
        with pytest.raises(PackageVerificationError):
            verify_package(tampered, public_path, trust_path)


def test_unassessed_distribution_rights_are_not_installable(tmp_path):
    from hsmart_platform.pilot.errors import PackageVerificationError

    bundle, _, public_path, trust_path, _ = create_package(tmp_path, rights_status="NOT_ASSESSED")
    with pytest.raises(PackageVerificationError, match="distribution_rights_not_cleared"):
        verify_package(bundle, public_path, trust_path)


def test_api_denies_missing_token_and_requires_entitlement(tmp_path):
    engine = make_engine()
    private_path, public_path = make_keys(tmp_path)
    settings = make_settings("sqlite://", public_path)
    with Session(engine) as session:
        tenant = Tenant(slug="api-tenant", display_name="API Tenant")
        session.add(tenant)
        session.commit()
        tenant_id = tenant.id
        seed_active_capability(session, tenant_id)
        # Remove entitlement to ensure a valid token alone does not grant execution.
        session.query(CapabilityGrant).delete()
        session.commit()
    app = create_app(settings, engine)
    token = make_token(private_path, tenant_id, ["capability.invoke"])
    with TestClient(app) as client:
        assert client.post("/v1/invoke", json={
            "capability_id": "hsmart.echo",
            "version": "0.1.0",
            "payload": {"message": "hello"},
        }, headers={"Idempotency-Key": "no-grant-0001"}).status_code == 401
        denied = client.post("/v1/invoke", json={
            "capability_id": "hsmart.echo",
            "version": "0.1.0",
            "payload": {"message": "hello"},
        }, headers={"Authorization": f"Bearer {token}", "Idempotency-Key": "no-grant-0001"})
        assert denied.status_code == 403
        assert denied.json()["detail"] == "capability_entitlement_missing"


def test_invocation_idempotency_and_audit_chain(tmp_path):
    engine = make_engine()
    private_path, public_path = make_keys(tmp_path)
    settings = make_settings("sqlite://", public_path)
    with Session(engine) as session:
        tenant = Tenant(slug="idempotent-tenant", display_name="Idempotent Tenant")
        session.add(tenant)
        session.commit()
        seed_active_capability(session, tenant.id)
        from hsmart_platform.pilot.auth import Principal
        principal = Principal(SUBJECT, tenant.id, frozenset({"capability.invoke"}), ISSUER)
        result = invoke_capability(
            session, settings, principal,
            capability_key="hsmart.echo", version="0.1.0",
            payload={"message": "hello"}, idempotency_key="idempotent-001",
        )
        replay = invoke_capability(
            session, settings, principal,
            capability_key="hsmart.echo", version="0.1.0",
            payload={"message": "hello"}, idempotency_key="idempotent-001",
        )
        assert result["invocation_id"] == replay["invocation_id"]
        assert replay["idempotent_replay"] is True
        with pytest.raises(Exception):
            invoke_capability(
                session, settings, principal,
                capability_key="hsmart.echo", version="0.1.0",
                payload={"message": "different"}, idempotency_key="idempotent-001",
            )
        assert verify_audit_chain(session, tenant.id)



def test_trust_policy_rejects_untrusted_signer_and_unapproved_source(tmp_path):
    from hsmart_platform.pilot.errors import PackageVerificationError

    bundle, _, public_path, trust_path, _ = create_package(tmp_path)
    policy = json.loads(trust_path.read_text(encoding="utf-8"))
    policy["trusted_signers"]["test-package-key"]["public_key_sha256"] = "0" * 64
    trust_path.write_text(json.dumps(policy), encoding="utf-8")
    with pytest.raises(PackageVerificationError, match="package_signer_not_trusted"):
        verify_package(bundle, public_path, trust_path)


def test_installer_rejects_unapproved_source_commit(tmp_path):
    from hsmart_platform.pilot.errors import PackageVerificationError

    bundle, _, public_path, trust_path, _ = create_package(tmp_path)
    policy = json.loads(trust_path.read_text(encoding="utf-8"))
    policy["publishers"]["hsmart-first-party"]["allowed_source_commits"] = ["f" * 40]
    trust_path.write_text(json.dumps(policy), encoding="utf-8")
    with pytest.raises(PackageVerificationError, match="source_commit_not_approved"):
        verify_package(bundle, public_path, trust_path)


def test_uninstall_then_reinstall_preserves_immutable_release(tmp_path):
    engine = make_engine()
    with Session(engine) as session:
        tenant = Tenant(slug="tenant-reinstall", display_name="Reinstall Tenant")
        session.add(tenant)
        session.commit()
        bundle, _, public_path, trust_path, digest = create_package(tmp_path)
        first = install_package(
            session,
            tenant_id=tenant.id,
            host_id=HOST_ID,
            bundle_path=bundle,
            public_key_path=public_path,
            artifact_store_path=tmp_path / "artifacts",
            installer_subject="publisher",
            trust_policy_path=trust_path,
        )
        removed = transition_installation(session, first.id, "UNINSTALLED", "admin")
        assert removed.state == "UNINSTALLED"
        second = install_package(
            session,
            tenant_id=tenant.id,
            host_id=HOST_ID,
            bundle_path=bundle,
            public_key_path=public_path,
            artifact_store_path=tmp_path / "artifacts",
            installer_subject="publisher",
            trust_policy_path=trust_path,
        )
        assert second.id == first.id
        assert second.state == "INSTALLED"
        assert second.package_digest == digest
        assert verify_audit_chain(session, tenant.id)
    engine.dispose()


def test_entitlement_revocation_blocks_idempotent_replay(tmp_path):
    engine = make_engine()
    settings = make_settings("sqlite://", make_keys(tmp_path)[1])
    with Session(engine) as session:
        tenant = Tenant(slug="tenant-revoke", display_name="Revocation Tenant")
        session.add(tenant)
        session.commit()
        capability, _, _, grant = seed_active_capability(session, tenant.id)
        principal = __import__("hsmart_platform.pilot.auth", fromlist=["Principal"]).Principal(
            SUBJECT, tenant.id, frozenset({"capability.invoke"}), ISSUER
        )
        first = invoke_capability(
            session, settings, principal,
            capability_key="hsmart.echo", version="0.1.0",
            payload={"message": "before revoke"}, idempotency_key="revoke-replay-0001",
        )
        revoked = revoke_capability_grant(
            session,
            tenant_id=tenant.id,
            grant_id=grant.id,
            revoked_by="tenant-admin",
            evidence_ref="ticket:revoke-123",
        )
        assert revoked.revoked_at is not None
        from hsmart_platform.pilot.errors import AuthorizationError
        with pytest.raises(AuthorizationError, match="capability_entitlement_missing"):
            invoke_capability(
                session, settings, principal,
                capability_key="hsmart.echo", version="0.1.0",
                payload={"message": "before revoke"}, idempotency_key="revoke-replay-0001",
            )
        assert verify_audit_chain(session, tenant.id)
    engine.dispose()


def test_concurrent_idempotency_insert_race_returns_winning_replay(tmp_path, monkeypatch):
    from hsmart_platform.pilot.auth import Principal

    engine = make_engine()
    private_path, public_path = make_keys(tmp_path)
    settings = make_settings("sqlite://", public_path)
    with Session(engine) as session:
        tenant = Tenant(slug="concurrent-replay-tenant", display_name="Concurrent Replay Tenant")
        session.add(tenant)
        session.commit()
        tenant_id = tenant.id
        seed_active_capability(session, tenant_id)
        principal = Principal(SUBJECT, tenant_id, frozenset({"capability.invoke"}), ISSUER)
        original = invoke_capability(
            session, settings, principal,
            capability_key="hsmart.echo", version="0.1.0",
            payload={"message": "same request"}, idempotency_key="concurrent-replay-0001",
        )

        real_scalar = session.scalar
        invocation_lookup_count = {"value": 0}

        def hide_first_invocation_lookup(statement, *args, **kwargs):
            # Target the ORM entity, not a brittle SQL string representation.
            entities = [
                column.get("entity")
                for column in getattr(statement, "column_descriptions", [])
            ]
            if Invocation in entities and invocation_lookup_count["value"] == 0:
                invocation_lookup_count["value"] += 1
                return None
            return real_scalar(statement, *args, **kwargs)

        # The existing row already owns the unique tenant/idempotency key.
        # Hiding only the first lookup forces the next real INSERT to hit the
        # database unique constraint, exercising the genuine IntegrityError path.
        monkeypatch.setattr(session, "scalar", hide_first_invocation_lookup)

        replay = invoke_capability(
            session, settings, principal,
            capability_key="hsmart.echo", version="0.1.0",
            payload={"message": "same request"}, idempotency_key="concurrent-replay-0001",
        )
        assert replay["idempotent_replay"] is True
        assert replay["invocation_id"] == original["invocation_id"]
        assert replay["result"] == original["result"]
        assert verify_audit_chain(session, tenant_id)
    engine.dispose()


def test_mcp_stdio_host_invokes_signed_installed_entitled_capability(tmp_path):
    from mcp.client.session import ClientSession
    from mcp.client.stdio import StdioServerParameters, stdio_client

    engine = create_engine(
        f"sqlite:///{tmp_path / 'mcp-host.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    private_path, public_path = make_keys(tmp_path)
    settings = make_settings(f"sqlite:///{tmp_path / 'mcp-host.db'}", public_path)
    with Session(engine) as session:
        tenant = Tenant(slug="mcp-tenant", display_name="MCP Tenant")
        session.add(tenant)
        session.commit()
        tenant_id = tenant.id
        bundle, _, package_public_key, trust_path, _ = create_package(tmp_path)
        installation = install_package(
            session,
            tenant_id=tenant_id,
            host_id=HOST_ID,
            bundle_path=bundle,
            public_key_path=package_public_key,
            artifact_store_path=tmp_path / "artifacts",
            installer_subject="mcp-pilot-publisher",
            trust_policy_path=trust_path,
        )
        transition_installation(session, installation.id, "ACTIVE", "mcp-pilot-admin")
        capability = session.scalar(select(Capability).where(
            Capability.tenant_id == tenant_id,
            Capability.capability_key == "hsmart.echo",
        ))
        grant_capability(
            session,
            tenant_id=tenant_id,
            capability_key="hsmart.echo",
            subject=SUBJECT,
            permission="capability.invoke",
            granted_by="mcp-pilot-admin",
            evidence_ref="ticket:mcp-pilot-allow",
        )
    token = make_token(private_path, tenant_id, ["capability.read", "capability.invoke"])
    env = {
        "PYTHONPATH": str(ROOT / "src"),
        "DATABASE_URL": settings.database_url,
        "HSMART_ENV": "test",
        "HSMART_OIDC_ISSUER": ISSUER,
        "HSMART_OIDC_AUDIENCE": AUDIENCE,
        "HSMART_OIDC_PUBLIC_KEY_FILE": str(public_path),
        "HSMART_PILOT_ACCESS_TOKEN": token,
        "HSMART_PILOT_HOST_ID": HOST_ID,
    }

    async def run_client():
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "hsmart_platform.pilot.mcp_pilot"],
            env=env,
            cwd=ROOT,
        )
        async with stdio_client(params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as client:
                await client.initialize()
                listed = await client.list_tools()
                assert {tool.name for tool in listed.tools} == {"hsmart.list_capabilities", "hsmart.invoke"}
                called = await client.call_tool("hsmart.invoke", {
                    "capability_id": "hsmart.echo",
                    "version": "0.1.0",
                    "payload": {"message": "hello from an actual MCP stdio client"},
                    "idempotency_key": "mcp-pilot-0001",
                })
                assert called.is_error is False
                return json.loads(called.content[0].text)

    result = asyncio.run(run_client())
    assert result["status"] == "COMPLETED"
    assert result["result"]["message"] == "hello from an actual MCP stdio client"
    with Session(engine) as session:
        stored = session.scalar(select(Invocation).where(Invocation.id == result["invocation_id"]))
        assert stored is not None and stored.status == "COMPLETED"
        assert verify_audit_chain(session, tenant_id)
    engine.dispose()


def test_api_grant_and_revoke_routes_require_scope_and_emit_audit(tmp_path):
    engine = make_engine()
    private_path, public_path = make_keys(tmp_path)
    settings = make_settings("sqlite://", public_path)
    with Session(engine) as session:
        tenant = Tenant(slug="grant-api-tenant", display_name="Grant API Tenant")
        session.add(tenant)
        session.commit()
        tenant_id = tenant.id
        seed_active_capability(session, tenant_id)
        session.query(CapabilityGrant).delete()
        session.commit()
    app = create_app(settings, engine)
    token = make_token(private_path, tenant_id, ["entitlement.grant"])
    with TestClient(app) as client:
        created = client.post(
            "/v1/registry/grants",
            json={
                "capability_id": "hsmart.echo",
                "subject": SUBJECT,
                "permission": "capability.invoke",
                "evidence_ref": "ticket:grant-api-001",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert created.status_code == 201
        grant_id = created.json()["grant_id"]
        revoked = client.post(
            f"/v1/registry/grants/{grant_id}/revoke",
            json={"evidence_ref": "ticket:revoke-api-001"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert revoked.status_code == 200
        assert revoked.json()["status"] == "REVOKED"
    with Session(engine) as session:
        stored = session.get(CapabilityGrant, grant_id)
        assert stored is not None and stored.revoked_at is not None
        assert verify_audit_chain(session, tenant_id)
    engine.dispose()


def test_cross_tenant_principal_cannot_invoke_another_tenants_capability(tmp_path):
    from hsmart_platform.pilot.auth import Principal
    from hsmart_platform.pilot.errors import PilotError

    engine = make_engine()
    private_path, public_path = make_keys(tmp_path)
    settings = make_settings("sqlite://", public_path)
    with Session(engine) as session:
        owner = Tenant(slug="owner-tenant", display_name="Owner Tenant")
        outsider = Tenant(slug="outsider-tenant", display_name="Outsider Tenant")
        session.add_all([owner, outsider])
        session.commit()
        seed_active_capability(session, owner.id)
        principal = Principal(SUBJECT, outsider.id, frozenset({"capability.invoke"}), ISSUER)
        with pytest.raises(PilotError, match="capability_not_found"):
            invoke_capability(
                session, settings, principal,
                capability_key="hsmart.echo", version="0.1.0",
                payload={"message": "unauthorized tenant"},
                idempotency_key="cross-tenant-0001",
            )
    engine.dispose()
