# HSMART Project Charter — Formal Ratification Record

**Record ID:** HSMART-GOV-RAT-001  
**Version:** 1.4.0  
**Charter:** docs/foundation/HSMART-PROJECT-CHARTER.md  
**Charter version:** 1.0.2  
**Prepared:** 2026-11-22  
**Status:** RATIFIED WITH CONDITIONS — INTERNAL PROJECT GOVERNANCE ADOPTION; GOV-02..GOV-06 RUNTIME ACTIVATION REMAINS BLOCKED

## 1. Purpose and distinction

Project Charter v1.0.2 is RATIFIED WITH CONDITIONS by GOV-01 on 2026-11-22 for internal HSMART project governance only. Repository publication, authorship, a PR draft or a successful CI run is not the ratification; the explicit GOV-01 decision is recorded under HSMART-GOV-DEC-2026-11-22-001. The conditions in this record constrain implementation and operation and do not create a legal entity or third-party authority.

GOV-01 is appointed through a founder self-declaration for internal project governance only. GOV-01 has also designated logical AI Functional Delegates for interim operational coverage of GOV-02 through GOV-06 under HSMART-GOV-AI-DEL-001. The human seats remain vacant, and runtime activation is pending. Neither the GOV-01 appointment nor the AI designations automatically ratify the Charter, approve the MVP, create a legal entity, appoint a human officer, or authorize external legal or commercial commitments.

This record does not fabricate a signature, legal identity verification, person, date, legal entity, delegated authority or organizational consensus.

## 2. Adoption evidence and outstanding operational conditions

The following evidence supports conditional adoption. Uncompleted runtime gates are retained as binding conditions; they are not represented as completed provisioning.

- [x] Canonical Charter v1.0.2 exists in the repository and is linked from the README.
- [x] Charter scope, product boundaries, governance principles, decision classes, risks and delivery stage gates are documented.
- [x] MVP Decision Record v1.1.0 has a bounded operating envelope, explicit non-goals and measurable acceptance criteria.
- [x] Role Appointment Register v1.3.0 records GOV-01's internal founder appointment and the boundaries of AI delegate designations.
- [x] GOV-01 Project Sponsor / Accountable Owner appointment is recorded under HSMART-GOV-FOUNDER-001 v1.0.0, effective 2026-11-22.
- [x] Interim AI Functional Delegate profiles GOV-02 through GOV-06 are designated under HSMART-GOV-AI-DEL-001.
- [x] GOV-01 explicitly approved MVP v1.1.0 as written on 2026-11-22.
- [x] GOV-01 explicitly selected RATIFY WITH CONDITIONS for Charter v1.0.2 on 2026-11-22.
- [x] Adoption conditions C-01 through C-09 are recorded below and in HSMART-GOV-DEC-2026-11-22-001.
- [ ] Human role seats GOV-02 through GOV-06 are appointed and accept responsibility, if/when qualified people become available.
- [ ] GOV-02..GOV-06 hosted runtimes, workload identities, exact model/provider bindings, Skill/Sub-Skill pins and compatibility evidence are provisioned and verified.
- [ ] Central policy enforcement is deployed outside the agent process and all mutating actions are mediated with deny-by-default and fail-closed behavior.
- [ ] Permission, bypass-resistance, outage and fail-closed integration tests pass for all five delegates.
- [ ] Production append-only/WORM audit storage is provisioned and passes retention-lock, deletion-denial, integrity and restore tests.
- [ ] GOV-07 Operations / Reliability responsibility is assigned or a documented, human-approved operating coverage arrangement is established before production workloads.
- [ ] Any required future Charter amendment is reviewed and merged through the repository PR process.

**Interpretation:** the checked items establish GOV-01's decision and the conditions for internal adoption. The unchecked items remain activation/production conditions. They do not authorize any AI runtime to act before its own technical activation evidence is complete.

## 3. Decision instrument

| Field | Required entry | Current value |
|---|---|---|
| Decision | RATIFY / RATIFY WITH CONDITIONS / RETURN FOR AMENDMENT | **RATIFY WITH CONDITIONS** |
| Accountable approver | Named person with confirmed authority | Harysaidno — GOV-01; self-declared Founder & Project Initiator authority for internal project governance only |
| Authority basis | Explicit source and limits | HSMART-GOV-FOUNDER-001 v1.0.0; does not confer legal-entity or third-party authority |
| Project Owner | Human role holder | VACANT; interim AI Functional Delegate `hsmart.gov02.project-owner.orchestrator` designated; runtime pending |
| Product Owner | Human role holder | VACANT; interim AI Functional Delegate `hsmart.gov03.product-owner.orchestrator` designated; runtime pending |
| Charter version reviewed | Exact version | 1.0.2 — reviewed and RATIFIED WITH CONDITIONS |
| MVP baseline reviewed | Exact version | 1.1.0 — APPROVED AS WRITTEN on 2026-11-22 |
| Effective date of Charter ratification | YYYY-MM-DD | 2026-11-22 — internal project governance only |
| GOV-01 appointment effective date | YYYY-MM-DD | 2026-11-22 |
| Conditions / exceptions | Explicit wording or NONE | C-01 through C-09 below; activation gates A1–A8 remain mandatory and unsatisfied until evidence is recorded |
| Evidence reference | Approved PR, meeting decision or signed approval reference | HSMART-GOV-DEC-2026-11-22-001; GOV-01 explicit written instruction in ChatGPT, 2026-11-22; no cryptographic signature supplied |

## 3.1 Conditions of adoption

The following conditions are part of GOV-01's conditional adoption decision and remain binding until explicitly closed by new evidence or a further GOV-01 decision.

| ID | Condition | Required interpretation / closure evidence |
|---|---|---|
| C-01 | Limited internal authority | Adoption governs only the unincorporated HSMART personal project and resources GOV-01 actually controls. It creates no legal entity, statutory authority, IP assignment, third-party right or external commitment. |
| C-02 | Human-seat and delegate transparency | Human seats GOV-02..GOV-06 remain VACANT. AI profiles are functional delegates, not natural persons, corporate officers or legal representatives. GOV-07 Operations / Reliability remains unassigned. No vacancy may be hidden by relabeling an AI profile as a human appointee. |
| C-03 | Per-delegate runtime activation gates | Each delegate remains NOT ACTIVE until A1–A8 in the Runtime Activation Plan independently pass for that delegate: isolated runtime and identity, verified model binding, immutable Skill/Sub-Skill pins, external policy enforcement, permission tests, fail-closed tests, WORM audit, and delegate/cross-evaluation validation. |
| C-04 | Human-only and least-privilege controls | GOV-01 retains final internal human approval authority. AI delegates may not write to or merge the main branch, deploy to production, alter policy or permissions, read raw secrets, approve their own actions, or override an unresolved security HOLD. R3/R4 and other high-impact matters require the stated independent human review. |
| C-05 | Production audit immutability | A hash chain, Git history or ordinary append-only database is not a WORM substitute. Before privileged or production workloads, provision an independently protected object-lock/WORM store with versioning, retention lock, protected signing, separated write/read roles, deletion-denial evidence, integrity verification and restore testing. |
| C-06 | Provider credentials and expenditure | Provider/model credentials must be stored only in the selected provider's secret manager. Never paste credentials into chat, GitHub or Notion. No paid resource may be created until GOV-01 separately approves the provider, scope, region and budget ceiling. |
| C-07 | Operations and incident accountability | Before production workloads, assign GOV-07 or explicitly document a human-approved interim operations owner, including monitoring, backup, restore, incident response, credential rotation and emergency suspension. |
| C-08 | MVP scope integrity | MVP v1.1.0 is approved as written. This adopts its scope and acceptance baseline but does not declare the MVP implemented, accepted at test level, released or production-ready. Any material scope or acceptance change requires a separate GOV-01 D2 decision. |
| C-09 | External legal/commercial boundaries | External legal, contractual, publisher, employment, privacy-regulatory, ownership or commercial commitments require a legally authorized person/entity and appropriate qualified review; this internal Charter ratification is not that authority. |

**Current condition state:** C-01, C-02, C-04, C-08 and C-09 are continuing governance constraints. C-03, C-05, C-06 and C-07 contain open provisioning/operational prerequisites. No condition is self-certified by an AI delegate.

## 4. Ratification procedure

1. GOV-01 appointment and AI Functional Delegate designations GOV-02 through GOV-06 are recorded for internal project governance. Human role seats remain vacant; the AI profiles must not be described as human appointments.
2. Before any Agent executes mutating work, provision its runtime, exact model and Skill provenance, least-privilege tool scopes, central policy enforcement and audit path; pass the activation gate in the AI Delegate Registry.
3. GOV-01 reviews Charter v1.0.2, MVP Decision Record v1.1.0 and the initial risk register. The AI delegates may prepare evidence but cannot approve these baselines.
4. If human role seats remain vacant during this founder-led phase, GOV-01 must explicitly accept the temporary operational coverage and limitations. This does not create legal authority or waive independent expert review for critical matters.
5. Record one of the three Charter adoption decisions in section 3, including approver identity, authority basis, date, conditions and evidence reference.
5. If conditions require normative changes, create or update the appropriate document in a reviewed PR. Do not silently rewrite the adopted baseline.
6. Update the Charter's status and ratification table only after the approval evidence is durable and read back.
7. Mark ratification complete only after the canonical repository reflects the same decision.

An explicit chat instruction may record a project-governance decision when the authorized human identifies themselves and the scope of their authority. It is not a cryptographic signature and is not a substitute for any legal instrument required by law or contract. The GOV-01 appointment and AI Functional Delegate designation recorded here are not themselves a Charter ratification instruction.

## 5. Decision rights and safeguards

1. Repository ownership or authorship does not automatically prove legal title or authority over every project contribution.
2. The assistant cannot ratify the Charter on behalf of a human authority.
3. No legal Foundation or Commercial Operator entity is created by this record.
4. No IP assignment, trademark, contributor agreement, publisher contract or commercial obligation is created by this record.
5. If adoption is conditional, each condition must have an owner, due condition and acceptance evidence.
6. If the authorized approver returns the Charter for amendment, the current version remains an unratified baseline until a revised version is approved.
7. GOV-01's self-declared authority is internal and limited to the personal project and resources the holder actually controls; it does not authorize acts on behalf of another person or entity.

## 6. Current disposition

**Charter v1.0.2 is RATIFIED WITH CONDITIONS** effective 2026-11-22 for internal HSMART project governance only. MVP v1.1.0 is APPROVED AS WRITTEN. The decision does not activate GOV-02..GOV-06. Their runtimes remain NOT_PROVISIONED / NOT_ACTIVE; human role seats remain VACANT; WORM audit and production policy enforcement remain unimplemented. Conditions C-01 through C-09 are binding. The operational task remains IN_PROGRESS until the relevant A1–A8 evidence is produced for each delegate and every required production condition is verified.
