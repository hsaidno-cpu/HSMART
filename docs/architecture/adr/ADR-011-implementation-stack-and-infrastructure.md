# ADR-011 — MVP Application Stack & Infrastructure Direction

- **Status:** RECOMMENDED BASELINE — FORMAL ACCEPTANCE PENDING
- **Version:** 1.1.0
- **Date:** 2026-11-22
- **Decision class:** D2
- **Decision owner:** Architecture Lead; accountable approval by Project Sponsor/Owner — appointments pending
- **Related:** ADR-001 through ADR-010; Project Charter v1.0.0; MVP Decision Record v1.1.0
- **Supersedes:** None

## 1. Context

HSMART's logical architecture is established, but its application stack, infrastructure provider, cloud region, identity provider, secret manager/KMS, object-storage provider, domain and production deployment target have not been selected.

The MVP requires one vertical slice with REST and Remote MCP distribution, durable registry metadata, immutable artifacts, policy enforcement, isolated execution, audit evidence and a basic synchronization/rollback path. A small-team-first design is preferable to premature microservices and infrastructure sprawl.

This ADR therefore separates (a) a recommended technology baseline for an engineering spike from (b) vendor, region, procurement and production decisions that require team, security, residency, budget and operating evidence.

## 2. Decision drivers

1. Preserve modular-monolith architecture and separable worker processes.
2. Support REST and Remote MCP through shared contracts and policy decisions.
3. Support immutable artifacts, provenance and digest verification.
4. Make local development and CI straightforward to reproduce.
5. Keep tenant, identity, runtime and data boundaries enforceable.
6. Minimize operational burden for an initially small team.
7. Keep provider-specific integrations behind narrow adapters.
8. Avoid paid commitments or production resource creation before authority and budget approval.
9. Prefer reversible, evidence-tested choices over broad vendor commitments.

## 3. Recommended MVP technology baseline

These are the recommended defaults to validate in a short vertical-slice spike. They are not an accepted procurement decision.

| Concern | Recommended baseline | Rationale / guardrail |
|---|---|---|
| Backend | Python 3.12 + FastAPI | Fits the AI/tooling ecosystem and existing Python contract harness; accept only after Engineering Lead confirms team capability |
| Application shape | Modular monolith with explicit domain modules and separate worker process | Matches ADR-001 and avoids premature distributed-systems overhead |
| Primary database | PostgreSQL | Transactions, relational constraints, JSON support and durable system-of-record behavior |
| Data access/migrations | SQLAlchemy 2.x + Alembic, subject to a minimal proof-of-fit spike | Mature typed persistence and explicit versioned migrations; do not hide SQL or tenant boundaries behind repository magic |
| Job orchestration | PostgreSQL-backed job/outbox table plus independently restartable worker | Supports initial durability/idempotency without introducing a broker before workload and retry semantics are measured |
| Artifact storage | S3-compatible object storage with versioning and provider-supported retention/Object Lock where appropriate | Keeps large immutable artifacts outside relational records; digest/provenance remain in the control plane |
| Identity | External OIDC/OAuth issuer behind a provider adapter | Avoid building a home-grown identity provider; bind token audience, issuer, principal and scopes |
| Application secrets | Managed secret manager and KMS-backed key operations | No home-grown root-key vault and no plaintext production secret in the database or Git |
| Packaging | OCI container images for API and worker | Portable build/deploy boundary; worker gets narrower credentials and network access than API |
| Deployment | One region and one managed container service for the first hosted acceptance environment | Lower operational load; exact provider and region remain undecided |
| Observability | OpenTelemetry-compatible traces, metrics and structured logs | Portable telemetry conventions; redact credentials and sensitive payloads |
| Infrastructure as code | Terraform or OpenTofu only after provider selection and ownership are confirmed | Avoid writing provider-specific infrastructure that cannot yet be run or reviewed |

## 4. Explicitly deferred choices

- **Message broker:** do not add Redis, RabbitMQ, NATS or a managed queue to the MVP by default. Revisit only when measured throughput, ordering, delayed delivery, retry/dead-letter or independent scaling needs exceed the database-backed outbox design.
- **Kubernetes:** not an MVP prerequisite. Revisit only if deployment topology, isolation, scheduling or operations demonstrably require it.
- **Microservices:** no service extraction until a domain or operational boundary justifies the distributed-system cost.
- **Cloud provider and region:** open until data classification/residency, team operations, cost, backup/restore, networking and legal requirements are documented.
- **OIDC vendor, KMS and secret manager:** open until identity lifecycle, recovery, key custody, region, audit and cost are assessed.
- **Artifact store vendor:** open until durability, immutability, lifecycle, egress, recovery and cost are compared.
- **Public domain/DNS/TLS and production endpoint:** no purchase or deployment until an authorized owner approves budget and legal responsibility.

## 5. Alternatives considered

### Backend

| Option | Strengths | Costs / risks | Current disposition |
|---|---|---|---|
| Python + FastAPI | Python-native AI ecosystem, JSON Schema support, async API support, fast vertical-slice development | Requires typed contracts, code review and domain-boundary discipline | Recommended; team capability spike required |
| TypeScript + NestJS | Strong typing, modular conventions, broad web ecosystem | More cross-language adapters may be needed for Python-native tools and workers | Viable fallback if team skills or client integration favor TypeScript |
| Other framework | May fit a verified team or deployment constraint | Must prove material benefit and long-term maintenance support | Not selected |

### Persistence and asynchronous work

- PostgreSQL is preferred over SQLite as the hosted system of record.
- SQLite may be used for isolated unit tests only when its behavior does not substitute for PostgreSQL integration tests.
- A database-backed outbox/job table is the default MVP approach; durable state must not depend on an in-process memory queue.
- A broker is a future optimization, not an architectural checkbox.

### Infrastructure model

- Use provider adapters and avoid provider-specific APIs in domain logic.
- Start with one non-production hosted environment and one region after approval.
- Separate local, CI and hosted environment configuration and credentials.
- Keep API and worker identities separate; default-deny worker egress except explicitly required endpoints.
- Backups are not accepted until restoration has been tested.
- Object versioning alone is not proof of immutability; verify provider retention controls and digest behavior with an integration test.

## 6. Required proof-of-fit before acceptance

1. Engineering Lead records team capability and completes a small FastAPI vertical-slice spike against the canonical OpenAPI contract. If the team cannot own it, compare NestJS before acceptance.
2. Architecture Lead proves PostgreSQL migrations, uniqueness, transaction boundaries, tenant isolation and outbox recovery.
3. Security & Privacy Lead reviews OIDC audience/issuer handling, worker identity, key lifecycle, secrets, data residency and default-deny egress.
4. Operations/Reliability Lead demonstrates deployment, backup/restore, logs/metrics/traces and recovery ownership.
5. Project Sponsor/Owner sets a budget envelope and approves any paid resource.
6. Candidate cloud providers/regions are compared against documented criteria: Indonesia/data residency needs, latency, availability, managed services, security controls, recovery, support, portability and total cost.
7. ADR approval is recorded by the roles with authority; the accepted ADR and decision log are updated in the same reviewed change.

## 7. Rollback / reconsideration

Reconsider before production if the selected stack fails the vertical-slice acceptance criteria, creates unacceptable operational burden, violates data-residency/security requirements or materially harms portability. Reconsideration requires an ADR amendment and migration plan; do not silently change the stack.

## 8. Approval record

| Approver role | Name | Decision | Date |
|---|---|---|---|
| Project Sponsor / Accountable Owner | NOT APPOINTED | PENDING | — |
| Architecture Lead | NOT APPOINTED | PENDING | — |
| Engineering Lead | NOT APPOINTED | PENDING | — |
| Security & Privacy Lead | NOT APPOINTED | PENDING | — |
| Operations / Reliability Lead | NOT APPOINTED | PENDING | — |

## 9. Current disposition

**The recommended technology baseline is sufficiently specific for a reversible engineering spike. The formal ADR is not accepted.** No cloud provider, region, domain, database service, OIDC issuer, KMS, secret manager or paid service has been procured or deployed. This record must not be cited as authorization to spend money or launch production infrastructure.
