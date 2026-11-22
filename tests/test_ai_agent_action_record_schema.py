from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "contracts" / "ai-agent-action-record.schema.json"


def load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    return schema


def valid_branch_write_event() -> dict[str, Any]:
    zero_digest = "sha256:" + ("0" * 64)
    return {
        "schema_version": "1.0.0",
        "event_id": "HSMART-EVT-TEST-0001",
        "occurred_at_utc": "2026-11-22T00:00:00Z",
        "event_type": "github.branch.write",
        "actor": {
            "actor_type": "orchestrator",
            "actor_id": "hsmart.gov05.engineering.orchestrator",
            "role_id": "GOV-05",
            "orchestrator_id": "hsmart.gov05.engineering.orchestrator",
            "sub_agent_ids": ["hsmart.gov05.implementation-agent"],
            "human_approver_id": "Harysaidno",
            "session_or_runtime_id": "runtime-test-001",
        },
        "task": {
            "task_id": "TASK-TEST-001",
            "objective": "Validate an authorized working-branch file update",
            "request_reference": "conversation://test-approval",
            "issue_or_ticket_reference": None,
            "parent_task_id": None,
            "urgency": "routine",
        },
        "authorization": {
            "grant_id": "HSMART-AUTH-GOV01-TEST-001",
            "approved_by": "Harysaidno",
            "approval_reference": "HSMART-AUTH-GOV01-TEST-001",
            "scope_digest": zero_digest,
            "grant_valid_until_utc": "2026-11-23T00:00:00Z",
            "revocation_reference": None,
            "authorization_mode": "explicit_grant",
        },
        "policy_decision": {
            "policy_id": "HSMART-GOV-AI-POL-001",
            "policy_version": "1.0.0",
            "decision_id": "POLICY-DECISION-TEST-001",
            "outcome": "allow",
            "reason_code": "GRANT_SCOPE_MATCH",
            "risk_class": "R2",
            "evaluated_at_utc": "2026-11-22T00:00:00Z",
        },
        "target": {
            "system": "github",
            "resource": "hsaidno-cpu/HSMART/docs/example.md",
            "repository_full_name": "hsaidno-cpu/HSMART",
            "base_ref": "main",
            "base_sha": zero_digest,
            "branch": "work/example",
            "file_paths": ["docs/example.md"],
            "notion_page_id": None,
            "notion_property_names": [],
            "commit_sha": None,
            "pull_request_url": None,
            "environment": "branch",
        },
        "action": {
            "operation": "update_file",
            "category": "branch_write",
            "mutating": True,
            "result": "success",
            "before_content_digest": zero_digest,
            "after_content_digest": zero_digest,
            "change_summary": "Update the authorized file in a working branch",
            "scope_deviation": False,
            "scope_deviation_reference": None,
        },
        "provenance": {
            "model_provider": "test-provider",
            "model_id": "test-model",
            "model_version": "test-version",
            "deployment_id": "test-deployment",
            "prompt_template_id": "test-template",
            "prompt_template_version": "1.0.0",
            "policy_config_digest": zero_digest,
            "skills": [
                {
                    "skill_id": "test-skill",
                    "version": "1.0.0",
                    "content_digest": zero_digest,
                    "source_reference": "https://example.invalid/skill",
                    "sub_skill_ids": ["test-sub-skill"],
                }
            ],
            "tools": [
                {
                    "tool_id": "github-update-file",
                    "version": "unknown",
                    "connector_id": "github-connector",
                    "permission_scope_reference": "HSMART-AUTH-GOV01-TEST-001",
                }
            ],
            "retrieval_source_snapshot": None,
            "configuration_digest": zero_digest,
        },
        "tool_invocations": [
            {
                "tool_id": "github-update-file",
                "connector_id": "github-connector",
                "tool_version": "unknown",
                "operation": "update_file",
                "request_id": "tool-request-001",
                "result": "success",
                "started_at_utc": "2026-11-22T00:00:00Z",
                "finished_at_utc": "2026-11-22T00:00:01Z",
                "input_digest": zero_digest,
                "output_digest": zero_digest,
                "secret_material_exposed": False,
                "redaction_applied": True,
                "trace_reference": "trace-001",
            }
        ],
        "evidence": {
            "source_references": ["https://github.com/hsaidno-cpu/HSMART"],
            "test_runs": ["CI-TEST-RUN-001"],
            "evaluation_references": ["EVAL-TEST-001"],
            "finding_references": [],
            "artifact_digests": [zero_digest],
            "human_decision_reference": "HSMART-AUTH-GOV01-TEST-001",
        },
        "outcome": {
            "status": "completed",
            "summary": "Authorized branch change passed test validation",
            "escalated": False,
            "escalation_reference": None,
            "human_disposition": "accepted",
            "limitations": [],
        },
        "audit_integrity": {
            "hash_algorithm": "SHA-256",
            "previous_event_hash": "genesis",
            "event_hash": zero_digest,
            "signature_reference": None,
            "append_only_store_reference": "test://append-only-store",
            "integrity_verified_at_utc": "2026-11-22T00:00:02Z",
        },
    }


def validator() -> Draft202012Validator:
    return Draft202012Validator(load_schema(), format_checker=FormatChecker())


def test_ai_agent_action_record_schema_is_valid() -> None:
    load_schema()


def test_authorized_mutating_event_passes() -> None:
    errors = list(validator().iter_errors(valid_branch_write_event()))
    assert not errors, "\n".join(error.message for error in errors)


def test_allowed_mutating_event_requires_gov01_grant() -> None:
    event = valid_branch_write_event()
    event["authorization"]["grant_id"] = None
    errors = list(validator().iter_errors(event))
    assert errors


def test_ai_agent_cannot_record_merge_as_permitted_action() -> None:
    event = valid_branch_write_event()
    event["action"]["category"] = "merge"
    errors = list(validator().iter_errors(event))
    assert errors


def test_raw_secret_exposure_is_rejected() -> None:
    event = valid_branch_write_event()
    event["tool_invocations"][0]["secret_material_exposed"] = True
    errors = list(validator().iter_errors(event))
    assert errors


def test_missing_model_version_provenance_is_rejected() -> None:
    event = valid_branch_write_event()
    del event["provenance"]["model_version"]
    errors = list(validator().iter_errors(event))
    assert errors
