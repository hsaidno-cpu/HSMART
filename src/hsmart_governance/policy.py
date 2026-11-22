"""Fail-closed reference policy decision engine for HSMART AI delegates.

This module is a deterministic local reference implementation. Production use
still requires authenticated workload identity, a trusted grant store, a
centrally managed policy distribution path, and an independently protected
audit sink. It deliberately does not infer approvals.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from fnmatch import fnmatchcase
from typing import FrozenSet, Optional


class Effect(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    HOLD = "HOLD"


@dataclass(frozen=True)
class ApprovalGrant:
    grant_id: str
    approver_id: str
    agent_ids: FrozenSet[str]
    repository: str
    branch: str
    path_patterns: FrozenSet[str]
    operations: FrozenSet[str]
    not_before: datetime
    expires_at: datetime
    revoked: bool = False


@dataclass(frozen=True)
class ActionRequest:
    request_id: str
    actor_id: str
    gov_role: str
    operation: str
    repository: str
    branch: str
    path: str
    risk: str
    grant: Optional[ApprovalGrant] = None
    identity_verified: bool = False
    audit_available: bool = False


@dataclass(frozen=True)
class PolicyDecision:
    effect: Effect
    reason: str
    policy_id: str = "HSMART-GOV-AI-POL-001"
    policy_version: str = "1.0.0"


RESERVED_OPERATIONS = frozenset({
    "merge_to_main",
    "write_main",
    "production_deploy",
    "change_policy",
    "change_permissions",
    "read_raw_secret",
    "approve_own_action",
})


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    return value.astimezone(timezone.utc)


def evaluate(request: ActionRequest, *, now: Optional[datetime] = None) -> PolicyDecision:
    """Evaluate one action. Any missing/ambiguous control results in DENY."""
    try:
        if not request.request_id or not request.actor_id or not request.operation:
            return PolicyDecision(Effect.DENY, "missing_action_identity_or_operation")
        if not request.identity_verified:
            return PolicyDecision(Effect.DENY, "actor_identity_not_verified")
        if not request.audit_available:
            return PolicyDecision(Effect.DENY, "audit_path_unavailable_fail_closed")
        if request.operation in RESERVED_OPERATIONS or request.risk == "R4":
            return PolicyDecision(Effect.DENY, "reserved_human_action")
        if request.risk not in {"R0", "R1", "R2", "R3"}:
            return PolicyDecision(Effect.DENY, "unknown_risk_class")
        if request.risk in {"R0", "R1"}:
            return PolicyDecision(Effect.ALLOW, "verified_identity_and_audit_for_read_or_draft")
        grant = request.grant
        if grant is None:
            return PolicyDecision(Effect.DENY, "mutating_action_requires_explicit_grant")
        if grant.revoked:
            return PolicyDecision(Effect.DENY, "grant_revoked")
        if not grant.grant_id or not grant.approver_id or grant.approver_id == request.actor_id:
            return PolicyDecision(Effect.DENY, "grant_or_independent_approver_invalid")
        instant = _utc(now or datetime.now(timezone.utc))
        if instant < _utc(grant.not_before) or instant >= _utc(grant.expires_at):
            return PolicyDecision(Effect.DENY, "grant_not_yet_valid_or_expired")
        if request.actor_id not in grant.agent_ids:
            return PolicyDecision(Effect.DENY, "actor_outside_grant")
        if (request.repository, request.branch) != (grant.repository, grant.branch):
            return PolicyDecision(Effect.DENY, "target_outside_grant")
        if request.operation not in grant.operations:
            return PolicyDecision(Effect.DENY, "operation_outside_grant")
        if not any(fnmatchcase(request.path, pattern) for pattern in grant.path_patterns):
            return PolicyDecision(Effect.DENY, "path_outside_grant")
        if request.risk == "R3":
            return PolicyDecision(Effect.HOLD, "R3_requires_separate_human_security_review")
        return PolicyDecision(Effect.ALLOW, "explicit_grant_scope_and_controls_valid")
    except Exception:
        # Enforcement must never fail open because a parser, clock, or grant
        # object behaved unexpectedly.
        return PolicyDecision(Effect.DENY, "policy_evaluation_error_fail_closed")
