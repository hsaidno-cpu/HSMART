"""Read-only discovery of HSO plugin and skill catalog entries for HSMART.

Catalog presence is inventory evidence only. No descriptor is marked ELIGIBLE by
this adapter because it does not fetch child repositories, clear rights, prove
instruction parity independently, activate a host, or execute a capability.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Any, Mapping, Protocol, Sequence


HSO_REPOSITORY = "hsaidno-cpu/Hypersystem-Orchestrator"
HSO_CATALOG_REF = "9853bde6d8484b486aa4d163e65f834fa632410b"
CATALOG_PATHS = {
    "plugins": "catalog/plugins.json",
    "repositories": "catalog/repositories.json",
    "instructions": "catalog/instruction-snapshots.json",
    "distribution": "catalog/distribution-registry.json",
    "runtime": "catalog/hso-runtime-capabilities.json",
    "compatibility": "catalog/compatibility-matrix.json",
}
_SHA40 = re.compile(r"^[a-f0-9]{40}$")
_CAPABILITY_KEY = re.compile(r"^[a-z0-9][a-z0-9._:-]{2,159}$")


class HsoCatalogError(RuntimeError):
    """Base error for HSO catalog discovery."""


class HsoCatalogNotConfigured(HsoCatalogError):
    """Raised if no authorized read-only catalog transport is bound."""


class HsoCatalogIntegrityError(HsoCatalogError):
    """Raised when canonical catalog files disagree or contain duplicate identities."""


class HsoCatalogTransport(Protocol):
    """Read-only port for pinned HSO catalog JSON files."""

    def read_json(self, *, path: str, ref: str) -> Mapping[str, Any]:
        """Read a JSON document from the exact repository ref."""
        ...


@dataclass(frozen=True, slots=True)
class HsoCapabilityDiscoveryResult:
    source_repository: str
    source_ref: str
    catalog_revision: str
    observed_at: str
    plugin_count: int
    skill_count: int
    descriptor_count: int
    runtime_capability_ids: tuple[str, ...]
    compatibility_edge_count: int
    compatibility_status_counts: Mapping[str, int]
    descriptors: tuple[Mapping[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": "1.0.0",
            "sourceRepository": self.source_repository,
            "sourceRef": self.source_ref,
            "catalogRevision": self.catalog_revision,
            "observedAt": self.observed_at,
            "counts": {
                "plugins": self.plugin_count,
                "skills": self.skill_count,
                "descriptors": self.descriptor_count,
            },
            "runtimeCapabilityIds": list(self.runtime_capability_ids),
            "compatibility": {
                "edgeCount": self.compatibility_edge_count,
                "statusCounts": dict(self.compatibility_status_counts),
            },
            "descriptors": [dict(item) for item in self.descriptors],
        }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _nonempty_text(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _license_identifier(*sources: Mapping[str, Any]) -> str | None:
    keys = ("license_identifier", "license_id", "license", "spdx_license_id", "spdx_id")
    for source in sources:
        for key in keys:
            value = _nonempty_text(source.get(key))
            if value and value.lower() not in {
                "cleared", "review_required", "not_declared", "not_assessed",
                "private_not_cleared", "inherited_from_canonical_source",
            }:
                return value
    return None


def _rights(
    repository: Mapping[str, Any],
    distribution: Mapping[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    raw_status = " ".join(
        str(value or "")
        for value in (distribution.get("license_status"), repository.get("license_status"))
    ).lower()
    distribution_status = str(distribution.get("distribution_status") or "").lower()
    license_id = _license_identifier(distribution, repository)

    if "noncommercial" in raw_status or "noncommercial" in (license_id or "").lower():
        return (
            {"state": "RESTRICTED", "license": license_id or "PolyForm-Noncommercial-1.0.0",
             "distributionAllowed": False},
            ["USAGE_RIGHTS_RESTRICTED_NONCOMMERCIAL"],
        )
    if "private_not_cleared" in raw_status or "private_source_restricted" in distribution_status:
        return (
            {"state": "RESTRICTED", "license": license_id, "distributionAllowed": False},
            ["PRIVATE_SOURCE_RIGHTS_NOT_CLEARED"],
        )

    installable = distribution_status in {"installable_public", "installable_private"}
    explicitly_cleared = raw_status.strip() == "cleared" or raw_status.strip() == "cleared cleared"
    if license_id and explicitly_cleared and installable:
        return (
            {"state": "CLEARED", "license": license_id, "distributionAllowed": True},
            [],
        )

    blockers = ["LICENSE_IDENTIFIER_OR_CLEARANCE_NOT_VERIFIED"]
    if distribution_status in {"blocked", "review_required", "snapshot_only", "candidate_incomplete", "legacy_redirect"}:
        blockers.append("DISTRIBUTION_NOT_INSTALLABLE")
    return (
        {"state": "UNDECLARED", "license": license_id, "distributionAllowed": False},
        blockers,
    )


def _parity(
    plugin: Mapping[str, Any],
    instruction_plugin: Mapping[str, Any],
) -> dict[str, Any]:
    declared = plugin.get("instruction_skill_count")
    skills = instruction_plugin.get("skills")
    observed = len(skills) if isinstance(skills, list) else 0
    if not isinstance(declared, int) or declared < 0:
        declared = observed
    status = str(plugin.get("source_instruction_parity_status") or "NOT_COMPARED").upper()

    if declared != observed:
        state = "DRIFT"
        drifted = ["INSTRUCTION_SKILL_COUNT_MISMATCH"]
    elif status in {"MATCH", "PASS", "VERIFIED"}:
        state = "PASS"
        drifted = []
    elif "DRIFT" in status or status in {"MISMATCH", "FAIL"}:
        state = "DRIFT"
        drifted = ["SOURCE_INSTRUCTION_PARITY_DRIFT_DETECTED"]
    elif status in {"NOT_APPLICABLE", "N/A"}:
        state = "NOT_APPLICABLE"
        drifted = []
        declared = 0
        observed = 0
    else:
        state = "NOT_COMPARED"
        drifted = []

    return {
        "state": state,
        "sourceFileCount": declared,
        "comparedFileCount": observed,
        "driftedFiles": drifted,
    }


class HsoCapabilityDiscoveryAdapter:
    """Discover plugin and skill identities from a pinned HSO catalog snapshot."""

    def __init__(
        self,
        transport: HsoCatalogTransport | None = None,
        *,
        source_ref: str = HSO_CATALOG_REF,
    ) -> None:
        if not _SHA40.fullmatch(source_ref):
            raise ValueError("source_ref must be a full 40-character Git commit SHA")
        self._transport = transport
        self._source_ref = source_ref

    def readiness(self) -> dict[str, Any]:
        return {
            "state": "TRANSPORT_BOUND_NOT_VERIFIED" if self._transport is not None else "NOT_CONFIGURED",
            "sourceRepository": HSO_REPOSITORY,
            "sourceRef": self._source_ref,
            "accessMode": "READ_ONLY",
            "writeOperationsExposed": False,
            "childRepositoryVerification": "NOT_PERFORMED",
            "runtimeInvocation": "NOT_PERFORMED",
        }

    def discover(self) -> HsoCapabilityDiscoveryResult:
        if self._transport is None:
            raise HsoCatalogNotConfigured("HSO catalog transport is not configured")

        docs = {
            key: self._transport.read_json(path=path, ref=self._source_ref)
            for key, path in CATALOG_PATHS.items()
        }
        plugins_doc = docs["plugins"]
        repositories_doc = docs["repositories"]
        instructions_doc = docs["instructions"]
        distribution_doc = docs["distribution"]
        runtime_doc = docs["runtime"]
        compatibility_doc = docs["compatibility"]

        plugins = self._unique_index(plugins_doc.get("plugins"), "plugin_key", "plugins.json")
        repositories = self._unique_index(repositories_doc.get("repositories"), "repository_id", "repositories.json")
        instruction_plugins = self._unique_index(instructions_doc.get("plugins"), "plugin_key", "instruction-snapshots.json")
        distributions = self._unique_index(distribution_doc.get("plugins"), "plugin_key", "distribution-registry.json")
        runtime_capabilities = runtime_doc.get("capabilities")
        integrations = compatibility_doc.get("integrations")

        if not isinstance(runtime_capabilities, list) or not all(isinstance(x, Mapping) for x in runtime_capabilities):
            raise HsoCatalogIntegrityError("runtime capabilities must be a list of objects")
        if not isinstance(integrations, list) or not all(isinstance(x, Mapping) for x in integrations):
            raise HsoCatalogIntegrityError("compatibility integrations must be a list of objects")

        expected_plugins = plugins_doc.get("expected_plugin_count")
        if expected_plugins != len(plugins):
            raise HsoCatalogIntegrityError("expected_plugin_count does not match plugin records")
        expected_skills = instructions_doc.get("total_skill_records")
        actual_skills = sum(
            len(item.get("skills", []))
            for item in instruction_plugins.values()
            if isinstance(item.get("skills"), list)
        )
        if not isinstance(expected_skills, int) or expected_skills != actual_skills:
            raise HsoCatalogIntegrityError("total_skill_records does not match skill snapshot entries")
        if set(plugins) != set(instruction_plugins):
            raise HsoCatalogIntegrityError("plugin catalog and instruction snapshot identities do not match")
        if distribution_doc.get("plugin_count") != len(distributions):
            raise HsoCatalogIntegrityError("distribution plugin_count does not match distribution records")
        if compatibility_doc.get("integration_count") != len(integrations):
            raise HsoCatalogIntegrityError("compatibility integration_count does not match integration records")

        runtime_by_plugin: dict[str, list[Mapping[str, Any]]] = {}
        for capability in runtime_capabilities:
            plugin_key = _nonempty_text(capability.get("plugin_key"))
            if plugin_key:
                runtime_by_plugin.setdefault(plugin_key, []).append(capability)

        observed_at = _now()
        descriptors: list[Mapping[str, Any]] = []
        for plugin_key, plugin in plugins.items():
            repo_id = plugin.get("source_repository_id")
            repository = repositories.get(repo_id, {}) if isinstance(repo_id, str) else {}
            distribution = distributions.get(plugin_key, {})
            instruction_plugin = instruction_plugins[plugin_key]
            parity = _parity(plugin, instruction_plugin)
            rights, rights_blockers = _rights(repository, distribution)
            runtime_entries = runtime_by_plugin.get(plugin_key, [])
            plugin_blockers = self._blockers(plugin, repository, distribution, parity, rights, runtime_entries, rights_blockers)

            plugin_descriptor = self._descriptor(
                capability_id=f"hso.plugin.{plugin_key}",
                display_name=str(plugin.get("display_name") or plugin_key),
                kind="PLUGIN",
                version=_nonempty_text(plugin.get("release_version")),
                plugin=plugin,
                repository=repository,
                parity=parity,
                rights=rights,
                runtime_entries=runtime_entries,
                blockers=plugin_blockers,
                observed_at=observed_at,
            )
            descriptors.append(plugin_descriptor)

            skills = instruction_plugin.get("skills")
            if not isinstance(skills, list):
                raise HsoCatalogIntegrityError(f"instruction snapshot skills for {plugin_key} is not a list")
            for skill in skills:
                if not isinstance(skill, Mapping):
                    raise HsoCatalogIntegrityError(f"skill record for {plugin_key} must be an object")
                skill_name = _nonempty_text(skill.get("skill_name"))
                if not skill_name:
                    raise HsoCatalogIntegrityError(f"skill_name missing for plugin {plugin_key}")
                capability_id = f"hso.skill.{plugin_key}.{skill_name}"
                if not _CAPABILITY_KEY.fullmatch(capability_id):
                    raise HsoCatalogIntegrityError(f"invalid capability ID: {capability_id}")
                descriptors.append(self._descriptor(
                    capability_id=capability_id,
                    display_name=skill_name,
                    kind="SKILL",
                    version=_nonempty_text(plugin.get("release_version")),
                    plugin=plugin,
                    repository=repository,
                    parity=parity,
                    rights=rights,
                    runtime_entries=runtime_entries,
                    blockers=plugin_blockers,
                    observed_at=observed_at,
                ))

        status_counts = Counter(str(item.get("status") or "UNKNOWN") for item in integrations)
        runtime_ids = tuple(sorted(
            str(item.get("capability_id"))
            for item in runtime_capabilities
            if isinstance(item.get("capability_id"), str)
        ))
        return HsoCapabilityDiscoveryResult(
            source_repository=HSO_REPOSITORY,
            source_ref=self._source_ref,
            catalog_revision=str(plugins_doc.get("catalog_revision") or "UNKNOWN"),
            observed_at=observed_at,
            plugin_count=len(plugins),
            skill_count=actual_skills,
            descriptor_count=len(descriptors),
            runtime_capability_ids=runtime_ids,
            compatibility_edge_count=len(integrations),
            compatibility_status_counts=dict(sorted(status_counts.items())),
            descriptors=tuple(descriptors),
        )

    @staticmethod
    def _unique_index(items: Any, key: str, document: str) -> dict[str, Mapping[str, Any]]:
        if not isinstance(items, list) or not all(isinstance(item, Mapping) for item in items):
            raise HsoCatalogIntegrityError(f"{document} {key} collection must be a list of objects")
        result: dict[str, Mapping[str, Any]] = {}
        for item in items:
            value = _nonempty_text(item.get(key))
            if not value:
                raise HsoCatalogIntegrityError(f"{document} contains an empty {key}")
            if value in result:
                raise HsoCatalogIntegrityError(f"{document} contains duplicate {key}: {value}")
            result[value] = item
        return result

    @staticmethod
    def _blockers(
        plugin: Mapping[str, Any],
        repository: Mapping[str, Any],
        distribution: Mapping[str, Any],
        parity: Mapping[str, Any],
        rights: Mapping[str, Any],
        runtime_entries: Sequence[Mapping[str, Any]],
        rights_blockers: Sequence[str],
    ) -> list[str]:
        blockers = set(str(x) for x in distribution.get("blockers", []) if isinstance(x, str))
        if not repository.get("url") or not repository.get("pinned_commit"):
            blockers.add("CANONICAL_CHILD_SOURCE_NOT_PINNED")
        else:
            blockers.add("CHILD_SOURCE_NOT_INDEPENDENTLY_VERIFIED")
        if rights.get("state") != "CLEARED" or rights.get("distributionAllowed") is not True:
            blockers.update(rights_blockers or ["USAGE_RIGHTS_NOT_CLEARED"])
        if parity.get("state") != "PASS":
            blockers.add("INSTRUCTION_PARITY_NOT_PASSED")
        if not runtime_entries:
            blockers.add("HOST_RUNTIME_CAPABILITY_NOT_REGISTERED")
        else:
            blockers.add("HOST_ACTIVATION_AND_INVOCATION_NOT_PROVEN")
        blockers.add("INTERFACE_CONTRACT_NOT_TESTED_FOR_TARGET_HOST")
        if plugin.get("version_alignment_state") not in (None, "ALIGNED", "SOURCE_AND_PLATFORM_MATCH"):
            blockers.add("PLUGIN_PLATFORM_VERSION_ALIGNMENT_NOT_CLEARED")
        if distribution.get("distribution_status") == "legacy_redirect":
            blockers.add("LEGACY_ALIAS_NOT_INDEPENDENTLY_INSTALLABLE")
        return sorted(blockers)

    def _descriptor(
        self,
        *,
        capability_id: str,
        display_name: str,
        kind: str,
        version: str | None,
        plugin: Mapping[str, Any],
        repository: Mapping[str, Any],
        parity: Mapping[str, Any],
        rights: Mapping[str, Any],
        runtime_entries: Sequence[Mapping[str, Any]],
        blockers: Sequence[str],
        observed_at: str,
    ) -> Mapping[str, Any]:
        repo_url = _nonempty_text(repository.get("url"))
        commit = _nonempty_text(repository.get("pinned_commit"))
        if not commit:
            commit = _nonempty_text(plugin.get("source_commit"))
        if not commit:
            commit = None
        if commit and not _SHA40.fullmatch(commit):
            commit = None
        source_state = "CANDIDATE" if repo_url else "NOT_IDENTIFIED"
        if not repo_url:
            commit = None

        runtime = next(
            (entry for entry in runtime_entries
             if entry.get("enabled") is True and entry.get("test_only") is False),
            None,
        )
        protocol = "MCP" if runtime and runtime.get("transport") == "STREAMABLE_HTTP" else "NONE"
        host_id = _nonempty_text(runtime.get("adapter_id")) if runtime else None
        eligibility_blockers = list(blockers) or ["RUNTIME_EVIDENCE_NOT_ASSESSED"]

        return {
            "schemaVersion": "1.0.0",
            "capabilityId": capability_id,
            "identity": {"displayName": display_name, "kind": kind, "version": version},
            "ownership": {
                "ownerSystem": "HSO",
                "ownerReference": f"https://github.com/{HSO_REPOSITORY}/tree/{self._source_ref}",
            },
            "source": {
                "repository": repo_url,
                "ref": commit,
                "commitSha": commit,
                "contentDigest": None,
                "state": source_state,
            },
            "rights": dict(rights),
            "instructionParity": dict(parity),
            "interface": {
                "protocol": protocol,
                "contractVersion": None,
                "contractTestState": "NOT_CONFIGURED",
            },
            "hostRuntime": {
                "hostId": host_id,
                "activationState": "NOT_CONFIGURED",
                "invocationState": "NOT_RUN",
                "evidenceReference": None,
            },
            "permissions": [],
            "eligibility": {
                "state": "BLOCKED",
                "policyVersion": "uede-hso-capability-readiness-v1",
                "evaluatedAt": observed_at,
                "blockers": eligibility_blockers,
            },
            "observedAt": observed_at,
        }
