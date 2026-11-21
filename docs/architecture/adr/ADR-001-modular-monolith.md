# ADR-001: Start with a Modular Monolith

- Status: Accepted baseline
- Date: 2026-11-21

## Context
HSMART has multiple bounded contexts, but team size, workload, and operational capacity are not yet known. Distributed services would introduce deployment, networking, observability, and consistency overhead before scale requirements are measured.

## Decision
Implement the first platform as a modular monolith with explicit domain modules and independently testable contracts. Extract workers or services only when scale, fault isolation, security boundary, or team ownership justifies it.

## Consequences
- Faster vertical-slice delivery.
- Easier local development and contract testing.
- Domain boundaries must be enforced through module interfaces and data ownership.
- Avoid shared tables and unrestricted cross-module imports.
- Service extraction requires an ADR and migration plan.
