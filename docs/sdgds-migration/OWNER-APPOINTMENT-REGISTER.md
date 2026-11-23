# SDGDS Human Owner Appointment Register

**Decision authority:** GOV-01  
**State:** All execution/assurance seats below remain UNASSIGNED until named humans explicitly accept the responsibilities.  
**Restriction:** AI agents may prepare analysis, code, tests, evidence and runbooks. They do not fill human accountability seats.

| Role | Required responsibility | Minimum acceptance evidence | State |
|---|---|---|---|
| GOV-01 | Final decision authority for scope, architecture, risk acceptance, cutover and retirement | Decision record with scope and limits | Existing authority; approval must be recorded per gate |
| Execution owner | Coordinate delivery, dependencies, scope, reporting and escalation | Named individual, acceptance, authority, capacity and escalation route | UNASSIGNED |
| Architecture owner | Own ADRs, module boundaries, API/data contracts and design consistency | Named individual, experience evidence and architecture review acceptance | UNASSIGNED |
| Migration lead / Data steward | Inventory, mapping, IDs, provenance, reconciliation, exceptions and data-quality disposition | Named individual, migration method, quality gates and exception approval boundary | UNASSIGNED |
| Platform/SRE operator | Runtime, database, network, secrets, observability, backups, restore, incidents and service recovery | Named individual, access boundary, on-call/availability model, restore and incident acceptance | UNASSIGNED |
| Security/privacy reviewer | Threat model, OIDC/JWKS, authorization, secrets, data classification, retention and security testing | Named independent reviewer, review scope and sign-off evidence | UNASSIGNED |
| Independent verifier | Reproduce gate tests and challenge evidence independently of implementation author | Named reviewer, independence statement, test plan and gate report | UNASSIGNED |

## Appointment rules

1. GOV-01 records a person's name, role, responsibilities, authority limits, access scope, availability and date of acceptance.
2. A person cannot independently verify their own implementation as the sole verifier.
3. Platform/SRE must explicitly accept backup, restore, recovery, incident response, credential rotation and emergency suspension.
4. A security reviewer must not be the sole implementation author for the controls being approved.
5. Until these seats are assigned and accepted, production readiness remains BLOCKED. Do not infer ownership from commit authorship, repository admin permission or AI-agent activity.
