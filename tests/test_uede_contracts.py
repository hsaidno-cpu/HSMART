from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from hsmart_platform.uede_contracts import execution_receipt_semantic_errors


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "docs" / "contracts"
DIGEST = "sha256:" + ("a" * 64)
SHA = "a" * 40


def load_schema(name: str) -> dict[str, Any]:
    with (SCHEMA_DIR / name).open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    return schema


def validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(name), format_checker=FormatChecker())


def sample_roadmap() -> dict[str, Any]:
    return {
        "schemaVersion": "1.0.0",
        "snapshotId": "pre-hsmart-2026-11-25-r1",
        "source": {
            "system": "PRE",
            "roadmapId": "HSMART-ROADMAP-PC-001",
            "revision": "1.0.0",
            "locator": "https://app.notion.com/p/42099868397f8100adc1f016d0994669",
            "updatedAt": "2026-11-25T10:00:00Z",
        },
        "capturedAt": "2026-11-25T10:30:00Z",
        "completeness": {
            "state": "COMPLETE", "paginationComplete": True, "pageCount": 1, "recordCount": 1,
            "expectedRecordCount": 1, "contentDigest": DIGEST, "freshness": "FRESH", "missingReferences": [],
        },
        "authority": {
            "owner": "PRE", "baselineState": "APPROVED", "decisionAuthority": "GOV-01",
            "approvalReference": "https://app.notion.com/p/42099868397f8100adc1f016d0994669",
            "approvedAt": "2026-11-25T09:00:00Z",
        },
        "roadmap": {
            "title": "HSMART Progressive Completion Roadmap", "stage": "R1",
            "workItems": [{
                "workItemId": "PC-007", "title": "Run independent KM 1 exit evaluation", "priority": "P1",
                "status": "IN_PROGRESS", "gateState": "HOLD", "dependencies": ["PC-005", "PC-006"],
                "acceptanceCriteria": ["GOV-01 records KM 1 ACCEPTED or return-to-work decision"],
                "sourceLocator": "https://github.com/hsaidno-cpu/HSMART/issues/20",
            }],
        },
        "accessMode": "READ_ONLY",
    }


def sample_capability() -> dict[str, Any]:
    return {
        "schemaVersion": "1.0.0", "capabilityId": "hso.skill-analyzer",
        "identity": {"displayName": "Skill Analyzer", "kind": "SKILL", "version": "1.3.0"},
        "ownership": {"ownerSystem": "HSO", "ownerReference": "hsaidno-cpu/Hypersystem-Orchestrator"},
        "source": {"repository": None, "ref": None, "commitSha": None, "contentDigest": None, "state": "NOT_IDENTIFIED"},
        "rights": {"state": "UNDECLARED", "license": None, "distributionAllowed": False},
        "instructionParity": {"state": "NOT_COMPARED", "sourceFileCount": 12, "comparedFileCount": 0, "driftedFiles": []},
        "interface": {"protocol": "MCP", "contractVersion": None, "contractTestState": "NOT_CONFIGURED"},
        "hostRuntime": {"hostId": None, "activationState": "NOT_CONFIGURED", "invocationState": "NOT_RUN", "evidenceReference": None},
        "permissions": ["read:catalog"],
        "eligibility": {
            "state": "BLOCKED", "policyVersion": "uede-capability-readiness-v1",
            "evaluatedAt": "2026-11-25T10:30:00Z",
            "blockers": ["SOURCE_NOT_IDENTIFIED", "RIGHTS_UNDECLARED", "HOST_NOT_CONFIGURED"],
        },
        "observedAt": "2026-11-25T10:30:00Z",
    }


def sample_receipt() -> dict[str, Any]:
    return {
        "schemaVersion": "1.0.0", "executionId": "UEDE-EXEC-TEST-001", "workItemReference": "HSMART:PC-007",
        "planReference": {
            "schemaVersion": "1.0.0",
            "artifactReference": "https://github.com/hsaidno-cpu/Hypersystem-Orchestrator/blob/main/contracts/hso-workflow-plan.schema.json",
            "contentDigest": DIGEST,
        },
        "startedAt": "2026-11-25T10:00:00Z", "finishedAt": "2026-11-25T10:05:00Z", "executionState": "COMPLETED",
        "target": {
            "repository": "hsaidno-cpu/HSMART", "branch": "feat/example", "baseCommitSha": "b" * 40,
            "headCommitSha": SHA, "changedFiles": ["docs/example.md"],
            "pullRequest": "https://github.com/hsaidno-cpu/HSMART/pull/33",
        },
        "ciRuns": [{
            "runReference": "https://github.com/hsaidno-cpu/HSMART/actions/runs/123",
            "commitSha": SHA, "conclusion": "SUCCESS", "completedAt": "2026-11-25T10:04:00Z",
        }],
        "verification": {
            "state": "PASS", "verifiedCommitSha": SHA,
            "evidenceReferences": ["https://github.com/hsaidno-cpu/HSMART/actions/runs/123"], "limitations": [],
        },
        "roadmapEffect": {"canonicalStageMutation": False, "writeBackMode": "EXECUTION_FACTS_ONLY"},
    }


@pytest.mark.parametrize("name", [
    "uede-roadmap-snapshot.schema.json",
    "uede-capability-descriptor.schema.json",
    "uede-execution-receipt.schema.json",
])
def test_uede_schema_definitions_are_valid(name: str) -> None:
    load_schema(name)


def test_complete_read_only_pre_snapshot_is_valid() -> None:
    assert not list(validator("uede-roadmap-snapshot.schema.json").iter_errors(sample_roadmap()))


def test_complete_pre_snapshot_cannot_claim_incomplete_pagination() -> None:
    sample = sample_roadmap()
    sample["completeness"]["paginationComplete"] = False
    assert list(validator("uede-roadmap-snapshot.schema.json").iter_errors(sample))


def test_approved_pre_baseline_requires_approval_reference_and_time() -> None:
    sample = sample_roadmap()
    sample["authority"]["approvalReference"] = None
    sample["authority"]["approvedAt"] = None
    assert list(validator("uede-roadmap-snapshot.schema.json").iter_errors(sample))


def test_partial_pre_snapshot_must_not_be_upgraded_to_complete() -> None:
    sample = sample_roadmap()
    sample["completeness"].update({
        "state": "PARTIAL", "paginationComplete": False, "freshness": "UNKNOWN",
        "missingReferences": ["next-page"],
    })
    assert not list(validator("uede-roadmap-snapshot.schema.json").iter_errors(sample))


def test_catalogued_but_unverified_skill_is_blocked_not_dispatchable() -> None:
    assert not list(validator("uede-capability-descriptor.schema.json").iter_errors(sample_capability()))


@pytest.mark.parametrize("mutate", [
    lambda x: x["source"].update({"state": "NOT_IDENTIFIED"}),
    lambda x: x["rights"].update({"state": "UNDECLARED", "distributionAllowed": False}),
    lambda x: x["instructionParity"].update({"state": "DRIFT", "driftedFiles": ["SKILL.md"]}),
    lambda x: x["interface"].update({"contractTestState": "NOT_RUN"}),
    lambda x: x["hostRuntime"].update({"activationState": "NOT_CONFIGURED"}),
    lambda x: x["hostRuntime"].update({"invocationState": "NOT_RUN"}),
])
def test_eligibility_cannot_pass_when_any_evidence_plane_fails(mutate) -> None:
    sample = sample_capability()
    sample["eligibility"] = {
        "state": "ELIGIBLE", "policyVersion": "uede-capability-readiness-v1",
        "evaluatedAt": "2026-11-25T10:30:00Z", "blockers": [],
    }
    sample["source"] = {
        "repository": "https://github.com/acme/tool", "ref": "main", "commitSha": SHA,
        "contentDigest": DIGEST, "state": "VERIFIED",
    }
    sample["rights"] = {"state": "CLEARED", "license": "MIT", "distributionAllowed": True}
    sample["instructionParity"] = {
        "state": "PASS", "sourceFileCount": 1, "comparedFileCount": 1, "driftedFiles": [],
    }
    sample["interface"] = {"protocol": "MCP", "contractVersion": "1.0.0", "contractTestState": "PASS"}
    sample["hostRuntime"] = {
        "hostId": "host-01", "activationState": "PASS", "invocationState": "PASS",
        "evidenceReference": "https://example.com/evidence/host-probe",
    }
    mutate(sample)
    assert list(validator("uede-capability-descriptor.schema.json").iter_errors(sample))


def test_execution_receipt_with_matching_verified_commit_is_valid() -> None:
    sample = sample_receipt()
    assert not list(validator("uede-execution-receipt.schema.json").iter_errors(sample))
    assert execution_receipt_semantic_errors(sample) == ()


def test_execution_receipt_rejects_pass_without_exact_commit() -> None:
    sample = sample_receipt()
    sample["verification"]["verifiedCommitSha"] = "c" * 40
    assert execution_receipt_semantic_errors(sample) == ("VERIFIED_COMMIT_SHA_MISMATCH",)


def test_execution_receipt_rejects_ci_from_a_different_commit() -> None:
    sample = sample_receipt()
    sample["ciRuns"][0]["commitSha"] = "d" * 40
    assert execution_receipt_semantic_errors(sample) == ("EXACT_HEAD_CI_SUCCESS_REQUIRED",)


def test_execution_receipt_cannot_mutate_canonical_pre_stage() -> None:
    sample = sample_receipt()
    sample["roadmapEffect"]["canonicalStageMutation"] = True
    assert list(validator("uede-execution-receipt.schema.json").iter_errors(sample))


def test_execution_receipt_pass_requires_evidence() -> None:
    sample = sample_receipt()
    sample["verification"]["evidenceReferences"] = []
    assert list(validator("uede-execution-receipt.schema.json").iter_errors(sample))


def test_all_contracts_reject_unknown_top_level_fields() -> None:
    cases = [
        ("uede-roadmap-snapshot.schema.json", sample_roadmap()),
        ("uede-capability-descriptor.schema.json", sample_capability()),
        ("uede-execution-receipt.schema.json", sample_receipt()),
    ]
    for name, sample in cases:
        candidate = copy.deepcopy(sample)
        candidate["unregisteredAdminFlag"] = True
        assert list(validator(name).iter_errors(candidate))
