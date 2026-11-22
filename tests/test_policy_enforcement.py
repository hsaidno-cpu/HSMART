from datetime import datetime, timedelta, timezone

from hsmart_governance.policy import (
    ActionRequest, ApprovalGrant, Effect, evaluate,
)


NOW = datetime(2026, 11, 22, 12, 0, tzinfo=timezone.utc)
AGENT = "hsmart.gov05.engineering.orchestrator"


def grant(**overrides):
    values = dict(
        grant_id="GOV01-GRANT-TEST-001",
        approver_id="human:gov01",
        agent_ids=frozenset({AGENT}),
        repository="hsaidno-cpu/HSMART",
        branch="feature/approved-work",
        path_patterns=frozenset({"src/**", "tests/**"}),
        operations=frozenset({"branch_write"}),
        not_before=NOW - timedelta(minutes=5),
        expires_at=NOW + timedelta(minutes=5),
    )
    values.update(overrides)
    return ApprovalGrant(**values)


def request(**overrides):
    values = dict(
        request_id="req-001",
        actor_id=AGENT,
        gov_role="GOV-05",
        operation="branch_write",
        repository="hsaidno-cpu/HSMART",
        branch="feature/approved-work",
        path="src/example.py",
        risk="R2",
        grant=grant(),
        identity_verified=True,
        audit_available=True,
    )
    values.update(overrides)
    return ActionRequest(**values)


def test_scoped_valid_grant_allows_branch_write():
    assert evaluate(request(), now=NOW).effect is Effect.ALLOW


def test_missing_grant_denied():
    assert evaluate(request(grant=None), now=NOW).effect is Effect.DENY


def test_unverified_identity_denied():
    assert evaluate(request(identity_verified=False), now=NOW).effect is Effect.DENY


def test_unavailable_audit_sink_fails_closed():
    decision = evaluate(request(audit_available=False), now=NOW)
    assert decision.effect is Effect.DENY
    assert "fail_closed" in decision.reason


def test_expired_grant_denied():
    expired = grant(expires_at=NOW - timedelta(seconds=1))
    assert evaluate(request(grant=expired), now=NOW).effect is Effect.DENY


def test_revoked_grant_denied():
    assert evaluate(request(grant=grant(revoked=True)), now=NOW).effect is Effect.DENY


def test_agent_outside_grant_denied():
    other = grant(agent_ids=frozenset({"hsmart.gov02.project-owner.orchestrator"}))
    assert evaluate(request(grant=other), now=NOW).effect is Effect.DENY


def test_path_escape_denied():
    assert evaluate(request(path="docs/governance/policy.md"), now=NOW).effect is Effect.DENY


def test_branch_escape_denied():
    assert evaluate(request(branch="main"), now=NOW).effect is Effect.DENY


def test_ai_merge_and_production_deploy_are_reserved():
    for operation in ("merge_to_main", "production_deploy", "write_main"):
        decision = evaluate(request(operation=operation), now=NOW)
        assert decision.effect is Effect.DENY


def test_r3_requires_human_security_review():
    decision = evaluate(request(risk="R3"), now=NOW)
    assert decision.effect is Effect.HOLD


def test_r4_is_reserved_for_humans():
    assert evaluate(request(risk="R4"), now=NOW).effect is Effect.DENY


def test_unknown_risk_denied():
    assert evaluate(request(risk="R9"), now=NOW).effect is Effect.DENY
