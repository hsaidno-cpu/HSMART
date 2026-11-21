# ADR-006: Use Risk-Adaptive Synchronization

- Status: Accepted baseline
- Date: 2026-11-21

## Context
Automatic update improves consistency but can propagate breaking changes or malicious releases. Pinning all versions prevents timely fixes and creates operational fragmentation.

## Decision
Reconcile desired and observed state under pinned, latest-compatible, or adaptive policies. Classify changes and require progressively stronger tests and approvals as risk increases.

## Consequences
- Published artifacts are immutable.
- Mandatory cryptographic and security checks cannot be bypassed.
- High-risk changes require explicit review.
- Rollout and rollback produce audit evidence.
- Client refresh is separate from server/runtime synchronization.
