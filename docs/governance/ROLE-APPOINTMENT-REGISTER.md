# HSMART Accountable Role Appointment Register

**Register ID:** HSMART-GOV-ROLE-001  
**Version:** 1.3.0  
**Prepared:** 2026-11-22  
**Status:** GOV-01 IS THE ONLY HUMAN AUTHORITY; GOV-02..GOV-12 AI FUNCTIONAL DELEGATES DESIGNATED; NO OTHER HUMAN ROLE SEATS  
**Authority:** Project Charter v1.0.2; Founder & Project Initiator Authority Declaration HSMART-GOV-FOUNDER-001; AI Functional Delegation Charter HSMART-GOV-AI-DEL-001

## 1. Operating rule

Every critical responsibility must have one accountable role owner, even when a small team assigns multiple roles to one person. Repository ownership, account access, authorship, or a username alone does not establish an appointment or legal authority.

For an unincorporated founder-led personal project, an explicit written founder self-declaration may establish an internal project appointment when it records the role holder, basis, effective date, accepted responsibility, decision limits, and evidence. Such a declaration cannot create authority over another person, legal entity, third-party asset, or right that the declarant does not control.

Each role must be read according to its recorded scope. An appointment to one role does not silently assign other roles.

## 2. Core appointment register

| Role ID | Role | Accountability | Decision rights | Appointment |
|---|---|---|---|---|
| GOV-01 | Project Sponsor / Accountable Owner | Strategic direction, internal project scope, priorities, and stewardship of resources actually controlled by the holder | D2 approval within internal project scope; D3 only for internal project-governance decisions and never to bind a third party or legal entity | APPOINTED — Harysaidno; founder self-declaration; internal project authority only |
| GOV-02 | Project Owner | Delivery coordination, Charter maintenance proposals, backlog, milestones, dependencies, risk tracking and evidence reporting | D0/D1 only within a GOV-01 authorization grant; escalates D2/D3 | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov02.project-owner.orchestrator`; human seat VACANT; runtime pending |
| GOV-03 | Product Owner | User needs, product discovery, requirement drafts, product priorities, acceptance proposals and product metrics | Product recommendations only; MVP/scope approval remains GOV-01 | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov03.product-owner.orchestrator`; human seat VACANT; runtime pending |
| GOV-04 | Architecture Lead | Architecture integrity, contracts, ADR proposals, domain boundaries, interoperability and quality attributes | Technical recommendation only; GOV-01 approves material D2 decisions | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov04.architecture.orchestrator`; human seat VACANT; runtime pending |
| GOV-05 | Engineering Lead | Engineering practices, implementation of approved work, code quality, tests, CI and technical documentation | Branch-scoped D1 only under explicit GOV-01 grant; no main write, merge or production release | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov05.engineering.orchestrator`; human seat VACANT; runtime pending |
| GOV-06 | Security & Privacy Lead | Threat modeling, security/privacy review, identity/policy assessment, supply-chain assurance and incident escalation | May recommend/maintain HOLD; cannot waive or accept its own finding or risk | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov06.security-privacy.orchestrator`; human seat VACANT; runtime pending |
| GOV-07 | Operations / Reliability Lead | Runbooks, service health, incident triage, backup/restore exercises and operational readiness | Bounded operation under GOV-01-approved playbooks; no independent production release | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov07.operations-reliability.orchestrator`; runtime NOT_PROVISIONED / NOT_ACTIVE |
| GOV-08 | Legal / Commercial Research | Legal/commercial issue spotting, jurisdiction research, license/contract drafting support | Research and drafting only; not legal counsel, not a lawyer, cannot sign or bind third parties | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov08.legal-commercial-research.orchestrator`; runtime NOT_PROVISIONED / NOT_ACTIVE |
| GOV-09 | Entitlement Governance Steward | Internal entitlement model, license-to-permission mapping, quota, expiry, revocation and entitlement evidence | Policy proposal and test evidence only; GOV-01 approves internal policy and rights remain with publishers | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov09.entitlement-governance.orchestrator`; runtime NOT_PROVISIONED / NOT_ACTIVE |
| GOV-10 | Repository Governance Lead | Main-branch ruleset specification, drift checks, change-control and protection evidence | Prepare/apply only with a specific GOV-01 grant and administrator authorization; no bypass or merge | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov10.repository-governance.orchestrator`; runtime NOT_PROVISIONED / NOT_ACTIVE |
| GOV-11 | Independent Assurance Reviewer | Separate-context AI review, challenge tests, evidence completeness, dissent and re-check | Read-only reviewer; no self-approval, GitHub-native human approval, merge or release | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov11.independent-assurance-reviewer.orchestrator`; runtime NOT_PROVISIONED / NOT_ACTIVE |
| GOV-12 | Business Continuity / Disaster Recovery Lead | Recovery plans, backup validation, DR test design, restoration evidence and continuity reporting | No claim of readiness without executed tests; no unilateral destructive failover | AI FUNCTIONAL DELEGATE DESIGNATED: `hsmart.gov12.business-continuity.orchestrator`; runtime NOT_PROVISIONED / NOT_ACTIVE |
| GOV-09 | Capability Publisher Owner | Accuracy, provenance, permissions and lifecycle of each published capability | Publisher-level content and release attestations within policy | PER PUBLISHER / NOT APPLICABLE YET |

### 2.1 GOV-01 appointment record

### 2.2 GOV-02 through GOV-06 AI Functional Delegate designation

| GOV | Stable Agent ID | Human role seat | Designation status | Authority boundary |
|---|---|---|---|---|
| GOV-02 | `hsmart.gov02.project-owner.orchestrator` | VACANT | DESIGNATED — runtime pending | Delivery coordination and evidence within grant; no scope, budget or risk approval |
| GOV-03 | `hsmart.gov03.product-owner.orchestrator` | VACANT | DESIGNATED — runtime pending | Product research and recommendation; no MVP/strategy approval |
| GOV-04 | `hsmart.gov04.architecture.orchestrator` | VACANT | DESIGNATED — runtime pending | Architecture and ADR proposals; no final material architecture approval |
| GOV-05 | `hsmart.gov05.engineering.orchestrator` | VACANT | DESIGNATED — runtime pending | Approved branch-scoped implementation, tests and PR preparation; no merge/release |
| GOV-06 | `hsmart.gov06.security-privacy.orchestrator` | VACANT | DESIGNATED — runtime pending | Security/privacy assessment and HOLD recommendation; no self-certification or self-risk-acceptance |

**Designation basis:** GOV-01 instruction dated 2026-11-22, approval `HSMART-AUTH-GOV01-20261122-002`, and AI Functional Delegation Charter `HSMART-GOV-AI-DEL-001`.

**Important distinction:** these are logical AI functional delegate profiles, not natural persons or human statutory role appointments. Runtime state is NOT PROVISIONED / NOT VERIFIED. Exact model, Skill, Sub-Skill and tool versions must be captured from a future runtime; until then they remain unknown or pending runtime binding.

The detailed mandates, sub-agent trees, Skills/Sub-Skills, logical tools, activation gates and lifecycle states are maintained in the [AI Functional Delegate Registry](AI-FUNCTIONAL-DELEGATE-REGISTRY.md) and machine-readable [registry JSON](AI-FUNCTIONAL-DELEGATE-REGISTRY.json). Permissions, cross-evaluation and audit rules are governed by the linked AI policies.


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

This matrix defines HSMART's intended decision routing. The AI Functional Delegates provide operational capacity only; they are not natural persons or legal officeholders and do not receive independent final decision authority. Every mutating operation remains subject to the centralized policy and a valid GOV-01 grant. A role may exercise only the authority explicitly recorded and lawfully available to its holder. No entry in this register creates legal, statutory, contractual, platform-owner, intellectual-property, or third-party authority. HSMART is currently a personal project and must not be represented as a legal entity.

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

For an AI Functional Delegate designation, additionally record the stable Agent ID, profile version, human role-seat status, exact mandate, runtime state, model/provider/version or `unknown`, Skill/Sub-Skill revisions and digests, tool/connector scopes, policy version, approval-grant lineage, independent evaluation results and audit-event references. A logical designation does not prove a runtime exists or is active.

## 5. Minimum governance before KM 0 exit

The interim operating coverage is now recorded as follows:

1. GOV-01 Project Sponsor / Accountable Owner — **HUMAN APPOINTED** to Harysaidno for internal project governance only.
2. GOV-02 Project Owner — **AI FUNCTIONAL DELEGATE DESIGNATED**; human role seat VACANT; runtime not provisioned/verified.
3. GOV-03 Product Owner — **AI FUNCTIONAL DELEGATE DESIGNATED**; human role seat VACANT; runtime not provisioned/verified.
4. GOV-04 Architecture Lead — **AI FUNCTIONAL DELEGATE DESIGNATED**; human role seat VACANT; runtime not provisioned/verified.
5. GOV-05 Engineering Lead — **AI FUNCTIONAL DELEGATE DESIGNATED**; human role seat VACANT; runtime not provisioned/verified.
6. GOV-06 Security & Privacy Lead — **AI FUNCTIONAL DELEGATE DESIGNATED**; human role seat VACANT; runtime not provisioned/verified.

The five AI designations provide interim functional coverage only. They do not appoint human occupants, confer legal capacity or satisfy any human-specific approval requirement. MVP approval, Charter ratification and technical acceptance remain separate decisions.

Operations/Reliability (GOV-07) must be appointed before hosted runtime or production operations. Legal/Commercial advice must be engaged before entity, IP, publisher, licensing or marketplace commitments.

## 6. Small-team role-combination rules

A small founding team may combine responsibilities, but combining roles does not erase independent review requirements.

- GOV-01 and GOV-02 may be held by one human during an early founder-led stage only when the appointment and authority are explicit. GOV-01 appointment does not itself appoint GOV-02. The GOV-02 AI Functional Delegate provides interim delivery coordination but does not become a human Project Owner.
- GOV-03 may be combined with GOV-02 when product scope and delivery trade-offs are documented.
- GOV-04 and GOV-05 may be combined during prototyping, but material architecture changes require independent review before release.
- GOV-06 is an AI security/privacy functional delegate, not a substitute for independent human expertise. It must not be the sole reviewer of its own work or the GOV-05 implementation it reviews. Use a separate evaluation context, appropriate automated tests and external human review for high/critical issues.
- GOV-07 may be combined with GOV-05 for local development only; hosted/production operations require explicit operational ownership.
- Legal advice must not be represented as legal approval by a person without the relevant authority.

No one may approve their own material security exception, production data-destruction action, or external legal/commercial commitment solely because they hold multiple project roles.

## 7. Separation of duties and escalation

Where staffing is limited, operational functions may be delegated to AI profiles, but authority remains centralized in GOV-01. Cross-evaluation must use multiple perspectives and context-appropriate methods; a model/persona vote is not sufficient evidence. Security-sensitive, production, data-destruction and commercial decisions require independent review and a human gate where applicable. A disagreement over security, privacy, legal exposure or data integrity defaults to HOLD until GOV-01 records a reasoned disposition and required expert review is complete. GOV-01 cannot change a test result or erase an unresolved critical finding merely by virtue of being the project sponsor.

## 8. Closure condition

The GOV-01 human appointment is recorded and effective for internal project governance as of 2026-11-22. GOV-02 through GOV-06 have been designated as interim AI Functional Delegates by GOV-01 under HSMART-AUTH-GOV01-20261122-002. Their human role seats remain VACANT and their runtime instances are not provisioned or verified. The core-role task is therefore PARTIALLY COVERED / IN_PROGRESS, not fully complete. MVP v1.1.0 approval is recorded as APPROVED AS WRITTEN and Charter v1.0.2 adoption is recorded as RATIFIED WITH CONDITIONS under HSMART-GOV-DEC-2026-11-22-001 / HSMART-GOV-RAT-001 v1.4.0. Policy enforcement implementation, hosted runtime provisioning, production WORM audit and Agent activation remain separate open gates.


## 9. GOV-01 decision addendum — AI-only role allocation beyond GOV-01

Effective 2026-11-22, GOV-01 has directed that GOV-01 is the sole human role in the internal HSMART governance model. GOV-02 through GOV-12 are logical AI Functional Delegates with distinct remits under decision `HSMART-GOV-DEC-2026-11-22-002`.

This does not turn AI profiles into natural persons, professional advisers, corporate officers or legal signatories. Each delegate remains DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE until its individual runtime activation gates pass. GOV-08 provides legal/commercial research only. External legal, tax, privacy, IP, publisher and commercial commitments still require a legally authorized person/entity and qualified human professional review where applicable.

GOV-11 is the designated logical AI reviewer. A review must disclose model/provider/context correlation. An AI review report is not a GitHub-native human approval. GOV-01 retains final human approval and merge authority.
