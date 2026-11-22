# ADR-011 — Initial Implementation Stack & Infrastructure Direction

- **Status:** PROPOSED — NOT ACCEPTED
- **Date:** 2026-11-22
- **Decision class:** D2
- **Decision owner:** Architecture Lead; accountable approval by Project Sponsor/Owner — appointments pending
- **Related:** ADR-001 through ADR-010; Project Charter v1.0.0; KM 1 roadmap
- **Supersedes:** None

## 1. Context

HSMART has accepted logical architecture decisions but has not selected the concrete application stack, database/migration tool, queue, OIDC issuer, secret manager/KMS, artifact storage provider, cloud region or deployment runtime.

Choosing vendors or frameworks without confirmed team skills, workload, budget, data classification, residency and operational responsibility would create avoidable lock-in. This ADR separates a recommended default direction from decisions that require evidence or explicit approval.

## 2. Decision drivers

1. Preserve modular-monolith architecture and separable workers.
2. Support REST and Remote MCP through shared contracts and policy decisions.
3. Support immutable artifacts, provenance and digest verification.
4. Make local development and CI reproducible.
5. Keep tenant, identity, runtime and data boundaries enforceable.
6. Minimize operational burden for an initially small team.
7. Keep provider-specific integrations behind adapters.
8. Avoid paid commitments or production resource creation before authority and budget approval.

## 3. Alternatives considered

### Application backend

| Option | Strengths | Costs / risks | Fit |
|---|---|---|---|
| Python + FastAPI | Strong AI/tooling ecosystem, direct JSON Schema support, async API support, concise service development | Team typing discipline and architecture boundaries must be enforced; async/concurrency design still needs review | Preferred candidate if team capability is confirmed |
| TypeScript + NestJS | Strong types, modular application patterns, broad web/backend ecosystem | Additional adapter/SDK boundary work may be needed for Python-native AI tooling; team familiarity unknown | Viable alternative |
| Other framework | May fit team or deployment constraints | Requires a concrete capability/maintenance rationale | Keep open |

Provisional recommendation: Python 3.12 + FastAPI as the first backend candidate, conditional on Engineering Lead confirmation of team proficiency and a short vertical-slice spike. This is not an accepted final stack decision.

### Persistence

| Option | Strengths | Risks / conditions | Provisional direction |
|---|---|---|---|
| PostgreSQL | Relational constraints, transactions, JSON support, mature migrations and multi-tenant modeling options | Requires careful tenant isolation, migration ownership, backups and connection management | Preferred primary system of record |
| SQLite | Very low local friction | Not the initial multi-tenant/operational system of record for a hosted service | Local-only testing convenience |
| Other relational store | Could fit team/provider constraints | Must demonstrate equivalent constraints, operations and portability | Revisit with evidence |

### Queue / background work

- Do not select a broker solely because the target architecture mentions workers.
- Start with a database-backed job/outbox strategy or a simple in-process development worker only if it satisfies the first workload and failure model.
- Introduce Redis Streams, RabbitMQ, NATS or a managed queue only after a spike establishes delivery semantics, retry/dead-letter, ordering, throughput and operational needs.
- A cache must not be mistaken for durable workflow state.

### Artifact storage

- Use an S3-compatible object-storage abstraction for immutable artifacts and metadata references.
- Require versioning/object-lock or an equivalent immutable retention control where the selected provider supports it.
- Keep digest/signature/provenance metadata in the control plane; verify content on publish and before trusted execution.
- Select the concrete provider only after region, residency, cost and recovery requirements are approved.

### Identity and secrets

- Use OIDC/OAuth-compatible issuer integration with audience/resource binding and workload identity where required.
- Use a managed secret manager/KMS-backed service; do not build a home-grown root-key vault.
- Select the concrete OIDC issuer, KMS and secret provider only after ownership, region, recovery, cost and compliance review.
- Keep key verifier/hash records separate from recoverable secret material.

### Deployment and observability

- Containerized modular monolith plus separable worker process is the initial deployment shape.
- Do not require Kubernetes for MVP.
- Keep separate local, test and hosted environment configurations; production isolation and secret boundaries are mandatory.
- Instrument service boundaries using portable trace/log/metric conventions (OpenTelemetry-compatible); select backend vendors later.
- No production domain, cloud account, DNS/TLS, database, OAuth issuer or paid service is assumed to exist.

## 4. Proposed baseline

| Concern | Candidate baseline | Decision status |
|---|---|---|
| Backend | Python 3.12 + FastAPI | PROPOSED |
| Primary database | PostgreSQL | PROPOSED |
| Migration tool | Alembic if SQLAlchemy is selected; otherwise equivalent versioned migrations | CONDITIONAL |
| Artifact store | S3-compatible immutable/versioned object storage | PROPOSED |
| Job queue | Defer concrete broker until workload spike | DEFERRED |
| Identity | OIDC/OAuth issuer adapter | REQUIRED CONTRACT; provider open |
| Secrets | Managed secret manager/KMS adapter | REQUIRED CONTROL; provider open |
| Packaging | OCI/container image for service/worker | PROPOSED |
| Deployment | Single-region managed container runtime first | PROPOSED; vendor/region open |
| Observability | OpenTelemetry-compatible traces/logs/metrics | PROPOSED |
| Infrastructure as code | Select after cloud/provider decision | OPEN |

## 5. Consequences

### Positive
- A concrete candidate path exists for engineering spikes without pretending a vendor has been procured.
- Portable adapters avoid binding core contracts to a single OIDC, storage or cloud vendor.
- Modular monolith keeps operational complexity proportionate.
- Queue selection is deferred until an actual workload/failure contract exists.

### Negative / risks
- Python/FastAPI may be wrong if team proficiency or consumer SDK requirements favor TypeScript.
- Provider-neutral abstractions can become over-engineered if too many adapters are designed before one integration works.
- Deferring a broker requires the first execution design to be explicit about durability, retries and job recovery.
- Object-store immutability and signature semantics vary by provider and must be tested, not assumed.

## 6. Required evidence before acceptance

- Engineering Lead confirms team proficiency and maintains a short comparative spike.
- Project Sponsor/Owner confirms budget envelope and authority for any paid services.
- Architecture Lead evaluates data model, migration, transaction, outbox and tenancy requirements.
- Security & Privacy Lead confirms identity, secrets, region, data residency and threat-model implications.
- Operations Lead confirms deployment, backup/restore, observability and incident ownership.
- Concrete providers and regions are selected only after the above evidence exists.
- Decision log and implementation roadmap are updated to the accepted ADR.

## 7. Rollback / reconsideration

Reconsider before production if the selected backend, data store or deployment model fails the vertical-slice acceptance criteria, produces unacceptable operational burden, violates data-residency/security requirements, or makes adapter portability materially worse. Reconsideration requires an ADR amendment and migration plan; do not silently change stack.

## 8. Approval record

| Approver role | Name | Decision | Date |
|---|---|---|---|
| Project Sponsor / Accountable Owner | NOT APPOINTED | PENDING | — |
| Architecture Lead | NOT APPOINTED | PENDING | — |
| Engineering Lead | NOT APPOINTED | PENDING | — |
| Security & Privacy Lead | NOT APPOINTED | PENDING | — |
| Operations / Reliability Lead | NOT APPOINTED | PENDING | — |

Until the approval record is completed, this file is a proposal and must not be cited as an accepted implementation-stack decision.
