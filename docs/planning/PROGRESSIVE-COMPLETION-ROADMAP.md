# HSMART Progressive Completion Roadmap

**ID:** HSMART-ROADMAP-PC-001  
**Version:** 1.1.0  
**Status:** ACTIVE EXECUTION CONTROL — KM 0 OPEN / KM 1 IN PROGRESS / KM 2 BLOCKED  
**Main baseline at record preparation:** `17c78dcd2ea59c6d40f9a07d188bab6f829f0596`

## 1. Mandatory order

1. PR #13 canonical governance merge — MERGED at `17c78dcd2ea59c6d40f9a07d188bab6f829f0596`.
2. GOV-07 designation and repository governance — role DESIGNATED; main protection NOT APPLIED.
3. KM 0 closure — OPEN until role and repository protection evidence are reconciled.
4. KM 1 — ADR-011 accepted as internal stack baseline; application environment and PostgreSQL CI/independent assurance underway.
5. KM 2 Registry — BLOCKED until KM 1 is accepted by GOV-01 on exact commit/evidence.

Do not start Registry, public Gateway, arbitrary-code Runtime, commercial entitlement service or Synchronization Engine before KM 1 exit.

## 2. Verified evidence and limitations

- MVP v1.1.0 approved as written; Charter v1.0.2 ratified with conditions.
- ADR-011 v1.2.0 accepted as an internal technology baseline. Vendor, region, paid service, OIDC issuer, domain, KMS and artifact-store choices remain deferred.
- GOV-01 is the only human role in the internal model; GOV-02..GOV-12 are logical AI delegates, DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE.
- Main was read back as `protected=false`.
- Local KM 1 tests: 11 passed, 2 PostgreSQL tests skipped because no local PostgreSQL service was available.
- Alembic migration smoke passed on SQLite only.
- Deterministic repository pre-review passed; it is not an LLM review or production security audit.
- Hosted PostgreSQL 16 CI must pass on this exact PR head. Independent KM 1 evaluation and GOV-01 exact-commit acceptance remain mandatory.
- Production deployment, DR restore/failover, WORM audit and production security readiness are NOT DEPLOYED / NOT TESTED / NOT VERIFIED.

## 3. Role and reviewer model

GOV-01 is the sole human authority. GOV-02 through GOV-12 are logical AI delegates with bounded mandates. GOV-08 performs legal/commercial research, not legal advice or signing. GOV-11 produces AI assurance reports in a separate read-only context; no AI persona is represented as native GitHub approving actor. GOV-01 retains final merge decision.

## 4. Repository protection

Desired configuration is in `docs/governance/REPOSITORY-MAIN-RULESET.json`; local operator is `scripts/github-governance.py`. Dry-run is default. Actual apply requires an administrator token with `Administration: write`, `--apply --confirm-main` and the exact expected main SHA. The connected GitHub connector has no write operation for branch protection/rulesets. Until administrator apply, read-back and negative-control tests pass, protection is NOT_APPLIED.

## 5. KM 1 exit

- Python 3.12 clean environment, dependency check, migration and tests pass.
- PostgreSQL 16 hosted integration job passes.
- Deterministic governance check passes.
- GOV-11/independent assurance report records model/context correlation and no unresolved P0/P1.
- GOV-01 accepts the exact commit and evidence bundle.
- Only then open KM 2.

## 6. Downstream gates

| Stage | Scope | Entry condition |
|---|---|---|
| KM 2 | Registry identity, manifests, versions, digest/provenance, discovery | KM 1 accepted |
| KM 3 | Gateway/access, OIDC, API keys, REST/MCP parity | KM 2 contracts accepted |
| KM 4 | Isolated runtime, egress, quotas, retries/cancellation | KM 3 accepted |
| KM 5 | Evaluation, traces, metrics, audit evidence | KM 3 + KM 4 evidence |
| KM 6 | Desired/observed sync, staged rollout and rollback | KM 2 + KM 4 + KM 5 stable |
| KM 7+ | First-party integrations, adapters, marketplace, production hardening | Prior gates and legal/security/operations evidence |

A document or module name is not a service. A local test is not hosted evidence. A CI pass applies only to its exact job and commit. A merged PR is not a deployment.
