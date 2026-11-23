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

Local package: `examples/sdgds-migration-spike/sdgds-migration-spike.zip` in this PR; a directly downloadable copy is also attached in the conversation.

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
