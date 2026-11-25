from __future__ import annotations

from collections import defaultdict
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from hsmart_platform.adapters.pre_readonly import (
    PRE_EVALUATION_LOG_SOURCE,
    PRE_TRANSITION_QUEUE_SOURCE,
    InvalidSourceRecord,
    PaginationProtocolError,
    PreAdapterNotConfigured,
    PreReadOnlyAdapter,
    ReadOnlyRowsPage,
)


SCHEMA_PATH = "docs/contracts/uede-pre-readonly-snapshot.schema.json"


class FakeTransport:
    def __init__(self, pages_by_source: dict[str, list[ReadOnlyRowsPage]]) -> None:
        self.pages = {key: list(value) for key, value in pages_by_source.items()}
        self.calls: list[tuple[str, str | None]] = []

    def query_rows(self, *, data_source_url: str, page_size: int, start_cursor: str | None) -> ReadOnlyRowsPage:
        self.calls.append((data_source_url, start_cursor))
        pages = self.pages[data_source_url]
        index = 0 if start_cursor is None else int(start_cursor)
        return pages[index]


def _schema_validator() -> Draft202012Validator:
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / SCHEMA_PATH
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _evaluation_row(**overrides: Any) -> dict[str, Any]:
    row = {
        "url": "https://example.com/pre/evaluations/1",
        "Evaluation ID": 1,
        "Evaluation Title": "HSMART KM 1 checkpoint",
        "Evaluation Type": "Milestone Acceptance",
        "Evaluator Role": "Human decision owner",
        "Gate State": "HOLD",
        "Next Disposition": "HOLD",
        "PRE Stage": "R6 Milestone Acceptance",
        "Delivery Completion %": 75,
        "Milestone Acceptance %": 0,
        "Verification Coverage %": 40,
        "Evidence Coverage": "Partial evidence",
        "Denominator & Calculation": "3 of 4 required items evidenced",
        "Uncertainty & Limitations": "Not all required evidence verified",
        "Related Work Item": '["https://example.com/work-items/PC-007"]',
        "Supporting Evidence": '["https://example.com/evidence/ci"]',
    }
    row.update(overrides)
    return row


def _transition_row(**overrides: Any) -> dict[str, Any]:
    row = {
        "url": "https://example.com/pre/transitions/1",
        "Request ID": 1,
        "Request": "Request R5 to R6",
        "Project ID": "HSMART",
        "Scope ID": "HSMART-KM1",
        "Correlation ID": "corr-1",
        "Idempotency Key": "idem-1",
        "From Stage": "R5 Formative Check",
        "Requested Stage": "R6 Milestone Acceptance",
        "Request State": "HOLD",
        "Gate Decision": "HOLD",
        "date:Evaluated At:start": "2026-11-25",
        "Block Reasons": "PC-007 evidence incomplete",
        "Evidence Envelope JSON": '{"evidenceCount": 2}',
        "Evaluation Receipt JSON": '{"decision": "HOLD"}',
        "Approval Receipt JSON": None,
        "Work Item": '["https://example.com/work-items/PC-007"]',
    }
    row.update(overrides)
    return row


def test_adapter_is_explicitly_not_configured_without_transport() -> None:
    adapter = PreReadOnlyAdapter()
    assert adapter.readiness()["state"] == "NOT_CONFIGURED"
    assert adapter.readiness()["accessMode"] == "READ_ONLY"
    assert adapter.readiness()["writeOperationsExposed"] is False
    with pytest.raises(PreAdapterNotConfigured):
        adapter.read_evaluation_log()


def test_reads_all_evaluation_pages_and_marks_freshness_unknown() -> None:
    transport = FakeTransport({
        PRE_EVALUATION_LOG_SOURCE: [
            ReadOnlyRowsPage([_evaluation_row()], has_more=True, next_cursor="1"),
            ReadOnlyRowsPage([_evaluation_row(**{"Evaluation ID": 2, "url": "https://example.com/pre/evaluations/2"})], has_more=False),
        ]
    })
    snapshot = PreReadOnlyAdapter(transport).read_evaluation_log()
    payload = snapshot.to_dict()
    assert payload["pagination"]["state"] == "COMPLETE"
    assert payload["pagination"]["pagesRead"] == 2
    assert payload["pagination"]["recordCount"] == 2
    assert payload["freshness"]["state"] == "UNKNOWN"
    assert payload["accessMode"] == "READ_ONLY"
    assert [call[1] for call in transport.calls] == [None, "1"]
    assert not list(_schema_validator().iter_errors(payload))


def test_transition_queue_preserves_hold_and_does_not_apply_it() -> None:
    transport = FakeTransport({
        PRE_TRANSITION_QUEUE_SOURCE: [
            ReadOnlyRowsPage([_transition_row()], has_more=False)
        ]
    })
    payload = PreReadOnlyAdapter(transport).read_transition_queue().to_dict()
    assert payload["records"][0]["requestState"] == "HOLD"
    assert payload["records"][0]["gateDecision"] == "HOLD"
    assert payload["records"][0]["approvalReceipt"] is None
    assert not list(_schema_validator().iter_errors(payload))


def test_max_page_limit_returns_explicit_partial_snapshot() -> None:
    transport = FakeTransport({
        PRE_EVALUATION_LOG_SOURCE: [
            ReadOnlyRowsPage([_evaluation_row()], has_more=True, next_cursor="1"),
            ReadOnlyRowsPage([_evaluation_row(**{"Evaluation ID": 2})], has_more=True, next_cursor="2"),
        ]
    })
    payload = PreReadOnlyAdapter(transport, max_pages=1).read_evaluation_log().to_dict()
    assert payload["pagination"]["state"] == "PARTIAL"
    assert payload["pagination"]["incompleteReason"] == "MAX_PAGE_LIMIT_REACHED"
    assert payload["pagination"]["nextCursorAvailable"] is True
    assert not list(_schema_validator().iter_errors(payload))


def test_repeated_cursor_is_rejected() -> None:
    transport = FakeTransport({
        PRE_EVALUATION_LOG_SOURCE: [
            ReadOnlyRowsPage([_evaluation_row()], has_more=True, next_cursor="1"),
            ReadOnlyRowsPage([_evaluation_row(**{"Evaluation ID": 2})], has_more=True, next_cursor="1"),
        ]
    })
    with pytest.raises(PaginationProtocolError):
        PreReadOnlyAdapter(transport).read_evaluation_log()


def test_has_more_without_cursor_is_rejected() -> None:
    transport = FakeTransport({
        PRE_EVALUATION_LOG_SOURCE: [ReadOnlyRowsPage([_evaluation_row()], has_more=True, next_cursor=None)]
    })
    with pytest.raises(PaginationProtocolError):
        PreReadOnlyAdapter(transport).read_evaluation_log()


def test_unknown_gate_states_do_not_become_pass() -> None:
    transport = FakeTransport({
        PRE_EVALUATION_LOG_SOURCE: [
            ReadOnlyRowsPage([_evaluation_row(**{"Gate State": "GREEN"})], has_more=False)
        ]
    })
    payload = PreReadOnlyAdapter(transport).read_evaluation_log().to_dict()
    assert payload["records"][0]["gateState"] == "UNKNOWN"


def test_bad_relation_json_fails_closed() -> None:
    transport = FakeTransport({
        PRE_EVALUATION_LOG_SOURCE: [
            ReadOnlyRowsPage([_evaluation_row(**{"Related Work Item": "not-json"})], has_more=False)
        ]
    })
    with pytest.raises(InvalidSourceRecord):
        PreReadOnlyAdapter(transport).read_evaluation_log()


def test_out_of_range_percentage_fails_closed() -> None:
    transport = FakeTransport({
        PRE_EVALUATION_LOG_SOURCE: [
            ReadOnlyRowsPage([_evaluation_row(**{"Delivery Completion %": 140})], has_more=False)
        ]
    })
    with pytest.raises(InvalidSourceRecord):
        PreReadOnlyAdapter(transport).read_evaluation_log()


def test_digest_is_deterministic_for_same_records() -> None:
    row = _evaluation_row()
    def capture() -> str:
        transport = FakeTransport({PRE_EVALUATION_LOG_SOURCE: [ReadOnlyRowsPage([row], has_more=False)]})
        return PreReadOnlyAdapter(transport).read_evaluation_log().content_digest
    assert capture() == capture()


def test_source_transport_only_exposes_query_method() -> None:
    adapter = PreReadOnlyAdapter(FakeTransport({
        PRE_EVALUATION_LOG_SOURCE: [ReadOnlyRowsPage([], has_more=False)]
    }))
    assert not hasattr(adapter, "apply_transition")
    assert not hasattr(adapter, "update_record")
    assert not hasattr(adapter, "delete_record")
