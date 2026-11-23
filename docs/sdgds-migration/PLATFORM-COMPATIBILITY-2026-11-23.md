# Platform Compatibility and Licensing Decision — 23 November 2026

**Status:** Repository/release metadata verified; live deployments not run.  
**Use:** Reproducible disposable proof-of-fit candidate, not production approval.

## AppFlowy

- Active server distribution: `AppFlowy-IO/AppFlowy-SelfHost-Commercial`. The old `AppFlowy-Cloud` repository is archived.
- Compose manifest inspected at repository commit `f58f4ffafab79f11bf895b0bfeb4ec9548223baa`, file blob `4a1f0088c238a61dff7c62373c6c674508530cfc`.
- Compose manifest currently pins Cloud/Worker/Search/AI family at `0.21.8`, Web at `0.20.15`, GoTrue at `0.20.6`, Admin frontend at `0.20.4` and other components by immutable digest.
- This current server distribution is under a **commercial per-server/machine license**, not FLOSS. README Free Tier advertises one user seat per instance and up to three guest editors. The license agreement restricts copying, modification, redistribution, reselling and license-key transfer.
- The current authentication guide says OIDC/OAuth, SAML and LDAP require Seed plan or higher. The Free Tier does not qualify as a free OIDC/SSO target.
- Official OpenAPI JSON: `/api/docs/openapi.json`; Swagger UI: `/api/docs`.
- Page creation: `POST /api/workspace/{workspace_id}/page-view`, body includes `parent_view_id`, `layout: 0`, `name`, `content_mode: "create_content"`.
- Authenticated business API uses a GoTrue user access token as `Authorization: Bearer <token>`. Do not substitute admin keys, JWT signing secrets or MCP tokens.
- Adapter tests are mock-only; no live AppFlowy service was started/called.

**Decision:** AppFlowy Self-Hosted Commercial is not approved as a default FLOSS workspace. It can remain a separately licensed alternative. If FLOSS is mandatory, evaluate Docmost or another genuinely FLOSS wiki against API, role/permission, attachment and export requirements.

## Baserow

- Selected candidate: **Baserow Open Source Edition (OSE), release 2.4.3**, published 14 November 2026.
- OSE core is MIT; documentation is CC BY-SA 4.0; `premium/` and `enterprise/` directories have separate license terms.
- Adapter API: `/api/database/rows/table/{table_id}/`.
- Auth header: `Authorization: Token <database-scoped-token>`.
- Use bounded pagination and user field names. Do not rely on Premium/Enterprise features unless a separate license decision authorizes them.
- Adapter tests are mock-only; no live Baserow service was started/called.

## PostgreSQL 16

A new GitHub Actions lane uses a disposable `postgres:16` service and runs schema, JSONB/check, unique index, FK, relation, outbox idempotency and transaction rollback/commit tests. First execution successfully applied the DDL and passed five tests, but the uniqueness test exposed a test-harness savepoint mistake. That harness was corrected; the latest rerun must be observed before accepting the lane.

## OIDC

Local tests use a generated RSA keypair, synthetic JWKS, issuer `https://issuer.synthetic.test`, audience `sdgds-api` and synthetic subject. This proves verifier behavior against locally generated test material only; no external IdP, user provisioning, real JWKS rotation or token revocation is claimed.

## Official source references

- AppFlowy self-host deployment: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial
- AppFlowy license: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial/blob/main/SELF_HOST_LICENSE_AGREEMENT.md
- AppFlowy OpenAPI guide: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial/blob/main/docs/OPENAPI.md
- AppFlowy authentication guide: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial/blob/main/docs/AUTHENTICATION.md
- AppFlowy release image pins: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial/blob/main/docs/RELEASE_IMAGES.md
- Baserow 2.4.3: https://github.com/baserow/baserow/releases/tag/2.4.3
- Baserow license: https://github.com/baserow/baserow/blob/develop/LICENSE


## Baserow live qualification addendum

The candidate Baserow OSE 2.4.3 image passed a disposable GitHub Actions integration. The test created a synthetic user, JWT session, workspace, database application and table; created a database token; constrained the token to create/read on one table; verified row create/read; and confirmed a delete request was denied. Result: **1 passed in 134.93 seconds**.

Evidence: https://github.com/hsaidno-cpu/HSMART/actions/runs/45195465246/job/137764610704

The Baserow all-in-one image's bundled PostgreSQL/Redis are internal to Baserow and are not the SDGDS PostgreSQL 16.16 instance. Startup emitted a `vector` extension permission warning, but the tested REST/ACL operation completed successfully. Vector/AI features remain untested.
