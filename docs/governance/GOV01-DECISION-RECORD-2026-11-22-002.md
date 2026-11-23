# HSMART GOV-01 Decision Record — ADR-011 Acceptance and AI Functional Delegation

**Decision ID:** HSMART-GOV-DEC-2026-11-22-002  
**Version:** 1.0.0  
**Decision date:** 2026-11-22  
**Decision authority:** GOV-01 — Harysaidno  
**Authority basis:** HSMART-GOV-FOUNDER-001; internal HSMART personal-project governance only  
**Decision method:** Explicit written instruction from GOV-01 in the ChatGPT conversation dated 2026-11-22  
**Evidence limitation:** Durable record of the explicit instruction; not a cryptographic signature or independent civil-identity verification.

## 1. Decisions

1. **ADR-011 v1.2.0 — ACCEPTED.** GOV-01 accepts the Python 3.12/FastAPI modular-monolith application baseline, PostgreSQL, SQLAlchemy/Alembic, PostgreSQL outbox worker, OIDC adapter, managed secrets/KMS, OCI packaging and OpenTelemetry conventions as HSMART's internal KM 1 technology direction.
2. **Only GOV-01 is human in the internal HSMART role model.** GOV-02 through GOV-12 are designated as bounded AI Functional Delegates with explicit role descriptions and prohibited actions.
3. **GOV-07 Operations/Reliability is designated** as an AI functional delegate. Its designation satisfies internal role allocation, not runtime provisioning or production operations proof.
4. **GOV-08 Legal/Commercial Research** is designated for issue spotting, research and document preparation. It is not legal counsel, cannot provide a binding legal opinion or sign/bind a person/entity.
5. **GOV-09 Entitlement Governance, GOV-10 Repository Governance, GOV-11 Independent Assurance and GOV-12 Business Continuity/DR** are designated as logical AI functional roles.
6. **AI reviewers are the designated review path** through GOV-11 and relevant domain reviewers. Their review reports must disclose model/provider/context correlation. An AI persona must not be represented as a GitHub-native human approving actor.
7. **GOV-01 retains final human authority** for internal policy, scope, acceptance, risk disposition and merge/release decisions within the authority GOV-01 actually controls.

## 2. ADR-011 scope and limits

The acceptance authorizes implementation of the internal KM 1 application foundation. It does not:
- claim that PostgreSQL hosted integration CI has already passed;
- close KM 1 or waive the independent KM 1 exit evaluation;
- select/procure a cloud provider, region, OIDC vendor, domain, KMS, secret manager, artifact store or paid service;
- approve production deployment or production data processing;
- approve any external legal, IP, licensing, contractual, publisher, tax or commercial commitment.

The vendor/provider/budget choices deferred in ADR-011 remain deferred until separately assessed and explicitly authorized.

## 3. GOV role model

| Role | AI functional delegate | State |
|---|---|---|
| GOV-01 | Harysaidno (human) | APPOINTED for internal project authority only |
| GOV-02 | `hsmart.gov02.project-owner.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-03 | `hsmart.gov03.product-owner.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-04 | `hsmart.gov04.architecture.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-05 | `hsmart.gov05.engineering.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-06 | `hsmart.gov06.security-privacy.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-07 | `hsmart.gov07.operations-reliability.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-08 | `hsmart.gov08.legal-commercial-research.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-09 | `hsmart.gov09.entitlement-governance.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-10 | `hsmart.gov10.repository-governance.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-11 | `hsmart.gov11.independent-assurance-reviewer.orchestrator` | DESIGNATED / NOT_ACTIVE |
| GOV-12 | `hsmart.gov12.business-continuity.orchestrator` | DESIGNATED / NOT_ACTIVE |

Designation is not a deployed Agent. All non-GOV01 roles must pass individual runtime, model, Skill, policy, permission, fail-closed and audit activation gates. All role human seats other than GOV-01 are intentionally unappointed.

## 4. AI reviewer controls

GOV-11 and domain-specific reviewer Agents may review artifacts in separate read-only contexts. Independence must be assessed, not presumed. Using the same model/provider, instructions or inherited context creates correlated-error risk and must be disclosed. The deterministic GitHub workflow `Repository Governance Review` checks repository policy and secret patterns only; it is not an LLM review. The AI review report is separate evidence. GitHub native review events must always identify the real GitHub actor. No bot persona may forge a human approval.

## 5. Operational and repository constraints

- `main` remains protected only when GitHub itself reports active rules and an administrator verifies the negative test. At decision time its protection was observed as disabled.
- The repository includes a dry-run/apply operator for branch protection and rulesets. Actual mutation requires an administrator token with repository `Administration: write`, used outside ChatGPT/Notion, and current `main` SHA precondition.
- Production remains blocked until runtime, identity, policy enforcement, WORM audit, security and recovery gates are met.
- No paid cloud resources are authorized by this decision.

## 6. Legal boundary

This is an internal operating model for an unincorporated personal project. It creates no legal entity, professional qualification, corporate office, statutory authority, IP ownership or third-party authority. GOV-08 is not legal counsel. Binding external legal/commercial commitments require an appropriately authorized person/entity and qualified human professional review where required.

**Final disposition:** ADR-011 accepted as the internal KM 1 technology baseline; GOV-02 through GOV-12 AI profiles designated, all runtimes not active; no production or external commercial approval.
