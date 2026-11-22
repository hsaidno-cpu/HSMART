import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-ai-review.py"
spec = importlib.util.spec_from_file_location("validate_ai_review", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

VALID = {
    "pr_number": 28,
    "reviewed_head_sha": "a" * 40,
    "review_result": "PASS_WITH_CAVEATS",
    "reviewer": {"role_id": "GOV-11"},
    "review_independence": "CORRELATION_LIMITED_NOT_INDEPENDENT_CERTIFICATION",
    "github_native_approval": False,
    "open_blocking_findings": 0,
    "findings": [{"id": "F-01", "severity": "MEDIUM", "status": "OPEN"}],
}

def test_valid_report_bound_to_exact_reviewed_commit():
    assert module.validate_report(VALID, pr_number=28, head_sha="b" * 40, changed_paths=[module.REPORT_PATH]) == []

def test_wrong_pr_is_rejected():
    errors = module.validate_report(VALID, pr_number=29, head_sha="b" * 40, changed_paths=[module.REPORT_PATH])
    assert "PR number mismatch" in errors

def test_native_approval_claim_is_rejected():
    data = {**VALID, "github_native_approval": True}
    errors = module.validate_report(data, pr_number=28, head_sha="b" * 40, changed_paths=[module.REPORT_PATH])
    assert "AI report must not claim native GitHub approval" in errors

def test_post_review_code_change_is_rejected():
    errors = module.validate_report(VALID, pr_number=28, head_sha="b" * 40, changed_paths=[module.REPORT_PATH, "src/hsmart_platform/app.py"])
    assert any("only the AI review report may change" in e for e in errors)

def test_open_critical_finding_is_rejected():
    data = {**VALID, "findings": [{"id": "F-CRIT", "severity": "CRITICAL", "status": "OPEN"}]}
    errors = module.validate_report(data, pr_number=28, head_sha="b" * 40, changed_paths=[module.REPORT_PATH])
    assert any("open critical/high" in e for e in errors)
