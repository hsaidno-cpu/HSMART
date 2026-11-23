# HSMART Prioritized Delivery Backlog — KM 0 to KM 2

**Backlog ID:** HSMART-PLAN-BL-001  
**Version:** 1.0.0  
**Prepared:** 2026-11-22  
**Status:** Initial prioritized baseline; owners and dates pending appointment  
**Source of truth:** GitHub issues/PRs for engineering evidence; Notion HSMART Tasks for accountable project actions

## 1. Prioritization rules

- P0 blocks KM 0 exit or creates unacceptable authority/integrity exposure.
- P1 is required before the next dependent stage or before safe vertical-slice implementation.
- P2 improves delivery quality but does not independently block the current gate.
- P3 is deferred or monitored.
- No task receives an invented assignee or due date.
- A task is complete only when its output and acceptance evidence are linked; document creation alone is insufficient for implementation tasks.

## 2. Active closeout: original eight tasks

| ID | Existing task | Priority | Stage | Dependency | Output / acceptance | Current disposition |
|---|---|---:|---|---|---|---|
| BL-001 | Approve MVP boundary and initial success measures | P0 | KM 0 | Charter and product decision owner | Approved MVP decision record with named approval and finite acceptance criteria | Decision package prepared; human approval pending |
| BL-002 | Appoint core accountable roles and decision rights | P0 | KM 0 | Sponsor/owner authority | Completed appointment register with named people, effective dates and delegated authority | Register prepared; appointments pending |
| BL-003 | Formally ratify Project Charter | P0 | KM 0 | BL-002 | Ratification record with authorized approver, effective date and accepted conditions | Record prepared; ratification pending |
| BL-004 | Prioritize KM 0–KM 2 backlog and dependencies | P1 | KM 0 | BL-001, BL-002 | This backlog, dependency order, acceptance and open decisions | Prepared; linked to canonical source |
| BL-005 | Create initial risk register and review KM 0 threat model | P1 | KM 0 | Charter, threat model | Initial risk register with controls, triggers, role owners and residual status | Initial review and register prepared |
| BL-006 | Define contract-test fixtures for manifest, event and demo capability | P1 | KM 1 | Canonical schemas | Positive/negative fixtures, automated tests and green CI on exact PR commit | COMPLETE: fixture/schema/OpenAPI suite merged in PR #7; extended strict-JSON negative tests and cross-platform validation passed in PR #9 CI run #19 on head SHA 4a739f9 |
| BL-007 | Build reproducible development environment and initial CI | P1 | KM 1 | Toolchain baseline | Documented Python contract-validation harness and CI; application/runtime environment remains stack-dependent | PARTIAL: contract tooling/bootstrap/CI passes on Ubuntu 24.04, Windows Server 2025 and macOS 15 (12 tests each, pip check clean); direct pins only, no transitive hash lock; application environment waits for accepted ADR-011 |
| BL-008 | Finalize stack and infrastructure decisions through ADRs | P1 | KM 1 | BL-002, workload and budget inputs | Approved ADRs for app stack, database, storage, queue, identity, secrets, hosting and deployment | ADR-011 v1.1.0 recommends a proof-of-fit baseline; formal acceptance, team/security/operations evidence, region and budget remain pending |

## 3. KM 0 work breakdown

### Governance and project control
- GOV-001 Appoint Sponsor/Accountable Owner and Project Owner.
- GOV-002 Appoint Product, Architecture, Engineering and Security/Privacy leads.
- GOV-003 Ratify Charter v1.0.0 and record conditions.
- GOV-004 Approve MVP decision record and non-goals.
- GOV-005 Confirm decision classes, escalation and change control.
- GOV-006 Establish risk owner and review cadence after appointments.

### Product definition
- PRD-001 Confirm primary user and publisher/consumer journey.
- PRD-002 Adopt the hsmart:demo:text-transformer use case.
- PRD-003 Confirm MVP acceptance matrix and exclusions.
- PRD-004 Set measurable finite demo criteria; defer production SLOs until workload evidence exists.

### Delivery controls
- PM-001 Link each task to one or more requirements and acceptance checks.
- PM-002 Prioritize P0/P1 dependencies before implementation.
- PM-003 Record owner, due date and decision owner after appointments.
- PM-004 Establish issue/PR/CI as engineering evidence and Notion as operational task view.
- PM-005 Reconcile task status to observed GitHub evidence.

## 4. KM 1 work breakdown

### Technical decisions
- TEC-001 Approve application language/framework after team-skill and workload review.
- TEC-002 Select PostgreSQL persistence and migration policy or record an alternative.
- TEC-003 Select artifact/object storage and immutability controls.
- TEC-004 Decide whether a queue is needed now or defer until runtime design.
- TEC-005 Select OIDC issuer and KMS/secret manager only after cost, region and ownership review.
- TEC-006 Decide deployment environment and domain/DNS/TLS path; no resource procurement without approval.

### Developer experience and CI
- DEV-001 Pin a supported Python minor for contract-validation tooling.
- DEV-002 Pin direct development dependencies and document bootstrap commands.
- DEV-003 Run JSON syntax and JSON Schema positive/negative contract tests.
- DEV-004 Validate OpenAPI 3.1 structure and required operations.
- DEV-005 Add unit/contract tests and retain evidence against commit SHA.
- DEV-006 Add formatting/type/lint checks once the application language is approved.
- DEV-007 Add secret scanning and dependency/SBOM checks before executable runtime code is accepted.

### Contract quality
- CON-001 Validate capability manifest required fields, formats, identity and additional properties.
- CON-002 Validate event envelope fields, version, timestamps and event type.
- CON-003 Validate invocation and error contracts in OpenAPI.
- CON-004 Add demo capability fixture conforming to the manifest.
- CON-005 Add compatibility and breaking-change examples.
- CON-006 Record contract versioning and deprecation policy.

## 5. KM 2 preview — Universal Capability Registry

Do not start KM 2 implementation until KM 1 exit evidence is accepted.

| Work ID | Deliverable | Acceptance |
|---|---|---|
| REG-001 | Capability and publisher identity model | Stable namespace and deterministic uniqueness constraints |
| REG-002 | Registry persistence and migrations | Reproducible migration from empty database; rollback strategy documented |
| REG-003 | Manifest validation service | Positive/negative schema tests integrated into registration |
| REG-004 | Draft/published capability lifecycle | Draft mutable; published version immutable |
| REG-005 | Artifact metadata and digest | Digest computed and verified on upload/read/deploy path |
| REG-006 | Discovery API | Tenant/visibility/entitlement filters enforced |
| REG-007 | Version and lifecycle endpoints | Semantic version and state transitions validated |
| REG-008 | Audit events | Register, validate, publish, deprecate and quarantine events attributable |
| REG-009 | Import staging | Provenance, schema, duplicates and risk review before publication |
| REG-010 | Registry acceptance suite | All defined positive, negative, boundary and authorization tests pass |

## 6. Dependency graph

~~~mermaid
flowchart TD
  A[Appoint accountable roles] --> B[Ratify Charter]
  A --> C[Approve MVP boundary]
  B --> D[Approve backlog and risks]
  C --> D
  D --> E[Approve stack and infrastructure ADRs]
  E --> F[Reproducible engineering environment]
  F --> G[Canonical contract test harness]
  G --> H[KM 1 exit review]
  H --> I[Registry persistence and identity]
  I --> J[Registry lifecycle and discovery]
  J --> K[KM 2 exit review]
~~~

## 7. Status and governance

Every task should eventually have: task ID, owner role/person, accountable approver, priority, KM stage, source requirement, dependency, repository path/issue, test/acceptance ID, due date, observed status and evidence locator.

A dependency cannot be marked complete because its downstream task exists. If a decision is pending, record NEEDS_DECISION; if work has a partial artifact, record IN_PROGRESS; if evidence is absent, do not mark DONE.

## 8. Immediate sequence

1. Human authority: appoint roles and ratify the Charter.
2. Product authority: approve MVP boundary and acceptance.
3. Project owner: adopt this backlog and assign accountable owners/dates.
4. Security lead: accept/assign the initial risk register and review cadence.
5. Architecture/Engineering leads: decide stack and infrastructure.
6. Engineering: complete reproducible toolchain and contract-test CI.
7. Project authority: review the KM 1 exit gate before KM 2.

No schedule commitment is set because capacity and owner appointments are not yet known.


## 9. GOV-01 canonical execution addendum — 2026-11-22

This addendum supersedes earlier role/owner assumptions above where they conflict with the later GOV-01 decision `HSMART-GOV-DEC-2026-11-22-002`.

- GOV-01 is the only human authority in the internal HSMART governance model.
- GOV-02..GOV-12 are bounded AI Functional Delegate designations; all are NOT_PROVISIONED / NOT_ACTIVE until individual runtime gates pass.
- GOV-07 covers Operations/Reliability as a logical delegate; this is not production operations evidence.
- GOV-08 is legal/commercial research and drafting only, not legal counsel or a signatory.
- GOV-09 maintains the internal entitlement baseline; entitlement service implementation is not part of KM 1.
- GOV-10 prepares repository protection configuration and drift reports. Main is NOT_APPLIED while GitHub reads back `protected=false`.
- GOV-11 provides AI review reports, not native GitHub human approvals. GOV-01 retains final merge authority.
- GOV-12 prepares continuity/DR controls; DR is NOT_TESTED.

### Current mandatory priority

1. PR #13 — MERGED to main at `17c78dcd2ea59c6d40f9a07d188bab6f829f0596`.
2. GOV-07 designation and repository governance — role DESIGNATED; main protection still NOT_APPLIED.
3. KM 0 — OPEN until governance and repository evidence are reconciled.
4. KM 1 — ADR-011 accepted as internal stack baseline; application environment implemented on working branch; PostgreSQL 16 CI and independent KM 1 review pending.
5. KM 2 Registry — BLOCKED until GOV-01 accepts KM 1 against exact commit and evidence.

Local KM 1 test evidence at preparation: 11 passed; 2 PostgreSQL integration tests skipped locally because no database service was available. SQLite migration smoke passed but is not a substitute for PostgreSQL. Production deployment, WORM audit, DR and production security readiness remain NOT VERIFIED.
