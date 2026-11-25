# UEDE PRE Read-only Adapter v1.0.0

**Status:** Draft implementation contract. This is a read-only adapter and deterministic mapper, not a deployed PRE runtime or live Notion connector.  
**Branch:** `feat/pre-readonly-adapter-contract-20261125`, stacked on HSMART PR #33.

## Authority split

- PRE owns progressive roadmap evaluation, gate and transition-policy decisions.
- HSMART/GitHub retain canonical ownership of HSMART source code, issues, PRs, CI and engineering evidence.
- The HSMART Tasks database is an operational tracker, not an authority to approve PRE transitions.
- The adapter reads two explicit PRE sources only: `PRE Evaluation & Gate Log` (`collection://42299868-397f-8191-ae68-000bbf780e69`) and `PRE Transition Queue — Policy Evaluations` (`collection://42299868-397f-819d-bb41-000b0d2a1886`).
- HSO's `HSO Master Roadmap & Milestones` is a separate HSO ecosystem roadmap and must not be silently relabeled as the HSMART project roadmap.

## Read contract

`PreReadOnlyAdapter` accepts an injected `PreReadOnlyTransport` with exactly one operation: `query_rows`. There are intentionally no mutation methods, approval endpoints, transition-apply operations or generic network client.

The transport normalizes each data-source page into `ReadOnlyRowsPage(records, has_more, next_cursor)`. Adapter behavior:

1. Reads every available page up to a bounded `max_pages` limit.
2. Detects missing and repeated cursors; rejects malformed source records.
3. Preserves unknown enum values as `UNKNOWN`; never converts unfamiliar values to PASS/ALLOW.
4. Produces a SHA-256 digest over deterministic normalized records.
5. Marks page-limited snapshots `PARTIAL` with the exact reason.
6. Keeps source freshness `UNKNOWN` until an authoritative source-modified timestamp is available. Capture time is not source freshness.
7. Exposes `READ_ONLY` access mode and no write operation.

## Why the adapter is not live

The PRE plugin package is USER/PRIVATE; its canonical Git source and manifest license are not declared; its shared runtime is specified but not deployed. The Notion connector can read the source schemas/pages, but its live query-data-source operation is currently unavailable due to an account usage limit. Therefore this PR supplies a host-neutral transport port, normalization, pagination, integrity checks and fixture tests. It does not claim live reads, complete current source records, or a deployed PRE endpoint.

## Data mapping

- Evaluation ledger: evaluation type, R0–R9 stage, evaluator role, gate state, next disposition, separate progress/acceptance/verification percentages, denominator, evidence, scope, uncertainty and related work/evidence URLs.
- Transition queue: source/requested stages, request state, policy gate decision, evaluation timestamps/digest, correlation and idempotency keys, work-item URLs, blockers, evidence/evaluation/approval receipt payloads and external audit locator.

The adapter records approval receipt data as source content only. It does not authenticate the signer, verify a cryptographic signature or infer that a request is approved/applied. That requires a separate authenticated policy-engine/approval contract and real key/authority evidence.

## Freshness and completeness semantics

- `pagination.state=COMPLETE` means the transport exhausted the page cursor chain, not that the database is authoritative, fresh or approved.
- `pagination.state=PARTIAL` is never eligible for a complete snapshot claim.
- `freshness.state=UNKNOWN` is deliberate. The normalized page contract does not expose an authoritative updated-at timestamp.
- The digest proves only the exact normalized records captured. Consumers must recompute it from the canonical serialized records.

## Runtime activation checklist

Do not mark this adapter `READ_ONLY_READY` in a host until all are true:

- PRE/GOV-01 authorizes the HSMART integration identity to read these exact two data sources.
- A Notion host transport maps raw provider pages into `ReadOnlyRowsPage` without write scopes.
- Pagination, relation decoding, permission-denied, rate-limit and source-deletion cases pass live contract tests.
- A source freshness field or explicit freshness policy is approved; otherwise it remains UNKNOWN.
- Captured source revision, exact row count, snapshot digest and error state are recorded in execution evidence.

No PRE transition is applied and no HSMART task, GitHub issue, branch, PR or KM stage is changed by this adapter.
