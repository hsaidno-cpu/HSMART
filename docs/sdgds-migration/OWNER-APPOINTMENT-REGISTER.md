# SDGDS Migration — GOV Delegate Mapping

**Authority:** HSMART GOV-01 Decision Addendum `HSMART-GOV-DEC-2026-11-22-002`  
**Snapshot:** 23 November 2026  
**Lifecycle:** DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE

GOV-01 is the sole human internal decision authority. SDGDS migration work is mapped to existing HSMART functional delegates; this does not create new GOV seats or activate any runtime.

| SDGDS workstream | Delegate | Scope | Reserved authority |
|---|---|---|---|
| Execution owner / delivery coordination | `hsmart.gov02.project-owner.orchestrator` | Critical path, dependencies, backlog, status and escalation | Cannot approve own baseline, accept risk or change scope |
| Architecture owner | `hsmart.gov04.architecture.orchestrator` | Domain boundaries, ADR, data/API/MCP contracts and compatibility | Prepares decisions; GOV-01 approves |
| Migration lead / data steward | `hsmart.gov05.database-agent` under `hsmart.gov05.engineering.orchestrator` | Read-only export mapping, stable IDs, ETL, schema migration, quality checks, reconciliation and exception reports | Cannot promote Proposed terms to Canonical or authorize source changes without grant |
| Platform / SRE operator | `hsmart.gov07.operations-reliability.orchestrator` | Disposable runtime, runbooks, service health, incidents and backup/restore evidence | No production deployment, destructive action or external procurement |
| Security / privacy reviewer | `hsmart.gov06.security-privacy.orchestrator` | Threat model, OIDC, authorization, least privilege, privacy and security HOLD recommendations | Cannot waive own findings or accept a security exception |
| Independent verifier | `hsmart.gov11.independent-assurance-reviewer.orchestrator`, coordinated by `hsmart.assurance.cross-evaluation-orchestrator` | Separate-context review, evidence completeness and challenge tests | Cannot self-approve, impersonate GitHub human review or merge/release |

## Activation gates

All delegates remain logical designations until each profile has a stable runtime identity, exact model/provider/version binding, versioned instructions and Skills, task-scoped tool grants, policy enforcement, positive/negative authorization tests, audit logging, fail-closed behaviour and GOV-01 activation approval.

No agent has been marked ACTIVE by this package. Production readiness remains blocked until delegate runtimes, tools, identity, audit and recovery evidence are provisioned and verified. GOV-01 retains final internal approval. External legal/commercial commitments and resources outside the project's controlled accounts remain subject to the legally authorized person/entity and qualified professional review where applicable.


## Human accountability and production-readiness gap

The delegates above are **logical AI workstream mappings only**. They are not human appointees and are not active runtime instances. The existing HSMART delegation charter records GOV-02 through GOV-06 human seats as vacant; this migration package contains no acceptance record from a qualified human production operator.

| Human accountability | Current disposition | Required before production |
|---|---|---|
| Internal final decision authority (GOV-01) | Identified in the HSMART charter | Retains approval, risk acceptance, cutover and merge authority |
| Execution accountable human | NOT APPOINTED / NOT ACCEPTED | Name and acceptance record for schedule, delivery and escalation accountability |
| Security/privacy human reviewer | NOT APPOINTED / NOT ACCEPTED | Qualified reviewer who can independently challenge security/privacy findings |
| Data steward / migration accountable human | NOT APPOINTED / NOT ACCEPTED | Named owner for data meaning, provenance, exception disposition and migration sign-off |
| Platform/SRE human operator (GOV-07 or accepted interim) | NOT APPOINTED / NOT ACCEPTED | Named qualified human accountable for monitoring, backup, restore, incident response, credential rotation, emergency suspension and recovery |
| Independent human verifier | NOT APPOINTED / NOT ACCEPTED | Reviewer independent of implementation author and with access to the required evidence |

AI delegates may prepare plans, operate authorized disposable test environments and collect evidence under scoped permissions. They cannot satisfy the human operational-accountability requirement, approve their own work, accept residual risk, authorize a production write, or replace an independent human review. Until the required human appointments and acceptances are recorded, M7 production readiness remains BLOCKED.
