#!/usr/bin/env python3
"""Deterministic repository-policy pre-review; not an LLM or legal review."""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = [
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key material"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "GitHub token-like secret"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "fine-grained GitHub token-like secret"),
]


def review() -> list[str]:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", ".venv", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern, description in FORBIDDEN:
            if pattern.search(content):
                findings.append(f"{path.relative_to(ROOT)}: possible {description}")
    ruleset = ROOT / "docs/governance/REPOSITORY-MAIN-RULESET.json"
    if not ruleset.exists():
        findings.append("canonical main ruleset specification is missing")
    else:
        import json
        data = json.loads(ruleset.read_text(encoding="utf-8"))
        if data.get("bypass_actors") != []:
            findings.append("main ruleset bypass_actors must be empty")
        if data.get("enforcement") != "active":
            findings.append("main ruleset must target active enforcement")
    return findings


def main() -> int:
    findings = review()
    if findings:
        print("Repository governance pre-review: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Repository governance pre-review: PASS")
    print("Scope: deterministic policy and secret-pattern checks only; not an LLM reviewer, legal opinion, or production security audit.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
