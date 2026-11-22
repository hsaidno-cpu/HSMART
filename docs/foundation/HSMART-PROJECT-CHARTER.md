# HSMART Project Charter

**Project:** HSMART — Hypersystem Synchronization & Management Architecture for Revolutionary Technology  
**Document ID:** HSMART-GOV-CHARTER-001  
**Version:** 1.0.1  
**Document date:** 2026-11-21  
**Last updated:** 2026-11-22  
**Document owner:** HSMART Project Owner — appointment required  
**Status:** Project governance baseline; formal owner ratification pending  
**Authority:** Governs project scope, delivery priorities, decision rights, and acceptance rules after adoption

---

## 1. Executive charter

HSMART is an initiative to build a **Universal AI Ecosystem Infrastructure Platform**: a vendor-neutral infrastructure layer for registering, governing, distributing, executing, evaluating, and synchronizing AI capabilities across compatible tools, platforms, organizations, and deployment environments.

HSMART is not intended to be another isolated AI assistant, model, plugin collection, or single-vendor marketplace. It is intended to provide the shared infrastructure and governance that allow independently developed capabilities to be identified, trusted, connected, invoked, updated, evaluated, and operated through consistent contracts and policies.

The project will be developed incrementally. It will first prove one complete capability lifecycle, then expand to first-party integrations, hybrid runtime, external publishers, and commercial marketplace functions.

**The first project outcome is not a large feature catalogue. It is one trustworthy end-to-end capability lifecycle with verifiable identity, authorization, execution, evaluation, synchronization, rollback, and audit evidence.**

This charter establishes the project baseline. It does not claim that a legal Foundation, commercial operating company, cloud environment, deployed service, or production runtime already exists.

## 2. Project identity

| Field | Charter definition |
|---|---|
| Project name | HSMART |
| Full name | Hypersystem Synchronization & Management Architecture for Revolutionary Technology |
| Product category | Universal AI Ecosystem Infrastructure Platform |
| Project type | Multi-phase platform engineering and ecosystem development |
| Primary delivery model | Incremental, stage-gated, evidence-based |
| Initial architecture | Modular monolith with separable workers |
| Execution direction | Hybrid managed cloud and self-hosted |
| Distribution direction | Protocol- and adapter-based; MCP and REST/HTTP initially |
| Governance direction | Hybrid Foundation + Commercial Operator, subject to legal structuring |
| Initial release objective | Demonstrable MVP vertical slice, not production marketplace |

## 3. Vision, mission, and strategic intent

### 3.1 Vision

Enable AI capabilities to move across compatible platforms and environments without being trapped in fragmented, incompatible, or opaque distribution systems.

### 3.2 Mission

Build and operate a secure, interoperable, extensible infrastructure that gives AI capabilities a governed lifecycle:

1. **Identify** — assign stable identity and ownership.
2. **Describe** — publish machine-readable contracts, metadata, dependencies, and permissions.
3. **Register** — establish an authoritative capability record and version history.
4. **Trust** — verify publisher, provenance, artifact integrity, and policy compliance.
5. **Discover** — make capabilities discoverable under visibility and entitlement rules.
6. **Authorize** — evaluate identity, tenant, scope, permission, quota, and entitlement for every invocation.
7. **Distribute** — expose approved capabilities through supported protocols and adapters.
8. **Execute** — run capabilities within enforceable resource and security boundaries.
9. **Evaluate** — produce compatibility, quality, security, and operational evidence.
10. **Synchronize** — reconcile desired and observed states using risk-aware rollout and rollback.
11. **Govern** — preserve accountability, auditability, licensing, and lifecycle control.

### 3.3 Strategic outcomes

- Reduce integration fragmentation through canonical contracts and stable capability identities.
- Separate capability identity and lifecycle management from any single model vendor or client platform.
- Provide a shared access and policy layer for internal and external capabilities.
- Support managed and self-hosted execution without weakening trust boundaries.
- Make updates and distribution observable, reversible, and risk-aware.
- Enable a multi-publisher ecosystem without treating marketplace visibility as execution permission.
- Make capability quality and trust measurable through evidence rather than marketing claims.

## 4. Problem statement

The AI ecosystem is fragmented across tools, assistants, plugin formats, skill packages, APIs, model providers, and deployment environments. Capability descriptions, identities, permissions, versions, dependencies, credentials, and update mechanisms are often managed independently.

That fragmentation creates predictable problems:

- The same capability may have multiple names or incompatible versions.
- A client may not understand a capability's inputs, outputs, dependencies, or risks.
- Authentication may exist without a consistent authorization decision across protocols.
- Credential handling may be scattered across connectors and deployments.
- Updates can introduce breaking changes without staged rollout or reliable rollback.
- A package's presence in a catalogue may be mistaken for permission to execute it.
- Evaluation evidence and runtime behavior may not be linked to a specific immutable artifact.
- Self-hosted and managed deployments may drift from each other.
- External publishers create provenance, intellectual-property, licensing, abuse, and support risks.

HSMART addresses these infrastructure and governance gaps. It does not promise to solve every problem in AI or guarantee the correctness of every capability's output.

## 5. Product boundaries

### 5.1 What HSMART is responsible for

HSMART is responsible for the platform-level lifecycle and controls it operates, including:

- Capability registry, identity, metadata, versioning, and discovery.
- Publisher and organization records.
- Canonical capability contracts and compatibility rules.
- Authentication integration, authorization, quotas, and access policy.
- API and protocol distribution, initially REST/HTTP and Remote MCP.
- Runtime orchestration and execution controls.
- Artifact integrity, provenance, and release lifecycle.
- Evaluation evidence, audit, telemetry, and operational visibility.
- Adaptive synchronization, staged rollout, and rollback.
- Publisher onboarding, listing governance, entitlement, and marketplace controls when that phase is approved.

### 5.2 What HSMART does not own by default

Unless explicitly agreed through a separate contract, HSMART does not:

- Own the underlying intellectual property of third-party capabilities.
- Own, train, or control every connected model or AI provider.
- Guarantee that a third-party model or capability produces correct, safe, or legally compliant outputs.
- Control refresh behavior of independently managed client applications.
- Override the security, policy, or operational controls of external platforms.
- Automatically acquire rights to submitted code, prompts, datasets, or artifacts.
- Guarantee uninterrupted availability of external APIs or model providers.
- Treat all imported, discovered, or registered capabilities as trusted or executable.

Responsibility for capability behavior, data processing, licensing, support, and liability must be allocated contractually between the relevant publisher, operator, provider, and consumer.

## 6. Strategic decisions established as the project baseline

The following are the agreed product and architecture direction for planning and implementation. They are not, by themselves, legal incorporation documents or proof that infrastructure has been procured.

| Decision area | Established baseline | Constraint |
|---|---|---|
| Ownership direction | Hybrid Foundation + Commercial Operator | Exact entities, IP ownership, control, and contracts require legal design |
| Execution model | Hybrid managed cloud + self-hosted | Managed execution is the first implementation path |
| Distribution | Universal, protocol- and adapter-based | Support is declared and tested per client/platform |
| Initial protocols | REST/HTTP and Remote MCP | SDKs, webhooks, and adapters expand incrementally |
| Synchronization | Adaptive and risk-based | High-risk and breaking changes require explicit controls |
| Ecosystem | Multi-publisher, internal and external | External publishing is deferred until governance gates exist |
| Architecture style | Modular monolith with separable workers | No premature microservices or Kubernetes requirement |
| Logical planes | Control Plane, Execution Plane, Data Plane | Boundaries are enforced even when deployed together |
| Contracts | Canonical capability manifest and versioned API/event contracts | Published contract changes require compatibility assessment |
| Artifacts | Immutable published versions with digest/provenance | New content creates a new version; no silent mutation |
| Security | Zero Trust, least privilege, tenant isolation | Authorization is evaluated on every invocation |
| Marketplace | Governed discovery and entitlement | Listing visibility never grants execution authorization |

## 7. Target users and primary use cases

### 7.1 Target user groups

- **Capability developers and publishers:** create, package, describe, version, and distribute capabilities.
- **Organizations and platform operators:** govern identities, policies, connectors, runtime, and synchronization.
- **AI platform integrators:** connect compatible client environments through MCP, REST, SDKs, or supported adapters.
- **Capability consumers:** discover and invoke capabilities they are authorized to use.
- **Security and governance reviewers:** evaluate provenance, permissions, evidence, policy, and operational risk.
- **Marketplace participants:** publish, license, obtain, and consume externally supplied capabilities after marketplace launch.

### 7.2 Primary use cases

1. Register a capability with a stable ID, publisher, manifest, version, dependencies, permissions, and provenance.
2. Validate and publish an immutable capability artifact.
3. Discover a capability according to tenant, visibility, and entitlement.
4. Invoke a permitted capability through REST or Remote MCP.
5. Execute it in a constrained runtime.
6. Trace the invocation and inspect evaluation and audit evidence.
7. publish a compatible update and synchronize it under release policy.
8. Block a high-risk or incompatible update pending required evaluation and approval.
9. Roll back a failed deployment to a known-good artifact.
10. Connect a self-hosted runtime without granting it broad administrative access.
11. Onboard an external publisher under explicit identity, licensing, and security requirements.

## 8. Scope

### 8.1 MVP scope

The MVP is the smallest complete proof of HSMART's core infrastructure lifecycle.

**Included:**

- A canonical capability manifest and validation rules.
- Stable capability identity and publisher identity.
- Registry registration, discovery, and immutable version metadata.
- Artifact metadata, digest, and provenance representation.
- Basic authentication and authorization policy enforcement.
- API key lifecycle minimum and OIDC integration path.
- REST invocation and Remote MCP invocation through a shared policy core.
- Managed execution of a deterministic demonstration capability.
- Tenant context and enforceable resource limits.
- Invocation result and lifecycle contracts.
- Basic evaluation gate and evidence linked to artifact version/digest.
- Structured logs, correlation, traceability, and security audit events.
- A minimal risk-aware synchronization path, including approval behavior and rollback.
- Negative tests for unauthorized access, invalid manifest, failure, and policy denial.

**First demonstration capability:**

\`hsmart:demo:text-transformer\`

This deterministic demonstration capability exists to prove registration, authorization, execution, and lifecycle infrastructure. It is not intended to demonstrate advanced AI intelligence.

### 8.2 Post-MVP scope

These areas are part of the broader HSMART direction but must follow the MVP proof:

- A.S.F.R.E.E Canonical integration as a first-party evaluation capability.
- A.S.F.R.E.E Legacy through an explicit compatibility adapter.
- Skill Analyzer integration.
- Anatomi Prompt v3 / Octa-Prompt integration.
- Self-hosted runtime agent and enrollment.
- SDKs and additional client/platform adapters.
- Full adaptive synchronization and expanded risk policy.
- External publisher onboarding and marketplace.
- Usage metering, billing, and commercial settlement.
- Multi-region, advanced resilience, and enterprise-scale operations.

### 8.3 Explicit non-goals for MVP

- Building all twelve domains as separately deployed microservices.
- Making Kubernetes a prerequisite.
- Supporting every AI platform or client from the first release.
- Building a full marketplace and payment settlement before core entitlement and authorization work.
- Migrating all planned skill records directly into a published state.
- Autonomous self-modification or unrestricted self-healing in production.
- Multi-region active-active architecture without a demonstrated requirement.
- Guaranteeing the quality or safety of outputs generated by external AI models.
- Building a general-purpose model hosting platform.

## 9. First-party ecosystem integration policy

The following capabilities are intended to be integrated into the HSMART ecosystem through the same canonical registry, access, execution, evaluation, and synchronization governance.

| Capability | Integration policy |
|---|---|
| A.S.F.R.E.E Canonical | Preferred first-party evaluation integration; preserve its independent product identity |
| A.S.F.R.E.E Legacy | Compatibility adapter with explicit behavior and deprecation policy; never silently substitute it for Canonical |
| Skill Analyzer | Register as a capability with declared input/output, dependencies, permissions, and versioned evaluation evidence |
| Anatomi Prompt v3 / Octa-Prompt | Register as a capability with explicit contract, version, and execution policy |
| Universal AI Invocation Gateway | Consolidate gateway responsibilities into HSMART Access, Distribution, and Orchestration domains; avoid a competing duplicate control plane |

Any planned bulk migration, including the previously discussed inventory of 427 candidate Skill Registry Records, must begin with source verification, provenance capture, duplicate resolution, schema validation, and staging. The stated count is a planning input, not a verified count of valid, publishable records.

## 10. Delivery strategy and stage gates

The implementation follows the HSMART KM 0–10 roadmap in \`docs/roadmap/IMPLEMENTATION-ROADMAP.md\`.

| Stage | Objective | Minimum exit evidence |
|---|---|---|
| KM 0 | Governance and project foundation | Charter adopted, accountable roles assigned, MVP and metrics approved |
| KM 1 | Technical foundation and canonical contract | Reproducible development environment, approved stack decisions, contract tests |
| KM 2 | Universal Registry | Registration, validation, versioning, discovery, and audit tests |
| KM 3 | Access and Distribution | OIDC/policy path, API key lifecycle, REST/MCP authorization tests |
| KM 4 | Managed Execution | Isolated execution, resource controls, failure and cancellation tests |
| KM 5 | Evaluation and Observability | Traceable invocations, evaluation evidence, operational signals |
| KM 6 | Adaptive Synchronization | Desired/observed reconciliation, staged rollout, approval, rollback |
| KM 7 | First-party integrations | At least one first-party capability completes the governed lifecycle |
| KM 8 | Hybrid and cross-platform | Managed and self-hosted contract compatibility; independent client-path tests |
| KM 9 | Publisher and Marketplace | Verified publisher, licensing/entitlement, moderation, and invocation enforcement |
| KM 10 | Production hardening | Security, resilience, restore, operational and governance readiness approvals |

A stage is not complete because its planned duration elapsed. It is complete only when its exit evidence has been reviewed and accepted.

## 11. Delivery principles

1. **Prove the lifecycle before multiplying features.** Build one complete path end to end.
2. **Contracts before integrations.** Stable manifests, APIs, events, and versioning precede broad adapters.
3. **Security is part of the design.** Do not postpone identity, tenant isolation, secret handling, and egress controls until after functionality.
4. **Evidence over assertion.** A feature is complete only with implementation, tests, review, and operational evidence.
5. **Modular before distributed.** Keep deployable complexity proportional to team size and demonstrated need.
6. **Immutable release history.** Published artifacts and versions must be reproducible and traceable.
7. **Fail safely.** Denial, quarantine, cancellation, rollback, and recovery paths are first-class behavior.
8. **Interoperate without pretending universality.** Declare and test supported protocols and clients; never infer compatibility from naming alone.
9. **Human approval for consequential changes.** High-risk, breaking, security-sensitive, and commercial-policy changes require designated authorization.
10. **No hidden privilege.** Runtime enrollment, marketplace listing, connector registration, or repository publication must not grant unrelated access.

## 12. Architecture and engineering constraints

### 12.1 System structure

- Maintain logical separation between Control Plane, Execution Plane, and Data Plane.
- Begin with a modular monolith and separable background workers.
- Enforce domain boundaries in code and contracts.
- Extract independent services only when operational scale, isolation, team ownership, or release independence makes the trade-off worthwhile.
- Keep provider-specific integrations behind explicit adapters.

### 12.2 Contracts and versioning

- Use a canonical, machine-readable capability manifest.
- Every capability must have a stable identity and explicit publisher namespace.
- Use semantic versioning where it accurately represents compatibility; document any domain-specific version behavior.
- Treat published versions as immutable.
- Bind evaluation and provenance evidence to artifact digest and version.
- Version APIs and event envelopes independently from internal implementation.
- Define backward compatibility and deprecation rules before broad distribution.

### 12.3 Access and trust

- Use workload and user identity appropriate to each interaction.
- Enforce least privilege and tenant isolation.
- Evaluate permission on each invocation; a valid credential alone is not sufficient.
- Keep secrets in a managed secret store or KMS-backed vault design; never commit secrets or expose them in logs.
- Treat external MCP servers, REST APIs, and imported artifacts as untrusted until verified and explicitly permitted.
- Apply outbound network restrictions and SSRF controls to connectors and execution workers.
- Verify artifact digest and signature/provenance before trusted execution.

### 12.4 Synchronization

- Reconcile desired state with observed state.
- Make synchronization operations idempotent and retry-safe.
- Classify changes by risk and bind risk class to test, approval, rollout, and rollback policy.
- Require approval for breaking, high-risk, security-sensitive, or policy-sensitive changes.
- Preserve a known-good version and auditable rollback evidence.
- Do not assume HSMART can force an independently managed client to refresh a changed tool manifest.

### 12.5 Data and privacy

- Define data ownership, purpose, access, retention, deletion, and export for each data category.
- Minimize collection of consumer payloads and credentials.
- Separate audit metadata from sensitive application payloads where practical.
- Define tenant boundaries at identity, API, persistence, cache, queue, storage, and runtime layers.
- Establish data-processing agreements before handling third-party personal or regulated data in commercial operation.

## 13. Governance and decision rights

### 13.1 Required accountable roles

The project is currently founder-led and has no legal-entity structure. GOV-01 is recorded through a founder self-declaration for internal project governance only. This does not appoint the remaining roles or create authority over third parties.

| Role | Accountability | Current status |
|---|---|---|
| Project Sponsor / Accountable Owner | Strategic direction, internal project scope, priorities, and stewardship of resources actually controlled by the holder | Appointed: Harysaidno — HSMART-GOV-FOUNDER-001; internal project authority only |
| Project Owner | Overall delivery accountability and charter maintenance | To appoint |
| Product Owner | User needs, priorities, acceptance, roadmap trade-offs | To appoint |
| Architecture Lead | Architecture integrity, contracts, ADRs, technical boundaries | To appoint |
| Engineering Lead | Implementation quality, delivery planning, code review | To appoint |
| Security & Privacy Lead | Threat model, security requirements, risk acceptance | To appoint |
| Operations / Reliability Lead | Deployment, monitoring, backup, incident and recovery readiness | To appoint |
| Legal / Commercial Advisor | Entity, IP, licensing, publisher, privacy, and commerce review | To appoint / engage when needed |
| Capability Publisher Owner | Accuracy and lifecycle of each published capability | Per publisher |

In an early single-person or small-team phase, one person may hold multiple roles. The responsibilities must still be explicitly assigned. High-impact security, production, data-destruction, and commercial decisions should receive independent review wherever practical.

### 13.2 Decision classes

| Class | Examples | Required control |
|---|---|---|
| D0 — Editorial | Typo, formatting, non-normative clarification | Maintainer review |
| D1 — Component | Internal implementation detail within approved contracts | Component owner review and tests |
| D2 — Architecture | Domain boundary, canonical schema, protocol, major dependency, data model | ADR, architecture review, compatibility assessment, and approval within recorded internal project authority |
| D3 — Critical | Security boundary, privilege model, production release, data retention, legal/commercial policy | Named accountable approval, documented risk review, and independent review where practical; external legal/commercial commitments require the legally authorized person/entity |

### 13.3 Change control

- Normative architecture or contract changes require an ADR.
- Changes to published contracts require compatibility and migration analysis.
- Security-policy changes require tests for both allowed and denied behavior.
- Changes affecting data ownership, privacy, licensing, or commercial rights require the appropriate legal/governance review.
- Breaking changes require a versioning, deprecation, migration, and rollback plan.
- Decisions must be recorded in the repository so they survive personnel and platform changes.

## 14. Success measures and acceptance metrics

The MVP is judged by whether the critical lifecycle works correctly and can be demonstrated repeatedly.

| Dimension | Initial success measure | Evidence |
|---|---|---|
| Contract integrity | All required manifest validation cases produce deterministic pass/fail outcomes | Contract test report |
| Identity | No duplicate active capability identity within its defined namespace | Registry tests and data constraints |
| Artifact integrity | Every published version is tied to a stable digest and immutable record | Artifact verification tests |
| Authorization | All defined positive and negative authorization cases pass | Policy test matrix |
| Tenant isolation | Cross-tenant access tests are denied at all applicable boundaries | Isolation test report |
| Execution | Demo capability runs under configured resource and execution limits | Runtime test report |
| Traceability | Every security-sensitive invocation and lifecycle action has a correlated audit record | Audit completeness test |
| Evaluation | Release decision references version-specific evaluation evidence | Evaluation records |
| Synchronization | Compatible update, gated risky update, failed rollout, and rollback are demonstrated | Synchronization test report |
| Reliability | Failure, timeout, cancellation, and recovery behavior are exercised | Fault and recovery test report |
| Operations | Logs, metrics, traces, alerts, and runbooks cover the MVP path | Operations review |

**Metrics intentionally not fixed yet:** production availability SLO, latency SLO, throughput, cloud cost per invocation, RPO, and RTO. These depend on expected workload, architecture, provider, deployment region, budget, and customer commitments. They must be baselined and approved before production launch rather than invented at charter time.

### 14.1 Business and ecosystem measures

After MVP, establish measurable targets for:

- Number of verified first-party capabilities.
- Time to onboard and validate a capability.
- Number of supported client paths with passing conformance tests.
- Capability invocation volume and successful completion rate.
- Publisher onboarding and retention.
- Consumer adoption and repeat usage.
- Marketplace conversion, revenue, refund, and dispute rates when commerce launches.
- Security incidents, abuse reports, quarantine time, and remediation time.

Targets must be set after initial usage and cost baselines exist.

## 15. Initial risks and mitigations

| Risk | Consequence | Required mitigation |
|---|---|---|
| Scope expansion before vertical slice | Long build with no proven end-to-end value | Enforce MVP boundary and stage gates |
| Unassigned decision owners | Delayed decisions and inconsistent implementation | Appoint accountable roles at KM 0 |
| Premature microservices | Operational overhead and fragmented contracts | Start modular monolith; extract only with evidence |
| Weak tenant or authorization boundaries | Cross-tenant exposure or privilege abuse | Threat model, negative tests, independent security review |
| Untrusted connector or artifact | SSRF, data exfiltration, code execution, supply-chain compromise | Quarantine, egress policy, sandboxing, digest/signature verification |
| Ambiguous IP and ownership | Disputes, takedowns, inability to commercialize | Legal review and explicit contributor/publisher agreements |
| Marketplace launched too early | Fraud, licensing, safety, billing, and support exposure | Defer until entitlement, moderation, and legal gates pass |
| Imported registry data treated as trusted | Invalid, duplicated, or unsafe capabilities published | Staging, provenance validation, duplicate resolution, approval |
| Provider lock-in | High migration cost and reduced interoperability | Adapter boundaries, portable contracts, documented exit strategy |
| Automated synchronization causes blast radius | Broken or unsafe deployment across clients | Risk classes, canary, approval, rollback, bounded rollout |
| Observability leaks sensitive data | Privacy or credential exposure | Data minimization, redaction, access controls, retention policy |
| Planning estimates mistaken for commitments | Unrealistic delivery expectations | Reforecast from capacity and measured engineering work |

## 16. Assumptions and external dependencies

The project plan assumes:

- The repository remains the authoritative source for normative project documentation and implementation history.
- A project owner and technical decision-makers will be appointed.
- A small, focused first vertical slice is more valuable than broad incomplete coverage.
- Managed execution can be proven before self-hosted fleet management is attempted.
- External provider and platform interfaces may change and require adapter maintenance.
- Third-party capabilities will require explicit licenses, publisher identity, and permission declarations.
- Cloud provider, region, identity issuer, secret manager/KMS, artifact storage, and operational budget will be selected before hosted implementation.
- Commercial operation requires legal and tax review in the relevant jurisdictions.
- Any proposed migration inventory must be confirmed from source data before scope or delivery targets are fixed.

## 17. Resource and funding principles

No budget, funding commitment, staffing capacity, cloud spend, or commercial runway is asserted by this charter.

Before infrastructure procurement or paid external commitments, the Project Owner must prepare a resource plan covering:

- Team capacity and required competencies.
- Development, test, staging, and production environments.
- Cloud compute, database, cache, queue, storage, network egress, and observability costs.
- Identity, KMS/secret-management, security scanning, and artifact-signing services.
- Legal, privacy, tax, licensing, and commercial support.
- Contingency for security remediation and operational incidents.

Prefer low-cost, reversible technical choices during the proof stage, but do not compromise security boundaries to save nominal infrastructure cost.

## 18. Communications and project records

- Repository issues are the authoritative work backlog once established.
- Pull requests are the authoritative implementation review record.
- ADRs are the authoritative architecture decision record.
- The risk register records unresolved project and delivery risks.
- Release notes record externally relevant behavior and compatibility changes.
- Security-sensitive incident details must be handled in an access-controlled channel; do not put secrets or exploit-enabling details in public issues.
- Project status must distinguish **planned**, **specified**, **implemented**, **tested**, **deployed**, and **production-approved** states.

## 19. Definition of done

A project deliverable is complete only when all applicable conditions are met:

1. The requirement, intended behavior, and non-goals are documented.
2. Implementation follows approved architecture and contracts.
3. Positive, negative, failure, and security-relevant tests pass.
4. Access, tenant, privacy, and data-handling behavior is verified.
5. Logs, metrics, traces, audit, and failure handling are implemented as required.
6. Operations and rollback instructions exist where the component can be operated.
7. A reviewer with appropriate accountability accepts the change.
8. Evidence is linked to the issue, pull request, and relevant release.
9. Documentation accurately reflects what is implemented; no planned capability is described as live.

## 20. Approval, adoption, and amendment

### 20.1 Adoption requirements

This charter becomes the adopted project governance baseline when all of the following are true:

- The Project Sponsor / Accountable Owner is explicitly appointed.
- The Project Owner and initial Product, Architecture, Engineering, and Security accountabilities are assigned.
- The MVP boundary and initial success measures are accepted.
- The document is approved through the repository's review and merge process.
- Any material legal or commercial assumption is marked as pending until reviewed by a qualified advisor.

The repository merge records adoption of this project baseline. It does **not** create a legal entity, transfer intellectual property, execute a publisher agreement, establish a Foundation, or authorize commercial activity.

### 20.2 Ratification record

| Approval role | Name / authority | Decision | Date |
|---|---|---|---|
| Project Sponsor / Accountable Owner | Harysaidno — GOV-01; HSMART-GOV-FOUNDER-001, internal project authority only | Appointment recorded; Charter ratification pending | 2026-11-22 |
| Project Owner | To be appointed | Pending | Pending |
| Product Owner | To be appointed | Pending | Pending |
| Architecture Lead | To be appointed | Pending | Pending |
| Security & Privacy Lead | To be appointed | Pending | Pending |

### 20.3 Amendment policy

- Minor editorial amendments may be made through normal review.
- Scope, decision-right, MVP, or success-metric changes require Project Owner and Product Owner review.
- Normative architecture, security, data, or protocol changes require the appropriate ADR and accountable technical/security review.
- Legal, ownership, and commercial changes require qualified legal/governance review.
- Every approved amendment increments the document version and records its rationale.

---

## 21. Immediate actions after charter adoption

The next execution sequence is:

1. GOV-01 is appointed for internal project governance; appoint the Project Owner (GOV-02).
2. Assign the initial Product, Architecture, Engineering, and Security responsibilities.
3. Approve the MVP demo capability and its acceptance tests.
4. Open and prioritize KM 0–2 backlog issues with dependencies and owners.
5. Finalize initial technology and infrastructure ADRs.
6. Establish reproducible local development and CI.
7. Begin Registry implementation only after the KM 1 exit gate is satisfied.

**Project control statement:** HSMART will be measured by verified capability lifecycle outcomes, security, interoperability, and operational evidence—not by the number of modules, diagrams, integrations, or documents produced.
