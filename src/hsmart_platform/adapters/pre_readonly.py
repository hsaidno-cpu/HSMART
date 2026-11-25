"""Fail-closed, read-only adapter boundary for PRE's Notion evidence stores.

This module deliberately does not implement a Notion network client. A host must
inject a transport with read-only query capability. No create/update/delete or
transition-apply operation is exposed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping, Protocol, Sequence


PRE_EVALUATION_LOG_SOURCE = "collection://42299868-397f-8191-ae68-000bbf780e69"
PRE_TRANSITION_QUEUE_SOURCE = "collection://42299868-397f-819d-bb41-000b0d2a1886"

GATE_STATES = {
    "NOT_RUN", "NOT_ASSESSED", "PASS", "PASS_WITH_CAVEATS",
    "HOLD", "FAIL", "BLOCKED", "NOT_APPLICABLE",
}
NEXT_DISPOSITIONS = {
    "CONTINUE", "HOLD", "RESEQUENCE", "REBASELINE", "SPLIT",
    "MERGE", "DEFER", "PILOT", "ROLLBACK", "STOP", "CLOSE",
}
REQUEST_STATES = {
    "PENDING", "EVALUATING", "HOLD", "BLOCKED", "ELIGIBLE_FOR_APPROVAL",
    "APPROVED", "POLICY_PASSED", "APPLIED", "REJECTED",
}
GATE_DECISIONS = {"ALLOW", "HOLD", "DENY", "NOT_RUN"}
PRE_STAGES = {
    "R0 Intake", "R1 Strategy & Baseline", "R2 Roadmap Design",
    "R3 Approval & Baseline Freeze", "R4 Iteration Execution",
    "R5 Formative Check", "R6 Milestone Acceptance",
    "R7 Outcome & Impact", "R8 Adaptation", "R9 Closure & Learning",
}


class PreAdapterError(RuntimeError):
    """Base exception for a failed or incomplete PRE read operation."""


class PreAdapterNotConfigured(PreAdapterError):
    """Raised when no authorized read-only transport is bound to the adapter."""


class PaginationProtocolError(PreAdapterError):
    """Raised when the source returns an unsafe or inconsistent cursor sequence."""


class InvalidSourceRecord(PreAdapterError):
    """Raised when a source record violates the normalized adapter contract."""


@dataclass(frozen=True, slots=True)
class ReadOnlyRowsPage:
    """One normalized page returned by an authorized source transport."""

    records: Sequence[Mapping[str, Any]]
    has_more: bool
    next_cursor: str | None = None


class PreReadOnlyTransport(Protocol):
    """Minimum transport capability. It intentionally has no write methods."""

    def query_rows(
        self,
        *,
        data_source_url: str,
        page_size: int,
        start_cursor: str | None,
    ) -> ReadOnlyRowsPage:
        """Return one page of normalized property-name/value mappings."""
        ...


@dataclass(frozen=True, slots=True)
class PreReadOnlySnapshot:
    schema_version: str
    snapshot_id: str
    source_system: str
    data_source_url: str
    data_source_name: str
    captured_at: str
    pagination_state: str
    pages_read: int
    record_count: int
    next_cursor_available: bool
    incomplete_reason: str | None
    freshness_state: str
    source_updated_at: str | None
    content_digest: str
    access_mode: str
    records: tuple[Mapping[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": self.schema_version,
            "snapshotId": self.snapshot_id,
            "source": {
                "system": self.source_system,
                "dataSourceUrl": self.data_source_url,
                "dataSourceName": self.data_source_name,
            },
            "capturedAt": self.captured_at,
            "pagination": {
                "state": self.pagination_state,
                "pagesRead": self.pages_read,
                "recordCount": self.record_count,
                "nextCursorAvailable": self.next_cursor_available,
                "incompleteReason": self.incomplete_reason,
            },
            "freshness": {
                "state": self.freshness_state,
                "sourceUpdatedAt": self.source_updated_at,
            },
            "contentDigest": self.content_digest,
            "accessMode": self.access_mode,
            "records": [dict(record) for record in self.records],
        }


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _string(value: Any, *, field: str, allow_empty: bool = False) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise InvalidSourceRecord(f"{field} must be text or null")
    normalized = value.strip()
    if not allow_empty and not normalized:
        return None
    return normalized


def _enum(value: Any, allowed: set[str], *, field: str) -> str:
    normalized = _string(value, field=field)
    if normalized is None:
        return "UNKNOWN"
    return normalized if normalized in allowed else "UNKNOWN"


def _number(value: Any, *, field: str, percentage: bool = False) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidSourceRecord(f"{field} must be a number or null")
    result = float(value)
    if percentage and not 0 <= result <= 100:
        raise InvalidSourceRecord(f"{field} must be between 0 and 100")
    return result


def _relation_urls(value: Any, *, field: str) -> list[str]:
    if value is None or value == "":
        return []
    parsed = value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise InvalidSourceRecord(f"{field} must be a JSON array of page URLs") from exc
    if not isinstance(parsed, list):
        raise InvalidSourceRecord(f"{field} must be a list")
    result: list[str] = []
    for item in parsed:
        if not isinstance(item, str) or not item.strip():
            raise InvalidSourceRecord(f"{field} contains a non-text or empty URL")
        result.append(item.strip())
    return list(dict.fromkeys(result))


def _json_value(value: Any, *, field: str) -> Any:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        if isinstance(value, (dict, list)):
            return value
        raise InvalidSourceRecord(f"{field} must contain JSON text, an object, a list, or null")
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise InvalidSourceRecord(f"{field} contains invalid JSON") from exc
    if not isinstance(parsed, (dict, list)):
        raise InvalidSourceRecord(f"{field} must decode to an object or array")
    return parsed


def _date(row: Mapping[str, Any], base_name: str) -> str | None:
    value = row.get(f"date:{base_name}:start", row.get(base_name))
    return _string(value, field=base_name)


def _map_evaluation(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "recordType": "EVALUATION",
        "recordUrl": _string(row.get("url"), field="url"),
        "evaluationId": row.get("Evaluation ID"),
        "title": _string(row.get("Evaluation Title"), field="Evaluation Title"),
        "evaluationType": _enum(
            row.get("Evaluation Type"),
            {"Intake Review", "Baseline Review", "Formative Check", "Milestone Acceptance",
             "Outcome & Impact", "Adaptation Decision", "Closure Review"},
            field="Evaluation Type",
        ),
        "preStage": _enum(row.get("PRE Stage"), PRE_STAGES, field="PRE Stage"),
        "evaluatorRole": _enum(
            row.get("Evaluator Role"),
            {"PRE", "Evaluator Team", "HSO", "Security reviewer", "Human decision owner", "Not assigned"},
            field="Evaluator Role",
        ),
        "gateState": _enum(row.get("Gate State"), GATE_STATES, field="Gate State"),
        "nextDisposition": _enum(row.get("Next Disposition"), NEXT_DISPOSITIONS, field="Next Disposition"),
        "measurementDate": _date(row, "Measurement Date"),
        "deliveryCompletionPercent": _number(
            row.get("Delivery Completion %"), field="Delivery Completion %", percentage=True
        ),
        "milestoneAcceptancePercent": _number(
            row.get("Milestone Acceptance %"), field="Milestone Acceptance %", percentage=True
        ),
        "verificationCoveragePercent": _number(
            row.get("Verification Coverage %"), field="Verification Coverage %", percentage=True
        ),
        "denominatorAndCalculation": _string(row.get("Denominator & Calculation"), field="Denominator & Calculation"),
        "evidenceCoverage": _string(row.get("Evidence Coverage"), field="Evidence Coverage"),
        "evaluationSummary": _string(row.get("Evaluation Summary"), field="Evaluation Summary"),
        "scopeAndExclusions": _string(row.get("Scope & Exclusions"), field="Scope & Exclusions"),
        "uncertaintyAndLimitations": _string(
            row.get("Uncertainty & Limitations"), field="Uncertainty & Limitations"
        ),
        "relatedWorkItemUrls": _relation_urls(row.get("Related Work Item"), field="Related Work Item"),
        "supportingEvidenceUrls": _relation_urls(row.get("Supporting Evidence"), field="Supporting Evidence"),
    }


def _map_transition(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "recordType": "TRANSITION_REQUEST",
        "recordUrl": _string(row.get("url"), field="url"),
        "requestId": row.get("Request ID"),
        "requestTitle": _string(row.get("Request"), field="Request"),
        "projectId": _string(row.get("Project ID"), field="Project ID"),
        "scopeId": _string(row.get("Scope ID"), field="Scope ID"),
        "correlationId": _string(row.get("Correlation ID"), field="Correlation ID"),
        "idempotencyKey": _string(row.get("Idempotency Key"), field="Idempotency Key"),
        "fromStage": _enum(row.get("From Stage"), PRE_STAGES, field="From Stage"),
        "requestedStage": _enum(row.get("Requested Stage"), PRE_STAGES - {"R0 Intake"}, field="Requested Stage"),
        "requestState": _enum(row.get("Request State"), REQUEST_STATES, field="Request State"),
        "gateDecision": _enum(row.get("Gate Decision"), GATE_DECISIONS, field="Gate Decision"),
        "evaluatedAt": _date(row, "Evaluated At"),
        "appliedAt": _date(row, "Applied At"),
        "requestedByActorId": _string(row.get("Requested By Actor ID"), field="Requested By Actor ID"),
        "decisionOwnerUrls": _relation_urls(row.get("Decision Owner"), field="Decision Owner"),
        "workItemUrls": _relation_urls(row.get("Work Item"), field="Work Item"),
        "sourceCommit": _string(row.get("Source Commit"), field="Source Commit"),
        "sourceEvent": _string(row.get("Source Event"), field="Source Event"),
        "evaluationDigest": _string(row.get("Evaluation Digest"), field="Evaluation Digest"),
        "blockReasons": _string(row.get("Block Reasons"), field="Block Reasons"),
        "evidenceEnvelope": _json_value(row.get("Evidence Envelope JSON"), field="Evidence Envelope JSON"),
        "evaluationReceipt": _json_value(row.get("Evaluation Receipt JSON"), field="Evaluation Receipt JSON"),
        "approvalReceipt": _json_value(row.get("Approval Receipt JSON"), field="Approval Receipt JSON"),
        "externalAuditReceiptUrl": _string(row.get("External Audit Receipt"), field="External Audit Receipt"),
    }


class PreReadOnlyAdapter:
    """Read PRE's evaluation and transition ledgers without granting write authority."""

    def __init__(
        self,
        transport: PreReadOnlyTransport | None = None,
        *,
        page_size: int = 100,
        max_pages: int = 100,
    ) -> None:
        if not 1 <= page_size <= 100:
            raise ValueError("page_size must be between 1 and 100")
        if not 1 <= max_pages <= 1000:
            raise ValueError("max_pages must be between 1 and 1000")
        self._transport = transport
        self._page_size = page_size
        self._max_pages = max_pages

    @property
    def configured(self) -> bool:
        return self._transport is not None

    def readiness(self) -> dict[str, Any]:
        return {
            "state": "TRANSPORT_BOUND_NOT_VERIFIED" if self.configured else "NOT_CONFIGURED",
            "liveReadState": "NOT_VERIFIED",
            "sourceAuthorizationState": "NOT_VERIFIED",
            "accessMode": "READ_ONLY",
            "writeOperationsExposed": False,
            "sources": {
                "evaluationLog": PRE_EVALUATION_LOG_SOURCE,
                "transitionQueue": PRE_TRANSITION_QUEUE_SOURCE,
            },
            "note": (
                "A read-only PRE transport is injected."
                if self.configured else
                "No PRE transport is bound. Live reads are disabled; no network call is attempted."
            ),
        }

    def read_evaluation_log(self) -> PreReadOnlySnapshot:
        return self._capture(
            source_url=PRE_EVALUATION_LOG_SOURCE,
            source_name="PRE Evaluation & Gate Log",
            mapper=_map_evaluation,
        )

    def read_transition_queue(self) -> PreReadOnlySnapshot:
        return self._capture(
            source_url=PRE_TRANSITION_QUEUE_SOURCE,
            source_name="PRE Transition Queue — Policy Evaluations",
            mapper=_map_transition,
        )

    def _capture(
        self,
        *,
        source_url: str,
        source_name: str,
        mapper: Any,
    ) -> PreReadOnlySnapshot:
        if self._transport is None:
            raise PreAdapterNotConfigured(
                "PRE read-only transport is not configured; live reads are disabled"
            )

        cursor: str | None = None
        seen_cursors: set[str] = set()
        raw_records: list[Mapping[str, Any]] = []
        pages_read = 0
        pagination_state = "COMPLETE"
        incomplete_reason: str | None = None

        while pages_read < self._max_pages:
            page = self._transport.query_rows(
                data_source_url=source_url,
                page_size=self._page_size,
                start_cursor=cursor,
            )
            if not isinstance(page, ReadOnlyRowsPage):
                raise PaginationProtocolError("transport must return ReadOnlyRowsPage")
            if not isinstance(page.records, Sequence) or isinstance(page.records, (str, bytes)):
                raise PaginationProtocolError("page records must be a sequence of mappings")
            for record in page.records:
                if not isinstance(record, Mapping):
                    raise InvalidSourceRecord("each source row must be a mapping")
                raw_records.append(dict(record))
            pages_read += 1

            if not page.has_more:
                if page.next_cursor is not None:
                    raise PaginationProtocolError("next_cursor must be null when has_more is false")
                break
            if not isinstance(page.next_cursor, str) or not page.next_cursor.strip():
                raise PaginationProtocolError("has_more=true requires a non-empty next_cursor")
            if page.next_cursor in seen_cursors or page.next_cursor == cursor:
                raise PaginationProtocolError("repeated pagination cursor detected")
            seen_cursors.add(page.next_cursor)
            cursor = page.next_cursor
        else:
            pagination_state = "PARTIAL"
            incomplete_reason = "MAX_PAGE_LIMIT_REACHED"

        mapped = tuple(mapper(record) for record in raw_records)
        canonical = json.dumps(
            [dict(record) for record in mapped],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        digest = "sha256:" + sha256(canonical).hexdigest()
        captured_at = _utc_now()
        return PreReadOnlySnapshot(
            schema_version="1.0.0",
            snapshot_id=f"pre:{source_name.lower().replace(' ', '-')}:sha256:{digest[7:23]}",
            source_system="PRE",
            data_source_url=source_url,
            data_source_name=source_name,
            captured_at=captured_at,
            pagination_state=pagination_state,
            pages_read=pages_read,
            record_count=len(mapped),
            next_cursor_available=pagination_state == "PARTIAL",
            incomplete_reason=incomplete_reason,
            freshness_state="UNKNOWN",
            source_updated_at=None,
            content_digest=digest,
            access_mode="READ_ONLY",
            records=mapped,
        )
