# HSMART Accountable Role Appointment Register

**Register ID:** HSMART-GOV-ROLE-001  
**Prepared:** 2026-11-22  
**Status:** Appointment template and decision-rights baseline; no people appointed by this record  
**Authority:** Project Charter v1.0.0, section 13

## 1. Operating rule

Every critical responsibility must have one accountable role owner, even when a small team assigns multiple roles to one person. A role is not appointed by appearing in a document, owning the repository, authoring a PR or being inferred from a username.

Names, authority and effective dates must be explicitly confirmed by the accountable project authority. Until then, roles below remain UNASSIGNED.

## 2. Appointment register

| Role ID | Role | Accountability | Decision rights | Appointment |
|---|---|---|---|---|
| GOV-01 | Project Sponsor / Accountable Owner | Strategic direction, funding/resources, scope and major risk decisions | D2/D3 approval and risk acceptance | UNASSIGNED |
| GOV-02 | Project Owner | Delivery accountability, Charter maintenance, escalation and project records | D0/D1 within delegated scope; escalates D2/D3 | UNASSIGNED |
| GOV-03 | Product Owner | User needs, product priorities, MVP scope, acceptance and roadmap trade-offs | Product decisions within approved Charter | UNASSIGNED |
| GOV-04 | Architecture Lead | Architecture integrity, contracts, ADRs, domain boundaries and compatibility | Technical recommendation; D2 approval only if delegated | UNASSIGNED |
| GOV-05 | Engineering Lead | Engineering practices, implementation quality, delivery plan and code review | D1 implementation within approved contracts | UNASSIGNED |
| GOV-06 | Security & Privacy Lead | Threat model, privacy/security controls, risk review and incident escalation | Security review; may hold unsafe release pending accountable decision | UNASSIGNED |
| GOV-07 | Operations / Reliability Lead | Deployment, monitoring, backup, restore, incident and recovery readiness | Operational readiness recommendation | UNASSIGNED |
| GOV-08 | Legal / Commercial Advisor | Entity, IP, licensing, publisher terms, privacy, tax and commerce review | Professional advice; legal approval by the appropriate authority | TO ENGAGE WHEN NEEDED |
| GOV-09 | Capability Publisher Owner | Accuracy, provenance, permissions and lifecycle of each published capability | Publisher-level content and release attestations within policy | PER PUBLISHER / NOT APPLICABLE YET |

## 3. Appointment record fields

For each appointment, record:
- Role ID and exact role title.
- Person's confirmed identity and organization/affiliation where relevant.
- Appointing authority and evidence of delegated authority.
- Effective date and, if applicable, expiry/review date.
- Responsibilities accepted and decision limits.
- Backup/deputy and escalation route.
- Conflict-of-interest declaration where material.
- Whether the same person holds another control/review role; document separation-of-duties exceptions.

## 4. Minimum governance before implementation expands

The following appointments are blocking for formal KM 0 exit:
1. Project Sponsor / Accountable Owner.
2. Project Owner.
3. Product Owner.
4. Architecture Lead.
5. Engineering Lead.
6. Security & Privacy Lead.

Operations/Reliability should be appointed before hosted runtime or production operations. Legal/Commercial advice is required before entity, IP, publisher, licensing or marketplace commitments.

## 5. Separation of duties

Where staffing is limited, one person may hold several roles, but the register must expose the combination. For security-sensitive, production, data-destruction and commercial decisions, independent review is preferred and any exception must be recorded.

## 6. Closure condition

This register is structurally prepared. The role-appointment task is not complete until the required named persons, appointing authority, effective dates and decision limits are confirmed and read back. No person has been silently assigned.
