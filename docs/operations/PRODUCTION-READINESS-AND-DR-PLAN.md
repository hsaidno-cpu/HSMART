# HSMART Production Readiness, Disaster Recovery and Security Plan

**Document ID:** HSMART-OPS-DR-001  
**Version:** 1.0.0  
**Status:** PLAN / NOT PRODUCTION-VERIFIED  
**Owner role:** GOV-07 Operations & Reliability AI Functional Delegate (designated; runtime not provisioned)  
**Security counterpart:** GOV-06; independent assurance: GOV-11  
**Decision authority:** GOV-01  
**Date:** 2026-11-22

## 1. Current verified posture

The repository contains a KM 1 FastAPI/SQLAlchemy/Alembic application foundation, PostgreSQL 16 CI integration workflow, local tests, deterministic repository-governance pre-review and a desired main-protection configuration. It does not contain evidence of a production cloud account, hosted endpoint, deployed workload, production database, identity provider, secret manager/KMS, WORM audit store, backup schedule, completed restore, tested failover, SLO, RPO or RTO.

**Production state: NOT DEPLOYED. DR state: NOT TESTED. Production security readiness: NOT VERIFIED.** A local code test, container recipe, successful CI check or architecture document cannot substitute for a target-environment exercise.

## 2. Environment separation

| Environment | Purpose | Data and secrets |
|---|---|---|
| Local development | FastAPI, migrations, unit tests and isolated developer work | Synthetic data; local-only credentials |
| CI | Reproducible contract/application/security checks | Ephemeral test credentials and synthetic data only |
| Hosted acceptance / staging | Provider proof-of-fit, OIDC, PostgreSQL, object retention, egress and restore tests | Synthetic/non-production data and distinct staging secrets |
| Production | Authorized user workloads after readiness gates | Approved data classes, managed secrets and access controls |

No environment shares broad database credentials or deployment tokens. CI from untrusted pull requests receives no production secrets.

## 3. Required production security controls

- OIDC issuer, audience, subject and token lifetime validation; short-lived workload identity for worker services.
- External policy enforcement point; default-deny and fail-closed if identity, policy, grant or audit dependencies are unavailable.
- Tenant-scoped database access and negative isolation tests.
- Managed secret manager and KMS/HSM-backed keys; no raw secrets in Git, chat, Notion, manifests, logs or prompts.
- Separate least-privilege API and worker identities; worker default-deny network egress.
- SSRF-resistant connector egress proxy with destination, DNS, redirect, scheme, port and response-size validation.
- Signed artifacts, immutable version IDs, digest verification, dependency lock, SBOM and build provenance.
- Centralized security logs with redaction, restricted read access, tamper-resistant/WORM retention and verified signing-key custody.
- Rate limits, quotas, timeouts, concurrency bounds, resource limits and abuse controls.
- CI checks, independent AI review evidence, security challenge, GOV-01 acceptance and rollback plan for release.

## 4. Backup and disaster-recovery design

The provider and topology are deliberately unselected pending data-residency, cost, recovery and security comparison. The eventual system must separately protect:

1. PostgreSQL system-of-record data and migration history.
2. Immutable capability artifacts and metadata/digests.
3. WORM audit evidence and signing/verification metadata.
4. Configuration, deployment manifests and infrastructure-as-code state.
5. Secret-manager recovery and KMS key custody (never by exporting plaintext keys to Git).

Backups must be encrypted, access-restricted, monitored, retained according to approved policy and stored in a failure domain separate from the primary service. Replication alone is not backup. Object versioning alone is not WORM. A successful backup job is not proof of recoverability.

## 5. DR exercise matrix

| Exercise | Expected result | Evidence required | Current state |
|---|---|---|---|
| PostgreSQL point-in-time restore | Restore to isolated target and reconcile committed data | Backup ID, restore logs, consistency queries, elapsed time | NOT RUN |
| Object artifact restore | Retrieve exact version and verify SHA-256/signature | Object version, digest comparison and access log | NOT RUN |
| WORM deletion-denial | Privileged normal identity cannot delete/shorten retention | Object-lock configuration and negative API result | NOT RUN |
| Audit integrity recovery | Verify signed checkpoints and complete event chain from independent storage | Verification report and signing-key reference | NOT RUN |
| Application redeploy | Rebuild OCI image from pinned source and deploy with migration controls | Image digest, build provenance and deployment ID | NOT RUN |
| Credential compromise | Revoke affected identity/key, rotate references and deny old credential | Revocation event and negative authentication test | NOT RUN |
| Region/provider outage | Restore service in approved recovery region/account if selected | Runbook execution, failover and data reconciliation | NOT RUN |
| Worker crash / duplicate delivery | No silent loss; idempotency and retry/dead-letter behavior hold | Integration test and event ledger | LOCAL FOUNDATION TEST ONLY |

RPO/RTO values must be derived from workload and business impact, explicitly approved by GOV-01, and measured during exercises. Do not invent numerical recovery objectives before deployment topology and data classes are selected.

## 6. Go-live gates

- Main branch protection and required CI checks verified by GitHub API read-back and negative test.
- KM 1 accepted with PostgreSQL 16 hosted CI and separate AI assurance report.
- GOV-07 delegate runtime and operational tool scopes provisioned and tested; GOV-01 approves the runbooks and emergency powers.
- Cloud provider, region, domain, budget ceiling, OIDC, secret manager, KMS, artifact storage and logging are selected and provisioned by an authorized account owner.
- Policy enforcement, permission and fail-closed tests pass at the deployed boundary.
- WORM retention, deletion denial, signing and restore tests pass.
- Backup restore and at least one DR exercise meet approved RPO/RTO.
- Independent security review has no open critical/high findings (or a specifically authorized, lawful risk disposition where acceptance is permitted).
- Incident response, alert routing, credential rotation, rollback and emergency suspension are exercised.
- GOV-01 explicitly accepts the exact release commit, artifact digest, environment and residual risk.

## 7. Stop conditions

Any missing owner, untested restore, failed tenant isolation, secret exposure, policy bypass, unverified artifact, unresolved critical finding, missing authorization or incomplete audit chain blocks production promotion. In an incident, containment may proceed under a pre-approved runbook; irreversible action or external commitment must follow its lawful authority and approval path.

**Disposition:** readiness plan only. No production deployment, successful disaster recovery, DR objective, independent security certification or production approval is claimed.
