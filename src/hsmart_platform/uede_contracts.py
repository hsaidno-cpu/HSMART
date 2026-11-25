"""Cross-field validation rules for versioned UEDE contracts.

JSON Schema validates the receipt shape. This module enforces semantic invariants
that standard JSON Schema cannot express, especially exact commit equality.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def execution_receipt_semantic_errors(receipt: Mapping[str, Any]) -> tuple[str, ...]:
    """Return fail-closed semantic violations for a UEDE execution receipt.

    Call this after JSON Schema validation. A PASS is only credible when the
    verification SHA equals the target HEAD and a successful CI run exists on
    that exact same commit. The receipt can record facts, never PRE stage writes.
    """
    errors: list[str] = []
    if not isinstance(receipt, Mapping):
        return ("RECEIPT_MUST_BE_OBJECT",)

    target = receipt.get("target")
    target = target if isinstance(target, Mapping) else {}
    verification = receipt.get("verification")
    verification = verification if isinstance(verification, Mapping) else {}
    roadmap_effect = receipt.get("roadmapEffect")
    roadmap_effect = roadmap_effect if isinstance(roadmap_effect, Mapping) else {}

    if roadmap_effect.get("canonicalStageMutation") is not False:
        errors.append("CANONICAL_PRE_STAGE_MUTATION_FORBIDDEN")
    if roadmap_effect.get("writeBackMode") != "EXECUTION_FACTS_ONLY":
        errors.append("ROADMAP_WRITEBACK_MUST_BE_FACTS_ONLY")

    if verification.get("state") != "PASS":
        return tuple(errors)

    head_sha = target.get("headCommitSha")
    verified_sha = verification.get("verifiedCommitSha")
    if not isinstance(head_sha, str) or not head_sha:
        errors.append("PASS_REQUIRES_TARGET_HEAD_SHA")
    elif verified_sha != head_sha:
        errors.append("VERIFIED_COMMIT_SHA_MISMATCH")

    if receipt.get("executionState") != "COMPLETED":
        errors.append("PASS_REQUIRES_COMPLETED_EXECUTION")

    ci_runs = receipt.get("ciRuns")
    exact_head_ci_passed = (
        isinstance(head_sha, str)
        and isinstance(ci_runs, list)
        and any(
            isinstance(run, Mapping)
            and run.get("commitSha") == head_sha
            and run.get("conclusion") == "SUCCESS"
            for run in ci_runs
        )
    )
    if not exact_head_ci_passed:
        errors.append("EXACT_HEAD_CI_SUCCESS_REQUIRED")

    evidence = verification.get("evidenceReferences")
    if not isinstance(evidence, list) or not any(
        isinstance(item, str) and item.strip() for item in evidence
    ):
        errors.append("PASS_REQUIRES_VERIFICATION_EVIDENCE")

    return tuple(errors)
