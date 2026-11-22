from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate-json.py"
SPEC = importlib.util.spec_from_file_location("hsmart_validate_json", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def test_duplicate_object_keys_are_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate object key"):
        VALIDATOR.reject_duplicate_keys([("same", 1), ("same", 2)])


def test_non_standard_json_numeric_constants_are_rejected() -> None:
    with pytest.raises(ValueError, match="non-standard numeric constant"):
        json.loads('{"value": NaN}', parse_constant=VALIDATOR.reject_nonfinite)


def test_unique_object_keys_are_preserved() -> None:
    assert VALIDATOR.reject_duplicate_keys([("first", 1), ("second", 2)]) == {
        "first": 1,
        "second": 2,
    }


def test_json_discovery_prunes_generated_and_vendor_directories(tmp_path: Path) -> None:
    source = tmp_path / "contracts"
    source.mkdir()
    (source / "valid.json").write_text('{"valid": true}', encoding="utf-8")

    generated = tmp_path / ".venv" / "site-packages" / "sample"
    generated.mkdir(parents=True)
    (generated / "must-not-scan.json").write_text("{}", encoding="utf-8")

    files = VALIDATOR.discover_json_files(tmp_path)
    assert files == [source / "valid.json"]
