# HSMART GOV-01 Decision Record — MVP v1.1.0 and Charter v1.0.2

**Decision ID:** HSMART-GOV-DEC-2026-11-22-001  
**Version:** 1.0.0  
**Decision date:** 2026-11-22  
**Decision authority:** GOV-01 — Project Sponsor / Accountable Owner, Harysaidno  
**Authority basis:** HSMART-GOV-FOUNDER-001 v1.0.0; internal HSMART personal-project governance only  
**Decision method:** Explicit written instruction from GOV-01 in the ChatGPT conversation dated 2026-11-22  
**Evidence limitation:** This is a durable record of the explicit instruction, not a cryptographic signature or independent civil-identity verification.

## 1. Decisions recorded

| Subject | Version | GOV-01 decision | Effect |
|---|---|---|---|
| HSMART MVP Boundary & Acceptance Decision Record | v1.1.0 | **APPROVED AS WRITTEN** | Sections 2–7 are adopted without scope amendment as the internal MVP product boundary and acceptance baseline |
| HSMART Project Charter | v1.0.2 | **RATIFY WITH CONDITIONS** | Adopted as the internal HSMART project-governance baseline, subject to C-01 through C-09 in HSMART-GOV-RAT-001 v1.4.0 |

## 2. MVP approval scope

GOV-01 accepts MVP v1.1.0 as written, including its operating envelope, in-scope capabilities, explicit non-goals, acceptance criteria AC-01 through AC-12, and initial success measures.

This approval:
- adopts the defined product scope and acceptance baseline;
- does not certify implementation or acceptance tests as passed;
- does not declare the MVP released, production-ready or generally available;
- does not approve a hosting provider, model provider, region, paid resource, budget or production deployment;
- does not authorize an expansion or silent change to the MVP boundary.

Any material scope or acceptance-criteria change remains a separate GOV-01 D2 decision.

## 3. Charter conditional adoption

Charter v1.0.2 is adopted with conditions for internal project governance only. The conditions are normative constraints on implementation and operation:

1. **C-01 — Authority limit:** HSMART remains an unincorporated personal project. This decision does not create a legal entity or confer authority over third-party people, assets, rights or obligations.
2. **C-02 — Human seats:** GOV-02 through GOV-06 human role seats remain VACANT. Their AI Functional Delegate profiles are not people, corporate officers or legal representatives. GOV-07 Operations/Reliability remains unassigned.
3. **C-03 — Runtime gates:** Each of the five delegates remains NOT ACTIVE until its own A1–A8 activation evidence is verified: isolated runtime/identity, model binding, pinned Skills, technical policy enforcement, permission tests, fail-closed tests, production WORM audit and delegate validation.
4. **C-04 — Human-only controls:** GOV-01 retains final internal human approval. AI delegates may not write to or merge the main branch, deploy to production, alter policy or permissions, read raw secrets, approve their own actions or override an unresolved security HOLD.
5. **C-05 — WORM audit:** Git history, hash chains and ordinary append-only stores are not substitutes for independently protected production WORM storage. Object-lock configuration, retention, protected signing, deletion-denial, integrity and restore tests are required before privileged/production workloads.
6. **C-06 — Credentials and budget:** Credentials must be entered directly into the selected provider's secret manager, never chat, GitHub or Notion. Paid resource creation requires a separate GOV-01 decision approving provider, region, scope and spending ceiling.
7. **C-07 — Operations accountability:** Before production workloads, assign GOV-07 or record a human-approved interim operations owner responsible for monitoring, backup, restore, incident response and emergency suspension.
8. **C-08 — MVP boundary:** MVP v1.1.0 approval does not declare delivery complete, waive acceptance criteria or authorize scope changes.
9. **C-09 — External commitments:** Legal, IP, contractual, publisher, privacy-regulatory or commercial commitments require an appropriately authorized person/entity and qualified review.

Condition detail and evidence closure are maintained in [CHARTER-RATIFICATION-RECORD.md](../foundation/CHARTER-RATIFICATION-RECORD.md).

## 4. Runtime disposition at the time of decision

This decision does **not** provision or activate GOV-02 through GOV-06. The repository contains the reference policy evaluator, tests and activation plan merged under PR #12, but the following are still unverified:
- five hosted compute runtimes and separate workload identities;
- exact provider/model IDs and operational credentials;
- immutable Skill/Sub-Skill lock records, artifact integrity and compatibility results;
- central policy gateway with complete tool interception and bypass denial;
- hosted permission and fail-closed integration tests;
- production append-only/WORM audit storage and retention-lock evidence;
- per-delegate activation and cross-evaluation reports.

All five delegate states therefore remain **DESIGNATED / NOT_PROVISIONED / NOT_ACTIVE**.

## 5. Governance safeguards

- GOV-01 is the sole final human decision authority for internal project baselines.
- AI Functional Delegates may prepare analysis, artifacts and evidence within approved grants, but may not approve their own access, policy exceptions, risk acceptance or activation.
- No AI delegate may write directly to or merge into the main branch.
- A successful CI run validates only the tests executed by that workflow; it does not establish runtime activation, WORM compliance, MVP delivery or Charter ratification.
- This decision does not verify the user's civil identity or create a cryptographic signature.

## 6. Related evidence

- [PR #12 — Runtime activation foundation](https://github.com/hsaidno-cpu/HSMART/pull/12) — merged; its Specification Validation workflow for head commit 6f10f786119f96729e5caa5cf93e6f8d0f44a809 completed successfully. This proves repository validation only, not hosted deployment.
- [Runtime Activation and Evidence Plan](../runtime/DELEGATE-RUNTIME-ACTIVATION-PLAN.md) — A1–A8 remain open; A9 and A10 decisions are recorded.
- [MVP Decision Record v1.1.0](../foundation/MVP-DECISION-RECORD.md).
- [Charter Ratification Record v1.4.0](../foundation/CHARTER-RATIFICATION-RECORD.md).

**Final disposition:** MVP v1.1.0 APPROVED AS WRITTEN. Charter v1.0.2 RATIFIED WITH CONDITIONS. GOV-02 through GOV-06 NOT ACTIVE.
