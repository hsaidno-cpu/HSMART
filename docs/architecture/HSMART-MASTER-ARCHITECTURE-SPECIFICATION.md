# HSMART Master Architecture Specification

- Document ID: HSMART-MAS-001
- Version: 1.0.0
- Status: Architecture baseline
- Date: 2026-11-21
- Implementation status: Not yet implemented or production-verified

## 1. Purpose and positioning

HSMART (Hypersystem Management & Synchronization Architecture for Revolutionary Technology) is a universal AI ecosystem infrastructure platform. It standardizes how independently owned AI capabilities are identified, discovered, authorized, executed, evaluated, distributed, and updated.

HSMART is an infrastructure and governance layer. It does not own the intelligence of every model or platform connected to it.

Lifecycle: Create → Register → Validate → Publish → Discover → Authorize → Execute → Synchronize → Evaluate → Improve → Retire.

## 2. Binding strategic decisions

| Dimension | Baseline |
|---|---|
| Ownership | Hybrid Foundation + Commercial Operator |
| Execution | Hybrid managed cloud + self-hosted runtime |
| Distribution | Universal through standard protocols and platform adapters |
| Synchronization | Adaptive and risk-based |
| Ecosystem | Governed multi-publisher marketplace |

These are architecture decisions, not proof of implementation or legal establishment.

## 3. Vision and outcomes

1. Reduce duplicated plugin distribution and lifecycle infrastructure.
2. Establish canonical capability identity and metadata.
3. Support MCP, REST/HTTP, SDKs, events, and adapters.
4. Execute approved capabilities in managed or customer-controlled environments.
5. Reconcile desired and observed versions without unsafe forced updates.
6. Provide traceable identity, permissions, publisher provenance, and execution audit.
7. Enable a trusted marketplace for internal and external publishers.

## 4. Architecture principles

- API-first: every domain exposes explicit, versioned contracts.
- MCP-native, not MCP-only: MCP is a preferred interoperability interface; REST/HTTP and SDKs remain first-class.
- Protocol-agnostic core: canonical semantics must not depend on one AI vendor.
- Control/execution separation: policy and lifecycle control are isolated from untrusted code execution.
- Hybrid runtime: managed cloud and self-hosted workers implement the same runtime contract.
- Immutable releases: published version artifacts are immutable and addressed by digest.
- Adaptive synchronization: change risk determines validation, approval, rollout, and rollback.
- Zero trust: no identity or workload is trusted solely because of network location.
- Tenant isolation: boundaries apply to data, credentials, invocations, and audit.
- Evidence-based governance: release and marketplace decisions require verifiable evidence.
- Reversible operations: deployments have a tested recovery path.
- Modular delivery: begin with a modular monolith and extract services only when evidence justifies it.

## 5. System context and actors

External actors include AI clients (ChatGPT, Claude, Gemini, local AI, custom applications), developers, publishers, organization administrators, marketplace consumers, Foundation governance, Commercial Operator, self-hosted runtime operators, and external model/API/MCP providers.

## 6. Logical planes

**Control Plane:** organization and publisher management; capability registry and lifecycle; policy and access governance; release, channel, and synchronization policy; marketplace metadata and entitlements.

**Execution Plane:** invocation dispatch; worker scheduling; sandbox and resource control; capability execution; results and runtime telemetry.

**Data Plane:** controlled artifact transfer; request/response transport; event delivery; customer-approved data movement.

These are logical boundaries. MVP deployment may colocate components while preserving access and data boundaries.

## 7. Twelve bounded contexts

| ID | Domain | Primary responsibility |
|---|---|---|
| D01 | Studio & Developer Experience | Authoring, validation, local test, publish workflow |
| D02 | Universal Registry | Identity, manifests, versions, dependencies, provenance |
| D03 | Publisher & Organization | Organizations, members, publisher identity, tenancy |
| D04 | Intelligence Orchestrator | Capability selection, task routing, workflow and agent coordination |
| D05 | Execution Runtime | Isolated cloud and self-hosted execution |
| D06 | Distribution Gateway | MCP, REST/HTTP, SDK, webhook, client adapters |
| D07 | Synchronization Engine | Desired/observed state, risk classification, rollout, rollback |
| D08 | Access & Identity | Authentication, authorization, API keys, connectors, vault references |
| D09 | Evaluation & Assurance | Functional, security, compatibility, regression, release evidence |
| D10 | Observability & Audit | Logs, metrics, traces, append-only audit evidence |
| D11 | Marketplace & Commerce | Listings, discovery, reviews, licensing, entitlement, usage |
| D12 | Infrastructure & Operations | Deployment, secrets integration, backup, recovery, operations |

Normative ownership and forbidden dependencies are in DOMAIN-BOUNDARIES.md.

## 8. Hybrid ownership model

**HSMART Foundation** governs mission, core standards, architecture constitution, trust requirements, certification criteria, trademark policy, and community governance.

**Commercial Operator** operates managed hosting, customer support, billing, marketplace operations, service-level commitments, and enterprise contracts under Foundation policy.

**Independent publishers** retain ownership of their capability IP and grant only clearly scoped distribution/execution rights under an explicit license.

The hybrid model is an operating design, not a legal entity structure. Legal incorporation, IP assignment, trademark ownership, data controller/processor roles, contribution terms, and liability must be resolved in separate legal instruments before commercial operation.

## 9. Hybrid execution model

### Managed cloud
HSMART operates gateway, scheduler, and isolated workers. Publisher artifacts are verified before execution. Tenant quota, data handling, network egress, and runtime permissions are policy-controlled.

### Self-hosted
A customer runs a HSMART runtime agent in its environment. It establishes workload identity, registers capabilities and health, receives signed desired-state instructions, verifies artifacts, executes locally, and reports observed state and permitted telemetry.

A self-hosted runtime must not gain Control Plane administrator privileges merely by registering. Control Plane access is outbound and narrowly scoped by default.

### Runtime trust
Use workload identity, short-lived credentials or certificates, signed instructions, artifact digest/signature verification, constrained egress, and explicit organization/environment binding. An API key alone is insufficient evidence of runtime trust.

## 10. Universal distribution

- Remote MCP for clients supporting MCP.
- REST/HTTP for generic integrations and clients without MCP support.
- SDKs for developer ergonomics.
- Webhooks/events for lifecycle and execution notifications.
- Platform adapters for client-specific authentication, tool schemas, and refresh behavior.

HSMART can publish updated server-side behavior after a safe deployment. It cannot guarantee that an external AI platform refreshes locally cached tool lists or configuration without client-side refresh, reconnect, or adapter action.

## 11. Adaptive synchronization

Synchronization reconciles **desired state** with **observed state**. It does not blindly force every consumer to the newest release.

Required stages:
1. Detect release or policy change.
2. Verify publisher, provenance, artifact digest, and signature.
3. Classify change and assess impact.
4. Resolve dependencies and compatibility.
5. Run functional, security, schema, and regression tests.
6. Obtain approvals required by risk or tenant policy.
7. Stage, canary, or deploy to eligible targets.
8. Verify health and observed version.
9. Promote or rollback.
10. Record evidence and notify consumers.

Default risk classes:
- R0: non-operational documentation/metadata; automated validation.
- R1: low-risk compatible fixes; automated tests and staged rollout.
- R2: functional minor changes; compatibility checks and staged rollout.
- R3: API/schema/dependency/migration changes; explicit approval and migration plan.
- R4: security, permission, data handling, or execution behavior changes; security review and explicit approval.
- R5: critical, suspicious, or unverifiable changes; quarantine and manual review.

Risk classification may recommend a control; deterministic policy and authorized humans determine mandatory approval. No model-generated risk assessment can waive cryptographic or security gates.

## 12. Functional requirements

### P0 — MVP
- Register organizations, publishers, and capabilities.
- Assign stable capability IDs and immutable version records.
- Validate canonical manifests and dependencies.
- Store artifact digests and release provenance.
- Discover capabilities with tenant visibility rules.
- Expose authenticated REST invocation and Remote MCP tools.
- Enforce scoped authorization and quotas.
- Execute approved capability artifacts in isolated cloud workers.
- Record invocation, version, outcome, and audit correlation.
- Evaluate candidate releases before stable deployment.
- Maintain desired and observed version state.
- Support revocation and quarantine.

### P1 — Growth
- Self-hosted runtime registration and reconciliation.
- Canary and staged rollout; automated rollback.
- Advanced dependency solving.
- Platform adapters and SDKs.
- Marketplace publisher onboarding, licensing, entitlement, and usage metering.
- Multi-agent orchestration subject to per-tool permissions and approval rules.

### P2 — Scale
- Multi-region topology and registry federation.
- Advanced marketplace analytics and settlement.
- Runtime federation and policy-aware placement.
- Automated recovery beyond basic rollback.

## 13. Non-functional requirements and initial targets

These are planning objectives, not achieved service guarantees. Validate through load, resilience, and security tests.

| Area | Initial target |
|---|---|
| Managed control-plane availability | 99.9% after production hardening |
| Gateway overhead | p95 below 300 ms, excluding model/skill execution |
| Registry query | p95 below 500 ms under agreed baseline load |
| Tenant isolation | No cross-tenant access without explicit grant |
| Recovery point objective | 15 minutes for critical state after DR implementation |
| Recovery time objective | 4 hours after DR implementation |
| Stateless scaling | Horizontal scaling |
| Security | TLS, least privilege, default deny, secret redaction |
| Reliability | Idempotency, bounded retries, circuit breakers, DLQ |
| Portability | Container-based runtime |
| Audit | Traceable privileged actions and release decisions |

## 14. Data and persistence

- PostgreSQL: organizations, identities, registry metadata, releases, policies, sync state, listings, entitlements, audit indexes.
- Object storage: immutable artifacts, SBOM, provenance, evaluation reports, assets.
- Redis: cache, rate limiting, short-lived coordination; never the system of record.
- Message broker: domain events and asynchronous work.
- KMS/secret manager: encryption keys and secret material.
- Observability backend: operational logs, metrics, and traces with retention controls.

See ../data/DATA-MODEL.md.

## 15. Security baseline

Apply Zero Trust and STRIDE-informed threat modeling. Core controls include OIDC/OAuth, audience-bound tokens, workload identity, least privilege, sandboxing, egress restrictions, signed immutable artifacts, SBOM/provenance, vault integration, SSRF protection, audit integrity, and incident response.

See ../security/THREAT-MODEL.md and ../security/SECURITY-BASELINE.md.

## 16. API and protocol contracts

- REST API is versioned under /v1.
- MCP endpoint is exposed separately (for example /mcp) and follows a pinned, tested MCP revision.
- Canonical manifest: ../contracts/capability-manifest.schema.json.
- REST contract: ../contracts/openapi.yaml.
- Event envelope and catalog: ../contracts/event-envelope.schema.json and ../contracts/EVENT-CATALOG.md.
- Every API defines authentication, authorization, validation, idempotency, pagination, errors, quotas, and audit behavior.

## 17. Technology selection policy

Initial candidates:
- Backend: Python/FastAPI or TypeScript; final selection requires an ADR and vertical-slice benchmark.
- Database: PostgreSQL.
- Cache: Redis.
- Artifact storage: S3-compatible object storage.
- Deployment: Docker.
- CI/CD: GitHub Actions.
- Identity: OIDC-compatible provider.
- Telemetry: OpenTelemetry-compatible stack.
- Messaging: broker abstraction; select concrete broker after reliability and operations evaluation.

Do not introduce Kubernetes, microservices, or multi-region complexity before a demonstrated need and operational owner exist.

## 18. Marketplace and licensing

Marketplace participation is governed by publisher verification, artifact integrity, permission disclosure, security evaluation, licensing, entitlement checks, abuse reporting, quarantine, and takedown procedures. A listing is not authorization to execute. Invocation independently enforces current entitlement and runtime policy.

See ../governance/OWNERSHIP-AND-MARKETPLACE.md.

## 19. Delivery roadmap

1. Architecture/governance foundation.
2. Registry and canonical manifest.
3. Access, MCP, and REST.
4. Isolated managed-cloud runtime.
5. Adaptive synchronization and release governance.
6. Self-hosted runtime and platform adapters.
7. Marketplace and commerce.
8. Production hardening and operational readiness.

See ../roadmap/IMPLEMENTATION-ROADMAP.md.

## 20. MVP definition of done

Evidence must demonstrate:
- a publisher registers a capability and validated manifest;
- a signed immutable release is published;
- a permitted MCP client and REST client discover/invoke it;
- an unauthorized request is denied;
- execution occurs in an isolated runtime;
- desired/observed versions are recorded;
- a compatible update is evaluated and propagated;
- a breaking or high-risk update is blocked pending approval;
- rollback restores a known-good release;
- audit records correlate publisher, release, runtime, tenant, and invocation;
- no secrets appear in logs, artifacts, manifests, or client-visible errors.

## 21. Open decisions

Cloud provider/region, backend language, message broker, OIDC provider, KMS, payment provider, legal entity/IP structure, public/private licensing boundaries, and initial SLO/support commitments remain open. Each requires an ADR and relevant security/legal review.

## 22. Status

This is the strategic architecture baseline. It does not claim that services, APIs, deployments, or production controls are implemented. Implementation status must be tracked separately through issues, pull requests, test evidence, and release records.
