"""Signed, deterministic package build and safe local installer."""
from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import tarfile
import uuid

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Capability, CapabilityVersion, Installation
from .audit import append_audit
from .errors import ConflictError, PackageVerificationError

MAX_PACKAGE_BYTES = 20 * 1024 * 1024
ALLOWED_ENTRYPOINTS = {"builtin:hsmart.echo.v1"}
SOURCE_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True, slots=True)
class VerifiedPackage:
    release: dict
    artifact_sha256: str
    signature_b64: str
    signer_key_id: str
    files: dict[str, bytes]


def canonical_json(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def build_package(
    *,
    metadata_path: str | Path,
    source_dir: str | Path,
    private_key_path: str | Path,
    signer_key_id: str,
    source_commit: str,
    output_path: str | Path,
    license_file_path: str | Path | None = None,
) -> str:
    if not SOURCE_SHA_RE.fullmatch(source_commit):
        raise PackageVerificationError("source_commit_must_be_immutable_git_sha")
    metadata = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    file_contents: dict[str, bytes] = {}
    root = Path(source_dir)
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise PackageVerificationError("symlink_not_allowed_in_package")
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            if not relative or relative.startswith("/") or ".." in PurePosixPath(relative).parts:
                raise PackageVerificationError("unsafe_package_path")
            file_contents[relative] = path.read_bytes()
    if license_file_path is not None:
        file_contents.setdefault("LICENSE", Path(license_file_path).read_bytes())
    if not file_contents:
        raise PackageVerificationError("package_payload_empty")
    metadata["source_commit"] = source_commit
    release = {
        "schema_version": "1.0.0",
        "manifest": metadata,
        "files": {path: hashlib.sha256(content).hexdigest() for path, content in sorted(file_contents.items())},
        "signing_algorithm": "Ed25519",
        "signer_key_id": signer_key_id,
    }
    private_key = serialization.load_pem_private_key(Path(private_key_path).read_bytes(), password=None)
    if not isinstance(private_key, Ed25519PrivateKey):
        raise PackageVerificationError("package_signing_key_must_be_ed25519")
    signature = base64.b64encode(private_key.sign(canonical_json(release)))
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as archive:
        _add_bytes(archive, "release.json", canonical_json(release))
        _add_bytes(archive, "signature.ed25519", signature)
        for name, content in sorted(file_contents.items()):
            _add_bytes(archive, f"files/{name}", content)
    with output.open("wb") as stream:
        with gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as compressed:
            compressed.write(raw.getvalue())
    return hashlib.sha256(output.read_bytes()).hexdigest()


def _add_bytes(archive: tarfile.TarFile, name: str, content: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(content)
    info.mode = 0o644
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    archive.addfile(info, io.BytesIO(content))


def verify_package(
    bundle_path: str | Path,
    public_key_path: str | Path,
    trust_policy_path: str | Path,
) -> VerifiedPackage:
    bundle = Path(bundle_path).read_bytes()
    if not bundle or len(bundle) > MAX_PACKAGE_BYTES:
        raise PackageVerificationError("package_size_out_of_bounds")
    archive_files: dict[str, bytes] = {}
    total_size = 0
    try:
        with tarfile.open(fileobj=io.BytesIO(bundle), mode="r:gz") as archive:
            members = archive.getmembers()
            if len(members) > 500:
                raise PackageVerificationError("package_file_count_out_of_bounds")
            for member in members:
                name = PurePosixPath(member.name)
                if name.is_absolute() or ".." in name.parts or member.issym() or member.islnk():
                    raise PackageVerificationError("unsafe_archive_member")
                if member.isdir():
                    continue
                if not member.isfile() or member.size > MAX_PACKAGE_BYTES or member.name in archive_files:
                    raise PackageVerificationError("unsupported_or_duplicate_archive_member")
                total_size += member.size
                if total_size > MAX_PACKAGE_BYTES:
                    raise PackageVerificationError("package_expanded_size_out_of_bounds")
                handle = archive.extractfile(member)
                if handle is None:
                    raise PackageVerificationError("unreadable_archive_member")
                archive_files[member.name] = handle.read(MAX_PACKAGE_BYTES + 1)
    except (tarfile.TarError, OSError, EOFError) as exc:
        raise PackageVerificationError("invalid_package_archive") from exc
    if "release.json" not in archive_files or "signature.ed25519" not in archive_files:
        raise PackageVerificationError("release_manifest_or_signature_missing")
    try:
        release = json.loads(archive_files.pop("release.json").decode("utf-8"))
        signature = base64.b64decode(archive_files.pop("signature.ed25519"), validate=True)
    except Exception as exc:
        raise PackageVerificationError("release_metadata_invalid") from exc
    if release.get("schema_version") != "1.0.0" or release.get("signing_algorithm") != "Ed25519":
        raise PackageVerificationError("unsupported_release_metadata")
    public_key = serialization.load_pem_public_key(Path(public_key_path).read_bytes())
    if not isinstance(public_key, Ed25519PublicKey):
        raise PackageVerificationError("package_verification_key_must_be_ed25519")
    try:
        public_key.verify(signature, canonical_json(release))
    except Exception as exc:
        raise PackageVerificationError("package_signature_invalid") from exc
    manifest = release.get("manifest")
    file_hashes = release.get("files")
    expected_paths = set(file_hashes) if isinstance(file_hashes, dict) else set()
    actual_paths = {name.removeprefix("files/") for name in archive_files if name.startswith("files/")}
    if not isinstance(manifest, dict) or actual_paths != expected_paths:
        raise PackageVerificationError("package_file_inventory_mismatch")
    payloads: dict[str, bytes] = {}
    for archive_name, content in archive_files.items():
        if not archive_name.startswith("files/"):
            raise PackageVerificationError("unexpected_archive_member")
        relative = archive_name.removeprefix("files/")
        if not relative or ".." in PurePosixPath(relative).parts:
            raise PackageVerificationError("unsafe_package_payload_path")
        if hashlib.sha256(content).hexdigest() != file_hashes.get(relative):
            raise PackageVerificationError("package_payload_digest_mismatch")
        payloads[relative] = content
    policy = json.loads(Path(trust_policy_path).read_text(encoding="utf-8"))
    if policy.get("schema_version") != "1.0.0":
        raise PackageVerificationError("publisher_trust_policy_invalid")
    signer = policy.get("trusted_signers", {}).get(str(release.get("signer_key_id", "")))
    public_key_bytes = Path(public_key_path).read_bytes()
    if not isinstance(signer, dict) or signer.get("public_key_sha256") != hashlib.sha256(public_key_bytes).hexdigest():
        raise PackageVerificationError("package_signer_not_trusted")
    required = [
        "capability_id", "version", "display_name", "description", "publisher_id",
        "entrypoint", "license_id", "rights_status", "rights_evidence_ref",
        "source_repository", "source_commit",
    ]
    if any(not manifest.get(field) for field in required):
        raise PackageVerificationError("required_manifest_field_missing")
    if manifest["rights_status"] != "CLEARED":
        raise PackageVerificationError("distribution_rights_not_cleared")
    if not SOURCE_SHA_RE.fullmatch(manifest["source_commit"]):
        raise PackageVerificationError("source_commit_must_be_immutable_git_sha")
    if not str(manifest["source_repository"]).startswith("https://"):
        raise PackageVerificationError("canonical_source_repository_required")
    if manifest["entrypoint"] not in ALLOWED_ENTRYPOINTS:
        raise PackageVerificationError("entrypoint_not_allowlisted")
    publisher = policy.get("publishers", {}).get(manifest["publisher_id"])
    if not isinstance(publisher, dict):
        raise PackageVerificationError("publisher_not_approved")
    if manifest["source_repository"] != publisher.get("source_repository"):
        raise PackageVerificationError("publisher_source_repository_not_approved")
    if manifest["capability_id"] not in publisher.get("allowed_capabilities", []):
        raise PackageVerificationError("publisher_capability_not_approved")
    if manifest["license_id"] not in publisher.get("allowed_license_ids", []):
        raise PackageVerificationError("license_not_approved_for_publisher")
    if manifest["rights_evidence_ref"] != publisher.get("rights_evidence_ref"):
        raise PackageVerificationError("rights_evidence_reference_not_approved")
    license_file = publisher.get("license_file_path")
    if not isinstance(license_file, str) or "LICENSE" not in payloads:
        raise PackageVerificationError("package_license_file_required")
    license_path = Path(license_file)
    if not license_path.is_absolute():
        license_path = Path(trust_policy_path).resolve().parent / license_path
    try:
        trusted_license_bytes = license_path.read_bytes()
    except OSError as exc:
        raise PackageVerificationError("trusted_license_evidence_unavailable") from exc
    if payloads["LICENSE"] != trusted_license_bytes:
        raise PackageVerificationError("package_license_file_does_not_match_trusted_evidence")
    return VerifiedPackage(
        release=release,
        artifact_sha256=hashlib.sha256(bundle).hexdigest(),
        signature_b64=base64.b64encode(signature).decode("ascii"),
        signer_key_id=str(release.get("signer_key_id", "")),
        files=payloads,
    )


def install_package(
    session: Session,
    *,
    tenant_id: str,
    host_id: str,
    bundle_path: str | Path,
    public_key_path: str | Path,
    artifact_store_path: str | Path,
    installer_subject: str,
    trust_policy_path: str | Path,
) -> Installation:
    verified = verify_package(bundle_path, public_key_path, trust_policy_path)
    manifest = verified.release["manifest"]
    store = Path(artifact_store_path) / "sha256"
    store.mkdir(parents=True, exist_ok=True)
    artifact_path = store / f"{verified.artifact_sha256}.tar.gz"
    if artifact_path.exists():
        if hashlib.sha256(artifact_path.read_bytes()).hexdigest() != verified.artifact_sha256:
            raise PackageVerificationError("content_addressed_artifact_store_corruption")
    else:
        temporary = store / f".{uuid.uuid4().hex}.tmp"
        temporary.write_bytes(Path(bundle_path).read_bytes())
        os.replace(temporary, artifact_path)

    capability = session.scalar(
        select(Capability).where(
            Capability.tenant_id == tenant_id,
            Capability.capability_key == manifest["capability_id"],
        )
    )
    if capability is None:
        capability = Capability(
            tenant_id=tenant_id,
            capability_key=manifest["capability_id"],
            display_name=manifest["display_name"],
            description=manifest["description"],
            publisher_id=manifest["publisher_id"],
            status="ACTIVE",
        )
        session.add(capability)
        session.flush()
    elif capability.publisher_id != manifest["publisher_id"]:
        raise ConflictError("capability_publisher_identity_conflict")

    version = session.scalar(
        select(CapabilityVersion).where(
            CapabilityVersion.capability_id == capability.id,
            CapabilityVersion.version == manifest["version"],
        )
    )
    if version is None:
        version = CapabilityVersion(
            capability_id=capability.id,
            version=manifest["version"],
            entrypoint=manifest["entrypoint"],
            manifest=manifest,
            artifact_sha256=verified.artifact_sha256,
            artifact_path=str(artifact_path),
            signer_key_id=verified.signer_key_id,
            signature_b64=verified.signature_b64,
            license_id=manifest["license_id"],
            rights_status=manifest["rights_status"],
            rights_evidence_ref=manifest["rights_evidence_ref"],
            status="PUBLISHED",
        )
        session.add(version)
        session.flush()
    elif version.status != "PUBLISHED":
        raise ConflictError("capability_version_is_not_publishable")
    elif version.artifact_sha256 != verified.artifact_sha256:
        raise ConflictError("immutable_version_already_exists_with_different_digest")

    installation = session.scalar(
        select(Installation).where(
            Installation.tenant_id == tenant_id,
            Installation.capability_version_id == version.id,
            Installation.host_id == host_id,
        )
    )
    if installation is None:
        installation = Installation(
            tenant_id=tenant_id,
            capability_version_id=version.id,
            host_id=host_id,
            package_digest=verified.artifact_sha256,
            installed_path=str(artifact_path),
            state="INSTALLED",
        )
        session.add(installation)
        session.flush()
        append_audit(
            session,
            tenant_id=tenant_id,
            actor=installer_subject,
            action="PACKAGE_INSTALLED",
            resource=f"{manifest['capability_id']}@{manifest['version']}",
            outcome="ALLOW",
            reason_code="SIGNATURE_DIGEST_AND_RIGHTS_VERIFIED",
            payload_sha256=verified.artifact_sha256,
        )
    session.commit()
    return installation


def transition_installation(session: Session, installation_id: str, target_state: str, actor: str) -> Installation:
    allowed = {
        "INSTALLED": {"ACTIVE", "REVOKED"},
        "ACTIVE": {"DISABLED", "REVOKED"},
        "DISABLED": {"ACTIVE", "REVOKED"},
        "REVOKED": set(),
    }
    installation = session.get(Installation, installation_id)
    if installation is None:
        raise PackageVerificationError("installation_not_found")
    if target_state not in allowed.get(installation.state, set()):
        raise ConflictError("invalid_installation_state_transition")
    version = session.get(CapabilityVersion, installation.capability_version_id)
    if version is None or version.rights_status != "CLEARED" or version.status != "PUBLISHED":
        raise PackageVerificationError("release_not_eligible_for_activation")
    now = datetime.now(timezone.utc)
    installation.state = target_state
    if target_state == "ACTIVE":
        installation.activated_at = now
        installation.disabled_at = None
    elif target_state == "DISABLED":
        installation.disabled_at = now
    elif target_state == "REVOKED":
        version.status = "REVOKED"
        installations = session.scalars(
            select(Installation).where(Installation.capability_version_id == version.id)
        ).all()
        for related in installations:
            related.state = "REVOKED"
    append_audit(
        session,
        tenant_id=installation.tenant_id,
        actor=actor,
        action=f"INSTALLATION_{target_state}",
        resource=version.version,
        outcome="ALLOW",
        reason_code="VALID_LIFECYCLE_TRANSITION",
        payload_sha256=installation.package_digest,
    )
    session.commit()
    return installation
