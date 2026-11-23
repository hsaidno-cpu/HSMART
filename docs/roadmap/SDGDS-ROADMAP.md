# SDGDS Progressive Roadmap & Evaluation

**Roadmap ID:** HSMART-SDGDS-ROADMAP-001  
**Revision:** 0.1.0  
**Snapshot:** 23 November 2026  
**Status:** PROPOSED, NOT APPROVED / NOT FROZEN  
**Host mode:** OTHER_HOST_ADAPTER  
**Decision owner:** GOV-01 under HSMART governance  
**Execution owner:** Not assigned

> **Executive disposition:** SDGDS has a validated foundation, not a completed operational system. The canonical registry and quality gates are implemented and CI-verified on PR #29. Notion's 25-term seed exists, but authenticated GitHub-to-Notion automation has not been verified. Autonomous term discovery, semantic graph governance, search, quality monitoring and measured user outcomes remain future work.

## 1. Current state

| Dimension | Observed state |
|---|---|
| HSMART parent foundation | PR #28 merged; current main/base is \`543bef61f1fd1ce3a736bd107857bee0b244c388\` |
| SDGDS implementation | PR #29 open, mergeable, 17 files changed; reviewed code SHA 9f610af, report-only head 3e72b17 |
| Canonical seed | 25 terminology records |
| SDGDS unit tests | 13/13 passed (8 terminology + 5 roadmap tests) |
| PR workflow groups | 5/5 succeeded on exact head \`0890bfa6538fbc7e23a61150f5a574128c4bc684\` |
| Notion term database | 25/25 records verified via All Terms saved view; one Proposed item in Review Queue |
| Automated Notion sync | **Not verified**; both CI sync steps were skipped because credentials/data-source access were not configured or evidenced |
| Term discovery across repositories | Not implemented |
| Semantic relation graph | Initial text IDs only; typed graph not implemented |
| Search API/MCP | Not implemented; Notion browsing only |
| Outcome/adoption | Not measured |

**No overall completion percentage is published.** There is no GOV-01-approved frozen denominator or approved weighting model. Counting files or terms as equal units would create a vanity metric. Delivery, verification, milestone acceptance, automation and outcome are reported separately.

Evidence:
- [HSMART PR #28 merged](https://github.com/hsaidno-cpu/HSMART/pull/28)
- [SDGDS PR #29](https://github.com/hsaidno-cpu/HSMART/pull/29)
- [SDGDS CI](https://github.com/hsaidno-cpu/HSMART/actions/runs/45098423084)
- [Repository Governance CI](https://github.com/hsaidno-cpu/HSMART/actions/runs/45098423077)
- [AI Reviewer Evidence CI](https://github.com/hsaidno-cpu/HSMART/actions/runs/45098423123)
- [Specification Validation CI](https://github.com/hsaidno-cpu/HSMART/actions/runs/45098423081)
- [KM1 application CI](https://github.com/hsaidno-cpu/HSMART/actions/runs/45098423090)

## 2. PRE R0–R9 lifecycle

| PRE stage | State | Evaluation |
|---|---|---|
| R0 Intake | Procedure applied | Intent, scope, non-goals, host mode and decision boundary established |
| R1 Strategy & Baseline | Applied with caveats | PR, branch, CI and Notion evidence reviewed; post-edit Notion aggregate read is blocked |
| R2 Roadmap Design | Proposed | This revision is built; approval/freeze pending |
| R3 Approval & Baseline Freeze | Blocked | GOV-01 disposition required; PR #29 remains open |
| R4 Iteration Execution | Partial | Registry, schema, validator, renderer, tests and workflow verified on branch; sync activation and discovery remain incomplete |
| R5 Formative Check | PASS_WITH_CAVEATS | Foundation validated; operational and coverage gaps remain |
| R6 Milestone Acceptance | NOT_ASSESSED | No approved/frozen milestone acceptance or post-merge evidence |
| R7 Outcome & Impact | NOT_ASSESSED | No measured lookup, comprehension or adoption outcomes |
| R8 Adaptation | Delta applied | Provenance, validation and sync retry/rate-limit hardening incorporated; no broader rebaseline justified |
| R9 Closure & Learning | NOT_STARTED | Operational owner, sync proof, measured outcomes and residual-risk disposition remain open |

PRE specialist procedures were applied in this host session. This does not mean separate PRE subagent runtimes were invoked or provisioned.

## 3. Roadmap milestones

### M0 — Intake and evidence baseline
**State:** VERIFIED / PASS_WITH_CAVEATS. Scope, target, authority boundary, non-goals, evidence and unknowns are recorded. The roadmap remains a proposal.

### M1 — Canonical registry and quality-gate foundation
**State:** VERIFIED ON PR BRANCH / PASS_WITH_CAVEATS.

Delivered: canonical JSON registry with 25 seed terms, JSON Schema, curation policy, stable Term IDs, aliases, domains, lifecycle status, provenance, validator, deterministic glossary index, eight SDGDS unit tests and GitHub Actions validation.

**Acceptance still required:** GOV-01 disposition and merge of PR #29. A green PR is verification evidence, not acceptance authority.

### M2 — Activate Notion automation
**State:** BLOCKED BY CONFIGURATION.

1. Share the SDGDS Terminology Registry and Roadmap & Evaluation Ledger with the same Notion integration.
2. Configure GitHub Actions secrets: \`NOTION_API_TOKEN\`, \`NOTION_GLOSSARY_DATA_SOURCE_ID\`, and \`NOTION_SDGDS_ROADMAP_DATA_SOURCE_ID\`.
3. Run authenticated sync and verify create, update, unchanged/no-op, pagination, retry and failure handling.
4. Record source commit and content hash on each row.

Manual seed insertion and a CI step that reports “SKIPPED” are not proof of automated synchronization.

### M3 — Automated terminology discovery
**Priority:** P1. Build a bounded scanner for approved sources in HSMART and Hypersystem-Orchestrator. Start with README, ADR, schema, manifests, API contracts, governance and architecture documents. Candidate extraction must preserve repository, path, commit, source locator and hash. New records enter Proposed only.

### M4 — Evidence enrichment and semantic governance
**Priority:** P1/P2. Add source authority tiers, external standards links, citation verification, typed relations, alias/synonym resolution, deprecation/successor graph, conflict detection and promotion review. Expert perspectives are conditional; never invent quotations.

### M5 — Search and retrieval
**Priority:** P2. Start with Notion views and generated GitHub index. Later add a versioned retrieval contract or MCP/REST search endpoint only after use cases and access controls are defined. Results should show canonical term, aliases, status, confidence, source and boundaries.

### M6 — Quality monitoring and outcome evaluation
**Priority:** P2. Define denominator-backed indicators for source coverage, stale references, missing evidence, duplicate/ambiguous candidates, orphan relations, sync lag, lookup success and user comprehension. Build dashboards only after indicators and thresholds are approved.

### M7 — Assurance and maintenance handoff
**Priority:** P3. Assign a maintenance owner, review cadence, source change process, failure response, deprecation policy and closure criteria. Do not close while automation, outcome and ownership gates are open.

## 4. Critical path and dependencies

\`\`\`mermaid
flowchart TD
  A["GOV-01 disposition of PR #29 and roadmap"] --> B["Merge and canonical branch read-back"]
  B --> C["Notion integration shared + three GitHub secrets"]
  C --> D["First authenticated glossary and roadmap sync"]
  D --> E["Two-repository discovery pilot"]
  E --> F["Evidence review and Proposed candidate queue"]
  F --> G["Typed semantic relations and conflict checks"]
  G --> H["Search/retrieval interface"]
  H --> I["Quality and outcome measurement"]
  I --> J["Assurance, maintenance handoff and closure"]
\`\`\`

The first dependency is a human governance decision, not more code. The second is Notion integration access and secrets. Repository discovery must not begin until source paths, rights, privacy and exclusion rules are agreed.

## 5. Evaluation indicators

| Indicator | Current observation | Interpretation |
|---|---:|---|
| Seed terms | 25 | Foundation seed, not total vocabulary |
| SDGDS unit tests | 13/13 pass | Code-level checks, not definition accuracy |
| PR workflow groups | 5/5 pass on current PR report-only head | Exact-commit repository CI evidence |
| PR #29 | Open, mergeable | Not merged or accepted |
| Automated Notion sync runs | 0 verified | CI skipped without credentials |
| Inventory coverage | Unknown | No agreed source/term denominator |
| Expert perspectives | Not yet verified/populated | Correctly left empty rather than fabricated |
| User lookup/comprehension outcomes | Not assessed | Requires pilot and baseline |

Indicators must be defined before measurement. No weighted score can override a blocked gate.

## 6. Risk register

| ID | Risk | Priority | Control / next action |
|---|---|---|---|
| RISK-001 | Notion sync lacks integration access and secrets | P1 | Share both databases, configure one token and two data-source secrets, verify end-to-end sync |
| RISK-002 | AI candidate definitions contain hallucinations or unsupported expert claims | P1 | Provenance, confidence, source authority tiers and human approval before Canonical |
| RISK-003 | Cross-repository scanning crosses private, confidential or licensed boundaries | P1 | Explicit repo/path allowlist, exclude private instructions/secrets, rights review |
| RISK-004 | Term identity and meaning drift between Notion and GitHub | P2 | Stable IDs, idempotent upsert, duplicate detection, typed relations and reconciliation |

Owners remain unassigned unless explicitly designated.

## 7. Priority recommendation

**P0 — close governance loop**
- GOV-01 reviews PR #29 and proposed roadmap revision 0.1.0.
- Preserve exact-commit evidence; merge only through authorized repository rules.
- Do not mark roadmap APPROVED until the decision is recorded.

**P1 — make current promises work**
- Configure Notion integration access and three GitHub Actions secrets.
- Execute a first authenticated sync and verify update/no-op behavior.
- Establish source allowlist and pilot candidate discovery on the two approved repositories.

**P2 — evolve from glossary database to intelligent knowledge system**
- Typed relationship graph and semantic conflict detection.
- External source and citation verification.
- Search/retrieval contract and quality monitoring.
- User task baseline and outcome measurement.

**P3 — scale and institutionalize**
- Reviewed bilingual content, maintenance ownership, periodic audits, impact review and closure.

Do not build an MCP search API before sync, source governance and semantic contracts are stable.

## 8. Adaptation and revision control

Revision 0.1.0 records current baseline and relative sequence. The prior foundation iteration applied provenance/source URL corrections and Notion sync rate-limit/retry hardening. No date-based rebaseline is justified because no schedule or capacity baseline exists.

Replan triggers: PR #29 is held/rejected or its base changes materially; Notion integration cannot be authorized; source rights/privacy exclusions change; discovery produces high false-positive/duplicate rates; review capacity is insufficient; or search outcomes fail the agreed user baseline. Every adaptation must create a new revision and preserve this snapshot.

## 9. Assurance and closure conditions

SDGDS is not closed until PR and roadmap have explicit GOV-01 disposition; the canonical registry and Notion mirror reconcile successfully; discovery and semantic governance have review controls; quality indicators have actual observations; user outcomes are measured against a baseline; and residual risks and maintenance ownership are accepted.

## 10. Evidence and records

- [GOV-11 AI assurance report](https://github.com/hsaidno-cpu/HSMART/blob/sdgds/implementation-20261123/docs/reviews/PR-29-AI-ASSURANCE.json)
- [Notion SDGDS home](https://app.notion.com/p/42199868397f81a19db8dc084105ce5b)
- [Notion Terminology Registry](https://app.notion.com/p/42199868397f81878cd6c5de0b2f20b9)
- [Notion Roadmap & Evaluation Ledger](https://app.notion.com/p/42199868397f81e7a6bbcc4ab3f075cb)

**Evidence snapshot:** 23 November 2026. Re-read GitHub and Notion before later decisions.
