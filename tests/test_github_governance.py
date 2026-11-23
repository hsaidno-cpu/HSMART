import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "github-governance.py"
spec = importlib.util.spec_from_file_location("github_governance", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_branch_protection_requires_all_ci_jobs_and_zero_bot_approvals():
    payload = module.branch_protection_payload()
    assert payload["enforce_admins"] is True
    assert payload["allow_force_pushes"] is False
    assert payload["allow_deletions"] is False
    assert payload["required_pull_request_reviews"]["required_approving_review_count"] == 0
    assert payload["required_status_checks"]["strict"] is True
    assert {item["context"] for item in payload["required_status_checks"]["checks"]} == set(module.REQUIRED_CHECKS)


def test_ruleset_has_no_bypass_and_targets_main_only():
    payload = module.ruleset_payload()
    assert payload["bypass_actors"] == []
    assert payload["enforcement"] == "active"
    assert payload["conditions"]["ref_name"]["include"] == ["refs/heads/main"]
    assert {item["type"] for item in payload["rules"]} >= {"pull_request", "required_status_checks", "non_fast_forward", "deletion"}


def test_dry_run_does_not_need_a_token(monkeypatch, capsys):
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    assert module.main(["apply-branch-protection", "--expected-main-sha", "a" * 40]) == 0
    out = capsys.readouterr().out
    assert '"mode": "dry-run"' in out


def test_apply_requires_confirmation_and_admin_token(monkeypatch):
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    try:
        module.main(["apply-branch-protection", "--expected-main-sha", "a" * 40, "--apply", "--confirm-main"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("write without admin token must be blocked")
