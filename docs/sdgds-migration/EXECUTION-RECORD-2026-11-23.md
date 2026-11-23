# SDGDS Migration — M0/M1 Execution Record

**Roadmap:** HSMART-SDGDS-MIGRATION-001  
**Revision:** 0.3.0  
**Snapshot:** 23 November 2026  
**M0 disposition:** APPROVED FOR BOUNDED NON-PRODUCTION DESIGN, READ-ONLY INVENTORY AND SYNTHETIC PROOF-OF-FIT  
**Decision authority:** GOV-01  
**AI delegate mapping:** GOV-02 / 04 / 05 / 06 / 07 / 11 — DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE  
**Production / cutover:** NOT AUTHORIZED

## 1. Baseline and scope

HSMART PR #29 is **MERGED**, merge commit `f72e00893fab05a9b109890c55c4ea7f5c945fab`. The inspected main baseline at the beginning of this execution was `ce0e83b864f5fe6e958c978080cbbfcf7a813e72`.

GOV-01 accepted ADR-011 v1.2.0 as the internal HSMART KM1 technology direction under `HSMART-GOV-DEC-2026-11-22-002`. This acceptance supports internal implementation and proof-of-fit; it does not authorize production deployment, procurement or external commitments.

This execution is bounded to architecture design, read-only Notion inspection, row-property checksums and synthetic/disposable technical validation. No original Notion Terminology Registry or Roadmap Ledger rows were edited, archived, deleted or imported. No production cutover or risk acceptance is approved.

## 2. M0 — architecture decision

HSMART already contains Python 3.12/FastAPI, SQLAlchemy, Alembic, PostgreSQL 16 and worker/outbox patterns under ADR-001 modular-monolith-first direction. SDGDS starts as a domain module within HSMART, not a separately deployed microservice.

| Component | Bounded role |
|---|---|
| GitHub / HSMART | Engineering source of truth: code, schemas, API/MCP contracts, migrations, policies, CI, seed and snapshots |
| PostgreSQL 16 | Future operational source of truth for live SDGDS data after separate cutover approval |
| FastAPI SDGDS module | Governed API and single canonical write path |
| MCP adapter | Expose approved operations through the same service and authorization layer; no SQL bypass |
| AppFlowy | Documentation/wiki/ADR/SOP workspace only if licensing and identity tier are acceptable |
| Baserow OSE | Review/dashboard projection; never a second canonical writer |
| Outbox worker | Idempotent projection and reconciliation to Baserow |
| Redis | Optional cache/coordination only; never canonical data storage |

No dual-writer pattern. AppFlowy and Baserow are clients/projections, not additional sources of truth.

## 3. M1 — read-only Notion inventory

Saved-view inventory returned:

| Asset | Active | Archived |
|---|---:|---:|
| Terminology Registry | 25 | 0 |
| Review Queue | 1 | 0 |
| Roadmap & Evaluation Ledger | 20 | 0 |

Terminology findings: 24 Canonical, 1 Proposed; 25 unique Term IDs and labels; all 25 have Primary Source URL; alias, terminological definition and related-term fields are populated. The Notion schema lacks a `slug` property present in GitHub canonical JSON.

Roadmap Ledger findings: 12 milestones, 4 risks, 2 dependencies, 1 evaluation and 1 work item; all 20 Work Item IDs are unique; all 20 Source Commit values have SHA-like syntax; no missing Acceptance Criteria or Evidence URL in returned rows.

### Row-level checksum manifest

Manifest: `docs/sdgds-migration/NOTION-READONLY-CHECKSUM-MANIFEST-2026-11-23.json`

- SHA-256 fingerprints all 45 active database rows (25 terminology + 20 ledger).
- Digest covers the entire row-property object returned by the saved view, with recursively sorted JSON object keys, preserved array order and UTF-8 encoding. Notion page URL is included.
- This is a row-property checksum, not a hash of block bodies or binary file bytes.
- The original Notion Content Hash and Last Synced Commit fields still contain placeholders, not evidence of automated synchronization.

### Individually fetched pages and recursive-inventory limitation

A scoped SDGDS search returned 50 page/database matches. All 45 individual database record pages were fetched, along with five container/schema assets: SDGDS root, current roadmap, migration roadmap, Terminology Registry database/schema and Roadmap Ledger database/schema.

Across these fetched outputs: zero stable Notion file-block references, zero nested child database references, zero visible discussion markers, and zero unknown-block/truncation markers surfaced.

However:
- The current connector did not expose raw recursive block-child traversal or a complete workspace export.
- The Notion comments endpoint returned `upgrade_required`; absence of visible markers is not evidence of zero comments.
- External URLs, inaccessible files, unindexed pages, hidden workspace assets and binary content are not included in this checksum manifest.

Therefore **database/schema/record inventory is VERIFIED READ-ONLY**, while exhaustive raw block-tree, comment and binary attachment inventory remains **PARTIAL / NOT VERIFIED**. No claim of full workspace inventory is made.

## 4. Technical proof-of-fit

All payloads, user identities, credentials and tokens used below were synthetic. No real Notion rows or user secrets were copied into test fixtures.

### PostgreSQL 16.16

A disposable GitHub Actions `postgres:16` service applied `examples/sdgds-migration-spike/migrations/001_sdgds_postgres.sql`. The tested suite passed **6/6**:

1. Schema installation and preservation of HSMART string IDs such as `HSMART-0001`.
2. Case-insensitive unique labels and slugs.
3. JSONB, status and Term ID checks.
4. Alias/relation foreign keys, relation type and no-self-relation checks.
5. Outbox idempotency-key uniqueness.
6. Atomic term + audit + outbox transaction rollback/commit.

Exact-current-head evidence (PR #31 head `3c20dd7789bb67b028563402ea5933c57a6094da`): https://github.com/hsaidno-cpu/HSMART/actions/runs/45197922794. The disposable PostgreSQL 16.16 service applied the DDL and the exact-head suite passed 6/6 in 0.36 seconds. The destructive reset is guarded by explicit opt-in and an exact disposable database/user identity.

The destructive schema reset in the test harness is now guarded by an explicit `SDGDS_TEST_ALLOW_DESTRUCTIVE_RESET=true` opt-in and exact disposable database/user identity `sdgds_spike`. The new guard was added after review to prevent accidental execution against an arbitrary database. The guarded version was re-run on the current PR head and passed. The tests use a disposable DB; they do not prove production backup/restore, HA, DR, load, database security, retention or SLO readiness.

This validates the tested DDL/constraints/transaction semantics only. It does not prove production backup/restore, HA, DR, load, database security, retention, or SLO readiness.

### Baserow OSE 2.4.3

A disposable `baserow/baserow:2.4.3` integration passed **1 test in 90.54 seconds on the current PR head**:

- Created a synthetic user and JWT session.
- Explicitly created a workspace through `POST /api/workspaces/` when no workspace was provisioned automatically.
- Created a database application and synthetic table.
- Created a database token scoped to one table with create/read only.
- Verified token, row creation and row read.
- Verified delete was denied with `delete:false`.
- Removed the disposable container and volume.

Exact-current-head evidence: https://github.com/hsaidno-cpu/HSMART/actions/runs/45197922816. The integration verified a synthetic user/JWT, explicit workspace, database/table, table-scoped create/read token, create/read success and delete denial. The disposable container and volume were removed.

The image's startup log reported that its internal database role could not create the `vector` extension. Core API and the tested table/token ACL flow passed; Baserow vector/AI features were not tested. The all-in-one image has its own internal PostgreSQL/Redis, separate from SDGDS PostgreSQL 16.

This exact-head run is current evidence for Baserow OSE 2.4.3. It does not validate Enterprise-only OIDC SSO, vector/AI features, production backup/restore or multi-tenant operational readiness.

### OIDC and authorization

Local synthetic tests use a generated RSA key pair and in-memory JWKS, issuer `https://issuer.synthetic.test`, audience `sdgds-api` and a synthetic subject. Tests validate RS256 signature, `kid`, issuer, audience, expiry, required claims, subject and scope enforcement.

Local suite result: **20 passed, 2 skipped**. PostgreSQL and Baserow tests skip locally without service URLs and run in separate disposable CI jobs.

This is not an external identity-provider integration, real user provisioning, production JWKS rotation/revocation, session lifecycle or full tenant authorization certification.

### MCP

The spike includes a narrow JSON-RPC smoke test for `initialize`, `tools/list` and `tools/call` through the shared authorization path. This is not full MCP protocol conformance or transport lifecycle validation.

### AppFlowy

No licensed live AppFlowy instance was provisioned or called. Current self-host server distribution is commercial, not FLOSS; OIDC/SAML/LDAP requires Seed tier or higher. Adapter proof remains mock-only. If FLOSS is a hard requirement, AppFlowy Self-Hosted Commercial is not approved as default; a genuinely FLOSS wiki such as Docmost must be separately evaluated.

## 5. GOV-01 delegate mapping

GOV-01 Decision Addendum `HSMART-GOV-DEC-2026-11-22-002` defines GOV-01 as the sole human internal authority; bounded AI Functional Delegates cover the other workstreams.

| Workstream | Existing delegate | Lifecycle |
|---|---|---|
| Delivery / execution | `hsmart.gov02.project-owner.orchestrator` | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| Architecture / ADR / contracts | `hsmart.gov04.architecture.orchestrator` | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| Migration / data stewardship | `hsmart.gov05.database-agent` under GOV-05 Engineering | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| Platform / SRE | `hsmart.gov07.operations-reliability.orchestrator` | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| Security / privacy | `hsmart.gov06.security-privacy.orchestrator` | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |
| Independent assurance | `hsmart.gov11.independent-assurance-reviewer.orchestrator`, coordinated by `hsmart.assurance.cross-evaluation-orchestrator` | DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE |

Logical designation does not prove runtime identity, model/version binding, Skills/instructions, task-scoped tool grants, policy enforcement, audit, fail-closed behaviour or activation. No delegate was activated by this execution. GOV-01 retains final decision authority; GitHub native review and merge remain separate platform controls.

## 6. Gate disposition

| Workstream | State |
|---|---|
| M0 bounded design / non-production approval | APPROVED |
| M1 45-row SHA-256 row-property manifest | CREATED |
| M1 individual record-page fetch (45) + container/schema fetch (5) | VERIFIED WITH SCOPE LIMITS |
| M1 exhaustive raw block-tree / comments / binary attachment inventory | PARTIAL / NOT VERIFIED |
| Local API/MCP/OIDC synthetic suite | PASS — 20 passed, 2 skipped |
| PostgreSQL 16.16 disposable integration | PASS — 6/6 on previously tested head; guarded exact-head rerun pending |
| Baserow OSE 2.4.3 disposable API/ACL integration | PASS — 1/1 on previously tested head; exact-head rerun pending |
| AppFlowy live API / licensed SSO tier | NOT RUN |
| GOV delegate runtime activation | NOT ACTIVE |
| Production security / backup / DR readiness | NOT RUN |
| Real Notion import / cutover / legacy retirement | NOT AUTHORIZED |

PR #31 remains OPEN / DRAFT / NOT MERGED. Exact-head status: Specification Validation PASS (https://github.com/hsaidno-cpu/HSMART/actions/runs/45197922839); Repository Governance PASS (https://github.com/hsaidno-cpu/HSMART/actions/runs/45197923064); PostgreSQL 16.16 PASS 6/6 (https://github.com/hsaidno-cpu/HSMART/actions/runs/45197922794); Baserow OSE 2.4.3 PASS 1/1 (https://github.com/hsaidno-cpu/HSMART/actions/runs/45197922816); AI Reviewer Evidence FAIL (https://github.com/hsaidno-cpu/HSMART/actions/runs/45197922761) because `docs/reviews/PR-31-AI-ASSURANCE.json` is missing. Do not fabricate an independent review artifact or bypass this gate. A real separate-context review and GOV-01 disposition are still required.

## 7. Next actions

1. Complete raw Notion block-child and attachment inventory only through an authorized read-only export route; checksum any binary assets and retain provenance/rights records.
2. Complete exact-head CI after the PostgreSQL destructive-reset guard and latest manifest update.
3. Create a correlation-limited GOV-11-labelled AI review artifact only as evidence from this assistant context; do not represent it as a separately provisioned independent GOV-11 runtime.
4. Provision existing GOV delegates only after stable identity/runtime, model/Skills, scopes, policy enforcement, audit and fail-closed tests.
5. Evaluate a genuinely FLOSS wiki if FLOSS is mandatory; do not assume AppFlowy Commercial meets that requirement.
6. Keep M2/M7/M8 blocked until provider, identity/secrets/KMS, network, budget, retention, SLO/RPO/RTO, security, recovery and governance evidence are approved.

**No aggregate completion percentage is reported.** Recursive assets are not exhaustively inventoried and no approved denominator/weighting model exists.
