# UEDE HSO Capability Routing Matrix

**Snapshot:** HSO catalog revision `2026-11-23`  
**Pinned parent source:** [Hypersystem-Orchestrator](https://github.com/hsaidno-cpu/Hypersystem-Orchestrator) @ `9853bde6d8484b486aa4d163e65f834fa632410b`  
**Consumer:** HSMART UEDE adapters, beginning with PR [#35](https://github.com/hsaidno-cpu/HSMART/pull/35).  
**Interpretation:** Catalog inventory and routing metadata only. This matrix is not an install or invoke grant.

## 1. Inventory

| HSO plugin identity | Skill records | Source state | Parity | Distribution state | Rights state |
|---|---:|---|---|---|---|
| Video Explainer Promkes V4.1.12 | 16 | integrated_submodule | NOT_COMPARED | blocked | not_declared |
| Skill Developer Orchestrator | 1 | integrated_submodule | DRIFT_DETECTED | blocked | cleared |
| Evaluator Team | 4 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| Master Photo Restoration | 1 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| Anatomi Prompt V3.0 — Octa-Prompt | 9 | integrated_submodule | MATCH | private_source_restricted | private_not_cleared |
| SKILL ANALYZER | 12 | integrated_submodule | DRIFT_DETECTED | review_required | not_declared |
| GODEX Motion Audio | 8 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| AI Prompt Finder & Creator | 7 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| Agent Jailbreak Skill DS | 11 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| Motion Graphic by arifanara V.01 | 19 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| Plugin Agent Orchestrator | 44 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| Photo Fixer | 12 | candidate_repository | NOT_APPLICABLE | candidate_incomplete | not_assessed |
| A.S.F.R.E.E | 13 | integrated_submodule | DRIFT_DETECTED | review_required | review_required |
| A.S.F.R.E.E Legacy | 1 | canonical_redirect | NOT_APPLICABLE | legacy_redirect | inherited_from_canonical_source |
| Cortex Workbench | 8 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| CommandCraft 56 | 14 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| Agent Skills Atlas | 17 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| People & Business Competency Academy | 9 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| AI Workflow Systems Orchestrator | 9 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| GrowthForge Business OS | 18 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| PVEE Promkes Super Orchestrator | 14 | candidate_repository | NOT_APPLICABLE | candidate_incomplete | not_assessed |
| Progressive Roadmap Evaluator (PRE) | 9 | pending_repository | NOT_COMPARED | snapshot_only | not_assessed |
| Ponytail Engineering System | 9 | pending_repository | NOT_APPLICABLE | snapshot_only | not_assessed |
| **Total** | **265** | **23 identities** | | | |

## 2. Distribution, rights and parity summary

| Dimension | State | Count |
|---|---|---:|
| Distribution | snapshot_only | 15 |
| Distribution | blocked | 2 |
| Distribution | private_source_restricted | 1 |
| Distribution | review_required | 2 |
| Distribution | candidate_incomplete | 2 |
| Distribution | legacy_redirect | 1 |
| Rights | not_assessed | 17 |
| Rights | not_declared | 2 |
| Rights | cleared | 1 |
| Rights | private_not_cleared | 1 |
| Rights | review_required | 1 |
| Rights | inherited_from_canonical_source | 1 |
| Instruction parity | DRIFT_DETECTED | 3 |
| Instruction parity | NOT_COMPARED | 2 |
| Instruction parity | MATCH | 1 |
| Instruction parity | NOT_APPLICABLE | 17 |

Source and rights states are independent. A source being present as a Git submodule does not clear its license. A package version being catalogued does not prove instruction parity. A `MATCH` parity value does not create a distribution permission.

## 3. Runtime and compatibility evidence

HSO records four runtime capabilities:

| Capability ID | Scope | Status / limitation |
|---|---|---|
| `sandbox.write_text` | Write a new UTF-8 file into an ephemeral isolated workspace | Built-in sandbox operation; not repository-wide write permission |
| `sandbox.verify_sha256` | Read a sandbox artifact and verify SHA-256 | Built-in read-only verification operation |
| `test.flaky_write_text` | Test-workspace fault injection | Test-only; not a production capability |
| `plugin.skill.invoke.remote-mcp.skill-analyzer` | One read-only analysis tool over Streamable HTTP | `READY_WITH_LIMITATIONS`; approval `ALWAYS`; not evidence of HSMART host activation |

The compatibility matrix contains 15 plugin-to-plugin edges. All 15 are `CONTRACT_TESTED`; host activation and runtime invocation remain `NOT_RUN`. Treat those edges as static/schema/mock compatibility only.

## 4. Routing responsibility matrix

The following is the proposed specialist allocation for HSMART development. Entries marked catalog-only or restricted are not live dispatch permissions.

| Capability / group | Recommended HSMART work | Current dispatch disposition |
|---|---|---|
| Plugin Agent Orchestrator master | Master planning, tier routing, handoff and risk coordination | Use as design/operating specification; do not assume generic HSO invocation is configured |
| Agent Design Orchestrator | Requirements, ADP, architecture, workflows and design gates | Skill specification consulted; no isolated agent runtime proven |
| Agent Build & Operations Orchestrator | Code, runtime, integration, tests, CI/CD, deployment and operations routing | Skill specification consulted; no independent runtime proven |
| Solution Architect / Requirements Architect | Architecture and requirement contracts | Role mapping; runtime not evidenced by catalog |
| Tool Integration / Integration Platform Engineer | PRE, GitHub, Notion, Supabase and external API/MCP contracts | HSMART adapters are being implemented as read-only ports |
| Security & Governance / Data Governance | Least privilege, data ownership, secrets, RLS, audit and approval policy | Required reviewer workstream; separate runtime not evidenced |
| Test Engineer / CI-CD / Deployment Architect | Regression, exact-head CI, release and rollback gates | GitHub Actions evidence is active for the HSMART PR stack |
| Evaluation & Evidence Authenticator | Evidence coverage, exact SHA and acceptance receipt verification | Assurance docs exist; reports are correlation-limited |
| Skill Analyzer | Technical anatomy, source/skill analysis and capability mapping | Catalogued remote MCP scope is restricted and ALWAYS approval; not invoked by this implementation |
| A.S.F.R.E.E | Deep technical anatomy and analysis method | Source parity is DRIFT_DETECTED; rights need review |
| Evaluator Team | Independent judgement and post-implementation review | Source pending; do not claim operational independence |
| Skill Developer Orchestrator | Controlled skill/plugin source lifecycle and regression | Source exists, but instruction parity is DRIFT_DETECTED |
| Progressive Roadmap Evaluator | Roadmap stage, gate and transition evaluation | PRE remains authority; only read-only adapter is being integrated |
| AI Workflow Systems Orchestrator | Workflow design and orchestration patterns | Source pending; use as catalog candidate, not as live execution engine |
| Agent Skills Atlas | Skill standards, reference patterns and evaluation checklist | Source pending; no runtime claim |
| Agent Jailbreak Skill DS | Adversarial prompt/tool boundary tests | Source pending; only plan as a future red-team input |
| Ponytail Engineering System | Engineering optimization and workflow support | Source pending; no runtime claim |
| Domain-specific creative/health/business plugins | Domain work only when relevant to HSMART product requirements | No blanket invocation or redistribution rights |

## 5. Capability admission policy

A catalog entry may be routed to a real HSMART host only after all of the following are evidenced:

1. Exact canonical child repository and immutable source commit.
2. Content digest recomputed from the authorized source artifact.
3. License and usage/distribution rights cleared for the specific intended use.
4. Source-to-platform instruction parity compared; any drift is resolved or explicitly accepted by the authorized owner.
5. Versioned interface contract and positive/negative contract tests pass.
6. Named target host activates the adapter under least-privilege scopes.
7. A real invocation succeeds and emits an evidence receipt bound to exact capability version, host, request and output artifact.
8. Required human approval policy is applied; permission denial cannot be bypassed by another plugin or provider.

Until then use `BLOCKED`, `NOT_ASSESSED`, `NOT_CONFIGURED` or `CANDIDATE`; never upgrade unknown states to PASS by inference.

## 6. Source reconciliation backlog

- Verify the 23 child repository owners, exact commits, manifests, licenses and package digests.
- Compare all 265 instruction records against canonical child source; resolve the three known drift cases and two un-compared cases.
- Reconcile Video Explainer Promkes source/deployed versions; the catalog notes source 4.1.9 and package 4.1.12.
- Reconcile the SDO instruction drift even though its package license is cleared.
- Resolve Skill Analyzer's missing license declaration before installation/distribution outside its currently scoped private use.
- Resolve A.S.F.R.E.E's PolyForm Noncommercial restrictions before commercial distribution; retain legacy as redirect-only.
- Verify all candidate and pending repositories before creating installable artifacts.
- Add named-host contract and runtime evidence only after a host adapter is actually configured.

## 7. Canonical source files

The inventory is derived from the pinned HSO parent catalog:
- `catalog/plugins.json`
- `catalog/repositories.json`
- `catalog/instruction-snapshots.json`
- `catalog/distribution-registry.json`
- `catalog/hso-runtime-capabilities.json`
- `catalog/compatibility-matrix.json`

Parent catalog revision: `2026-11-23`; parent commit: `9853bde6d8484b486aa4d163e65f834fa632410b`.

This matrix is a time-stamped read-only interpretation. It must be regenerated or reconciled when the canonical HSO catalog changes.
