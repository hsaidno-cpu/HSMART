#!/usr/bin/env python3
"""Apply/read HSMART GitHub main protection. Dry-run is the default.

Requires an administrator token with repository Administration: write to apply.
The token is read only from GH_TOKEN and is never printed or written. Do not use the workflow's default GITHUB_TOKEN for repository administration.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API = "https://api.github.com"
API_VERSION = "2022-11-28"
REPO_DEFAULT = "hsaidno-cpu/HSMART"
BRANCH_DEFAULT = "main"
REQUIRED_CHECKS = [
    "Contract tests (ubuntu-24.04)",
    "Contract tests (windows-2025)",
    "Contract tests (macos-15)",
    "OpenAPI and required repository files",
    "KM1 application integration (PostgreSQL 16)",
    "Repository Governance Review",
    "AI Reviewer Evidence",
]
RULESET_NAME = "HSMART Main Governance"


def branch_protection_payload() -> dict:
    return {
        "required_status_checks": {
            "strict": True,
            "checks": [{"context": check} for check in REQUIRED_CHECKS],
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "require_last_push_approval": False,
            "required_approving_review_count": 0,
            "bypass_pull_request_allowances": {"users": [], "teams": [], "apps": []},
        },
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": True,
        "lock_branch": False,
        "allow_fork_syncing": True,
    }


def ruleset_payload() -> dict:
    return {
        "name": RULESET_NAME,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {
            "ref_name": {"include": ["refs/heads/main"], "exclude": []}
        },
        "rules": [
            {"type": "pull_request", "parameters": {
                "required_approving_review_count": 0,
                "dismiss_stale_reviews_on_push": True,
                "require_code_owner_review": False,
                "require_last_push_approval": False,
                "required_review_thread_resolution": True,
            }},
            {"type": "required_status_checks", "parameters": {
                "strict_required_status_checks_policy": True,
                "do_not_enforce_on_create": False,
                "required_status_checks": [{"context": name} for name in REQUIRED_CHECKS],
            }},
            {"type": "required_linear_history"},
            {"type": "non_fast_forward"},
            {"type": "deletion"},
        ],
    }


class GitHubAPIError(RuntimeError):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


def api_request(method: str, path: str, token: str | None = None, payload: dict | None = None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "HSMART-Repository-Governance",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = Request(f"{API}{path}", data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=20) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else {}
    except HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        # Do not echo headers or request payloads: either may contain sensitive values.
        raise GitHubAPIError(exc.code, f"GitHub API returned HTTP {exc.code}: {body[:1000]}") from exc
    except URLError as exc:
        raise RuntimeError(f"GitHub API connection failed: {exc.reason}") from exc


def check_main_sha(repo: str, expected_sha: str, token: str) -> None:
    _, branch = api_request("GET", f"/repos/{repo}/branches/{BRANCH_DEFAULT}", token)
    actual = branch.get("commit", {}).get("sha")
    if actual != expected_sha:
        raise RuntimeError(f"main moved: expected {expected_sha}, found {actual}; re-read and retry")


def apply_branch_protection(repo: str, expected_sha: str, token: str, dry_run: bool) -> dict:
    payload = branch_protection_payload()
    if dry_run:
        return {"mode": "dry-run", "method": "PUT", "path": f"/repos/{repo}/branches/main/protection", "expected_main_sha": expected_sha, "payload": payload}
    check_main_sha(repo, expected_sha, token)
    _, result = api_request("PUT", f"/repos/{repo}/branches/main/protection", token, payload)
    return {"mode": "applied", "result": result}


def apply_ruleset(repo: str, expected_sha: str, token: str, dry_run: bool) -> dict:
    payload = ruleset_payload()
    if dry_run:
        return {"mode": "dry-run", "method": "POST-or-PUT", "path": f"/repos/{repo}/rulesets", "expected_main_sha": expected_sha, "payload": payload}
    check_main_sha(repo, expected_sha, token)
    _, existing = api_request("GET", f"/repos/{repo}/rulesets?includes_parents=true", token)
    matches = [item for item in existing if item.get("name") == RULESET_NAME]
    if len(matches) > 1:
        raise RuntimeError(f"multiple rulesets named {RULESET_NAME!r}; resolve manually")
    if matches:
        ruleset_id = matches[0]["id"]
        _, result = api_request("PUT", f"/repos/{repo}/rulesets/{ruleset_id}", token, payload)
        return {"mode": "updated", "ruleset_id": ruleset_id, "result": result}
    _, result = api_request("POST", f"/repos/{repo}/rulesets", token, payload)
    return {"mode": "created", "result": result}


def read_status(repo: str, token: str | None) -> dict:
    _, branch = api_request("GET", f"/repos/{repo}/branches/main", token)
    protected = branch.get("protected", False)
    try:
        protection_status, protection = api_request("GET", f"/repos/{repo}/branches/main/protection", token)
    except GitHubAPIError as exc:
        if exc.status != 404:
            raise
        protection_status, protection = 404, {"message": str(exc)}
    _, rulesets = api_request("GET", f"/repos/{repo}/rulesets?includes_parents=true", token)
    named_rulesets = [item for item in rulesets if item.get("name") == RULESET_NAME]
    return {
        "main_sha": branch.get("commit", {}).get("sha"),
        "protected": protected,
        "protection_http_status": protection_status,
        "required_status_checks": protection.get("required_status_checks") if isinstance(protection, dict) else None,
        "enforce_admins": protection.get("enforce_admins") if isinstance(protection, dict) else None,
        "hsmart_rulesets": named_rulesets,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["status", "apply-branch-protection", "apply-ruleset"])
    parser.add_argument("--repo", default=REPO_DEFAULT)
    parser.add_argument("--expected-main-sha", default="")
    parser.add_argument("--apply", action="store_true", help="perform a write; otherwise print a dry-run")
    parser.add_argument("--confirm-main", action="store_true", help="required together with --apply")
    args = parser.parse_args(argv)

    token = os.getenv("GH_TOKEN")
    try:
        if args.command == "status":
            print(json.dumps(read_status(args.repo, token), indent=2))
            return 0
        if args.apply and not args.confirm_main:
            parser.error("--apply requires --confirm-main")
        if args.apply and not token:
            parser.error("--apply requires GH_TOKEN with repository Administration: write")
        if not args.expected_main_sha:
            parser.error("--expected-main-sha is required for a protection mutation")
        if args.command == "apply-branch-protection":
            result = apply_branch_protection(args.repo, args.expected_main_sha, token or "", dry_run=not args.apply)
        else:
            result = apply_ruleset(args.repo, args.expected_main_sha, token or "", dry_run=not args.apply)
        print(json.dumps(result, indent=2))
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
