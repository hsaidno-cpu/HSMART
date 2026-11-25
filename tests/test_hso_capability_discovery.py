from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from hsmart_platform.adapters.hso_capability_discovery import (
    CATALOG_PATHS,
    HSO_CATALOG_REF,
    HsoCatalogIntegrityError,
    HsoCatalogNotConfigured,
    HsoCapabilityDiscoveryAdapter,
)


class FakeCatalogTransport:
    def __init__(self, docs: dict[str, Mapping[str, Any]]) -> None:
        self.docs = docs
        self.calls: list[tuple[str, str]] = []

    def read_json(self, *, path: str, ref: str) -> Mapping[str, Any]:
        self.calls.append((path, ref))
        return self.docs[path]


def _documents() -> dict[str, Mapping[str, Any]]:
    plugin = {
        "plugin_key": "sample-plugin",
        "display_name": "Sample Plugin",
        "source_repository_id": "sample-repo",
        "release_version": "1.2.0",
        "instruction_skill_count": 2,
        "source_instruction_parity_status": "MATCH",
        "version_alignment_state": "ALIGNED",
    }
    skills = {
        "plugin_key": "sample-plugin",
        "skill_count": 2,
        "skills": [
            {"skill_name": "first-skill", "source_uri": "skills://plugins/sample-plugin/first-skill"},
            {"skill_name": "second-skill", "source_uri": "skills://plugins/sample-plugin/second-skill"},
        ],
    }
    return {
        CATALOG_PATHS["plugins"]: {
            "catalog_revision": "2026-11-23", "expected_plugin_count": 1, "plugins": [plugin],
        },
        CATALOG_PATHS["repositories"]: {
            "repositories": [{
                "repository_id": "sample-repo", "url": "https://github.com/acme/sample-plugin",
                "pinned_commit": "a" * 40, "license_status": "NOT_DECLARED_AT_REPOSITORY_ROOT",
            }],
        },
        CATALOG_PATHS["instructions"]: {
            "total_skill_records": 2, "plugins": [skills],
        },
        CATALOG_PATHS["distribution"]: {
            "plugin_count": 1, "plugins": [{
                "plugin_key": "sample-plugin", "distribution_status": "blocked",
                "license_status": "not_declared", "blockers": ["PACKAGE_ARTIFACT_NOT_PUBLISHED"],
            }],
        },
        CATALOG_PATHS["runtime"]: {
            "capabilities": [{
                "capability_id": "plugin.skill.invoke.remote-mcp.sample-plugin",
                "plugin_key": "sample-plugin", "adapter_id": "remote-mcp-test-host",
                "enabled": True, "test_only": False, "transport": "STREAMABLE_HTTP",
            }],
        },
        CATALOG_PATHS["compatibility"]: {
            "integration_count": 1, "integrations": [{"integration_id": "INT-1", "status": "CONTRACT_TESTED"}],
        },
    }


def _descriptor_validator() -> Draft202012Validator:
    schema_path = Path(__file__).resolve().parents[1] / "docs/contracts/uede-capability-descriptor.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def test_no_transport_is_not_configured_and_never_calls_network() -> None:
    adapter = HsoCapabilityDiscoveryAdapter()
    assert adapter.readiness()["state"] == "NOT_CONFIGURED"
    assert adapter.readiness()["accessMode"] == "READ_ONLY"
    assert adapter.readiness()["writeOperationsExposed"] is False
    with pytest.raises(HsoCatalogNotConfigured):
        adapter.discover()


def test_catalog_discovery_emits_plugin_and_skill_descriptors() -> None:
    transport = FakeCatalogTransport(_documents())
    result = HsoCapabilityDiscoveryAdapter(transport).discover()
    assert result.plugin_count == 1
    assert result.skill_count == 2
    assert result.descriptor_count == 3
    assert result.runtime_capability_ids == ("plugin.skill.invoke.remote-mcp.sample-plugin",)
    assert [call[1] for call in transport.calls] == [HSO_CATALOG_REF] * 6
    assert all(not list(_descriptor_validator().iter_errors(dict(item))) for item in result.descriptors)


def test_catalog_presence_never_becomes_runtime_eligibility() -> None:
    result = HsoCapabilityDiscoveryAdapter(FakeCatalogTransport(_documents())).discover()
    assert all(item["eligibility"]["state"] == "BLOCKED" for item in result.descriptors)
    assert all(item["hostRuntime"]["activationState"] == "NOT_CONFIGURED" for item in result.descriptors)
    assert all(item["hostRuntime"]["invocationState"] == "NOT_RUN" for item in result.descriptors)
    assert all(item["interface"]["contractTestState"] == "NOT_CONFIGURED" for item in result.descriptors)


def test_remote_mcp_registration_does_not_prove_host_activation() -> None:
    result = HsoCapabilityDiscoveryAdapter(FakeCatalogTransport(_documents())).discover()
    plugin = result.descriptors[0]
    assert plugin["interface"]["protocol"] == "MCP"
    assert plugin["hostRuntime"]["hostId"] == "remote-mcp-test-host"
    assert plugin["hostRuntime"]["activationState"] == "NOT_CONFIGURED"


def test_unmatched_plugin_and_instruction_snapshot_is_rejected() -> None:
    docs = _documents()
    docs[CATALOG_PATHS["instructions"]] = {"total_skill_records": 0, "plugins": []}
    with pytest.raises(HsoCatalogIntegrityError):
        HsoCapabilityDiscoveryAdapter(FakeCatalogTransport(docs)).discover()


def test_expected_plugin_count_mismatch_is_rejected() -> None:
    docs = _documents()
    docs[CATALOG_PATHS["plugins"]] = {"catalog_revision": "2026-11-23", "expected_plugin_count": 2, "plugins": []}
    with pytest.raises(HsoCatalogIntegrityError):
        HsoCapabilityDiscoveryAdapter(FakeCatalogTransport(docs)).discover()


def test_noncommercial_license_is_restricted() -> None:
    docs = _documents()
    repos = dict(docs[CATALOG_PATHS["repositories"]])
    repos["repositories"] = [{
        "repository_id": "sample-repo", "url": "https://github.com/acme/sample-plugin",
        "pinned_commit": "a" * 40, "license_status": "POLYFORM_NONCOMMERCIAL_1_0_0",
    }]
    docs[CATALOG_PATHS["repositories"]] = repos
    result = HsoCapabilityDiscoveryAdapter(FakeCatalogTransport(docs)).discover()
    assert result.descriptors[0]["rights"]["state"] == "RESTRICTED"
    assert result.descriptors[0]["rights"]["distributionAllowed"] is False


def test_unverified_child_source_stays_candidate_not_verified() -> None:
    result = HsoCapabilityDiscoveryAdapter(FakeCatalogTransport(_documents())).discover()
    source = result.descriptors[0]["source"]
    assert source["state"] == "CANDIDATE"
    assert source["contentDigest"] is None


def test_source_and_platform_match_is_not_misclassified_as_version_drift() -> None:
    docs = _documents()
    plugins = dict(docs[CATALOG_PATHS["plugins"]])
    items = [dict(item) for item in plugins["plugins"]]
    items[0]["version_alignment_state"] = "SOURCE_AND_PLATFORM_MATCH"
    plugins["plugins"] = items
    docs[CATALOG_PATHS["plugins"]] = plugins
    result = HsoCapabilityDiscoveryAdapter(FakeCatalogTransport(docs)).discover()
    assert "PLUGIN_PLATFORM_VERSION_ALIGNMENT_NOT_CLEARED" not in result.descriptors[0]["eligibility"]["blockers"]


def test_catalog_digest_or_repository_metadata_cannot_clear_license() -> None:
    result = HsoCapabilityDiscoveryAdapter(FakeCatalogTransport(_documents())).discover()
    assert result.descriptors[0]["rights"]["state"] == "UNDECLARED"
    assert result.descriptors[0]["rights"]["distributionAllowed"] is False
