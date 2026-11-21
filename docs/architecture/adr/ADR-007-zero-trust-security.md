# ADR-007: Adopt Zero-Trust Security and Workload Identity

- Status: Accepted baseline
- Date: 2026-11-21

## Context
HSMART connects external AI clients, third-party publishers, connectors, managed workers, and customer-operated runtimes across trust boundaries.

## Decision
Apply default-deny authorization, least privilege, OIDC/OAuth for user/application access, workload identity for runtime, artifact signing, sandboxing, egress controls, and tamper-evident audit.

## Consequences
- Network location is not an authorization decision.
- Runtime registration does not grant administration.
- Secrets are stored in a dedicated vault/KMS.
- Every protected invocation is authorized at execution time.
