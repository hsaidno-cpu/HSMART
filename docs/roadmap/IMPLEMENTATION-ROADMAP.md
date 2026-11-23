## Current execution snapshot — 23 November 2026

- PR #13 merged; GOV-01 MVP/Charter decisions are canonical on main (`17c78dcd2ea59c6d40f9a07d188bab6f829f0596`).
- GOV-01 is the only human internal authority; GOV-02..GOV-12 are AI Functional Delegates designated but all runtimes remain NOT_PROVISIONED / NOT_ACTIVE.
- GOV-07 role allocation is resolved as an AI delegate; production operations controls remain unprovisioned.
- ADR-011 v1.2.0 accepted by GOV-01; acceptance is not production procurement approval.
- PR #28 contains the KM 1 app foundation. Contract/OpenAPI, PostgreSQL 16 integration and repository governance CI passed on the inspected PR head; the AI Reviewer Evidence gate awaits a report-only commit.
- Main is still unprotected. Desired controls and local admin bootstrap are in `docs/governance/REPOSITORY-BASELINE-CONTROLS.md`; apply and read back with repository Administration: write privileges before merging.
- KM 0 OPEN; KM 1 IN PROGRESS; KM 2+ blocked until the exact KM 1 exit decision.
- No Registry/Gateway/managed Runtime/Evaluation/Synchronization service, production deployment, WORM audit store, disaster recovery exercise or production security certification is evidenced.
- Indonesian legal basis is mapped in `docs/legal/INDONESIA-LEGAL-BASIS-AND-ENTITY-BOUNDARIES.md`; it is not a legal opinion or formation/registration evidence.

# HSMART Execution Roadmap

**Document status:** Execution planning baseline  
**Applies to:** HSMART Universal AI Ecosystem Infrastructure Platform  
**Roadmap model:** Stage-gated, dependency-driven, evidence-based  
**Planning note:** Duration ranges are estimates, not delivery commitments. Reforecast after team capacity, cloud choices, legal structure, and technical spike results are known.

---

## 1. Purpose

This roadmap translates the approved HSMART architecture baseline into an executable sequence. It defines what to build first, what depends on what, what evidence is required to move forward, and what must deliberately remain out of scope until the platform has earned the complexity.

The objective is not to implement all twelve domains simultaneously. The objective is to prove one complete, secure, observable capability lifecycle, then expand that proven path.

## 2. Current baseline and starting position (historical; see current execution snapshot below)

The architecture baseline has been merged into \`main\` through PR #1. It includes the master architecture, domain boundaries, ADRs, access-management design, contracts, security baseline, runtime and synchronization specifications, governance, and an initial implementation roadmap.

This is a documentation and contract baseline. It does **not** mean that HSMART has a deployed runtime, production database, identity provider, cloud environment, marketplace, or working execution gateway.

### Starting status

| Area | Status |
|---|---|
| Strategic direction | Defined |
| Architecture baseline | Merged into \`main\` |
| Domain boundaries and ADRs | Documented |
| Canonical manifest and API contracts | Initial specifications exist |
| CI structural validation | Initial workflow exists |
| Project Charter and accountable owners | Charter baseline merged; formal ratification and owner appointments pending |
| Technology and infrastructure decisions | To be finalized through ADRs |
| Runtime, registry, gateway, synchronization services | Not implemented |
| Production and legal operating model | Not approved / not established |

The next action is therefore KM 0: establish execution governance and measurable acceptance criteria.

### Verified execution snapshot — 22 November 2026

The canonical repository snapshot inspected for this control plan is main @ e796b5842f98277716fc5d81026ac175d0591f36. The current verified stage state is recorded in [PROGRESSIVE-COMPLETION-ROADMAP.md](../planning/PROGRESSIVE-COMPLETION-ROADMAP.md).

- KM 0 remains OPEN. GOV-01's MVP/Charter decisions are recorded in PR #13 but are not yet canonical on main.
- KM 1 is PARTIAL: contract schemas, fixtures and cross-platform contract CI exist; ADR-011 remains a recommendation and the full application environment is not yet delivered.
- KM 2–KM 8 application services are NOT STARTED on the inspected main baseline.
- KM 9 is DEFERRED; KM 10 is NOT STARTED.
- The main branch was observed unprotected. The required repository controls are specified in [REPOSITORY-BASELINE-CONTROLS.md](../governance/REPOSITORY-BASELINE-CONTROLS.md), but have not been applied or verified.
- The local policy reference evaluator is not a deployed authorization gateway; no production WORM storage or hosted delegate runtime is evidenced.

Reconcile this snapshot after PR #13 and the next accepted changes merge. Never infer deployment or stage completion from documentation or CI alone.


## 3. Executive roadmap map

\`\`\`mermaid
flowchart TD
    K0["KM 0 · Governance & Project Foundation"]
    K1["KM 1 · Technical Foundation & Canonical Contract"]
    K2["KM 2 · Universal Capability Registry"]
    K3["KM 3 · Identity, Access & Distribution Gateway"]
    K4["KM 4 · Managed Execution Runtime"]
    K5["KM 5 · Evaluation & Observability"]
    K6["KM 6 · Adaptive Synchronization"]
    K7["KM 7 · First-Party Ecosystem Integration"]
    K8["KM 8 · Self-Hosted & Cross-Platform Distribution"]
    K9["KM 9 · Publisher & Marketplace"]
    K10["KM 10 · Production Hardening & Scale"]

    K0 --> K1 --> K2 --> K3 --> K4 --> K5 --> K6
    K5 --> K7 --> K8 --> K9 --> K10
    K6 --> K8
    K5 --> K9

    K10 --> DONE["HSMART · Operable Universal AI Ecosystem Infrastructure"]
\`\`\`

The main path is sequential where contracts and runtime dependencies require it. Work such as legal review, threat modeling, documentation, and platform research can run in parallel, but parallel activity must not bypass stage gates.

## 4. Kilometer-by-kilometer plan

### KM 0 — Governance and project foundation

**Planning range:** 1–2 weeks

**Objective:** Turn the architecture vision into an owned project with boundaries, decision rights, measurable outcomes, and a controlled backlog.

**Work**
- Formally ratify the merged HSMART Project Charter and record the adoption decision.
- Define the initial target users, primary use cases, non-goals, and MVP boundary.
- Assign accountable owners for product, architecture, platform, security, and operations. One person may cover multiple roles initially, but accountability must remain explicit.
- Define decision rights for the Foundation and Commercial Operator model.
- Record unresolved legal and commercial questions: entity structure, IP assignment, trademark, publisher terms, contribution terms, data roles, and licensing.
- Establish the decision log, risk register, change-control rules, and backlog workflow.
- Define product success metrics and engineering quality gates.

**Deliverables**
- \`docs/foundation/HSMART-PROJECT-CHARTER.md\`
- Named owner/role matrix
- Initial product requirements and non-goals
- Prioritized MVP backlog
- Risk and decision registers

**Exit gate**
- A project owner approves scope, accountability, success criteria, and the first vertical slice.
- No critical architecture or governance decision is left without an owner and due condition.

### KM 1 — Technical foundation and canonical contract

**Planning range:** 2–3 weeks

**Objective:** Make the repository and local development system reproducible before implementing business capabilities.

**Work**
- Finalize stack choices through ADRs, not preference alone. Benchmark Python/FastAPI against TypeScript only where there is a concrete reason.
- Establish local development, configuration management, secrets handling, CI, linting, type checks, and automated tests.
- Define PostgreSQL migration policy and a reproducible developer database.
- Confirm the canonical capability manifest, identity rules, semantic-version rules, artifact digest, provenance, permission declarations, and compatibility metadata.
- Define API and event versioning, error envelopes, idempotency rules, correlation IDs, and pagination.
- Create an architecture fitness test for prohibited dependencies and domain boundaries.

**Deliverables**
- Approved implementation-stack ADRs
- Local development setup and CI baseline
- Versioned manifest and event contracts
- API conventions and contract-test harness
- Initial threat-model review for the MVP

**Exit gate**
- A new contributor can build and run the project from documented instructions.
- Contracts validate automatically and have positive and negative test fixtures.
- No secret is committed to source control.

### KM 2 — Universal Capability Registry

**Planning range:** 3–4 weeks

**Objective:** Establish the authoritative identity and metadata source for every capability.

**Work**
- Implement stable capability IDs and publisher namespaces.
- Implement manifest validation and schema-version compatibility.
- Implement immutable published versions and mutable draft records.
- Store artifact metadata, digest, provenance, dependencies, and visibility policy.
- Implement registration, validation, version listing, discovery, and lifecycle state.
- Add audit events for registration and publication.
- Create a staging/import process for bulk migration; never auto-publish unverified imported records.

**Deliverables**
- Registry API and persistence layer
- Manifest validation service
- Capability/version lifecycle
- Discovery endpoints
- Import staging report and rejection reasons

**Exit gate**
- A capability can be registered, validated, discovered, and versioned.
- Duplicate identities and invalid manifests are rejected deterministically.
- Published versions cannot be silently mutated.
- Registry operations produce traceable audit records.

### KM 3 — Identity, access, and distribution gateway

**Planning range:** 3–5 weeks

**Objective:** Ensure every invocation is authenticated, authorized, rate-controlled, and attributable.

**Work**
- Integrate an OIDC issuer for human and service identities.
- Implement tenant and publisher identity boundaries.
- Implement API key lifecycle: generate, validate, scope, rotate, revoke, and audit.
- Implement policy evaluation for identity, capability, operation, tenant, quota, and entitlement.
- Implement REST/HTTP invocation and a Remote MCP server against the same authorization core.
- Add request validation, rate limiting, abuse protection, audit correlation, and error normalization.
- Implement secure connector registration with outbound network controls, SSRF defenses, and credential isolation.

**Universal Access Manager implementation order**
1. \`identity-policy-engine\` — common identity, scope, permission, and quota decisions.
2. \`api-key-manager\` — machine credential lifecycle.
3. \`credential-vault\` — secure storage and controlled retrieval through a managed secret service or KMS-backed design.
4. \`mcp-access-manager\` — MCP authentication and authorization.
5. \`custom-api-connector\` — governed external REST/HTTP connectivity.
6. \`custom-mcp-connector\` — governed external MCP connectivity.

The six subskills are logical modules under one \`universal-access-manager\`; they do not need six independent deployed services in the MVP.

**Deliverables**
- OIDC integration
- Shared authorization policy interface
- API key management
- REST and Remote MCP endpoints
- Connector registration controls
- Positive and negative authorization test suite

**Exit gate**
- Authorized clients can invoke only permitted operations.
- Unauthorized, expired, revoked, cross-tenant, and over-quota requests are denied.
- REST and MCP enforce equivalent policy decisions.
- Credentials are not exposed in logs or API responses.

### KM 4 — Managed execution runtime

**Planning range:** 3–5 weeks

**Objective:** Execute a registered capability under controlled and observable resource boundaries.

**Work**
- Implement invocation lifecycle and execution job state.
- Implement worker and queue management.
- Establish isolated execution boundaries appropriate to the selected workload model.
- Enforce time, memory, CPU, concurrency, payload, and network egress limits.
- Add cancellation, timeout, retry, idempotency, and quarantine behavior.
- Bind execution to immutable capability version, tenant, publisher, and invocation identity.
- Emit structured execution events and trace context.
- Start with managed cloud execution only; defer fleet-scale self-hosted runtime.

**Deliverables**
- Managed worker runtime
- Invocation and result contract
- Resource policy enforcement
- Job state and failure handling
- Runtime integration tests

**Exit gate**
- A registered demo capability executes in an isolated worker.
- The result is associated with the exact artifact digest and version.
- Timeout, cancellation, resource exhaustion, and denied egress behave as designed.
- A failed workload cannot compromise another tenant's execution context.

### KM 5 — Evaluation, assurance, and observability

**Planning range:** 2–3 weeks

**Objective:** Make execution and release decisions evidence-based rather than dependent on a green HTTP response.

**Work**
- Implement structured logs, metrics, distributed traces, and audit correlation.
- Define service-level indicators for availability, latency, failure rate, queue delay, and execution cost.
- Implement contract, regression, compatibility, and basic security checks.
- Define evaluation results as versioned evidence linked to artifact digest.
- Add release gates and policy for missing, stale, or failed evaluation evidence.
- Create dashboards and operational alerts for the vertical slice.

**Deliverables**
- Observability baseline
- Evaluation runner and evidence record
- Quality gate policy
- Initial operational dashboard and alerts
- Test reports linked to capability versions

**Exit gate**
- Each invocation can be traced from client request through authorization, scheduling, execution, and result.
- A capability release cannot pass the defined quality gate without required evidence.
- Failures are diagnosable without leaking credentials or sensitive payloads.

### KM 6 — Adaptive synchronization

**Planning range:** 4–6 weeks

**Objective:** Reconcile desired capability state with observed runtime state using risk-aware rollout decisions.

**Work**
- Define desired and observed state models.
- Implement reconciliation loops with idempotent operations.
- Classify changes by risk (R0–R5) and map risk to approval, testing, rollout, and rollback policy.
- Check dependencies, compatibility, permissions, and target runtime capability.
- Implement staged rollout and canary controls.
- Implement rollback to a known-good immutable artifact.
- Store complete synchronization and approval evidence.
- Prevent a marketplace listing or registry update from implicitly authorizing deployment.

**Deliverables**
- Synchronization controller
- Risk policy matrix
- Desired/observed state store
- Staged rollout and rollback workflow
- Synchronization audit timeline

**Exit gate**
- A compatible low-risk release propagates automatically within policy.
- A breaking or high-risk change is blocked pending required evaluation and approval.
- A failed rollout returns to a known-good state.
- Reconciliation is safe to retry and does not create duplicate or divergent operations.

### KM 7 — First-party ecosystem integration

**Planning range:** 2–4 weeks after KM 3–6 interfaces stabilize

**Objective:** Prove that HSMART can govern real internal capabilities through one universal contract.

**Integration sequence**
1. \`A.S.F.R.E.E Canonical\` as the first-party evaluation capability.
2. \`A.S.F.R.E.E Legacy\` through an explicit compatibility adapter, never by silently replacing Canonical.
3. \`Skill Analyzer\` as a capability with declared inputs, outputs, execution policy, and evidence.
4. \`Anatomi Prompt v3 / Octa-Prompt\` as a capability with explicit contract and versioning.
5. Consolidate the prior Universal AI Invocation Gateway responsibilities into HSMART's Access, Distribution, and Orchestration domains rather than creating a competing second gateway.

**Deliverables**
- First-party publisher records
- Integration adapters where needed
- Compatibility and regression suites
- Version and dependency declarations
- Migration and rollback plan for each integration

**Exit gate**
- At least one first-party capability completes the entire register → authorize → invoke → execute → evaluate → synchronize lifecycle.
- Legacy compatibility behavior is explicit and testable.
- No integrated product bypasses HSMART authorization or audit controls.

### KM 8 — Self-hosted runtime and cross-platform distribution

**Planning range:** 4–6 weeks

**Objective:** Extend the same capability contract across managed and customer-controlled environments.

**Work**
- Design runtime enrollment and revocation.
- Use workload identity and signed deployment intent.
- Verify artifact digest and signature before execution.
- Implement a self-hosted runtime agent with least privilege and explicit outbound connectivity.
- Publish stable SDKs and client examples for supported languages.
- Add platform adapters based on verified platform capabilities; do not promise universal support based only on protocol similarity.
- Test interoperability with at least two independent client implementations.

**Deliverables**
- Self-hosted runtime agent
- Runtime enrollment and trust workflow
- SDK and integration examples
- Adapter compatibility matrix
- Hybrid deployment integration tests

**Exit gate**
- The same capability contract works in managed and self-hosted execution.
- A compromised or revoked runtime identity cannot continue authorized operations.
- Artifact integrity and policy decisions are independently verified by the target runtime.
- At least two independent client paths pass end-to-end tests.

### KM 9 — Publisher ecosystem and marketplace

**Planning range:** 4–6 weeks

**Objective:** Open controlled publishing and consumption to external organizations.

**Work**
- Implement publisher onboarding and identity verification.
- Define listing lifecycle, review state, category, metadata, and permission disclosure.
- Implement license, entitlement, subscription or purchase rights, and usage metering.
- Enforce authorization at invocation time independently from marketplace visibility.
- Establish quarantine, takedown, dispute, appeal, and publisher suspension workflows.
- Complete legal review of publisher terms, consumer terms, licenses, IP, data processing, and commercial operator responsibilities.
- Integrate payments only after legal, tax, fraud, refund, and settlement requirements are approved.

**Deliverables**
- Publisher portal and lifecycle
- Marketplace listing and discovery
- Entitlement and usage accounting
- Moderation and incident workflows
- Approved commercial and legal operating policies

**Exit gate**
- An external publisher can submit and maintain a capability under verified identity.
- Consumers can invoke only when identity, policy, license, entitlement, and capability permissions all allow it.
- Quarantined, revoked, or non-compliant capabilities cannot execute.
- Usage and commercial records are auditable.

### KM 10 — Production hardening and scale

**Planning range:** 3–5 weeks, followed by continuous operations

**Objective:** Demonstrate that the platform can be operated safely, recovered reliably, and scaled based on evidence.

**Work**
- Complete independent security review and remediate findings.
- Run load, soak, resilience, fault-injection, and tenant-isolation tests.
- Establish backup, restore, disaster recovery, and data-retention procedures.
- Define SLOs, error budgets, incident severity, on-call ownership, and escalation.
- Establish vulnerability management, dependency scanning, SBOM, artifact signing, provenance verification, and patch policy.
- Add deployment controls, environment separation, change approvals, and rollback.
- Conduct production-readiness review with engineering, security, operations, and governance owners.

**Deliverables**
- Security assessment and remediation report
- Load and resilience test report
- Backup/restore and disaster-recovery evidence
- Incident and operational runbooks
- Production readiness decision

**Exit gate**
- Critical security findings are closed or formally risk-accepted by authorized owners.
- Restore and disaster-recovery exercises meet documented recovery objectives.
- SLOs, monitoring, and incident ownership are operational.
- Production launch is explicitly approved; passing CI alone is insufficient.

## 5. MVP vertical slice: the first proof that HSMART works

Do not start by integrating every internal product. Start with one deterministic demonstration capability:

\`hsmart:demo:text-transformer\`

It should perform a small, predictable transformation. Its purpose is to prove the platform lifecycle, not showcase sophisticated AI.

**Required end-to-end path**
1. Register publisher and capability identity.
2. Validate the canonical manifest.
3. Store an immutable artifact and verify digest/signature.
4. Publish a versioned capability.
5. Discover it through the Registry.
6. Authenticate and authorize a client.
7. Invoke through REST and Remote MCP.
8. Execute in the managed isolated runtime.
9. Record traces, metrics, audit, and evaluation evidence.
10. Publish a compatible patch version.
11. Reconcile a target runtime through synchronization.
12. Demonstrate denied access, failed rollout, rollback, and audit reconstruction.

**MVP acceptance tests**
- Valid registration succeeds; malformed or conflicting registration fails.
- Published versions are immutable.
- Expired, revoked, unauthorized, cross-tenant, and over-quota invocations fail.
- REST and MCP apply equivalent authorization.
- Execution respects resource and egress controls.
- Evaluation evidence is linked to the immutable artifact digest.
- A compatible update rolls out according to policy.
- A high-risk update requires approval.
- A failed rollout restores the known-good version.
- All significant actions are attributable in the audit trail.

A successful demo is not production readiness. The MVP proves the architecture's critical path; production readiness is a later, separately gated achievement.

## 6. Mapping the 12 HSMART domains to the roadmap

| Domain | Primary implementation window | Notes |
|---|---|---|
| D01 Studio & Developer Experience | KM 1, then KM 8 | Developer workflow, SDKs, tooling |
| D02 Universal Registry | KM 2 | Stable identity and capability lifecycle |
| D03 Publisher & Organization | KM 2 minimum; KM 9 full | Internal publishers first, external onboarding later |
| D04 Intelligence Orchestrator | KM 3–7 incrementally | Start with routing/policy hooks; defer advanced orchestration |
| D05 Execution Runtime | KM 4; KM 8 hybrid | Managed runtime before self-hosted fleet |
| D06 Distribution Gateway | KM 3; KM 8 expansion | REST and MCP first; adapters later |
| D07 Synchronization Engine | KM 6 | Desired/observed state and controlled rollout |
| D08 Access & Identity | KM 3 | Implement the shared policy core first |
| D09 Evaluation & Assurance | KM 5 onward | Evidence and release gates |
| D10 Observability & Audit | KM 3–5 onward | Correlation begins at gateway and expands end-to-end |
| D11 Marketplace & Commerce | KM 9 | Do not build before access and entitlement foundations |
| D12 Infrastructure & Operations | KM 1, KM 4, KM 10 | Baseline early; harden continuously |

This mapping is a planning view, not a mandate to create twelve deployable services. Keep the initial codebase modular and extract services only when scale, isolation, ownership, or release independence justifies it.

## 7. Planning ranges and sequencing

| Kilometer | Planning range |
|---|---:|
| KM 0 | 1–2 weeks |
| KM 1 | 2–3 weeks |
| KM 2 | 3–4 weeks |
| KM 3 | 3–5 weeks |
| KM 4 | 3–5 weeks |
| KM 5 | 2–3 weeks |
| KM 6 | 4–6 weeks |
| KM 7 | 2–4 weeks |
| KM 8 | 4–6 weeks |
| KM 9 | 4–6 weeks |
| KM 10 | 3–5 weeks |

These are rough planning windows for scoped phases, not an additive launch promise. The actual calendar depends on team size, contributor experience, stack decisions, hosting setup, legal review, and the number of integrations. KM 0–6 should be treated as the core platform proof. KM 7–9 expand the ecosystem. KM 10 is a release-readiness program, not a cosmetic final sprint.

## 8. Workstreams that can run in parallel

Parallelize discovery and governance, not core dependencies.

| Workstream | Can begin | Must not bypass |
|---|---|---|
| Product and governance | KM 0 | Approved scope and decision owners |
| Legal and ownership review | KM 0 | Legal approval before commercial marketplace launch |
| Security and threat modeling | KM 0 | Security gates before production |
| Platform engineering | KM 1 | Canonical contracts and architecture decisions |
| Registry and publisher model | KM 2 | Stable manifest and identity rules |
| Access and distribution | KM 3 | Shared policy model |
| Runtime | KM 4 | Artifact integrity, tenant and resource boundaries |
| Evaluation and observability | KM 3–5 | Evidence linkage and audit integrity |
| Internal integrations | KM 7 | Stable interfaces and authorization |
| Marketplace | Discovery may start at KM 0; implementation at KM 9 | Entitlement, policy, moderation, and legal approval |

## 9. Explicitly defer these items

Do not put the following into the first MVP unless a proven requirement forces the decision:

- Microservices and Kubernetes as default architecture.
- Multi-region active-active deployment.
- Fully automated billing settlement and complex revenue sharing.
- Full external marketplace automation.
- Autonomous self-modifying or self-healing production behavior.
- Dozens of platform-specific adapters before two independent client paths work.
- Bulk migration of all planned registry records directly into published state.
- A full enterprise self-hosted fleet-management suite.
- Sophisticated AI routing before deterministic invocation, policy, and telemetry are reliable.

The inventory of 427 candidate Skill Registry Records is a migration-planning input, not evidence that 427 validated records are already available. Import them into staging, validate provenance and contracts, resolve duplicates, then approve publication in controlled batches.

## 10. Global governance gates

Every kilometer must satisfy these cross-cutting conditions:

1. **Architecture:** contracts and domain boundaries remain coherent; deviations require an ADR.
2. **Security:** threat model, least privilege, tenant isolation, secrets handling, and egress control are tested at the relevant layer.
3. **Data:** ownership, retention, privacy, integrity, and deletion behavior are explicit.
4. **Quality:** automated tests and measurable acceptance criteria exist before a feature is marked complete.
5. **Operations:** logs, metrics, traces, failure modes, rollback, and runbooks match the implemented behavior.
6. **Governance:** publishing, access, approvals, and commercial rights are independently enforced.
7. **Evidence:** completion is supported by merged code, passing tests, review records, and operational evidence—not by a document claiming that a feature exists.

## 11. First 30-day execution checklist

The first month is for making HSMART buildable, not for pretending the entire platform can be completed in a month.

### Week 1 — Lock the project
- Formally ratify the merged Project Charter and record the adoption decision.
- Name accountable owners and decision-makers.
- Confirm MVP use case, non-goals, and measurable acceptance criteria.
- Open the prioritized backlog and risk register.

### Week 2 — Lock the technical foundation
- Decide the initial backend and persistence stack through ADRs.
- Set up reproducible local development and CI.
- Finalize the manifest and event contract test fixtures.
- Document environment and secret-management requirements.

### Week 3 — Start the first vertical slice
- Implement minimal publisher and capability identity.
- Implement manifest validation and Registry persistence.
- Add registration and discovery API tests.
- Record artifact digest and immutable version metadata.

### Week 4 — Demonstrate a trustworthy registry path
- Register and discover the demo capability.
- Verify positive and negative manifest cases.
- Test duplicate IDs and immutable published versions.
- Review the next dependency set for KM 3: OIDC, policy interface, REST/MCP boundary.

At day 30, the expected result is a governed, reproducible project with a working first Registry slice—not a complete HSMART platform.

## 12. Definition of done

A roadmap item is not complete because its code compiles or its endpoint returns HTTP 200. It is complete only when:

- The intended behavior and non-goals are documented.
- The implementation follows approved contracts and domain boundaries.
- Positive, negative, failure, and security-relevant tests pass.
- Access, audit, and data handling are verified.
- Observability and operational behavior are documented.
- A reviewer accepts the change.
- Evidence is linked to the issue or pull request.

## 13. Immediate next actions

1. Ratify the [HSMART Project Charter](../foundation/HSMART-PROJECT-CHARTER.md) and appoint the accountable Project Sponsor and Project Owner.
2. Assign accountable owners for the first vertical slice.
3. Finalize the implementation-stack ADRs.
4. Define the manifest contract tests and demo capability fixture.
5. Create a prioritized KM 0–2 issue backlog with explicit dependencies.
6. Start Registry implementation only after the KM 1 exit gate is met.

**The first strategic milestone is not “HSMART has many modules.” It is “one capability can be registered, authorized, executed, evaluated, updated, synchronized, and rolled back with evidence.”**
