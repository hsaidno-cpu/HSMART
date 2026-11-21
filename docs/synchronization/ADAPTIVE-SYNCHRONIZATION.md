# HSMART Adaptive Synchronization Engine

## Purpose
Reconcile desired capability/runtime state with observed state while preserving compatibility, security, approval, and rollback controls.

## State model
- Desired state: target capability version and policy selected by an authorized owner.
- Observed state: version actually verified and running on a target.
- Candidate state: release under validation or staged rollout.
- Blocked state: update cannot proceed until a condition is resolved.
- Quarantined state: capability, release, or connector is prevented from use pending review.

Never infer observed state from a successful control-plane request. Runtime must report verified state with artifact digest and deployment identity.

## Change-risk classification

| Class | Typical change | Minimum handling |
|---|---|---|
| R0 | Documentation or non-operational metadata | Validate and publish |
| R1 | Low-risk compatible fix | Automated tests, staged promotion |
| R2 | Minor behavior change | Regression and compatibility tests, rollout |
| R3 | API/schema/dependency/migration change | Explicit approval, migration plan |
| R4 | Permission, security, data handling, execution behavior | Security review, owner approval |
| R5 | Critical or suspicious change | Quarantine, manual investigation |

The classifier may recommend a risk class; deterministic rules and authorized humans determine mandatory controls. A model-generated assessment cannot waive hard security gates.

## Reconciliation workflow
1. Receive release event or authorized synchronization request.
2. Resolve target scope and policy.
3. Verify publisher, signature, digest, provenance, and channel.
4. Compare candidate version and dependencies with observed state.
5. Generate a change-impact report.
6. Run schema, API, dependency, functional, regression, security, and compatibility checks.
7. Obtain approvals required by risk and tenant policy.
8. Create rollout plan and immutable deployment intent.
9. Deploy to canary or staged target.
10. Verify runtime health, version, and artifact digest.
11. Promote, pause, or rollback.
12. Record evidence and notify consumers.

## Update modes
- pinned: use an exact approved version.
- latest-compatible: choose the newest version satisfying declared constraints and policy.
- adaptive: resolve version based on channel, risk, compatibility, approvals, target health, and tenant rules.

Stable is a release channel, not a guarantee that every target updates instantly.

## Rollout strategies
- immediate: only for low-risk, pre-authorized changes.
- staged: progressively update an explicitly defined target set.
- canary: update a small representative target group, observe, then promote.

Define health thresholds before rollout. A failed canary halts promotion and triggers rollback or quarantine.

## Safety invariants
- Never deploy an unsigned or digest-mismatched artifact.
- Never bypass mandatory evaluation gates.
- Never update an incompatible pinned consumer silently.
- Never restore a revoked permission through synchronization.
- Never retry a non-idempotent side effect without deduplication.
- Preserve last-known-good release metadata.
- Rollback is a new deployment action with audit evidence; do not rewrite history.
- Client-side manifest refresh is separate from server/runtime deployment.

## Reconciliation statuses
pending, classifying, evaluation_pending, approval_required, blocked, staging, canary, promoting, completed, failed, rolling_back, rolled_back, quarantined.

## Required telemetry
Record sync ID, target ID, capability ID, desired version, observed version, candidate digest, policy version, risk class, evaluation run, approval record, rollout stage, health evidence, actor, timestamps, and outcome.

## Failure handling
Use bounded retries with exponential backoff and jitter for transient failures. Repeatedly failing work goes to a dead-letter path. Conflicts or stale desired-state updates require reconciliation rather than blind retry. Rollback verifies the prior artifact and runtime compatibility before activation.
