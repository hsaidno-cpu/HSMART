# ADR-011 — MVP Application Stack & Infrastructure Direction

- **Status:** ACCEPTED BY GOV-01 — INTERNAL TECHNICAL BASELINE; PROVIDER/PROCUREMENT CHOICES DEFERRED
- **Version:** 1.2.0
- **Date:** 2026-11-22
- **Decision class:** D2
- **Decision owner:** GOV-01 Project Sponsor / Accountable Owner; AI technical delegates provide bounded recommendations only
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

GOV-01 accepts these defaults as the internal MVP application stack baseline for KM 1. This acceptance does not select a cloud vendor, region, identity provider, object-store vendor, paid service or spending ceiling.

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

## 6. Proof-of-fit and implementation verification

1. GOV-05 AI Engineering Delegate maintains the FastAPI implementation against the canonical OpenAPI contract; Python 3.12 CI is the reference environment.
2. GOV-04 AI Architecture Delegate challenges PostgreSQL migrations, uniqueness, transaction boundaries, tenant isolation and outbox recovery.
3. GOV-06 AI Security & Privacy Delegate assesses OIDC audience/issuer handling, workload identity, key lifecycle, secrets, data residency and default-deny egress.
4. GOV-07 AI Operations/Reliability Delegate prepares deployment, backup/restore, observability and recovery evidence; its runtime is inactive until A1–A8 pass.
5. GOV-01 separately approves any provider, region, budget and paid resource before provisioning.
6. Candidate cloud providers/regions are compared against documented criteria: Indonesia/data residency needs, latency, availability, managed services, security controls, recovery, support, portability and total cost.
7. GOV-01 acceptance is recorded in HSMART-GOV-DEC-2026-11-22-002. KM 1 exit still requires hosted CI, AI assurance and GOV-01 acceptance of the exact implementation commit.

## 7. Rollback / reconsideration

Reconsider before production if the selected stack fails the vertical-slice acceptance criteria, creates unacceptable operational burden, violates data-residency/security requirements or materially harms portability. Reconsideration requires an ADR amendment and migration plan; do not silently change the stack.

## 8. Approval record

| Approver role | Name | Decision | Date |
|---|---|---|---|
| GOV-01 — Project Sponsor / Accountable Owner | Harysaidno | ACCEPTED — HSMART-GOV-DEC-2026-11-22-002 | 2026-11-22 |
| GOV-04 — Architecture Lead (AI delegate) | Designated; runtime inactive | Technical recommendation only | 2026-11-22 |
| GOV-05 — Engineering Lead (AI delegate) | Designated; runtime inactive | Implementation/evidence within grant | 2026-11-22 |
| GOV-06 — Security & Privacy Lead (AI delegate) | Designated; runtime inactive | Security challenge/HOLD recommendation | 2026-11-22 |
| GOV-07 — Operations & Reliability Lead (AI delegate) | Designated; runtime inactive | Operational evidence/runbook preparation | 2026-11-22 |

## 9. Current disposition

**ADR-011 v1.2.0 is ACCEPTED by GOV-01 as the internal KM 1 application-stack baseline** under `HSMART-GOV-DEC-2026-11-22-002`. This accepts Python 3.12 + FastAPI, modular monolith, PostgreSQL, SQLAlchemy/Alembic, PostgreSQL outbox worker, OCI packaging, OIDC adapter, managed secrets/KMS conventions and OpenTelemetry-compatible observability as the internal technical direction. It does not select or procure a cloud provider, region, domain, identity provider, KMS, secret manager, artifact-store vendor or paid service.

Acceptance of ADR-011 is distinct from KM 1 exit acceptance. KM 1 still requires passing contract, application/PostgreSQL and repository-governance CI; AI assurance evidence; and a separate GOV-01 decision on the exact implementation commit. This record does not certify production deployment or approve spending/external commitments.
