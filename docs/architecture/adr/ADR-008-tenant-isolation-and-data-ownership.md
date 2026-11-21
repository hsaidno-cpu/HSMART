# ADR-008: Enforce Tenant Isolation and Domain Data Ownership

- Status: Accepted baseline
- Date: 2026-11-21

## Context
HSMART is multi-tenant and includes independent publishers and organizations. Cross-tenant leakage would be a critical platform failure.

## Decision
Each domain owns authoritative data. Cross-domain access uses contracts/events rather than direct database writes. Tenant scope is derived from authenticated identity and grants, then applied to every resource query and object access.

## Consequences
- Tenant context cannot be trusted from request body alone.
- Isolation is tested across APIs, search, caches, artifacts, logs, and asynchronous workers.
- Audit evidence is append-only.
- Retention, deletion, and residency must be explicit.
