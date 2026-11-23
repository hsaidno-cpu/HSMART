# HSMART Progressive Completion Roadmap

**Document ID:** HSMART-ROADMAP-PC-001  
**Version:** 1.0.0  
**Prepared:** 2026-11-22  
**Status:** ACTIVE EXECUTION CONTROL BASELINE — KM 0 OPEN / KM 1 PARTIAL  
**Authority:** Project Charter v1.0.2, subject to canonical synchronization through PR #13  
**Repository baseline inspected:** main @ e796b5842f98277716fc5d81026ac175d0591f36  
## Current evidence snapshot — 23 November 2026

This section supersedes the 22 November baseline and older state text below.

| Workstream | Current evidence | Current state |
|---|---|---|
| Canonical GOV-01 decisions | PR #13 merged to main at `17c78dcd2ea59c6d40f9a07d188bab6f829f0596`; MVP v1.1.0 and Charter v1.0.2 decisions canonical | MERGED / CANONICAL |
| GOV-07 | AI delegate `hsmart.gov07.operations-reliability.orchestrator` designated; no separate human GOV-07 seat | DESIGNATED; runtime NOT_PROVISIONED |
| Main protection | Desired config, CLI operator and manual Actions workflow in PR #28; GitHub still reports `protected=false` | NOT_APPLIED / NOT_VERIFIED |
| ADR-011 | v1.2.0 accepted by GOV-01 under `HSMART-GOV-DEC-2026-11-22-002` | DECISION ACCEPTED |
| KM 1 application foundation | FastAPI, SQLAlchemy/Alembic, PostgreSQL 16, migration CI, Compose API/worker and outbox concurrency test | IMPLEMENTED ON PR #28 BRANCH; HOSTED CI PASSED |
| AI assurance | GOV-11 report is bound to exact reviewed SHA; report-only commit and AI Reviewer Evidence CI still pending | IN PROGRESS |
| KM 0 | Repository protection and evidence-based exit decision not complete | OPEN |
| KM 1 | Proof-of-fit accepted; application environment/evaluation and exact-commit GOV-01 exit decision remain | IN PROGRESS |
| KM 2–KM 8 | Registry, Gateway, managed Runtime, Evaluation and Synchronization not operational | BLOCKED UNTIL KM 1 ACCEPTED |
| Production/legal | No production deployment, WORM store, restore exercise, PSE registration, entity formation or commercial approval evidenced | NOT VERIFIED |

PR #28: https://github.com/hsaidno-cpu/HSMART/pull/28  
Specification validation: https://github.com/hsaidno-cpu/HSMART/actions/runs/45081190812  
PostgreSQL 16 application CI: https://github.com/hsaidno-cpu/HSMART/actions/runs/45081190720  
Repository Governance Review: https://github.com/hsaidno-cpu/HSMART/actions/runs/45081190729  
AI Reviewer Evidence (pre-report expected failure): https://github.com/hsaidno-cpu/HSMART/actions/runs/45081190713

---

# HSMART Progressive Completion Roadmap

**Document ID:** HSMART-ROADMAP-PC-001  
**Version:** 1.1.0  
**Prepared:** 2026-11-23  
**Status:** ACTIVE EXECUTION CONTROL BASELINE — KM 0 OPEN / KM 1 IN PROGRESS  
**Authority:** Project Charter v1.0.2 and GOV-01 decisions canonical on main via merged PR #13; ADR-011 acceptance recorded in PR #28  
**Repository main:** 17c78dcd2ea59c6d40f9a07d188bab6f829f0596; active implementation branch `governance/km1-ops-adr011-20261122`  
**Related:** IMPLEMENTATION-ROADMAP.md; BACKLOG-KM0-KM2.md; MVP-DECISION-RECORD.md; ADR-011; DELEGATE-RUNTIME-ACTIVATION-PLAN.md

---

## 1. Purpose and operating rule

This document turns the KM 0–KM 10 strategy into a dependency-controlled completion programme. It replaces vague claims of progress with observable work packages, named decision authorities, evidence requirements, acceptance tests, and explicit stop conditions.

The programme has five rules:

1. A stage is complete only when its exit criteria are met and the accountable decision owner accepts the evidence.
2. A document, schema, test file, CI workflow, pull request, or local reference implementation is not proof that a deployed service exists.
3. A task may be partially complete. Preserve that state rather than forcing it into Done.
4. Do not start downstream implementation merely because an upstream design document exists.
5. Never invent an owner, deadline, infrastructure account, model provider, budget, test result, or production capability.

This roadmap is an execution-control document. The original IMPLEMENTATION-ROADMAP remains the strategic sequence; this document governs current closeout, dependencies, and delivery evidence.

## 2. Verified baseline and current disposition

Snapshot date: 22 November 2026. Re-check branch and PR state before each consequential write.

| Area | Observed baseline | Disposition |
|---|---|---|
| Repository main | Commit e796b5842f98277716fc5d81026ac175d0591f36; default branch main | Current inspected baseline |
| PR #13 | GOV-01 decision record; OPEN / DRAFT / NOT MERGED; head e0082584c68b5926f976f5700552989e05176259 | Governance synchronization pending |
| PR #13 CI | Four jobs passed on the exact observed head | Repository checks only |
| Charter | v1.0.2 on PR #13 branch; conditional decision recorded there | Not yet canonical on main |
| MVP | v1.1.0 approved as written on PR #13 branch | Approval recorded; acceptance tests not thereby passed |
| GOV-01 | Appointed for internal project governance | Recorded |
| GOV-02..GOV-06 | AI functional delegate profiles designated; human seats vacant; runtimes not provisioned | Designation only, not activation |
| GOV-07 Operations/Reliability | Unassigned | P0 decision blocker before hosted production operations |
| Main branch protection | GitHub reports main protected=false; required status checks are not enforced | P0 repository-control gap |
| KM 0 | Governance baseline and initial backlog exist; PR #13 and operational accountability remain open | OPEN |
| KM 1 | JSON/schema/OpenAPI contract suite, fixtures, Python contract-tooling environment, and local policy reference evaluator exist | PARTIAL |
| KM 2–KM 8 | Architecture/contracts documented; production application services not evidenced | NOT STARTED |
Snapshot date: 23 November 2026. Re-check branch and PR state before each consequential write.

| Area | Observed baseline | Disposition |
|---|---|---|
| Repository main | Commit 17c78dcd2ea59c6d40f9a07d188bab6f829f0596; default branch main; protected=false | Current inspected baseline |
| PR #13 | GOV-01 decision record; MERGED; merge commit 17c78dcd2ea59c6d40f9a07d188bab6f829f0596 | Governance decisions canonical |
| PR #13 CI | Four jobs passed on the exact observed head | Repository checks only |
| Charter | v1.0.2; RATIFIED WITH CONDITIONS and canonical on main | Decision recorded; activation gates remain |
| MVP | v1.1.0 APPROVED AS WRITTEN and canonical on main | Approval recorded; delivery acceptance remains evidence-gated |
| GOV-01 | Appointed for internal project governance | Recorded |
| GOV-02..GOV-12 | AI Functional Delegates designated; GOV-01 is the only human internal authority; all runtimes NOT_PROVISIONED / NOT_ACTIVE | Designation only, not activation |
| GOV-07 Operations/Reliability | AI delegate designated by GOV-01; runtime NOT_PROVISIONED / NOT_ACTIVE | Internal role allocation resolved; operational activation still open |
| Main branch protection | GitHub reports main protected=false; admin operator and workflow are in PR #28; application requires Administration: write | P0 repository-control gap; NOT_APPLIED / NOT_VERIFIED |
| KM 0 | PR #13 canonical; AI role allocation recorded; branch protection and KM 0 exit evidence remain open | OPEN |
| KM 1 | ADR-011 v1.2.0 accepted; FastAPI/SQLAlchemy/Alembic app foundation, Compose worker and PostgreSQL 16 integration CI pass on PR #28; AI evidence and exact-commit acceptance pending | IN PROGRESS |
| KM 2–KM 8 | Registry/Gateway/managed Runtime/Evaluation/Synchronization services not operational; wait for KM 1 acceptance | BLOCKED / NOT STARTED |
| KM 9 | Marketplace intentionally deferred | DEFERRED |
| KM 10 | Production hardening not evidenced | NOT STARTED |

### Important distinctions

- PR #13 records the GOV-01 decisions for MVP v1.1.0 and Charter v1.0.2. Those decisions are not yet part of main. Do not describe them as canonical repository state until PR #13 is merged and read back.
- The green PR #13 workflow validates the checks actually run on its head commit. It does not prove runtime deployment, hosted authorization, provider connectivity, production WORM storage, or MVP acceptance.
- The local policy evaluator in src/hsmart_governance is a reference decision engine, not a production policy gateway.
- The current development environment validates contracts. It is not the HSMART application runtime or full application development environment.
- The 12 HSMART domains are logical bounded contexts, not a requirement to create 12 deployable services.

## 3. Completion status model

Use the following states consistently in GitHub and Notion:

| State | Meaning | Evidence needed |
|---|---|---|
| NOT_STARTED | No execution artifact or activity is evidenced | None |
| PLANNED | Scope, owner role, dependency, and acceptance are defined | Approved backlog item |
| IN_PROGRESS | Work has started but acceptance is incomplete | Current artifact and remaining gaps |
| IMPLEMENTED | Code/configuration/document change exists on a named branch or commit | Read-back of exact files and commit |
| VERIFIED | Required applicable tests passed on the exact commit/environment | Test report, CI run, logs, and limitations |
| ACCEPTED | Accountable owner accepted the stage/task evidence | Durable decision/acceptance record |
| MERGED | GitHub reports merge into the intended base branch | Merge commit SHA and read-back |
| DEPLOYED | Target environment reports the intended version running | Deployment ID, environment and health evidence |
| RELEASED | Approved release/publish operation completed | Release record and independent read-back |
| BLOCKED | Required authority, input, capability, resource, or dependency is unavailable | Explicit blocker and recovery path |
| DEFERRED | Intentionally postponed by scope or risk decision | Decision and trigger for reconsideration |

Never infer VERIFIED from IMPLEMENTED, MERGED from PR_OPEN, or DEPLOYED from MERGED.

Do not publish an overall completion percentage from the number of tasks or documents. Stage gates are not interchangeable units, and averaging them would hide critical blockers.

## 4. Critical path and gate sequence

The critical path is:

1. GOV-01 decision synchronization: review, approve and merge PR #13 under the repository's human approval rules; read back all six changed files from main.
2. KM 0 accountability closure: assign GOV-07 or record an explicitly accepted human interim operations owner; document authority, scope, escalation and operational limits.
3. Repository governance: enforce pull-request, review, CI, conversation-resolution, deletion and force-push controls on main.
4. KM 0 exit review: confirm scope, decision rights, risk disposition, backlog ownership and critical-decision ownership.
5. KM 1 stack proof-of-fit: execute the reversible FastAPI/OpenAPI and persistence spike; accept ADR-011 through an authorized decision.
6. KM 1 engineering environment: extend contract tooling into the approved application development environment, database migration workflow and application CI.
7. KM 1 exit evaluation: clean-checkout reproducibility, contract/schema tests, application tests, security checks, dependency checks and documentation read-back.
8. KM 2 Registry: begin implementation only after KM 1 is ACCEPTED.
9. KM 3 access/distribution and KM 4 managed execution: integrate against the accepted Registry and shared authorization contracts.
10. KM 5 evaluation/observability and KM 6 adaptive synchronization: deliver evidence-linked evaluation, telemetry, staged rollout and rollback.
11. KM 7–KM 10: first-party integrations, hybrid distribution, marketplace and production hardening only after their predecessor and governance gates pass.

### Dependency graph

- PR13 canonical synchronization -> KM 0 closure decision.
- GOV-07 accountable coverage + repository controls + KM 0 evidence -> KM 0 ACCEPTED.
- Accepted ADR-011 + reproducible application environment + contract baseline -> KM 1 ACCEPTED.
- KM 1 ACCEPTED -> KM 2 Registry implementation.
- KM 2 accepted Registry contracts -> KM 3 Access/Distribution implementation.
- KM 3 authorization and invocation contracts -> KM 4 Managed Runtime.
- KM 3 + KM 4 execution evidence -> KM 5 Evaluation/Observability.
- KM 5 evidence model + stable Registry/Runtime state -> KM 6 Adaptive Synchronization.
- KM 3–KM 6 stable interfaces -> KM 7 First-Party Ecosystem Integration.
- KM 4 + KM 3 stable trust contracts -> KM 8 Self-Hosted/Cross-Platform.
- KM 3, KM 5, KM 7 plus legal, entitlement and moderation approval -> KM 9 Marketplace.
- KM 3–KM 9 relevant controls + operations ownership + security/recovery evidence -> KM 10 Production Hardening.

Parallel work is permitted for research, threat-model refinement, documentation, legal discovery and test-design preparation. Parallel work must not bypass the technical or governance exit gate.

## 5. Gate 0 — Governance and repository control

### G0.1 Canonical synchronization of GOV-01 decisions

**Current status:** BLOCKED ON REVIEW / MERGE.  
**Source:** PR #13.

Required actions:
- Independently inspect the complete PR #13 diff.
- Confirm the decision record accurately captures the explicit GOV-01 decisions and their authority limits.
- Confirm Charter v1.0.2, Ratification Record v1.4.0, MVP v1.1.0, GOV-01 Decision Record, Role Appointment Register and Runtime Activation Plan tell one consistent story.
- Confirm the unchecked runtime and production conditions remain open.
- Obtain the required human review and merge authorization.
- After merge, fetch all changed files from main and verify their versions, status text and cross-links.

Acceptance:
- PR #13 is reported MERGED by GitHub.
- The merge commit is recorded.
- Main read-back contains the expected six-file update.
- No document claims delegate activation or production readiness.
- Notion's snapshot, task tracker and links refer to the new main commit.

### G0.2 GOV-07 Operations/Reliability accountability

**Current status:** BLOCKED — no accountable owner recorded.

Before hosted production workloads, one of the following must be recorded:
- A named, qualified human GOV-07 who accepts monitoring, backup, restore, incident response, credential rotation, emergency suspension and recovery responsibility; or
- A specifically named human interim operations owner with the same bounded responsibilities, authority, availability expectations and review/expiry condition.

An AI delegate may prepare runbooks, inspect telemetry and recommend actions when authorized. An AI profile alone does not satisfy human incident accountability or C-07 of the Charter ratification conditions.

Acceptance:
- Role register names the human owner and acceptance evidence.
- Decision rights, on-call/escalation path and emergency suspension authority are explicit.
- Backup/restore and incident responsibilities have no unowned critical gap.
- No production workload begins before this gate passes.

### G0.3 Repository governance

**Current status:** BLOCKED — main is unprotected in the observed GitHub configuration.

Required repository controls:
- Require changes to enter main through pull requests.
- Require at least one independent human approval before merge.
- Dismiss stale approvals after new reviewable commits.
- Require approval of the latest push where supported.
- Require the applicable CI jobs: Contract tests (ubuntu-24.04), Contract tests (windows-2025), Contract tests (macos-15), and OpenAPI and required repository files.
- Require conversation resolution.
- Require the branch to be up to date with main before merge.
- Prohibit force pushes and deletion of main.
- Do not configure a broad AI/delegate bypass. Keep administrator bypass disabled where repository settings permit.
- Add a qualified independent human reviewer before enforcing an approval rule that cannot be satisfied by the sole repository owner.
- Verify the active ruleset/branch protection from GitHub after configuration; a documentation checkbox is not evidence.
### G0.2 GOV-07 Operations/Reliability AI accountability

**Current status:** INTERNAL ROLE ALLOCATION RESOLVED; RUNTIME / OPERATIONAL EVIDENCE BLOCKED.

GOV-01 designated `hsmart.gov07.operations-reliability.orchestrator` as the AI Functional Delegate for GOV-07. No separate human GOV-07 seat is part of the internal HSMART model. GOV-01 remains the single human accountable authority internally. Designation does not mean an on-call runtime, telemetry, backup/restore, incident runbook or recovery action is available.

Before hosted production workloads, provision and verify:
- Isolated runtime identity, exact model, pinned Skills/Sub-Skills and task-scoped tools.
- Health, metrics, alerts, incident evidence scopes and emergency suspension controls.
- Approved runbooks for service restart, restore, credential revocation/rotation and incident containment.
- Tested backup restoration, RPO/RTO evidence and WORM audit integration where privileged production operations require it.

Acceptance:
- GOV-07 passes A1–A8 and is read back VERIFIED/ACTIVE before operational mutations.
- Monitoring, escalation and runbooks are exercised in a non-production environment.
- Restore evidence and recovery ownership are verified.
- Charter C-07 remains open for production until these controls pass.

### G0.3 Repository governance and AI review evidence

**Current status:** NOT_APPLIED / NOT_VERIFIED — main remains unprotected.

Required controls:
- All changes to main enter through pull requests; direct-to-main changes must be prohibited.
- Require strict/up-to-date status checks, conversation resolution and administrator enforcement.
- Require seven exact contexts: Contract tests (ubuntu-24.04), Contract tests (windows-2025), Contract tests (macos-15), OpenAPI and required repository files, KM1 application integration (PostgreSQL 16), Repository Governance Review and AI Reviewer Evidence.
- Require no force-push and no branch deletion; keep ruleset bypass actors empty.
- Native GitHub approving-review count is zero by design: GOV-01 is the only human internal authority; AI delegates are not GitHub human actors. GOV-11 supplies a transparent report validated by CI; GOV-01 retains the final merge decision.
- Personal-repository GitHub push-restriction lists for named users/teams/apps are not available; enforce PR-only changes and no bypass instead.
- Initial bootstrap before PR #28 merges uses the local admin script with a repository token carrying Administration: write. After merge, the Repository Main Protection workflow can manage later changes. Never paste the token into chat or commit it.

The current connected GitHub action surface does not expose branch-protection/ruleset mutation. Therefore this roadmap records the exact target configuration but does not claim to have applied it.

Acceptance:
- GitHub reports main protected or the applicable ruleset active.
- Required checks match the workflow's actual job names.
- A test PR demonstrates that missing review/checks prevent merge.
- Force push and branch deletion are denied under the active rule.
- The observed settings and test evidence are recorded.

### KM 0 exit gate

KM 0 may be ACCEPTED only when:
- The canonical Charter/MVP decision state is synchronized to main.
- Project scope, MVP non-goals and acceptance baseline are approved.
- GOV-01 authority and delegate limits are recorded.
- Every critical governance/operational decision has an accountable human owner or explicitly accepted interim human coverage.
- GOV-07 operational accountability is resolved for the next intended environment.
- Every internal workstream has a designated GOV role; GOV-01 is the only human decision authority and the other roles are AI delegates. Production operational controls must be provisioned and tested before workloads.
- GOV-07 role allocation is resolved; its runtime, monitoring, backup/restore and incident controls must be verified before production.
- Repository controls are enforced or a documented, human-approved exception defines a safe non-production-only scope and expiry.
- Initial risk register, prioritized backlog, dependencies and change control are active.
- Every P0 item has passed or a specific authorized decision explicitly defers it without misrepresenting KM 0 as closed.

Until then, KM 0 remains OPEN. Contract-test and documentation work may continue in parallel if it does not require privileged/production operations.

## 6. KM 1 — Technical foundation and canonical contract

**Current status:** PARTIAL.  
**Implemented evidence:** manifest/event schemas, OpenAPI contract, positive/negative fixtures, cross-platform contract CI, contract-tooling bootstrap, local policy reference tests.

### Work package K1.1 — Accept the technology direction

- Complete a narrow FastAPI proof-of-fit against the existing OpenAPI 3.1 contract.
- Demonstrate request/response validation, health endpoint, error envelope, correlation ID and a deterministic demo endpoint.
- Demonstrate PostgreSQL connectivity and one reversible migration using the proposed data-access approach.
- Record developer capability and operational trade-offs.
- Compare NestJS only if the proof-of-fit shows Python/FastAPI is not maintainable by the accountable engineering capacity.
- Keep exact cloud provider, region, OIDC issuer, KMS/secret manager, object-store vendor and spending decisions open until security, residency, operations and budget evidence exists.
- Have authorized role holders accept or amend ADR-011. A recommendation is not an accepted ADR.

### Work package K1.2 — Reproducible application environment

After ADR-011 acceptance:
- Define the supported application runtime and exact dependency lock method.
- Generate the lockfile through the selected dependency tool; do not hand-invent transitive pins or hashes.
- Add local configuration examples without secrets.
- Add a reproducible PostgreSQL development service and explicit migration/rollback workflow.
- Add formatting, lint, static typing and application test commands.
- Make CI exercise contract tests, application tests, migration checks and dependency consistency on the declared supported environments.
- Keep contract tooling and the application runtime clearly distinguished.
- Document clean checkout, bootstrap, test, database reset and recovery procedures.

### Work package K1.3 — Contract hardening

- Validate the canonical capability manifest and event envelope with positive, negative and boundary fixtures.
- Validate OpenAPI structure and representative request/response schemas.
- Test semantic/version compatibility and deterministic error behavior.
- Document idempotency, pagination, correlation, timestamps, error codes and schema evolution.
- Add architecture fitness checks for prohibited cross-domain dependencies.
- Verify no test secrets or real credentials are committed.

### KM 1 exit gate

KM 1 may be ACCEPTED only when:
- ADR-011 has an explicit accepted decision and required consultations.
- A clean checkout reproduces the documented application development environment.
- Database migrations apply, roll back and reapply in a clean test environment.
- Contract, application, lint, type, dependency and migration checks pass on the exact commit.
- No required check is NOT_RUN, BLOCKED or UNVERIFIABLE without an explicit accepted exception.
- Contract fixtures include valid, invalid, boundary and compatibility cases.
- Architecture, security and repository documentation match the implementation.
- The independent reviewer accepts the test evidence.

Do not begin KM 2 implementation until KM 1 is ACCEPTED. Registry data models and test scenarios may be prepared as design work only.

## 7. KM 2 — Universal Capability Registry

**Current status:** NOT STARTED — design preparation only.

Implementation sequence:
1. Publisher and capability identity model with stable namespaces.
2. Canonical manifest ingestion and schema-version validation.
3. Draft, validated, published, deprecated, revoked and quarantined lifecycle states.
4. Immutable published versions and artifact digest/provenance records.
5. Persistence migrations, constraints and duplicate detection.
6. Registration, lookup, version-listing and discovery API.
7. Audit events for registration, validation, publication and revocation.
8. Import staging for candidate records, including provenance, schema, duplicate and approval checks.

Acceptance:
- Valid capability registration succeeds with stable identity.
- Invalid, duplicate, untrusted or incompatible manifests are rejected or quarantined deterministically.
- Draft metadata may change under policy; published artifacts and versions cannot be silently mutated.
- Every published version records immutable digest, provenance, schema version and publisher.
- Discovery returns only records permitted by visibility policy.
- Lifecycle and publication actions create attributable audit evidence.
- Integration tests cover tenant/publisher isolation and unauthorized access.

The earlier 427 candidate records remain an unverified migration inventory, not a publishable product count. No bulk publication is permitted without staging and review.

## 8. KM 3 and KM 4 — Access, distribution and managed execution

### KM 3 — Identity, Access and Distribution

**Current status:** NOT STARTED.

Build in this order:
1. Shared identity-policy-engine and canonical authorization decision contract.
2. API key lifecycle: generation, verifier storage, scope, rotation, revocation and audit.
3. Credential-vault adapter backed by an approved managed secret service; never invent a home-grown production root-key vault.
4. MCP authentication/authorization adapter.
5. REST/HTTP gateway.
6. Custom REST/API and MCP connector onboarding with endpoint validation, SSRF defenses, egress policy, credential isolation and quarantine.

Acceptance:
- OIDC issuer, audience, signature, expiry, issuer and scopes are verified.
- Every invocation is authorized against identity, capability, operation, tenant, quota and entitlement.
- REST and MCP produce equivalent authorization outcomes for the same principal and action.
- Expired, revoked, insufficient-scope, cross-tenant and over-quota calls are denied.
- Connector access cannot bypass policy.
- Logs and responses do not disclose credentials or sensitive payloads.

### KM 4 — Managed Execution Runtime

**Current status:** NOT STARTED.

Build:
- Invocation/job lifecycle and durable state.
- Managed worker and queue or database-backed job/outbox implementation.
- Isolation, CPU/memory/time/concurrency/payload limits and egress controls.
- Cancellation, timeout, retry, idempotency and quarantine behavior.
- Immutable artifact binding and digest verification.
- Invocation identity, policy decision and tenant propagation.

Acceptance:
- The registered demo capability runs in an isolated managed worker.
- Resource limits and cancellation are observed in tests.
- A failed, timed-out or cancelled job has deterministic state and audit evidence.
- A runtime cannot execute an unverified artifact or exceed its authorized scope.
- Failure and retry tests prove no duplicate side effect where idempotency is required.

## 9. KM 5 and KM 6 — Evaluation, observability and synchronization

### KM 5 — Evaluation and Observability

**Current status:** NOT STARTED.

Build:
- Invocation-wide trace and correlation across client, gateway, policy, registry, worker and result.
- Structured logs, metrics and redaction.
- Evaluation records linked to capability version and artifact digest.
- Contract, compatibility, security and regression runners.
- Release gate for missing, stale, failed or incomplete evaluation evidence.
- Dashboards and alerts for failure rate, latency, queue delay, cost and critical security events when workload data exists.

Acceptance:
- An invocation can be reconstructed from its trace and audit events.
- Evaluation results are reproducible and tied to a precise artifact version.
- Secrets and sensitive payloads are not exposed in ordinary logs.
- A release cannot pass when required evidence is absent or failed.

### KM 6 — Adaptive Synchronization

**Current status:** NOT STARTED.

Build:
- Desired-state and observed-state records.
- Idempotent reconciliation loop.
- Risk classification with approval, test, rollout and rollback policy.
- Compatibility/dependency checks before propagation.
- Canary and bounded staged rollout.
- Immutable known-good release pointer and rollback workflow.
- Complete synchronization decision, approval and audit timeline.

Acceptance:
- Compatible low-risk changes propagate within approved policy.
- Breaking/high-risk changes are held for required approval.
- Failed rollout restores the exact known-good artifact/version.
- Reconciliation is safe to retry and does not create duplicate or divergent state.
- Registry visibility or marketplace listing never grants runtime execution permission.

## 10. KM 7–KM 10 — Expansion and production

| Stage | Planned scope | Hard prerequisite |
|---|---|---|
| KM 7 | A.S.F.R.E.E Canonical first; Legacy adapter; Skill Analyzer; Anatomi Prompt v3; gateway consolidation | KM 3–KM 6 stable contracts and one complete governed lifecycle |
| KM 8 | Self-hosted runtime enrollment, revocation, SDKs, platform adapters, independent clients | KM 3 trust and KM 4 execution contracts |
| KM 9 | External publisher, listing, entitlement, licensing, moderation and commerce | Qualified legal review, identity, security, entitlement and support operations |
| KM 10 | Independent security, load/soak/resilience, tenant isolation, backup/restore/DR, incident and production readiness | All production-relevant predecessors accepted and GOV-07 operational ownership active |

KM 9 remains intentionally deferred until legal, licensing, privacy, tax, moderation and commerce responsibilities are approved. KM 10 is an evidence-based operations programme, not a final documentation sprint.

## 11. Backlog and accountable decision routing

| ID | Priority | Work package | Accountable decision / owner role | Dependency | Current state |
|---|---|---|---|---|---|
| PC-001 | P0 | Review and synchronize PR #13; read back six canonical files | GOV-01; independent reviewer | Existing PR #13 | BLOCKED ON REVIEW/MERGE |
| PC-002 | P0 | Assign GOV-07 or accept a named human interim operations owner | GOV-01 | Human acceptance and role evidence | BLOCKED |
| PC-003 | P0 | Enforce main ruleset and required CI/review controls | GOV-01 / repository owner | Independent human reviewer; settings access | BLOCKED |
| PC-004 | P0 | KM 0 exit review and risk/decision-owner reconciliation | GOV-01 | PC-001 to PC-003 | PLANNED |
| PC-005 | P1 | Execute FastAPI/OpenAPI/PostgreSQL proof-of-fit and accept ADR-011 | GOV-01 with architecture, engineering, security and operations consultation | PC-002; technical capacity | PLANNED |
| PC-006 | P1 | Build reproducible application environment, database migrations, lint/type/test CI | Engineering owner under accepted ADR | PC-005 | PLANNED |
| PC-007 | P1 | KM 1 independent exit evaluation | GOV-01; independent reviewer | PC-005 and PC-006 | PLANNED |
| PC-008 | P1 | Implement Registry identity, manifest, persistence, immutable versions and discovery | Engineering owner | PC-007 | NOT STARTED |
| PC-009 | P2 | Implement shared identity/policy core and REST/MCP gateway | Engineering/security owners | PC-008 | NOT STARTED |
| PC-010 | P2 | Implement managed execution runtime and isolation | Engineering/operations owners | PC-009 | NOT STARTED |
| PC-011 | P2 | Implement evaluation, trace, metrics and audit evidence | Evaluation/operations owners | PC-009 and PC-010 | NOT STARTED |
| PC-012 | P2 | Implement desired/observed sync, staged rollout and rollback | Architecture/engineering/operations owners | PC-008, PC-010 and PC-011 | NOT STARTED |
| PC-013 | P3 | First-party integrations and hybrid distribution | Product/architecture owners | KM 3–KM 6 accepted | DEFERRED |
| PC-014 | P3 | Marketplace and production hardening | GOV-01 with legal/security/operations approval | Publisher/legal/entitlement and recovery gates | DEFERRED |

Role labels are accountable functions, not assertions that vacant human positions or inactive AI runtimes are occupied. Task assignees and due dates remain unassigned until accepted by the relevant person. Do not convert a role label into a person assignment.

## 12. Risk, control and recovery register

| Risk | Severity | Control / trigger | Stop or recovery action |
|---|---|---|---|
| PR #13 decisions not canonical on main | P1 | PR review, merge and six-file read-back | Keep governance sync OPEN; do not claim canonical status |
| GOV-07 has no owner | P1 | Human appointment or human-approved interim coverage | No hosted production workload |
| Main branch unprotected | P1 | Active ruleset, independent review and required CI | Hold privileged merges and delegate activation |
| ADR-011 is only recommended | P1 | Proof-of-fit and authorized decision | Do not build provider-specific application infrastructure |
| Contract tooling mistaken for app runtime | P1 | Explicit environment boundary and application CI | Keep KM 1 PARTIAL |
| Registry started before KM 1 acceptance | P1 | Stage dependency and KM 1 exit review | Stop implementation; allow design preparation only |
| Local policy evaluator mistaken for gateway | P1 | External gateway and bypass-resistance tests | No delegate activation or privileged mutation |
| WORM design mistaken for provisioned storage | P1 | Object-lock, deletion-denial, retention and restore evidence | Keep A7 open; no production privileged workload |
| Scope expansion / premature microservices | P2 | MVP boundary, modular monolith and ADRs | Defer unrelated modules |
| Unverified 427-record import | P1 | Staging, provenance, schema, duplicate and review controls | Quarantine; never bulk-publish |

## 13. Evidence and Definition of Done

Every work package must produce a compact evidence record containing:
- Work ID and requirement IDs.
- Owner role, actual assignee where accepted, and accountable approver.
- Baseline branch and commit SHA.
- Changed file paths and read-back state.
- Exact tests run, environment, expected/actual result and status.
- CI run URL and exact tested head SHA.
- Security/privacy review and residual risks where relevant.
- Decision/approval reference.
- Current implementation, verification and release state.
- Blockers, exceptions, recovery and next gate.

A work package is DONE only when:
1. Scope and acceptance criteria are explicit.
2. Required implementation exists on a named commit.
3. Relevant tests actually ran and passed.
4. Independent review and accountable acceptance are recorded.
5. Source documents, tracker, versions and links are consistent.
6. No critical P0/P1 blocker remains undisclosed.
7. Deployment/release is claimed only when target read-back proves it.

### Global stop conditions

Stop the affected work package when authority is ambiguous, GOV-01 approval is required but missing, the baseline changes unexpectedly, secrets are exposed, a critical security/privacy risk is uncontrolled, a required test fails, a provider/credential is unavailable, or rollback is not viable. Preserve partial progress and report the exact blocker; do not mark the task Done.

---

**Executive decision:** HSMART is not ready to enter KM 2. Close the canonical governance synchronization and KM 0 controls, then complete KM 1 and accept its exit gate. The Registry is the next major implementation milestone, not the next activity to start before its prerequisites pass.
