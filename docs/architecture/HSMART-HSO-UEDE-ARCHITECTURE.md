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
