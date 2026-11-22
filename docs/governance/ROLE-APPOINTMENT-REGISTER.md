# HSMART Accountable Role Appointment Register

**Register ID:** HSMART-GOV-ROLE-001  
**Version:** 1.1.0  
**Prepared:** 2026-11-22  
**Status:** READY FOR APPOINTMENT — PEOPLE NOT YET APPOINTED  
**Authority:** Project Charter v1.0.0, section 13 and decision-rights provisions

## 1. Operating rule

Every critical responsibility must have one accountable role owner, even when a small team assigns multiple roles to one person. A role is not appointed by appearing in a document, owning the repository, authoring a PR or being inferred from a username.

A valid appointment requires a named person, explicit appointing authority, effective date, accepted responsibility, decision limits and a durable record. Until those fields are completed and confirmed, the role remains UNASSIGNED.

## 2. Core appointment register

| Role ID | Role | Accountability | Decision rights | Appointment |
|---|---|---|---|---|
| GOV-01 | Project Sponsor / Accountable Owner | Strategic direction, funding/resources, scope and major risk decisions | D2/D3 approval and project-level risk acceptance within lawful authority | UNASSIGNED |
| GOV-02 | Project Owner | Delivery accountability, Charter maintenance, escalation and project records | D0/D1 within delegated scope; escalates D2/D3 | UNASSIGNED |
| GOV-03 | Product Owner | User needs, product priorities, MVP scope, acceptance and roadmap trade-offs | Product decisions within the approved Charter and budget | UNASSIGNED |
| GOV-04 | Architecture Lead | Architecture integrity, contracts, ADRs, domain boundaries and compatibility | Technical recommendation; D2 approval only if expressly delegated | UNASSIGNED |
| GOV-05 | Engineering Lead | Engineering practices, implementation quality, delivery plan and code review | D1 implementation within approved contracts and ADRs | UNASSIGNED |
| GOV-06 | Security & Privacy Lead | Threat model, privacy/security controls, risk review and incident escalation | Independent security review; may place a safety/security hold on release pending accountable disposition | UNASSIGNED |
| GOV-07 | Operations / Reliability Lead | Deployment, monitoring, backup, restore, incident and recovery readiness | Operational readiness recommendation and stop authority for unsafe operations under approved policy | UNASSIGNED |
| GOV-08 | Legal / Commercial Advisor | Entity, IP, licensing, publisher terms, privacy, tax and commerce review | Professional advice; legal approval remains with the legally authorized person/entity | TO ENGAGE WHEN NEEDED |
| GOV-09 | Capability Publisher Owner | Accuracy, provenance, permissions and lifecycle of each published capability | Publisher-level content and release attestations within policy | PER PUBLISHER / NOT APPLICABLE YET |

## 3. Decision-rights matrix

| Decision class | Examples | Accountable decision | Required consultation / evidence |
|---|---|---|---|
| D0 — Routine | Reversible maintenance, documentation corrections, routine test fixes | Delegated operational owner | Change record and relevant test |
| D1 — Delivery | Implementation within approved scope, contracts, ADRs and budget | Project Owner / delegated Engineering Lead | Code review, contract and regression tests |
| D2 — Baseline | MVP scope/acceptance, architecture baseline, material risk treatment or budget changes | Project Sponsor / Accountable Owner, with Product or technical owner for their domain | Written rationale, alternatives, risk and impact analysis, explicit approval |
| D3 — Project commitment | Charter adoption/amendment, project termination, legal/commercial obligations, ownership/IP commitments | Legally/organizationally authorized accountable authority | Required governance/legal review and durable decision evidence |

This table defines the intended HSMART decision routing. A role may exercise only the authority explicitly delegated to it. Legal, statutory, contractual or platform-owner authority cannot be created by this register.

## 4. Appointment evidence required

For each appointment, record:

- Role ID and exact role title.
- Person's confirmed full name and organization/affiliation where relevant.
- Appointing authority and evidence that the authority can make the appointment.
- Effective date and, if applicable, expiry/review date.
- Responsibilities accepted and explicit decision limits.
- Backup/deputy and escalation route.
- Conflict-of-interest declaration where material.
- Other roles held by the same person and any separation-of-duties exception.
- A durable approval reference (approved PR, meeting decision record or signed appointment instrument).

## 5. Minimum governance before KM 0 exit

The following are blocking:

1. Project Sponsor / Accountable Owner (GOV-01).
2. Project Owner (GOV-02).
3. Product Owner (GOV-03).
4. Architecture Lead (GOV-04).
5. Engineering Lead (GOV-05).
6. Security & Privacy Lead (GOV-06).

Operations/Reliability (GOV-07) must be appointed before hosted runtime or production operations. Legal/Commercial advice must be engaged before entity, IP, publisher, licensing or marketplace commitments.

## 6. Small-team role-combination rules

A small founding team may combine responsibilities, but combining roles does not erase independent review requirements.

- GOV-01 and GOV-02 may be held by one person during an early founder-led stage only when the appointment and authority are explicit.
- GOV-03 may be combined with GOV-02 when product scope and delivery trade-offs are documented.
- GOV-04 and GOV-05 may be combined during prototyping, but material architecture changes require independent review before release.
- GOV-06 should remain independent of the person implementing the security-sensitive change whenever feasible. If staffing makes this impossible, record the conflict and obtain an external review for high-risk releases.
- GOV-07 may be combined with GOV-05 for local development only; hosted/production operations require explicit operational ownership.
- Legal advice must not be represented as legal approval by a person without the relevant authority.

No one may approve their own material security exception, production data-destruction action or legal/commercial commitment solely because they hold multiple project roles.

## 7. Separation of duties and escalation

Where staffing is limited, role combinations must be visible in this register. Security-sensitive, production, data-destruction and commercial decisions require independent review where feasible. A disagreement over security, privacy, legal exposure or data integrity defaults to HOLD until the accountable authority records a reasoned disposition.

## 8. Closure condition

The register is structurally ready. The appointment task is not complete until the required named persons, appointing authority, effective dates, accepted responsibilities and decision limits are confirmed and read back. No person has been silently assigned.
