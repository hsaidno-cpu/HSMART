#!/usr/bin/env python3
"""Local-only bootstrap helpers. These test keys must never be used in production."""
from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from sqlalchemy import select
from sqlalchemy.orm import Session

from hsmart_platform.database import build_engine
from hsmart_platform.models import Capability, CapabilityGrant
from hsmart_platform.pilot.seed import ensure_tenant
from hsmart_platform.settings import Settings


def generate_oidc_test_keys(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    private = Ed25519PrivateKey.generate()
    private_path = output_dir / "oidc-test-private.pem"
    public_path = output_dir / "oidc-test-public.pem"
    private_path.write_bytes(private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    public_path.write_bytes(private.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ))
    private_path.chmod(0o600)
    public_path.chmod(0o644)
    print(f"private_key={private_path}")
    print(f"public_key={public_path}")
    print(f"public_key_sha256={hashlib.sha256(public_path.read_bytes()).hexdigest()}")
    print("LOCAL/TEST ONLY. Hosted environments must use an external OIDC issuer and HTTPS JWKS.")


def mint_token(private_key_path: Path, issuer: str, audience: str, subject: str, tenant_id: str, scopes: list[str]) -> str:
    now = datetime.now(timezone.utc)
    claims = {
        "iss": issuer,
        "aud": audience,
        "sub": subject,
        "tenant_id": tenant_id,
        "scope": " ".join(scopes),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=10)).timestamp()),
        "jti": __import__("secrets").token_urlsafe(18),
    }
    private_key = private_key_path.read_text(encoding="utf-8")
    return jwt.encode(claims, private_key, algorithm="EdDSA")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    keys = sub.add_parser("oidc-test-keygen")
    keys.add_argument("--output-dir", type=Path, default=ROOT / ".local" / "keys")

    token = sub.add_parser("mint-test-token")
    token.add_argument("--private-key", type=Path, required=True)
    token.add_argument("--issuer", required=True)
    token.add_argument("--audience", required=True)
    token.add_argument("--subject", required=True)
    token.add_argument("--tenant-id", required=True)
    token.add_argument("--scope", nargs="+", required=True)

    tenant_cmd = sub.add_parser("seed-tenant")
    tenant_cmd.add_argument("--slug", required=True)
    tenant_cmd.add_argument("--display-name", required=True)

    grant_cmd = sub.add_parser("grant")
    grant_cmd.add_argument("--tenant-id", required=True)
    grant_cmd.add_argument("--capability-id", required=True)
    grant_cmd.add_argument("--subject", required=True)
    grant_cmd.add_argument("--permission", default="capability.invoke")
    grant_cmd.add_argument("--evidence-ref", required=True)

    args = parser.parse_args()
    if args.command == "oidc-test-keygen":
        generate_oidc_test_keys(args.output_dir)
        return 0
    if args.command == "mint-test-token":
        print(mint_token(args.private_key, args.issuer, args.audience, args.subject, args.tenant_id, args.scope))
        return 0

    settings = Settings.from_env()
    engine = build_engine(settings.database_url)
    with Session(engine) as session:
        if args.command == "seed-tenant":
            tenant = ensure_tenant(session, args.slug, args.display_name)
            session.commit()
            print(f"tenant_id={tenant.id}")
            return 0
        if args.command == "grant":
            capability = session.scalar(select(Capability).where(
                Capability.tenant_id == args.tenant_id,
                Capability.capability_key == args.capability_id,
            ))
            if capability is None:
                raise SystemExit("capability_not_found")
            session.add(CapabilityGrant(
                tenant_id=args.tenant_id,
                capability_id=capability.id,
                subject=args.subject,
                permission=args.permission,
                granted_by="local-pilot-operator",
                evidence_ref=args.evidence_ref,
            ))
            session.commit()
            print("grant_created")
    engine.dispose()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
