# Platform Compatibility and Licensing — 23 November 2026

**Status:** Version/license metadata verified; live proof-of-fit available only where explicitly stated below.  
**Scope:** Disposable proof-of-fit, not production approval.

## AppFlowy

- Active self-host server distribution: `AppFlowy-IO/AppFlowy-SelfHost-Commercial`. The old `AppFlowy-Cloud` repository is archived.
- Inspected Compose manifest at repository commit `f58f4ffafab79f11bf895b0bfeb4ec9548223baa`, file blob `4a1f0088c238a61dff7c62373c6c674508530cfc`.
- Compose manifest pins Cloud/Worker/Search/AI family at `0.21.8`, Web at `0.20.15`, GoTrue at `0.20.6`, Admin frontend at `0.20.4` and other components by immutable digest.
- Current server distribution has a **commercial per-server/machine license**, not FLOSS. Published Free Tier advertises one seat plus up to three guest editors. OIDC/OAuth, SAML and LDAP require Seed tier or higher.
- Official OpenAPI JSON: `/api/docs/openapi.json`; page create: `POST /api/workspace/{workspace_id}/page-view`; authenticated user access uses a GoTrue bearer token.
- AppFlowy adapter is mock-tested only. No licensed live server or Seed identity tier was provisioned.

**Disposition:** AppFlowy Self-Hosted Commercial is not a FLOSS default. If FLOSS is mandatory, evaluate Docmost or another FLOSS wiki separately for API, permissions, attachments, export and OIDC.

## Baserow

- Candidate: **Baserow Open Source Edition 2.4.3**, published 14 November 2026.
- OSE core is MIT; docs CC BY-SA 4.0; premium and enterprise paths have separate licensing.
- Live disposable `baserow/baserow:2.4.3` integration passed **1/1 test in 134.93 seconds**.
- Verified: synthetic user/JWT, explicit workspace creation, database/table creation, one-table database token with create/read only, successful row create/read, denied delete, and disposable container/volume cleanup.
- Evidence: https://github.com/hsaidno-cpu/HSMART/actions/runs/45195465246/job/137764610704
- Startup emitted a permission warning when the bundled internal database role attempted to create PostgreSQL `vector` extension. Core API and table-scoped token ACL test passed; vector/AI feature was not part of the test.
- The Baserow all-in-one image's internal PostgreSQL/Redis are separate from the SDGDS PostgreSQL 16 service.

## PostgreSQL 16

- Disposable GitHub Actions service used `postgres:16`, reporting PostgreSQL 16.16.
- DDL and six tests passed on a previously tested head: string IDs, schema, JSONB/check constraints, unique labels/slugs, foreign keys and relation constraints, outbox idempotency, transaction rollback/commit.
- Evidence: https://github.com/hsaidno-cpu/HSMART/actions/runs/45195465115/job/137764609621
- Test reset now requires an explicit destructive opt-in and exact disposable database/user `sdgds_spike`; a fresh exact-head rerun remains pending.
- This does not prove production backup/restore, HA, DR, load or security readiness.

## OIDC

Local synthetic verifier tests use a generated RSA keypair, synthetic JWKS, issuer `https://issuer.synthetic.test`, audience `sdgds-api` and a synthetic subject. They validate RS256 signature, `kid`, issuer, audience, expiry, required claims and scope. No external IdP, live JWKS rotation or revocation endpoint was tested.

## Official references

- AppFlowy self-host: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial
- AppFlowy license: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial/blob/main/SELF_HOST_LICENSE_AGREEMENT.md
- AppFlowy OpenAPI: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial/blob/main/docs/OPENAPI.md
- AppFlowy authentication: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial/blob/main/docs/AUTHENTICATION.md
- AppFlowy OIDC: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial/blob/main/docs/OIDC.md
- Baserow 2.4.3: https://github.com/baserow/baserow/releases/tag/2.4.3
- Baserow license: https://github.com/baserow/baserow/blob/develop/LICENSE
