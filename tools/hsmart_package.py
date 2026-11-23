#!/usr/bin/env python3
"""Build, verify, install and transition HSMART signed capability packages."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from sqlalchemy.orm import Session

from hsmart_platform.database import build_engine
from hsmart_platform.models import Tenant
from hsmart_platform.pilot.packages import build_package, install_package, transition_installation, verify_package
from hsmart_platform.settings import Settings


def keygen(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    private = Ed25519PrivateKey.generate()
    private_path = output_dir / "package-signing-private.pem"
    public_path = output_dir / "package-signing-public.pem"
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
    print("Keep the private key outside Git. The public key is used by installers to verify releases.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    key_parser = commands.add_parser("keygen")
    key_parser.add_argument("--output-dir", type=Path, default=ROOT / ".local" / "package-keys")

    build_parser = commands.add_parser("build")
    build_parser.add_argument("--metadata", type=Path, default=ROOT / "examples/pilot/hsmart-echo/manifest.json")
    build_parser.add_argument("--source-dir", type=Path, default=ROOT / "examples/pilot/hsmart-echo/files")
    build_parser.add_argument("--private-key", type=Path, required=True)
    build_parser.add_argument("--signer-key-id", default="hsmart-dev-ed25519-1")
    build_parser.add_argument("--source-commit", required=True)
    build_parser.add_argument("--output", type=Path, default=ROOT / "dist" / "hsmart-echo-0.1.0.tar.gz")

    verify_parser = commands.add_parser("verify")
    verify_parser.add_argument("--bundle", type=Path, required=True)
    verify_parser.add_argument("--public-key", type=Path, required=True)

    install_parser = commands.add_parser("install")
    install_parser.add_argument("--bundle", type=Path, required=True)
    install_parser.add_argument("--public-key", type=Path, required=True)
    install_parser.add_argument("--tenant-id", required=True)
    install_parser.add_argument("--host-id", default="hsmart-local-mcp-host-v1")
    install_parser.add_argument("--installer-subject", required=True)
    install_parser.add_argument("--artifact-store", type=Path, default=ROOT / ".hsmart-artifacts")

    transition_parser = commands.add_parser("transition")
    transition_parser.add_argument("--installation-id", required=True)
    transition_parser.add_argument("--state", choices=["ACTIVE", "DISABLED", "REVOKED"], required=True)
    transition_parser.add_argument("--actor", required=True)

    args = parser.parse_args()
    if args.command == "keygen":
        keygen(args.output_dir)
    elif args.command == "build":
        digest = build_package(
            metadata_path=args.metadata,
            source_dir=args.source_dir,
            private_key_path=args.private_key,
            signer_key_id=args.signer_key_id,
            source_commit=args.source_commit,
            output_path=args.output,
        )
        print(f"bundle={args.output}")
        print(f"sha256={digest}")
    elif args.command == "verify":
        verified = verify_package(args.bundle, args.public_key)
        manifest = verified.release["manifest"]
        print(f"PASS: {manifest['capability_id']}@{manifest['version']}")
        print(f"sha256={verified.artifact_sha256}")
        print(f"signer={verified.signer_key_id}")
        print(f"license={manifest['license_id']}")
    elif args.command == "install":
        settings = Settings.from_env()
        engine = build_engine(settings.database_url)
        with Session(engine) as session:
            tenant = session.get(Tenant, args.tenant_id)
            if tenant is None:
                raise SystemExit("tenant_not_found")
            installation = install_package(
                session,
                tenant_id=tenant.id,
                host_id=args.host_id,
                bundle_path=args.bundle,
                public_key_path=args.public_key,
                artifact_store_path=args.artifact_store,
                installer_subject=args.installer_subject,
            )
        engine.dispose()
        print(f"installation_id={installation.id}")
        print(f"state={installation.state}")
        print(f"sha256={installation.package_digest}")
    elif args.command == "transition":
        settings = Settings.from_env()
        engine = build_engine(settings.database_url)
        with Session(engine) as session:
            installation = transition_installation(session, args.installation_id, args.state, args.actor)
        engine.dispose()
        print(f"installation_id={installation.id}")
        print(f"state={installation.state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
