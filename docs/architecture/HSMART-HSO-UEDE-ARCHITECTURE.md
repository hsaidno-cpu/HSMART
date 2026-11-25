# HSMART–HSO Unified Ecosystem and UEDE Architecture

**Status:** Proposed architecture baseline for GOV-01 review; not yet accepted, deployed, or production-operational.  
**Date:** 2026-11-25  
**Decision scope:** HSMART, Hypersystem-Orchestrator (HSO), Universal Ecosystem Development Engine (UEDE), and Progressive Roadmaps Evaluation (PRE).

## 1. Executive decision

Adopt a **hybrid, federated-repository architecture**:

- HSMART and HSO are one logically unified, mutually developing ecosystem.
- Keep HSMART and HSO in their existing canonical repositories. Do not merge them into a monorepo or transfer HSO source into HSMART at this stage.
- UEDE is a shared logical development control plane, implemented as modular components with explicit contracts and adapters. It may be deployed as an independently scalable service, while using HSMART platform services and HSO capabilities.
- PRE is the authoritative direction-setting and progress-evaluation source. UEDE consumes approved roadmap state and writes execution evidence through governed interfaces; it must not silently redefine strategic objectives, acceptance criteria, or authority.
- HSO supplies the engineering capabilities (skills, plugins, subskills, scripts, agents, orchestration and specialist workflows) that UEDE discovers and invokes to develop both HSMART and HSO.
- HSMART supplies shared foundation services (identity, authorization, registry, API/MCP gateway, data, secrets, audit, runtime and policy) as they become implemented and accepted.

This is a **unified ecosystem with separated source ownership and deployable boundaries**, not two competing systems and not a premature repository merger.

## 2. Why hybrid is the correct current choice

The current HSMART project record shows its foundation is still progressing through KM gates: KM 0/KM 1 acceptance and protection/assurance work remain open in the latest documented baseline; KM 2 and later platform capabilities are gated or in progress. It would be unsafe to assume that every planned HSMART service is already operational.

HSO already has a substantial central ecosystem repository: plugin identity catalog, instruction snapshots, compatibility/distribution registries, plan-only workflow planning, a controlled sandbox super-orchestrator runtime, and tests. Its README explicitly states a hybrid multi-repository model for plugin source ownership.

Therefore:
1. Preserve HSO's existing capability inventory and engineering assets.
2. Preserve HSMART's canonical foundation roadmap and governance gates.
3. Define the integration contract now, without claiming runtime integration that has not been tested.
4. Build UEDE in staged increments, starting read-only and then adding bounded execution.
5. Revisit deployment topology only after HSMART service contracts and UEDE adapters have passed acceptance tests.

## 3. System responsibilities

| System | Owns | Does not unilaterally own |
|---|---|---|
| HSMART | Shared platform foundation, identity, policy, data, registry, distribution/gateway, execution services, audit and platform governance | HSO plugin source ownership or strategic PRE roadmap decisions |
| HSO | Ecosystem capability catalog, plugin/skill/subskill/script/agent orchestration, routing, capability selection, engineering workflows and adapters | HSMART core security policy, identity authority, PRE strategic baseline |
| UEDE | Cross-ecosystem development control loop, task selection, execution coordination, verification orchestration, evidence reconciliation and capability-gap detection | Independent authority to change governance, grant itself privileges, approve its own critical changes |
| PRE | Roadmap lifecycle, objectives, phases, milestones, dependencies, baseline, evaluation, adaptation and closure | Code execution, repository write authority, independent acceptance of its own implementation |
| GitHub | Canonical source, branch/PR history, CI results and merged engineering evidence | Notion roadmap authority or runtime truth beyond evidence actually recorded |
| Notion | Human-readable project control and PRE records, decisions, operational context | Canonical source code or proof of a CI/runtime result not linked to evidence |

## 4. UEDE logical architecture

UEDE should be composed of bounded modules behind versioned interfaces:

1. **Roadmap Adapter & Intelligence** — reads PRE roadmap versions, approved work items, dependencies, gates and acceptance criteria.
2. **Capability Discovery & Registry Adapter** — queries HSO catalog and capability state; filters by owner, version, host compatibility, trust, rights, permissions and readiness.
3. **Task Decomposition & Policy Planner** — turns an eligible roadmap item into a bounded execution plan and explicit acceptance mapping.
4. **Workflow Controller** — manages scheduling, idempotency, leases, retries, cancellation, timeout, durable state and recovery.
5. **Engineering Worker Adapter** — dispatches approved work to OpenHands or another replaceable worker inside isolated workspaces.
6. **Verification & Assurance Coordinator** — runs repository-native tests, CI, contract checks, security checks and independent evidence review.
7. **Evidence & Roadmap Reconciler** — records commit SHA, PR, workflow run, test results, review disposition and roadmap transition evidence.
8. **Capability Evolution Manager** — detects missing capabilities and proposes new HSO skills/plugins/scripts or HSMART services, subject to source rights, tests and approval.
9. **Governance Guard** — enforces identity, least privilege, risk tier, approval policy, immutable audit and protected recovery controls.

No module may treat a planned service as deployed merely because its interface is documented.

## 5. Runtime placement and FLOSS components

Preferred initial runtime composition:

- **Kestra (Apache-2.0):** workflow scheduling, event triggers, retries and durable workflow coordination.
- **OpenHands (MIT):** replaceable software-engineering worker for bounded repository tasks.
- **LangGraph (MIT, optional):** complex stateful reasoning only when simple deterministic planning is insufficient.
- **GitHub Actions:** repository-native CI and validation.
- **HSMART services:** shared identity, policy, audit, secrets, persistence and gateways when their KM acceptance gates are passed.
- **HSO adapters:** capability discovery, capability invocation and specialist handoffs, only where real host invocation is verified.

Kestra and OpenHands are runtime components, not UEDE's canonical control logic. UEDE must remain portable and must not depend on either implementation's proprietary internal state. Do not introduce LangGraph until an evidenced use case requires it.

## 6. PRE integration contract

PRE remains the direction-setting authority. UEDE consumes a versioned, read-only roadmap snapshot containing at minimum:

- roadmap ID and revision;
- approved objective, scope and non-goals;
- phase/milestone/work-item identifiers;
- dependency references and eligibility;
- priority and risk;
- acceptance criteria and required verification;
- approval policy and decision authority;
- current state, blockers and evidence references.

UEDE must not:
- invent progress, owners, dates, approvals or test outcomes;
- mark a milestone accepted based solely on an agent's self-report;
- edit an approved baseline or acceptance criteria to make a failing task pass;
- overwrite historical roadmap revisions;
- count NOT_RUN, NOT_ASSESSED, HOLD, FAIL or BLOCKED as PASS.

Write-back is restricted to execution facts and evidence references through an authorized PRE/HSMART API. Any proposed replan is a proposal/new revision requiring the PRE-defined decision authority.

## 7. Bidirectional HSMART–HSO development

The systems can develop one another through explicit requests and contracts:

- UEDE may route an HSMART platform task to HSO engineering capabilities.
- UEDE may route an HSO capability/catalog/runtime task to HSMART platform services and HSO engineering capabilities.
- HSMART services may provide authenticated registry, policy, execution, audit and data interfaces to HSO.
- HSO capabilities may propose or implement HSMART changes through isolated branches and PRs.
- A capability created to solve a gap must itself pass provenance, rights, schema, compatibility, security, test and release gates before becoming eligible for future autonomous use.

This is bidirectional collaboration, not an uncontrolled circular dependency. Shared contracts must be versioned; dependency direction, ownership and recovery paths must be explicit.

## 8. Autonomy and approval tiers

| Tier | Allowed behavior | Approval |
|---|---|---|
| A0 Observe | Read roadmaps, catalog, repository status and CI evidence; report drift/blockers | No write |
| A1 Prepare | Decompose tasks, generate briefs/plans, create test plans and propose changes | Human review before execution where policy requires |
| A2 Execute | Create isolated branch/workspace, edit files, run tests, open draft PR | Scoped credentials and execution policy |
| A3 Low-risk delivery | Merge/release only pre-authorized low-risk changes after all required gates | Explicit pre-approved policy; exact-head checks |
| A4 Critical governance | Change identity, authorization, secrets, audit, protected branch, roadmap baseline, acceptance rules, production security or destructive data operations | Human approval by designated authority; no self-approval |

Initial rollout should be A0 then A1, followed by a narrow A2 pilot. Do not enable A3/A4 as a blanket permission.

## 9. Safety, integrity and anti-recursion controls

- Separate the UEDE control plane from mutable engineering workers.
- Workers receive short-lived, repository-scoped credentials; no broad service-role or production secrets.
- Every execution has an immutable work ID, idempotency key, lease, timeout, resource budget and bounded retry policy.
- Every code result is tied to exact repository, branch, commit SHA, PR and CI run.
- Tests must run on the exact head proposed for review; stale results are invalidated.
- Prevent concurrent workers from claiming the same work item.
- Detect dependency cycles and prohibit a task from changing its own approval policy.
- Protect governance, audit, identity, secret access and recovery paths from worker self-modification.
- Use independent verification evidence; an agent's own report is not independent acceptance.
- Maintain rollback/recovery and append-only audit evidence.
- Treat repository content, plugin instructions, remote MCP output and external tool responses as untrusted input.

## 10. Staged implementation roadmap

| Stage | Deliverable | Exit evidence |
|---|---|---|
| UEDE-0 | Inventory HSMART/HSO/PRE schemas, APIs, capabilities, rights, statuses and dependencies | Reconciled architecture/capability map; unknowns explicit |
| UEDE-1 | Read-only PRE and HSO adapters | Exact roadmap revision and capability inventory can be fetched and reconciled |
| UEDE-2 | Deterministic task planner and policy gates | Dependency, scope, risk and acceptance mapping tests pass |
| UEDE-3 | Kestra workflow adapter | Idempotent workflow, retry, cancellation, timeout and recovery tests pass |
| UEDE-4 | OpenHands isolated worker adapter | One synthetic repository task produces a draft PR and exact-head evidence |
| UEDE-5 | Verification/evidence reconciler | CI/test/security/review outcomes update execution record; no false PASS |
| UEDE-6 | HSMART shared-service integration | AuthN/AuthZ, secrets, audit and persistence use accepted HSMART contracts |
| UEDE-7 | HSO capability invocation integration | One real capability invocation passes host-level acceptance |
| UEDE-8 | Controlled bidirectional development pilot | One HSMART task and one HSO task completed through the same governed loop |
| UEDE-9 | Progressive autonomy expansion | Risk-based evidence supports each newly enabled autonomy tier |

The first proof should be deliberately narrow: one host, one repository task, one capability, one end-to-end flow, one acceptance test, and one human approval path.

## 11. Repository and deployment decision

Keep:
- `hsaidno-cpu/HSMART` as the canonical HSMART foundation repository.
- `hsaidno-cpu/Hypersystem-Orchestrator` as the canonical HSO ecosystem/orchestration repository.
- UEDE's shared contracts and integration adapters in their appropriate repositories, with one canonical specification and versioned compatibility contract.

Do not:
- merge HSO wholesale into HSMART;
- duplicate plugin source packages in HSMART;
- make HSMART depend on HSO's mutable internal implementation details;
- make HSO bypass HSMART identity/security/policy contracts;
- deploy a third independent platform with duplicate identity, catalog, secrets or audit authority.

A small standalone UEDE runtime/deployment may be appropriate, but it is not a third source-of-truth repository by default. Keep the runtime replaceable and the logical control plane governed by the unified ecosystem.

Reassess monorepo or repository consolidation only after HSMART KM foundation gates, HSO canonical-source/rights controls, cross-repository contracts, CI and rollback are proven. A repository merge is not a prerequisite for unified operation.

## 12. Current known blockers and non-claims

- HSMART's documented foundation and service roadmap is not fully accepted or operational; verify latest exact PR/main state before planning execution.
- HSO has a mature catalog/planner/sandbox baseline, but catalog presence does not prove a plugin is host-activated or executable.
- PRE's shared competency learning/runtime is specified but not deployed; its canonical source and licensing status have previously been recorded as unresolved.
- Live generic HSO plugin dispatch and broad Remote MCP execution are not established merely by sandbox tests.
- No UEDE runtime, Kestra deployment, OpenHands worker deployment, live PRE adapter, or end-to-end HSMART↔HSO autonomous loop is claimed by this document.

## 13. Acceptance criteria for this architecture

- [ ] GOV-01 records the architecture disposition against this document's commit/PR head.
- [ ] HSMART and HSO remain separate canonical source repositories under one ecosystem identity.
- [ ] PRE adapter reads an exact approved roadmap revision without mutating it.
- [ ] HSO adapter returns capability status, owner, version, rights, permissions and evidence.
- [ ] Task planner rejects unresolved dependencies, unknown capability readiness and policy violations.
- [ ] Worker execution is isolated, scoped, idempotent and exact-SHA traceable.
- [ ] CI and verification are tied to the exact PR head.
- [ ] Human approval is enforced for critical changes.
- [ ] Evidence reconciliation never promotes unverified work to accepted progress.
- [ ] One end-to-end synthetic task passes before broader autonomy is enabled.

## 14. Decision record

**Recommended disposition:** ACCEPT THE HYBRID ARCHITECTURE AS THE TARGET DESIGN, subject to GOV-01 review and staged implementation. This is a proposed engineering architecture, not a claim that deployment or integration has already occurred.

**Core principle:** one ecosystem, two canonical systems, one governed development loop, replaceable runtimes, explicit contracts, and evidence-based autonomy.


## 15. Owner-prioritized UEDE delivery sequence (P0–P9)

The following order is normative for UEDE delivery. It is a single dependency-aware workstream, not a second project or a parallel release train. Every implementation change must land in the repository that owns the affected artifact and pass that repository's existing PR, CI, security, architecture and KM acceptance gates.

| Priority | Work | Allowed scope before prerequisites pass | Exit evidence |
|---|---|---|---|
| P0 | Review and establish this architecture through HSMART PR #32 and HSO PR #25 | Documentation, architecture reconciliation and evidence review only | Both documents agree on ownership, contracts, autonomy, gates and PR sequencing; exact-head CI is green; GOV-01 records the decision against the exact PR heads |
| P1 | Audit HSO capabilities that can develop HSMART and HSO | Read-only inventory of source, skills, ownership, rights, version, parity, permissions and host readiness | Capability-to-task matrix distinguishes documented, source-verified, rights-cleared, host-tested and invocation-ready states |
| P2 | Audit PRE schema, API and actual implementation | Read-only inspection of PRE specification, Notion data source, queue, HSO Mission Control schema, integrations and deployed endpoints | Authority map, schema/revision baseline, API availability and deployment evidence; unavailable components explicitly marked NOT_DEPLOYED |
| P3 | Define UEDE Core Contracts and adapter interfaces | Versioned schemas and contract tests; no platform migration | RoadmapSnapshot, CapabilityDescriptor, TaskPlan, ExecutionRequest, ExecutionReceipt, VerificationEvidence, ApprovalReceipt and ReconciliationRecord contracts validated for compatibility |
| P4 | Implement PRE Read-only Adapter | Read-only access to the currently authorized PRE/roadmap source; immutable snapshot and pagination/freshness proof | Exact approved revision is fetched reproducibly; digest and provenance recorded; no roadmap, stage, approval or scope mutation is possible |
| P5 | Implement HSO Capability Discovery Adapter | Read-only access to HSO catalog, instruction index, rights, distribution, compatibility and runtime readiness | Adapter reports owner, source pin, version, rights, parity, host, permissions, readiness and evidence without treating catalog presence as invocation |
| P6 | Implement deterministic task planner | Reuse and extend the existing HSO plan-only planner; do not create a competing planner | Same input revision produces the same ordered plan; unresolved dependencies, cycles, stale evidence, rights gaps and unavailable capabilities fail closed |
| P7 | Integrate Kestra and OpenHands | Adapter-level integration behind disabled-by-default execution flags | Kestra recovery/idempotency tests pass; OpenHands runs in isolated, ephemeral workspaces with scoped credentials, resource/network limits and no approval or governance authority |
| P8 | Test one end-to-end autonomous engineering workflow | One synthetic, low-risk task on a non-production repository/branch | PRE read → HSO discovery → deterministic plan → isolated worker → exact-head CI → independent artifact read-back → execution receipt → owner decision, all traceable |
| P9 | Enable progressive autonomous execution | Increase autonomy only one evidenced risk tier at a time | Each tier has explicit scope, policy, rollback, observability, cost limit and acceptance evidence; no blanket autonomous merge or production authority |

### 15.1 Current source and gate baseline (2026-11-25)

- HSMART PR #32 and HSO PR #25 are documentation-only architecture proposals and remain drafts pending exact-head validation and the owner decision. Their open state is not architecture acceptance.
- HSMART KM 0 remains OPEN and KM 1 remains IN_PROGRESS in the latest project control record. KM 2 and later remain blocked until KM 1 is formally accepted. HSMART PR #30 and PR #31 retain their own scope and gates; UEDE must not merge, retarget or absorb them.
- HSMART PR #32's current AI Reviewer Evidence run failed because the expected GOV-11 report file was absent. This is an evidence-artifact failure, not proof that the architecture tests themselves failed. A review report must disclose its correlation limits and must not claim GitHub-native approval.
- HSO PR #25's current catalog-validation run failed one existing compatibility-matrix assertion: the test expects `INTERFACE_DEFINED_NOT_EXECUTED` while the checked-out matrix contains `CONTRACT_TESTED`. Catalog and distribution validation steps passed. Reconcile this against the approved PR/base sequence; do not change a test or status merely to make the check green.
- HSO PR #15 remains an upstream governance/contract dependency with unresolved technical review findings and exact-head evidence obligations. PR #24, PR #16 and PR #17 remain stacked on its branch. UEDE work must not retarget, merge, reorder or bypass those dependencies.
- HSO Mission Control currently has five source registrations marked `not_configured`; its synced work-item table has no imported roadmap rows. Its Supabase schema is not evidence of a deployed PRE runtime or a live PRE API.
- The HSMART platform services planned for identity, policy, gateway, registry, runtime, secrets and audit must be treated as unavailable until their own KM acceptance and live service evidence exist. Read-only adapters may use separately authorized sources; they must not impersonate HSMART platform services.

### 15.2 Capability and PRE audit disposition

The HSO catalog currently indexes 23 plugin identities and 265 skill definitions. The following are the relevant engineering/development candidates; these labels are readiness observations, not invocation permission:

| Capability | Recorded evidence | Current limitation | UEDE treatment |
|---|---|---|---|
| Skill Developer Orchestrator (SDO) | Canonical SPDO source v0.1.0; Apache-2.0; package version also 0.1.0 | 0/4 instruction files match the package/source comparison; no general live host invocation receipt | Preferred skill/plugin lifecycle engineer after parity disposition; not assumed to be a HSMART code executor |
| A.S.F.R.E.E | Canonical private source v0.5.0-rc.1; 13 indexed skills; technical forensics, remediation, runtime lab, QA and security governance | PolyForm Noncommercial; package is behind and instruction drift exists | Suitable only within granted non-commercial rights and after source/package parity and host gates |
| SKILL ANALYZER | Source v1.3.0; 12 indexed skills; analysis/evidence/audit support | No source license declaration; package behind and instruction drift; generic plugin dispatch is not configured | Analysis support only until rights and invocation are resolved |
| Plugin Agent Orchestrator | 44 indexed skills covering code, test, runtime, integration, security and agent lifecycle | Canonical source repository not identified; package/snapshot presence only | Candidate design inventory, not an executable engineering workforce |
| Ponytail Engineering System | 9 indexed skills; bounded software engineering and review methodology | No canonical source repository identified; explicitly does not own writes/commits/PRs/merges | Use as design/method reference only until source and runtime are verified |
| Progressive Roadmap Evaluator (PRE) | v0.1.1 package specification; 1 master + 8 specialist skills; 32 behavioral acceptance specifications | No canonical Git source or declared license; shared runtime and learning federation are SPECIFIED_NOT_DEPLOYED | Roadmap authority by approved records; no assumed PRE API or autonomous runtime |

HSO's existing plan-only planner and controlled sandbox runtime are reusable foundations. The sandbox can write and verify a local artifact; generic `plugin.skill.invoke` and generic `mcp.remote.invoke` remain NOT_CONFIGURED. A narrow SKILL ANALYZER Remote MCP pilot does not establish a generic capability adapter or live PRE invocation.

The PRE/roadmap audit currently finds an HSO Master Roadmap & Milestones Notion data source with 20 records, R0–R9 lifecycle properties, dependencies, gate state, approvals and evidence fields. This is the observed roadmap record, not proof that the PRE package has a deployed API. PRE's shared runtime remains SPECIFIED_NOT_DEPLOYED; a canonical PRE Git source and license declaration are missing. HSO Supabase is an HSO Mission Control store, not a PRE database: its five source registrations are all `not_configured`, its `hso_work_items` table has zero rows, and no successful source synchronization has been recorded.

### 15.3 Mandatory integration invariants

1. **One delivery path:** UEDE schedules and supervises work inside existing repository branches, PRs, CI and acceptance systems. It does not create an alternate merge lane, parallel roadmap, shadow catalog or duplicate execution ledger.
2. **One human decision authority:** GOV-01 is the sole human approval authority defined for HSMART/HSO. No second human engineering reviewer or separate human security approver is required. Technical reviews, AI assurance, tests and security checks are supporting evidence, not human approval and not a fabricated GitHub `APPROVED` review.
3. **No gate inheritance by proximity:** a green UEDE test cannot satisfy a HSMART KM gate, an HSO source-rights gate, a PRE transition gate or a repository protection requirement unless that exact gate explicitly accepts the evidence.
4. **Read-only before write:** P4/P5 remain read-only. P6 may produce plans, not dispatch. P7/P8 may execute only within a named synthetic scope and explicit credential policy. No production or HSMART foundation write is enabled by architecture acceptance.
5. **KM protection:** no UEDE task may advance HSMART to KM 2+ before KM 1 is formally accepted. A KM status cannot be inferred from merged PRs or green CI alone.
6. **No self-acceptance:** the executor cannot approve its own result, alter its acceptance criteria, edit its authority policy or promote its own capability state.
7. **Fail closed:** missing roadmap revision, incomplete pagination, stale source, unresolved rights, instruction drift, unknown host, absent permission, unverified CI head or missing evidence blocks execution.
8. **Evidence binding:** each task and result binds to PRE revision/digest, capability source/version, repository, branch, commit SHA, PR, CI run, test output, verifier and owner disposition.
9. **No parallel source of truth:** HSMART and HSO retain canonical source ownership; Notion provides governance/roadmap records; GitHub provides source/PR/CI; UEDE keeps only the minimal execution state and receipts required for deterministic recovery.

**P0 exit condition:** PR #32 and PR #25 may be considered architecturally established only after their contract text is reconciled, the exact-head evidence checks pass, the PR dependency graph remains intact, and GOV-01 records a decision against the exact final heads. Merge is a separate action and remains subject to the existing repository and KM gates.


## 15. Human approval and manual-action notification contract

HSMART adopts [HAP-01 — Human Approval, Manual Action & Notification Procedure](https://github.com/hsaidno-cpu/Hypersystem-Orchestrator/blob/main/governance/HUMAN-APPROVAL-AND-ACTION-NOTIFICATION-PROCEDURE.md) as the canonical cross-ecosystem procedure. HSMART's integration-specific obligations are captured in [UEDE Human Action Integration](../governance/UEDE-HUMAN-ACTION-INTEGRATION.md).

GOV-01 is the sole human decision authority. Human approval is distinct from a manual UI action. When either is required, the workflow must stop at the gate and provide the owner with the exact repository, PR/issue, branch, base and head SHA, direct UI link, precise UI location, numbered instructions, expected result, risk, forbidden premature actions and staleness conditions. One idempotent record must be maintained in the [UEDE Human Action & Approval Inbox](https://app.notion.com/p/42399868397f8152b2b7d1bf8cc15712).

Green CI is technical evidence, not approval or KM acceptance. A changed head/base, dependency, policy or PRE revision invalidates the prior action request. HSMART KM gates, service acceptance, security and production controls remain unchanged. No second human reviewer/approver is introduced and no AI may approve its own work.

All HSMART ecosystem responses must state whether human action is required, show exact links/instructions when applicable, report evidence and finish with one next-work recommendation plus one ready-to-copy Indonesian next prompt. Automated GitHub webhooks, dispatchers and push notifications remain NOT_CONFIGURED until a live end-to-end test proves delivery; the Notion Inbox and explicit assistant response are the currently available record/notification path.
