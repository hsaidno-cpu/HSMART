# GOV-02..GOV-12 AI Functional Delegate Runtime Activation and Evidence Plan

**Document ID:** HSMART-RUNTIME-GOV-DELEGATES-001  
**Version:** 0.1.0  
**Status:** IMPLEMENTATION FOUNDATION — DEPLOYMENT BLOCKED BY EXTERNAL PROVISIONING  
**Authority:** GOV-01; internal HSMART project scope only  
**Date:** 2026-11-22

## 1. Executive status

The five GOV-02..GOV-06 AI Functional Delegate profiles are designated but are not executable runtime instances. This document establishes a repeatable activation path and a reference policy enforcement implementation. It does not claim that a cloud account, hosted runtime, model endpoint, credential, Skill package, WORM store, or production control plane has been provisioned.

**Current lifecycle:** DESIGNATED.  
**Runtime state:** NOT_PROVISIONED.  
**Activation decision:** BLOCKED until every mandatory evidence gate in section 6 passes.

Human GOV-02..GOV-06 seats remain VACANT. AI functional delegates provide bounded interim task execution only; they do not become human officers or legal representatives.

## 2. Runtime topology

Use one isolated workload identity and runtime deployment per delegate, even if deployments share a hosting project:

| Role | Stable Agent ID | Runtime service name | Human seat |
|---|---|---|---|
| GOV-02 Project Owner | `hsmart.gov02.project-owner.orchestrator` | `hsmart-gov02-project-owner` | VACANT |
| GOV-03 Product Owner | `hsmart.gov03.product-owner.orchestrator` | `hsmart-gov03-product-owner` | VACANT |
| GOV-04 Architecture Lead | `hsmart.gov04.architecture.orchestrator` | `hsmart-gov04-architecture` | VACANT |
| GOV-05 Engineering Lead | `hsmart.gov05.engineering.orchestrator` | `hsmart-gov05-engineering` | VACANT |
| GOV-06 Security & Privacy Lead | `hsmart.gov06.security-privacy.orchestrator` | `hsmart-gov06-security-privacy` | VACANT |

Each service must have a separate workload identity, resource limits, environment, network policy, tool allowlist, model binding, Skill lockfile and audit correlation namespace. Do not share broad GitHub or Notion credentials between delegates.

## 3. Provider and model binding

No provider/model is selected by this record. The deployment operator must choose the actual provider and exact supported model/deployment ID after account and regional availability are confirmed.

For every deployment, record:
- Provider legal/service name and endpoint region.
- Exact model ID, immutable snapshot/version where provider exposes one, and deployment ID.
- API compatibility mode and inference parameters.
- Credential reference in a secret manager; never store the secret value in Git, Notion or logs.
- Date verified, verification method, and a redacted connectivity test result.

A family label such as "GPT", "Claude" or "Gemini" is insufficient provenance. If the provider does not expose an immutable model revision, record that limitation explicitly.

## 4. Skill/Sub-Skill installation and pinning

For each delegate, create a lock record containing Skill ID, source repository, immutable commit SHA or release digest, Sub-Skill manifest digest, dependency lock digest, license/provenance and installed runtime path. Floating branches and unpinned package tags are prohibited for activation.

A Skill is not considered installed merely because its name appears in the delegate registry. Run compatibility, permission-surface and regression tests in an isolated environment before activation.

## 5. Technical policy enforcement

A reference implementation is included at `src/hsmart_governance/policy.py`. It enforces:
- Verified actor identity and available audit path as prerequisites.
- DENY when approval grant is absent, invalid, revoked, expired or out of scope.
- Exact repository, branch, operation and path matching.
- Reserved human-only actions (merge, main write, production deploy, policy/permission change and raw-secret reads).
- HOLD for R3 pending separate human security review.
- DENY on unexpected evaluation errors.

The reference engine is not yet a production authorization service. Production integration must authenticate workload identity cryptographically, load grants from a trusted store, centralize policy version distribution, mediate every tool call at the gateway, prevent direct connector bypass, and emit an audit decision before allowing mutation. The enforcement point must be outside the Agent process.

## 6. Mandatory activation gates

| Gate | Required evidence | Failure disposition |
|---|---|---|
| A1 Runtime | Five distinct hosted runtime instances, health checks, isolated identities and resource/network policies | NOT_PROVISIONED |
| A2 Model | Provider, exact model/deployment ID, version semantics and successful redacted inference test per runtime | NOT_VERIFIED |
| A3 Skills | Immutable Skill/Sub-Skill lock records, digests, license/provenance and regression results | NOT_PINNED |
| A4 Policy | Central enforcement gateway intercepts every mutating tool operation; direct bypass denied | NOT_ENFORCED |
| A5 Permission | Positive/negative matrix passes, including no-grant, expired, revoked, scope escape, role mismatch and R4 denial | NOT_PASSED |
| A6 Fail-closed | Policy service outage, identity outage, grant-store outage and audit outage all deny mutation | NOT_PASSED |
| A7 Audit | Separate append-only/WORM store, retention lock, protected signing, integrity verification and restore test | NOT_PROVISIONED |
| A8 Delegate validation | Per-agent identity, model, Skills, tools, scope, cross-evaluation and incident-suspension tests | NOT_VERIFIED |
| A9 MVP | GOV-01 decision on exact MVP version, boundaries, success measures, exceptions and effective date | SATISFIED — HSMART-GOV-DEC-2026-11-22-001; MVP v1.1.0 APPROVED AS WRITTEN (2026-11-22) |
| A10 Charter | GOV-01 explicit RATIFY / RATIFY WITH CONDITIONS / RETURN FOR AMENDMENT decision with durable evidence | SATISFIED WITH CONDITIONS — Charter v1.0.2 RATIFIED WITH CONDITIONS (2026-11-22); HSMART-GOV-RAT-001 v1.4.0 |

No single gate may be waived by an AI delegate. Any exception requires a specific GOV-01 decision and must not weaken reserved human-only actions.

## 7. WORM audit target

The target design is a separate object-storage account/project with object lock enabled at bucket creation, compliance-mode retention selected by GOV-01 after legal/operational review, versioning, server-side encryption, a signing key protected by a KMS/HSM boundary, restricted write-only ingestion identity, separate read-only audit identity, and independent integrity/restore verification.

The repository's hash-chain reference or Git history is not WORM. A hash chain detects tampering only when trusted checkpoints and protected storage exist; it does not prevent an administrator from deleting the only copy. Do not mark A7 complete until object-lock configuration and deletion/retention-denial tests are evidenced.

## 8. Required external inputs

The following are prerequisites for actual cloud provisioning and cannot be safely fabricated:
1. Selected hosting/cloud account and project/workspace with owner authorization.
2. Verified deployment domain and DNS/TLS control if public endpoints are required.
3. Provider account, region, model ID and funded/authorized API credential.
4. Skill source repositories and exact approved revisions.
5. Secret-manager access and identity federation configuration.
6. WORM-capable object storage account, retention/legal-hold policy and protected signing key.
7. GOV-01 approval of any paid resource creation, budget ceiling and deployment scope.

Credentials must be entered directly into the chosen provider's secure connection/secret manager, never pasted into repository files or chat.

## 9. MVP and Charter decisions

The MVP Decision Record v1.1.0 was APPROVED AS WRITTEN by GOV-01 on 2026-11-22. Charter v1.0.2 was RATIFIED WITH CONDITIONS by GOV-01 on 2026-11-22 for internal HSMART project governance only. These decisions satisfy A9 and A10 as governance decision gates, but do not waive A1–A8, certify delivery, approve cloud expenditure, or activate any delegate. All five delegate runtimes remain NOT_PROVISIONED / NOT_ACTIVE until their individual technical evidence gates pass.

## 10. Per-delegate activation ledger

| Delegate | Runtime | Model | Skill pins | Policy tests | WORM audit | Cross-evaluation | Activation |
|---|---|---|---|---|---|---|---|
| GOV-02 | BLOCKED | PENDING | PENDING | PENDING | PENDING | PENDING | NOT ACTIVE |
| GOV-03 | BLOCKED | PENDING | PENDING | PENDING | PENDING | PENDING | NOT ACTIVE |
| GOV-04 | BLOCKED | PENDING | PENDING | PENDING | PENDING | PENDING | NOT ACTIVE |
| GOV-05 | BLOCKED | PENDING | PENDING | PENDING | PENDING | PENDING | NOT ACTIVE |
| GOV-06 | BLOCKED | PENDING | PENDING | PENDING | PENDING | PENDING | NOT ACTIVE |

Update this ledger only from deployment and test evidence. A successful local unit test does not prove hosted runtime activation.


## 11. Provisioning execution status — 2026-11-22

| Workstream | Verified current state | Evidence required to close |
|---|---|---|
| Compute and workload identity | No hosting project/account or five hosted service instances provisioned through the available connected tools | Select and connect an authorized provider account; create five isolated services with separate workload identities, resource/network policies, health checks and deploy provenance |
| Model/provider and credentials | No provider, exact model ID/snapshot, endpoint region or active model credential bound | GOV-01 selects provider/model and region; enter credential directly into the provider secret manager; record secret reference only and run a redacted inference test |
| Skill/Sub-Skill installation | Skill lock records/runtime installation/digests not evidenced by the merged reference foundation | Approve exact Skill sources/revisions, generate immutable lockfiles, verify artifact/dependency digests, license/provenance and compatibility/regression results per delegate |
| Technical policy enforcement | Local reference evaluator and 13 unit tests are in repository; no external gateway interception or bypass control is deployed | Deploy central authorization enforcement outside agents; cryptographically authenticate workload identities; mediate every connector/tool mutation; prove no bypass and policy outage DENY |
| Permission and fail-closed validation | Local reference tests exist; hosted integration matrix and outage tests not verified in this record | Prove positive/negative scopes, revoked/expired grants, role mismatch, branch/path escape, reserved human actions and fail-closed behavior for identity, policy, grant store and audit outages |
| Production audit | WORM design and event schema exist; no production object-lock storage provisioned | Connect WORM-capable storage; set retention only after GOV-01 decision; prove object-lock mode, protected signing, write-only ingestion, deletion-denial, integrity, backup/restore and independent read |
| Operations | GOV-07 Operations/Reliability remains unassigned | Appoint an operations owner or record human-approved interim coverage before production workloads |
| Deployment authority and budget | No hosting-provider connection, resource-creation authorization or budget ceiling recorded in this session | GOV-01 separately approves selected provider, project, region, expected spend ceiling and production/non-production scope |

**Connection finding:** The current session has GitHub and Notion project access, but no connected hosting/deployment, cloud IAM, model-provider, secret-manager or WORM-storage control-plane action. Provider discovery returned Railway and Render as available but not installed; no deployment action has been performed. Do not treat plugin discovery as an authenticated provider connection.

**Runtime disposition:** all five delegates remain DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE. This plan is an evidence register, not a deployment claim. Secrets must never be placed in GitHub, Notion or chat.


## 12. GOV-07 through GOV-12 runtime activation extension

The GOV-01 decision addendum `HSMART-GOV-DEC-2026-11-22-002` designates six additional AI Functional Delegates. Each is subject to mandatory A1–A8 activation gates and must have a distinct runtime identity, model binding, Skill pins, tool allowlist, approval-grant lineage and audit namespace.

| Delegate | Stable Agent ID | Scope | Runtime state | Activation |
|---|---|---|---|---|
| GOV-07 | `hsmart.gov07.operations-reliability.orchestrator` | Operations, reliability, incident triage and recovery evidence | NOT_PROVISIONED | NOT ACTIVE |
| GOV-08 | `hsmart.gov08.legal-commercial-research.orchestrator` | Legal/commercial research and drafting support only | NOT_PROVISIONED | NOT ACTIVE |
| GOV-09 | `hsmart.gov09.entitlement-governance.orchestrator` | Entitlement rules, rights evidence and quota tests | NOT_PROVISIONED | NOT ACTIVE |
| GOV-10 | `hsmart.gov10.repository-governance.orchestrator` | Repository protection specification and drift checks | NOT_PROVISIONED | NOT ACTIVE |
| GOV-11 | `hsmart.gov11.independent-assurance-reviewer.orchestrator` | Independent-context AI review and evidence challenge | NOT_PROVISIONED | NOT ACTIVE |
| GOV-12 | `hsmart.gov12.business-continuity.orchestrator` | Backup, restore, continuity and DR evidence | NOT_PROVISIONED | NOT ACTIVE |

The GOV-07 role designation satisfies internal functional allocation; it does not prove a hosted operations system, monitoring, backup, restore, on-call response or recovery process exists. GOV-08 is not legal counsel and cannot approve or sign external instruments. GOV-11 must not represent a correlated second persona as independent certification or submit a false GitHub-native human approval.

All six new delegates remain BLOCKED until A1–A8 evidence is recorded. Do not mark production operations, DR or security readiness complete from a designation, runbook or local test alone.
