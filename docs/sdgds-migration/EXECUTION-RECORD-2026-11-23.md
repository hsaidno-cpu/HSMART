# SDGDS Migration — M0/M1 Execution Record

**Roadmap:** HSMART-SDGDS-MIGRATION-001  
**Revision:** 0.1.0  
**Snapshot:** 23 November 2026  
**Disposition:** M0 approved for bounded non-production design, read-only inventory and synthetic spike. Production is NOT approved.  
**Decision authority:** GOV-01  
**Execution owner:** UNASSIGNED  
**Baseline:** HSMART main @ `ce0e83b864f5fe6e958c978080cbbfcf7a813e72`

## 1. M0 — Charter and architecture

PR #29 is now **MERGED**, merge commit `f72e00893fab05a9b109890c55c4ea7f5c945fab`. This supersedes older Notion text and ledger entries describing PR #29 as open/pending.

M0 is accepted for the explicitly bounded scope requested: architecture design, read-only inventory and synthetic technical proof-of-fit. It does **not** authorize production deployment, cloud procurement, importing real Notion content, changing Notion permissions, production data cutover, risk acceptance or Notion retirement.

### Architecture decision

HSMART main already contains Python/FastAPI, SQLAlchemy, Alembic, PostgreSQL 16, a worker pattern and ADR-001 modular-monolith-first direction. The initial SDGDS implementation should therefore be a **domain module within the existing HSMART application**, not a separately deployed microservice.

| Component | Approved bounded role |
|---|---|
| GitHub/HSMART | Engineering source of truth: code, schemas, API/MCP contracts, migrations, policies, CI and reproducible seed/export |
| PostgreSQL | Future operational source of truth for live SDGDS records after a separate cutover approval |
| FastAPI SDGDS service | One governed read/write API and shared domain/policy service layer |
| MCP adapter | Expose approved operations using the same authorization/service layer; no SQL bypass |
| AppFlowy | Narrative documentation/wiki/ADR/SOP workspace |
| Baserow | Review queue and dashboard projection; no direct writes to canonical SDGDS tables |
| Outbox worker | Idempotent projection and reconciliation to Baserow |

No dual-writer pattern. Redis, if later introduced, is cache/coordination only, never canonical storage. ADR-011 remains a recommended stack direction with formal acceptance pending; this execution does not convert it into production procurement approval.

## 2. M1 — Read-only Notion inventory

No source Notion records were edited, archived or deleted. Saved-view inventory returned:

| Asset | Active | Archived |
|---|---:|---:|
| Terminology Registry | 25 | 0 |
| Review Queue | 1 | 0 |
| Roadmap & Evaluation Ledger | 20 | 0 |

Terminology findings: 24 Canonical, 1 Proposed; 25 unique Term IDs and labels; no missing primary source URL in the returned rows; all required alias/definition/related-term fields populated. There are **zero real 64-hex SHA-256 Content Hash values**; the field contains pending-sync placeholders. Last Synced Commit values are explanatory placeholders, not verified commit hashes. Notion schema also lacks a `slug` field present in the GitHub canonical JSON.

Roadmap ledger findings: 12 milestones, 4 risks, 2 dependencies, 1 evaluation and 1 work item. All 20 Work Item IDs unique; all 20 have a 40-character hexadecimal Source Commit; no missing Acceptance Criteria or Evidence URL in the retrieved rows; zero real 64-hex SHA-256 Content Hash values.

The scoped SDGDS search returned 50 page/database matches. This is not a complete recursive block/file/attachment manifest. Child-block content, file binaries, MIME sizes/checksums, comments and downloadable attachment rights remain unknown. Therefore **M1 database/schema/record inventory is VERIFIED READ-ONLY; recursive page/file/attachment inventory is PARTIAL / NOT VERIFIED**.

The old PR #29 status in Notion is stale and must be reconciled through the canonical GitHub-to-Notion mechanism when that sync is configured. This task did not mutate the Notion ledger.

## 3. Synthetic technical spike

Local synthetic package is supplied as a downloadable conversation artifact. The repository PR records the execution findings; the downloadable package is kept separate until source-level review and import into the repository are approved.

- **Tests:** 11 passed; `compileall` passed; Compose YAML parsed; synthetic secret-placeholder scan passed.
- **API Gateway:** FastAPI read/search and Proposed-only candidate creation with explicit synthetic scopes.
- **MCP:** narrow `initialize`, `tools/list` and `tools/call` JSON-RPC smoke test. Not full MCP conformance.
- **Baserow:** REST path, `Authorization: Token` header, bounded pagination and synthetic projection mapping tested against an HTTP mock.
- **AppFlowy:** OpenAPI discovery, operationId lookup, path substitution and synthetic page creation tested against an HTTP mock.
- **PostgreSQL:** PostgreSQL 16 DDL prepared and statically checked; the local API CRUD tests used SQLite as a portable test double.

### Environment limitations

Docker/Compose and `psql` are unavailable in the execution environment. No PostgreSQL server, AppFlowy instance, Baserow instance, OIDC issuer or staging gateway was provisioned. Live integration, actual DDL execution, OIDC/JWKS validation, backup/restore, DR, load, security and production gates remain NOT_RUN. The spike contains synthetic records and fake tokens only; no real Notion records or credentials were used.

## 4. Gate disposition

| Gate | State |
|---|---|
| M0 bounded charter/design approval | APPROVED |
| M1 database/schema/record inventory | VERIFIED READ-ONLY |
| M1 recursive block/file/attachment inventory | PARTIAL / NOT VERIFIED |
| Synthetic API/MCP/adapter contract checks | PASS — 11 tests |
| Live PostgreSQL/AppFlowy/Baserow integration | NOT_RUN |
| M2 production infrastructure | NOT_STARTED |
| M7 production readiness / DR | NOT_RUN |
| M8 cutover | NOT_AUTHORIZED |

## 5. Next actions

1. Finish recursive Notion page-block and attachment inventory with a checksum-based manifest, still read-only.
2. Run a live proof-of-fit in an operator-controlled disposable environment: PostgreSQL 16 first, then exact AppFlowy/Baserow edition and API builds.
3. Reconcile stale Notion statuses using a verified sync path only after credentials/access are authorized.
4. Assign architecture, migration, platform/SRE, security, data-steward and independent-verification roles before production planning.
5. Keep M2+ proposed until provider, OIDC, secrets/KMS, network, budget, retention, SLO/RPO/RTO and operational ownership are explicitly approved.

**No aggregate completion percentage is reported.** The approved denominator and weights do not exist, and M1's recursive asset scope is incomplete.


## 7. Follow-up qualification — 23 November 2026

### Read-only Notion checksum manifest

A SHA-256 manifest now fingerprints all **45 active database rows** returned by the two saved views:
- `docs/sdgds-migration/NOTION-READONLY-CHECKSUM-MANIFEST-2026-11-23.json`
- 25 terminology rows and 20 roadmap ledger rows.
- Each digest covers the entire row property object returned by the saved-view query, with recursively sorted JSON object keys and preserved array order, encoded as UTF-8. It includes the Notion page URL.
- This is a row-property checksum manifest, **not** a recursive block or binary attachment checksum export.

Scoped Notion search returned 50 matching pages and all 50 were fetched. No `notion-file-block://` references or visible discussion references were found in those page contents. The current connector did not expose a recursive block-children traversal operation. Notion's comments endpoint returned `upgrade_required` for the checked pages. Thus this improves row-level integrity evidence, but does not close the full recursive inventory. The search result limit/permission boundary also means no claim is made that all inaccessible or unindexed pages have been discovered.

### PostgreSQL 16 real integration lane

A disposable GitHub Actions service using `postgres:16` was started and the DDL was applied. The first run proved that schema creation succeeded and that JSONB/status/ID, foreign-key, self-relation and outbox-idempotency constraints fired as designed, but **1 of 6 tests failed** because an expected constraint violation aborted the whole test transaction and the test then incorrectly assumed earlier seed rows still existed.

The test harness was corrected to isolate expected constraint failures inside savepoints. The rerun for the new PR head is pending at the time of this record. Do not mark the PostgreSQL lane PASS until the latest commit's result is completed and all six tests pass.

### Synthetic OIDC tests

The local suite now reports **20 passed, 1 skipped**. The passing OIDC tests use a generated RSA keypair and in-memory synthetic JWKS at `https://issuer.synthetic.test`, audience `sdgds-api`, and a synthetic test subject. They validate RS256 signature, `kid`, issuer, audience, expiry, required claims, subject and scope enforcement. This is not an external IdP integration, real user provisioning, production JWKS rotation or token revocation test. The one local skip is the PostgreSQL integration module, which runs only when `SDGDS_TEST_DATABASE_URL` points to a disposable PostgreSQL 16 instance.

### AppFlowy/Baserow build and licensing disposition

- **AppFlowy:** active self-host deployment uses `AppFlowy-IO/AppFlowy-SelfHost-Commercial`, not the archived old `AppFlowy-Cloud` repository. The inspected Compose manifest at commit `f58f4ffafab79f11bf895b0bfeb4ec9548223baa` pins the Cloud/Worker/Search/AI family at `0.21.8` and Web at `0.20.15`, with image digests. The current server is under a commercial per-server license, not FLOSS. Its advertised Free Tier is one seat plus up to three guest editors. OIDC/SAML/LDAP requires Seed tier or higher. Its documented API is `/api/docs/openapi.json`; page creation is `POST /api/workspace/{workspace_id}/page-view` with a GoTrue user access token. Adapter tests use a mock; no live instance was provisioned.
- **Baserow:** candidate is OSE release `2.4.3` (published 14 November 2026). OSE core is MIT; documentation and premium/enterprise paths carry separate licenses. Adapter tests use a mock and table-scoped synthetic token; no live instance was provisioned.
- Exact licensing, API paths and image pin references are documented in `docs/sdgds-migration/PLATFORM-COMPATIBILITY-2026-11-23.md`.

If FLOSS is a hard requirement, AppFlowy Self-Hosted Commercial is not accepted as the default workspace. Treat it as a commercial alternative only; evaluate a genuinely FLOSS wiki separately before selection.

### Human ownership gate

The following roles remain `UNASSIGNED`: execution owner, architecture owner, migration lead/data steward, Platform/SRE operator, security/privacy reviewer and independent verifier. The responsibility/acceptance register is `docs/sdgds-migration/OWNER-APPOINTMENT-REGISTER.md`. No AI delegate is counted as a substitute for human operational accountability.

## 8. Current execution disposition

| Workstream | State |
|---|---|
| M0 bounded non-production architecture | APPROVED |
| M1 45-row SHA-256 manifest | CREATED; row-level scope only |
| M1 recursive blocks/comments/files | PARTIAL / NOT VERIFIED |
| Local API/MCP/OIDC synthetic suite | 20 PASS, 1 SKIPPED (PostgreSQL lane) |
| PostgreSQL 16 disposable CI lane | RERUN PENDING |
| AppFlowy live API | NOT RUN; commercial build/licensing identified |
| Baserow live API | NOT RUN; OSE 2.4.3 identified |
| Human role appointments | UNASSIGNED |
| Production/cutover | NOT AUTHORIZED |
