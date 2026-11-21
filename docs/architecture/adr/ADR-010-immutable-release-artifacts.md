# ADR-010: Make Published Release Artifacts Immutable

- Status: Accepted baseline
- Date: 2026-11-21

## Context
Mutable artifacts make it impossible to establish what was evaluated, deployed, or executed. They undermine provenance, rollback, and incident investigation.

## Decision
Every published artifact is addressed by cryptographic digest, carries publisher/build provenance, and is signed. Corrections are new versions; published content is never overwritten.

## Consequences
- Promotion moves an immutable artifact between channels without changing content.
- Runtime verifies digest and signature before deployment and execution.
- Rollback deploys a prior artifact and is itself auditable.
