# HSMART Accountable Role Appointment Register

**Register ID:** HSMART-GOV-ROLE-001  
**Version:** 1.2.0  
**Prepared:** 2026-11-22  
**Status:** PARTIALLY APPOINTED — GOV-01 APPOINTED; OTHER CORE ROLES PENDING  
**Authority:** Project Charter v1.0.1 and Founder & Project Initiator Authority Declaration HSMART-GOV-FOUNDER-001

## 1. Operating rule

Every critical responsibility must have one accountable role owner, even when a small team assigns multiple roles to one person. Repository ownership, account access, authorship, or a username alone does not establish an appointment or legal authority.

For an unincorporated founder-led personal project, an explicit written founder self-declaration may establish an internal project appointment when it records the role holder, basis, effective date, accepted responsibility, decision limits, and evidence. Such a declaration cannot create authority over another person, legal entity, third-party asset, or right that the declarant does not control.

Each role must be read according to its recorded scope. An appointment to one role does not silently assign other roles.

## 2. Core appointment register

| Role ID | Role | Accountability | Decision rights | Appointment |
|---|---|---|---|---|
| GOV-01 | Project Sponsor / Accountable Owner | Strategic direction, internal project scope, priorities, and stewardship of resources actually controlled by the holder | D2 approval within internal project scope; D3 only for internal project-governance decisions and never to bind a third party or legal entity | APPOINTED — Harysaidno; founder self-declaration; internal project authority only |
| GOV-02 | Project Owner | Delivery accountability, Charter maintenance, escalation and project records | D0/D1 within delegated scope; escalates D2/D3 | UNASSIGNED |
| GOV-03 | Product Owner | User needs, product priorities, MVP scope, acceptance and roadmap trade-offs | Product decisions within the approved Charter and budget | UNASSIGNED |
| GOV-04 | Architecture Lead | Architecture integrity, contracts, ADRs, domain boundaries and compatibility | Technical recommendation; D2 approval only if expressly delegated | UNASSIGNED |
| GOV-05 | Engineering Lead | Engineering practices, implementation quality, delivery plan and code review | D1 implementation within approved contracts and ADRs | UNASSIGNED |
| GOV-06 | Security & Privacy Lead | Threat model, privacy/security controls, risk review and incident escalation | Independent security review; may place a safety/security hold on release pending accountable disposition | UNASSIGNED |
| GOV-07 | Operations / Reliability Lead | Deployment, monitoring, backup, restore, incident and recovery readiness | Operational readiness recommendation and stop authority for unsafe operations under approved policy | UNASSIGNED |
| GOV-08 | Legal / Commercial Advisor | Entity, IP, licensing, publisher terms, privacy, tax and commerce review | Professional advice; legal approval remains with the legally authorized person/entity | TO ENGAGE WHEN NEEDED |
| GOV-09 | Capability Publisher Owner | Accuracy, provenance, permissions and lifecycle of each published capability | Publisher-level content and release attestations within policy | PER PUBLISHER / NOT APPLICABLE YET |

### 2.1 GOV-01 appointment record

| Field | Recorded value |
|---|---|
| Role ID / title | GOV-01 — Project Sponsor / Accountable Owner |
| Role holder | Harysaidno (name exactly as supplied; separate civil-identity verification not performed) |
| Appointment type | Founder self-appointment for an unincorporated personal project |
| Authority basis | Founder & Project Initiator Authority Declaration, HSMART-GOV-FOUNDER-001 v1.0.0 |
| Appointing and accepting authority | Harysaidno, acting as the declared Founder and Project Initiator |
| Effective date | 2026-11-22 |
| Accepted accountability | Internal strategy, project scope, priorities, project-level decisions, and stewardship of resources actually controlled by the role holder |
| Decision limits | D2 within internal project scope; D3 restricted to internal governance. No legal-entity representation, third-party commitment, unverified IP ownership, or authority over assets not controlled by the role holder |
| Evidence | Explicit written project-governance instruction dated 2026-11-22 and durable declaration HSMART-GOV-FOUNDER-001 |
| Signature status | No separate handwritten, electronic, or cryptographic signature supplied; the written instruction is the recorded declaration evidence |
| Other roles | No other role is inferred or appointed by this record |

**Appointment disposition:** APPOINTED — INTERNAL PROJECT GOVERNANCE ONLY. This is not a corporate appointment, statutory authorization, proof of civil identity, or proof of title to all HSMART-related intellectual property.

## 3. Decision-rights matrix

| Decision class | Examples | Accountable decision | Required consultation / evidence |
|---|---|---|---|
| D0 — Routine | Reversible maintenance, documentation corrections, routine test fixes | Delegated operational owner | Change record and relevant test |
| D1 — Delivery | Implementation within approved scope, contracts, ADRs and authorized budget | Project Owner / delegated Engineering Lead | Code review, contract and regression tests |
| D2 — Baseline | Internal MVP scope/acceptance, architecture baseline, material risk treatment or project-resource changes | GOV-01 for internal project approval, with Product or technical owner for their domain | Written rationale, alternatives, risk and impact analysis, explicit approval |
| D3 — Project commitment | Internal Charter adoption/amendment or project termination; separately, any external legal/commercial, ownership/IP or contractual commitment | GOV-01 may decide internal project-governance matters only. External commitments require the legally authorized person/entity and applicable professional review | Durable internal decision record; for external matters, separate authority, legal review and valid instrument |

This matrix defines HSMART's intended decision routing. A role may exercise only the authority explicitly recorded and lawfully available to its holder. No entry in this register creates legal, statutory, contractual, platform-owner, intellectual-property, or third-party authority. HSMART is currently a personal project and must not be represented as a legal entity.

## 4. Appointment evidence required

For each appointment, record:

- Role ID and exact role title.
- Person's confirmed name and organization/affiliation where relevant.
- Appointing authority and evidence that the authority can make the appointment.
- Effective date and, if applicable, expiry/review date.
- Responsibilities accepted and explicit decision limits.
- Backup/deputy and escalation route.
- Conflict-of-interest declaration where material.
- Other roles held by the same person and any separation-of-duties exception.
- A durable approval reference (approved PR, meeting decision record or signed appointment instrument).

For a founder's internal self-appointment in an unincorporated personal project, the evidence must explicitly state the founder/initiator capacity and must preserve the limitations in HSMART-GOV-FOUNDER-001.

## 5. Minimum governance before KM 0 exit

The following remain blocking:

1. GOV-01 Project Sponsor / Accountable Owner — **APPOINTED** to Harysaidno for internal project governance only.
2. GOV-02 Project Owner — UNASSIGNED.
3. GOV-03 Product Owner — UNASSIGNED.
4. GOV-04 Architecture Lead — UNASSIGNED.
5. GOV-05 Engineering Lead — UNASSIGNED.
6. GOV-06 Security & Privacy Lead — UNASSIGNED.

GOV-01 being appointed does not satisfy the remaining role appointments, MVP approval, or Charter ratification requirements.

Operations/Reliability (GOV-07) must be appointed before hosted runtime or production operations. Legal/Commercial advice must be engaged before entity, IP, publisher, licensing or marketplace commitments.

## 6. Small-team role-combination rules

A small founding team may combine responsibilities, but combining roles does not erase independent review requirements.

- GOV-01 and GOV-02 may be held by one person during an early founder-led stage only when the appointment and authority are explicit. GOV-01 appointment does not itself appoint GOV-02.
- GOV-03 may be combined with GOV-02 when product scope and delivery trade-offs are documented.
- GOV-04 and GOV-05 may be combined during prototyping, but material architecture changes require independent review before release.
- GOV-06 should remain independent of the person implementing the security-sensitive change whenever feasible. If staffing makes this impossible, record the conflict and obtain an external review for high-risk releases.
- GOV-07 may be combined with GOV-05 for local development only; hosted/production operations require explicit operational ownership.
- Legal advice must not be represented as legal approval by a person without the relevant authority.

No one may approve their own material security exception, production data-destruction action, or external legal/commercial commitment solely because they hold multiple project roles.

## 7. Separation of duties and escalation

Where staffing is limited, role combinations must be visible in this register. Security-sensitive, production, data-destruction and commercial decisions require independent review where feasible. A disagreement over security, privacy, legal exposure or data integrity defaults to HOLD until the accountable authority records a reasoned disposition. GOV-01 cannot override an independent security hold merely by virtue of being the project sponsor.

## 8. Closure condition

The GOV-01 appointment is recorded and effective for internal project governance as of 2026-11-22. The overall core-role appointment task remains IN_PROGRESS because GOV-02 through GOV-06 remain unassigned and the required role, review, and decision evidence is incomplete. No additional person or role has been silently appointed.
