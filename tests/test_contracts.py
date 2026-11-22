from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate_spec


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
MANIFEST_SCHEMA_PATH = ROOT / "docs" / "contracts" / "capability-manifest.schema.json"
EVENT_SCHEMA_PATH = ROOT / "docs" / "contracts" / "event-envelope.schema.json"
OPENAPI_PATH = ROOT / "docs" / "contracts" / "openapi.yaml"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validator_for(path: Path) -> Draft202012Validator:
    schema = load_json(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def assert_valid(validator: Draft202012Validator, instance: Any) -> None:
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    assert not errors, "\n".join(
        f"{list(error.path)}: {error.message}" for error in errors
    )


def assert_invalid(validator: Draft202012Validator, instance: Any) -> None:
    assert list(validator.iter_errors(instance)), "fixture unexpectedly passed schema validation"


def test_manifest_schema_is_valid_json_schema() -> None:
    validator_for(MANIFEST_SCHEMA_PATH)


def test_valid_capability_manifest_fixture_passes() -> None:
    assert_valid(
        validator_for(MANIFEST_SCHEMA_PATH),
        load_json(FIXTURES / "manifest-valid.json"),
    )


@pytest.mark.parametrize(
    "fixture_name",
    [
        "manifest-invalid-missing-spec.json",
        "manifest-invalid-extra-property.json",
    ],
)
def test_invalid_capability_manifest_fixtures_fail(fixture_name: str) -> None:
    assert_invalid(
        validator_for(MANIFEST_SCHEMA_PATH),
        load_json(FIXTURES / fixture_name),
    )


def test_event_schema_is_valid_json_schema() -> None:
    validator_for(EVENT_SCHEMA_PATH)


def test_valid_event_envelope_fixture_passes() -> None:
    assert_valid(
        validator_for(EVENT_SCHEMA_PATH),
        load_json(FIXTURES / "event-valid.json"),
    )


def test_event_missing_required_producer_is_rejected() -> None:
    assert_invalid(
        validator_for(EVENT_SCHEMA_PATH),
        load_json(FIXTURES / "event-invalid-missing-producer.json"),
    )


def test_openapi_document_is_valid_and_has_core_invocation_contract() -> None:
    with OPENAPI_PATH.open("r", encoding="utf-8") as handle:
        spec = yaml.safe_load(handle)

    validate_spec(spec)

    assert spec["openapi"] == "3.1.0"
    assert "/v1/capabilities" in spec["paths"]
    assert "/v1/invoke" in spec["paths"]
    invoke = spec["paths"]["/v1/invoke"]["post"]
    assert invoke["operationId"] == "invokeCapability"
    idempotency_header = next(
        parameter
        for parameter in invoke["parameters"]
        if parameter.get("name") == "Idempotency-Key"
    )
    assert idempotency_header["required"] is True
