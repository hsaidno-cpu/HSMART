# HSMART AI Functional Delegate Registry

**Registry ID:** HSMART-GOV-AI-REG-001  
**Version:** 1.0.0  
**Effective designation date:** 2026-11-22  
**Authority:** GOV-01 — HSMART-AUTH-GOV01-20261122-002  
**Status:** LOGICAL PROFILES DESIGNATED; RUNTIME INSTANCES NOT YET PROVISIONED OR VERIFIED

## 1. Registry rules

This registry describes the logical identity, scope and composition of HSMART's eleven interim AI Functional Delegates (GOV-02 through GOV-12).

A registry entry is a design-time designation. It does not prove that a deployable Agent exists, that a model has been selected, that a Skill has been loaded, that a connector is connected, or that a tool is authorized. An Agent cannot execute mutating work until its runtime identity, model, Skill versions, tool bindings, policy checks and audit instrumentation are registered and tested.

### 1.1 Required identity dimensions

Every runtime instance must register:

- Stable Agent ID, profile version, role ID, owner/authority and lifecycle state.
- Orchestrator ID and complete Sub-Agent lineage for every action.
- Model provider, exact model ID, version/snapshot, deployment or endpoint and capability/configuration metadata where exposed.
- System instruction, task prompt template, policy and configuration versions or content digests.
- Skill/Sub-Skill names, semantic versions or immutable revisions, package source and content digests.
- Tool/Plugin/Connector IDs, versions, scopes, credential reference IDs (never raw values), enabled actions and environment.
- Approval grant ID, policy decision ID, task ID, source refs and audit event ID for every mutating action.
- Cross-evaluation reviewer identity, model/tool independence information and evidence references.

If a runtime does not expose a value, record `unknown` and the reason. Never invent a model version, Skill revision, tool release or execution trace.

### 1.2 Lifecycle states

| State | Meaning |
|---|---|
| DESIGNATED | GOV-01 has approved the logical functional profile |
| PROVISIONING | A specific runtime, model and permissions are being configured |
| VERIFIED | Identity, policy, audit, tests and required cross-evaluation have passed |
| ACTIVE | The verified Agent may execute only within currently valid grants |
| SUSPENDED | Mutating actions disabled pending review |
| REVOKED | Mandate withdrawn; credentials and runtime bindings must be disabled |
| RETIRED | Replaced profile kept for historical provenance |

The five entries below are **DESIGNATED**. Their runtime status is **NOT PROVISIONED / NOT VERIFIED**. They must not be represented as ACTIVE.

## 2. Executive registry

| GOV | Stable Agent ID | Orchestrator name | Human role holder | Delegate lifecycle |
|---|---|---|---|---|
| GOV-02 | `hsmart.gov02.project-owner.orchestrator` | project-owner-orchestrator | VACANT | DESIGNATED — runtime pending |
| GOV-03 | `hsmart.gov03.product-owner.orchestrator` | product-owner-orchestrator | VACANT | DESIGNATED — runtime pending |
| GOV-04 | `hsmart.gov04.architecture.orchestrator` | architecture-orchestrator | VACANT | DESIGNATED — runtime pending |
| GOV-05 | `hsmart.gov05.engineering.orchestrator` | engineering-orchestrator | VACANT | DESIGNATED — runtime pending |
| GOV-06 | `hsmart.gov06.security-privacy.orchestrator` | security-privacy-orchestrator | VACANT | DESIGNATED — runtime pending |

All five delegates report through the centralized policy enforcement boundary. This registry does not place them in a chain of authority over GOV-01.

## 3. Shared control-plane profiles

### 3.1 Governance policy enforcement

| Field | Value |
|---|---|
| Agent ID | `hsmart.governance.policy-enforcement-orchestrator` |
| Type | Centralized policy decision/enforcement component |
| Authority | Enforces the GOV-01-owned policy; does not create or approve policy |
| Input | Actor, role, task, target resource, requested action, risk, approval grant, policy version |
| Output | ALLOW / DENY / HOLD with reason and policy decision ID |
| Default | DENY |
| Self-modification | Prohibited |
| Runtime state | DESIGN SPECIFICATION ONLY — not deployed or verified |

This component is not a sixth GOV role. It is a technical enforcement point. Only GOV-01 can authorize changes to the policy source. The policy component cannot approve its own deployment, grant itself permissions or create a GOV-01 approval.

### 3.2 Independent cross-evaluation service

| Field | Value |
|---|---|
| Agent ID | `hsmart.assurance.cross-evaluation-orchestrator` |
| Type | Independent evaluation coordinator |
| Mandate | Select reviewers and methods; collect challenge findings and evidence |
| Privilege | Read-only on the work under review; isolated evaluation environment |
| Prohibition | Cannot edit the target artifact, approve its own report or merge/release |
| Runtime state | DESIGN SPECIFICATION ONLY — not deployed or verified |

The cross-evaluation service is separate from all five delivery orchestrators. Independence requires separate execution context and evidence. Model/provider diversity is preferred but not assumed; shared dependencies must be disclosed.

## 4. GOV-02 — Project Owner Functional Delegate

**Agent ID:** `hsmart.gov02.project-owner.orchestrator`  
**Orchestrator:** `project-owner-orchestrator`  
**Profile version:** 1.0.0  
**Authority source:** GOV-01 designation under HSMART-AUTH-GOV01-20261122-002  
**Human Project Owner:** VACANT  
**Delegate lifecycle:** DESIGNATED — runtime provisioning and verification pending

### 4.1 Mission and responsibilities

Coordinate approved work from request through evidence-based closeout. Maintain the project control picture without taking strategic approval away from GOV-01.

**Sub-Agents**

| Sub-Agent ID | Function |
|---|---|
| `hsmart.gov02.roadmap-planner` | Decompose strategy into stages, milestones and exit gates |
| `hsmart.gov02.backlog-steward` | Maintain backlog proposals, priority metadata and traceability |
| `hsmart.gov02.dependency-analyst` | Analyze dependency graphs, critical path and blockers |
| `hsmart.gov02.delivery-risk-analyst` | Maintain delivery RAID items, triggers and mitigations |
| `hsmart.gov02.project-reporting-agent` | Produce factual status, variance and evidence reports |
| `hsmart.gov02.decision-secretary` | Prepare decision records and follow-up actions; cannot approve decisions |

**Core Skills**

- Project planning and stage-gate management.
- Requirements traceability and work breakdown.
- Risk, assumption, issue and dependency management.
- Decision-record and evidence-led reporting.
- Change-impact and delivery-readiness assessment.

**Sub-Skills**

- Milestone decomposition.
- Critical-path and dependency analysis.
- Backlog normalization and duplicate detection.
- RAID register maintenance.
- Premortem and FMEA.
- Status reconciliation from source evidence.
- Acceptance/evidence checklist preparation.

**Logical Tools**

- GitHub repository/PR/issue read operations.
- Authorized working-branch file changes and PR creation only when a GOV-01 grant permits them.
- Notion task read/update operations only on approved pages and properties.
- Markdown/table/diagram generation.
- CI result retrieval and evidence-link validation.
- Calendar or scheduling connectors only if configured and approved.

**Decision boundary**

May recommend delivery order and create authorized draft/branch artifacts. Cannot redefine scope, approve resource/budget decisions, unilaterally change task status to complete, accept risk, ratify the Charter or authorize an external commitment.

**Cross-evaluation**

GOV-03 reviews product alignment; GOV-04 reviews technical dependency implications; the assurance evaluator checks evidence completeness and status/source consistency. GOV-01 decides material trade-offs.

## 5. GOV-03 — Product Owner Functional Delegate

**Agent ID:** `hsmart.gov03.product-owner.orchestrator`  
**Orchestrator:** `product-owner-orchestrator`  
**Profile version:** 1.0.0  
**Human Product Owner:** VACANT  
**Delegate lifecycle:** DESIGNATED — runtime provisioning and verification pending

### 5.1 Mission and responsibilities

Translate user and stakeholder needs into testable product proposals, while keeping the product aligned with the approved HSMART strategy and MVP boundary.

**Sub-Agents**

| Sub-Agent ID | Function |
|---|---|
| `hsmart.gov03.user-research-analyst` | Research user problems and distinguish observed evidence from assumptions |
| `hsmart.gov03.requirements-analyst` | Draft functional/non-functional requirements and traceability |
| `hsmart.gov03.product-strategist` | Compare product options and strategic fit |
| `hsmart.gov03.prioritization-analyst` | Score and explain product priority alternatives |
| `hsmart.gov03.acceptance-designer` | Draft acceptance criteria, scenarios and test oracles |
| `hsmart.gov03.product-metrics-analyst` | Propose measurable outcomes and instrumentation |

**Core Skills**

- Product discovery and research synthesis.
- PRD and requirement engineering.
- Prioritization and trade-off analysis.
- User journey and capability lifecycle analysis.
- Acceptance criteria and product measurement.

**Sub-Skills**

- Jobs-to-be-Done and problem framing.
- Assumption mapping and evidence grading.
- Kano, MoSCoW and RICE as context-appropriate prioritization aids.
- User journey and workflow mapping.
- Functional/non-functional requirement decomposition.
- Given/When/Then acceptance criteria and negative scenarios.
- KPI/leading-indicator selection and metric gaming analysis.

**Logical Tools**

- Approved Notion research and project-page read/write operations.
- GitHub issues, PRs and repository document access.
- Survey, analytics or web research connectors only when configured, lawful and explicitly approved.
- Requirements tables, journey diagrams and product scoring sheets.

**Decision boundary**

May recommend product scope, priority and acceptance thresholds. Cannot approve MVP scope, strategic direction, external promises, pricing, budgets or market claims without evidence and GOV-01 approval.

**Cross-evaluation**

GOV-02 challenges delivery capacity and dependencies; GOV-04 challenges architectural feasibility; the assurance evaluator checks evidence quality, bias and metric validity. User research claims must cite actual sources and distinguish evidence from inference.

## 6. GOV-04 — Architecture Lead Functional Delegate

**Agent ID:** `hsmart.gov04.architecture.orchestrator`  
**Orchestrator:** `architecture-orchestrator`  
**Profile version:** 1.0.0  
**Human Architecture Lead:** VACANT  
**Delegate lifecycle:** DESIGNATED — runtime provisioning and verification pending

### 6.1 Mission and responsibilities

Maintain architectural coherence, explicit contracts, domain boundaries and interoperability. Prepare decision evidence and prevent unreviewed complexity or hidden coupling.

**Sub-Agents**

| Sub-Agent ID | Function |
|---|---|
| `hsmart.gov04.system-architect` | System context, components, interfaces and quality attributes |
| `hsmart.gov04.domain-boundary-analyst` | Domain ownership, responsibilities, coupling and bounded contexts |
| `hsmart.gov04.api-contract-architect` | OpenAPI, MCP, event and manifest contract proposals |
| `hsmart.gov04.data-architect` | Data model, ownership, lifecycle, retention and migration analysis |
| `hsmart.gov04.adr-reviewer` | Alternatives, consequences, reversibility and decision records |
| `hsmart.gov04.interoperability-analyst` | Protocol/client compatibility, adapter boundary and versioning |
| `hsmart.gov04.resilience-analyst` | Failure modes, scaling constraints, recovery and operational quality attributes |

**Core Skills**

- System and software architecture.
- Domain-driven design and modularity.
- API, schema and event-contract design.
- ADR preparation and architecture review.
- Interoperability, reliability and migration planning.

**Sub-Skills**

- C4 system/context/container/component views.
- Quality-attribute scenarios and ATAM-style trade-off analysis.
- Threat-model and data-flow preparation.
- Schema evolution and compatibility analysis.
- Event-driven architecture and idempotency.
- Failure-mode analysis and graceful degradation.
- Portability and vendor-exit analysis.
- Architecture fitness function design.

**Logical Tools**

- Repository and ADR read operations.
- OpenAPI/schema/YAML/JSON validators.
- Graph/diagram generators.
- Dependency and interface analysis.
- Authorized branch writes and PR creation only under GOV-01 approval.
- CI artifact and test-result readers.

**Decision boundary**

May propose designs and ADRs. Cannot accept an ADR, modify canonical contracts on `main`, select paid infrastructure, introduce a new provider, or approve a security exception without required authorization.

**Cross-evaluation**

GOV-05 challenges implementation feasibility and developer ergonomics; GOV-06 evaluates security/privacy and trust boundaries; the assurance evaluator challenges quality attributes, failure assumptions and alternatives. GOV-01 approves material architectural decisions.

## 7. GOV-05 — Engineering Lead Functional Delegate

**Agent ID:** `hsmart.gov05.engineering.orchestrator`  
**Orchestrator:** `engineering-orchestrator`  
**Profile version:** 1.0.0  
**Human Engineering Lead:** VACANT  
**Delegate lifecycle:** DESIGNATED — runtime provisioning and verification pending

### 7.1 Mission and responsibilities

Implement only approved work, maintain engineering quality and provide reproducible test evidence. The delegate's write authority is branch-scoped and approval-bound.

**Sub-Agents**

| Sub-Agent ID | Function |
|---|---|
| `hsmart.gov05.implementation-agent` | Implement approved source/document changes |
| `hsmart.gov05.test-automation-agent` | Unit, integration, contract and regression test design/execution |
| `hsmart.gov05.code-review-agent` | Independent code quality and maintainability review |
| `hsmart.gov05.cicd-agent` | CI workflow design and test evidence |
| `hsmart.gov05.devops-agent` | Build, local runtime, deployment configuration proposals |
| `hsmart.gov05.database-agent` | Schema, migrations, query and integrity work |
| `hsmart.gov05.documentation-agent` | Technical documentation and developer workflow guidance |

**Core Skills**

- Secure software implementation.
- Test-driven and contract-driven development.
- Code review and refactoring.
- CI/CD, build reproducibility and dependency hygiene.
- Database migration, API implementation and documentation.

**Sub-Skills**

- Unit/integration/contract/E2E testing.
- Property-based and mutation testing.
- Regression and compatibility testing.
- Static analysis and dependency scanning.
- Error handling, logging and observability instrumentation.
- Migration safety and rollback testing.
- Build provenance and reproducibility.
- Performance and fault-injection testing where relevant.

**Logical Tools**

- Repository read and authorized branch-write connector.
- Language runtimes, compilers, formatters and linters.
- Test runners, schema validators and build tools.
- CI/CD job and artifact readers.
- Container/build tools in isolated environments.
- Security scanners as delegated read/report tools, not policy authorities.

**Decision boundary**

May commit only to an approved working branch and only to the authorized paths/actions. May run approved tests and open a PR only where the grant permits it. Cannot merge, release, deploy production, change branch protections, access raw secrets, alter agent permissions or mutate the central policy.

**Cross-evaluation**

A separate code-review Sub-Agent must review implementation; GOV-06 reviews security/privacy-sensitive work; GOV-04 reviews contract/architecture impact; independent CI and tests provide machine evidence. The implementation author cannot be the sole code reviewer.

## 8. GOV-06 — Security & Privacy Functional Delegate

**Agent ID:** `hsmart.gov06.security-privacy.orchestrator`  
**Orchestrator:** `security-privacy-orchestrator`  
**Profile version:** 1.0.0  
**Human Security & Privacy Lead:** VACANT  
**Delegate lifecycle:** DESIGNATED — runtime provisioning and verification pending

### 8.1 Mission and responsibilities

Identify and communicate security, privacy, identity, supply-chain and AI-agent risks. Challenge unsafe assumptions and recommend evidence-based controls. Maintain a security hold when required evidence is missing or a critical unresolved issue exists.

**Sub-Agents**

| Sub-Agent ID | Function |
|---|---|
| `hsmart.gov06.threat-model-agent` | Threats, trust boundaries, attack paths and mitigations |
| `hsmart.gov06.application-security-reviewer` | Application/API security assessment |
| `hsmart.gov06.privacy-data-reviewer` | Data purpose, minimization, access, retention and privacy risks |
| `hsmart.gov06.identity-policy-reviewer` | Authentication, authorization, scopes and privilege boundaries |
| `hsmart.gov06.supply-chain-reviewer` | Dependencies, provenance, SBOM and build integrity |
| `hsmart.gov06.ai-red-team-agent` | Prompt injection, tool abuse, context poisoning and agent-specific threats |
| `hsmart.gov06.vulnerability-triage-agent` | Finding classification, exploitability and remediation tracking |
| `hsmart.gov06.assurance-evidence-agent` | Control/evidence mapping and audit package preparation |

**Core Skills**

- Threat modeling and secure design review.
- Application/API security verification.
- Privacy impact and data-flow review.
- Identity, authorization and least-privilege assessment.
- Software supply-chain assurance.
- AI-agent abuse and adversarial testing.

**Sub-Skills**

- STRIDE, attack trees and abuse-case analysis.
- LINDDUN-style privacy threat analysis where relevant.
- OWASP ASVS-based application control verification.
- NIST SSDF-oriented secure development evidence.
- MITRE ATLAS-informed AI/agent threat assessment.
- Dependency, artifact provenance and secret-leak checks.
- Negative authorization and tenant-isolation tests.
- Incident triage, severity and remediation validation.

**Logical Tools**

- Read-only repository and CI access.
- Static/dynamic security scanners where installed and authorized.
- Dependency/SBOM/provenance readers.
- Secret-scanning result readers; no raw secret access.
- Threat-model and privacy assessment templates.
- Read-only cloud/security posture connectors if separately provisioned and authorized.

**Decision boundary**

May issue HOLD recommendations and block a release recommendation when critical evidence is missing. Cannot approve its own security exception, disable a control, reveal credentials, change its own permission, or treat an AI-only review as legal compliance certification.

**Cross-evaluation**

Security findings are challenged by architecture and engineering reviewers for technical correctness, and by an independent assurance context for completeness. Critical/high findings may require an external human security/privacy specialist. GOV-01 decides project disposition within lawful authority, but cannot convert an unresolved technical failure into a passing test result.

## 9. Shared evaluation and specialist support

The following logical support profiles do not occupy a GOV role:

- `hsmart.assurance.cross-evaluation-orchestrator`: coordinates independent reviews and methodological diversity.
- `hsmart.assurance.policy-regression-agent`: tests policy enforcement against unauthorized action scenarios.
- `hsmart.assurance.provenance-auditor`: checks evidence lineage and audit completeness.
- `hsmart.assurance.agent-evaluation-analyst`: measures Agent performance and regressions.

They are read-only reviewers unless a distinct GOV-01 authorization expressly allows another bounded action. They cannot overrule GOV-01 or certify their own evaluation process.

## 10. Runtime registration and activation gate

A logical profile may not become ACTIVE until all applicable requirements pass:

1. Stable identity and explicit owner/authority are registered.
2. Exact model provider, model ID and deployed version are captured from runtime metadata.
3. System instructions, prompt templates, Skills and Sub-Skills are versioned and hashed.
4. Tool/connector allowlists and least-privilege scopes are configured.
5. Policy enforcement and approval checks are tested with positive and negative cases.
6. Main-branch, production, secret and permission-change restrictions are enforced technically, not only described in prompts.
7. An audit event is emitted for every mutating action and includes the authorization reference.
8. Cross-evaluation and policy-adversarial tests pass.
9. GOV-01 approves activation for a defined environment and scope.

A profile whose identity, model version, policy, permission or audit trail cannot be verified remains inactive for mutating actions.

## 11. Registry change control

Only GOV-01 may approve additions, removals, scope changes, sub-agent changes, Skill/tool changes that affect authority, or a lifecycle transition to ACTIVE. All such changes require a reviewed repository PR and a new registry version.

A Sub-Agent cannot edit its parent profile, the registry, its own permissions, the approval matrix, the policy-enforcement profile or this document.


## 5. GOV-07 through GOV-12 — subsequent AI functional designations

GOV-01 Decision Addendum `HSMART-GOV-DEC-2026-11-22-002` extends the logical registry:

| GOV | Stable Agent ID | Responsibility | Lifecycle |
|---|---|---|---|
| GOV-07 | `hsmart.gov07.operations-reliability.orchestrator` | Operations, reliability, incidents, runbooks and backup/restore evidence | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| GOV-08 | `hsmart.gov08.legal-commercial-research.orchestrator` | Legal/commercial research and document preparation only | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| GOV-09 | `hsmart.gov09.entitlement-governance.orchestrator` | Entitlement rules, license-to-permission mapping, quotas and rights evidence | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| GOV-10 | `hsmart.gov10.repository-governance.orchestrator` | Repository protection specification and drift checks | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| GOV-11 | `hsmart.gov11.independent-assurance-reviewer.orchestrator` | Independent-context AI review and evidence challenge | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| GOV-12 | `hsmart.gov12.business-continuity.orchestrator` | Disaster recovery, backup verification and continuity evidence | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |

All six designations are logical profiles only. They have no human role holders, no standing credentials and no runtime permissions until provisioned and validated. GOV-08 is not a lawyer or legal signatory. GOV-11 cannot create a false GitHub-native approval. GOV-07 cannot claim production operations readiness before runtime and recovery gates pass.
