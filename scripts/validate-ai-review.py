#!/usr/bin/env python3
"""Validate GOV-11 AI assurance evidence and bind it to an exact reviewed commit."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPORT_DIR = "docs/reviews"

def report_path_for_pr(pr_number: int) -> str:
    return f"{REPORT_DIR}/PR-{pr_number}-AI-ASSURANCE.json"

SHA_RE = re.compile(r"^[0-9a-f]{40}$")

def validate_report(report: dict, *, pr_number: int, head_sha: str, changed_paths: list[str], expected_report_path: str | None = None) -> list[str]:
    errors: list[str] = []
    if report.get("pr_number") != pr_number:
        errors.append("PR number mismatch")
    reviewed = report.get("reviewed_head_sha", "")
    if not SHA_RE.fullmatch(reviewed):
        errors.append("reviewed_head_sha must be a full 40-character SHA")
    if not SHA_RE.fullmatch(head_sha):
        errors.append("head_sha must be a full 40-character SHA")
    if report.get("review_result") not in {"PASS", "PASS_WITH_CAVEATS"}:
        errors.append("review_result must be PASS or PASS_WITH_CAVEATS")
    if report.get("reviewer", {}).get("role_id") != "GOV-11":
        errors.append("reviewer role must be GOV-11")
    if report.get("review_independence") != "CORRELATION_LIMITED_NOT_INDEPENDENT_CERTIFICATION":
        errors.append("review independence/correlation limitation must be explicit")
    if report.get("github_native_approval") is not False:
        errors.append("AI report must not claim native GitHub approval")
    findings = report.get("findings", [])
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []
    for item in findings:
        if item.get("status") == "OPEN" and item.get("severity") in {"CRITICAL", "HIGH"}:
            errors.append("open critical/high finding blocks review gate")
    if report.get("open_blocking_findings") != 0:
        errors.append("open_blocking_findings must be zero")
    expected_path = expected_report_path or report_path_for_pr(pr_number)
    if sorted(set(changed_paths)) != [expected_path]:
        errors.append(f"only {expected_path} may change after reviewed_head_sha; code changes require a new review")
    if reviewed == head_sha:
        errors.append("reviewed_head_sha must precede the report-only evidence commit")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr-number", type=int, required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--report", default="")
    args = parser.parse_args()
    report_path = args.report or report_path_for_pr(args.pr_number)
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    reviewed = report.get("reviewed_head_sha", "")
    if not SHA_RE.fullmatch(reviewed):
        print("invalid reviewed_head_sha", file=sys.stderr)
        return 2
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{reviewed}..{args.head_sha}"],
        check=True, capture_output=True, text=True,
    )
    changed = [line for line in result.stdout.splitlines() if line]
    errors = validate_report(report, pr_number=args.pr_number, head_sha=args.head_sha, changed_paths=changed, expected_report_path=report_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(f"AI review evidence valid for PR #{args.pr_number}; reviewed code SHA {reviewed}")
    print("Scope is report-only after the reviewed commit; no GitHub-native approval is asserted.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
