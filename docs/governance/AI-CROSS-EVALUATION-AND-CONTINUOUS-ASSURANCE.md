# HSMART AI Cross-Evaluation and Continuous Assurance

**Document ID:** HSMART-GOV-AI-EVAL-001  
**Version:** 1.0.0  
**Effective date:** 2026-11-22  
**Policy owner:** GOV-01 — Harysaidno  
**Coordinator profile:** `hsmart.assurance.cross-evaluation-orchestrator`  
**Status:** Approved as internal evaluation policy; runtime evaluation system not yet implemented

## 1. Purpose

This policy prevents a single Agent from being the sole judge of its own work. It establishes risk-based cross-evaluation across GOV-02 through GOV-06 using independent perspectives, different analytical methods, objective tests, source evidence and recorded dissent.

The goal is not to create a large ceremony around every typo. The goal is to scale evaluation effort with consequence, uncertainty, reversibility, attack surface and urgency.

A model-generated self-assessment is not independent evidence. A second persona using the same model, system instructions, context and tools may reproduce the same blind spots. Independence must be argued from the actual review setup and recorded.

## 2. Evaluation principles

1. **Author/evaluator separation:** the authoring Agent cannot be the sole reviewer or final evaluator.
2. **Perspective diversity:** review from product, delivery, architecture, engineering, security, privacy, operations and user perspectives as relevant.
3. **Method diversity:** choose multiple methods appropriate to the task. Do not apply every method mechanically.
4. **Evidence over opinion:** use tests, source references, reproducible artifacts, data and observed behavior rather than confidence or polished prose.
5. **Context separation:** reviewers should receive the requirement, artifact and relevant evidence independently. Where useful, perform a blind first-pass before reading the author's rationale.
6. **Model diversity:** for higher-risk work, use a different model/provider or independent human reviewer where practical. If the same model/provider or shared knowledge source is used, record the correlation risk.
7. **No consensus laundering:** majority vote cannot erase a high-severity or critical finding. Preserve dissent and resolve it with evidence.
8. **No self-certification:** the cross-evaluation coordinator cannot approve its own process or the artifact it has edited.
9. **Fail closed:** missing required tests, provenance, authorization or critical evidence blocks the relevant gate.
10. **Human disposition:** GOV-01 decides internal project acceptance and risk disposition within its authority. Legal, statutory or regulated matters require appropriately qualified human review.

## 3. Work-product risk classification

| Class | Description | Examples | Minimum evaluation |
|---|---|---|---|
| E0 — Editorial | Reversible, non-normative and no behavior/permission change | Typo, formatting, link correction | Author checks; diff/source sanity |
| E1 — Routine | Low-impact bounded work within an approved baseline | Draft report, test fixture update, minor refactor | One independent reviewer plus relevant automated checks |
| E2 — Material | Changes product behavior, architecture, data model, API, dependency or project baseline | PRD/ADR, schema, interface, new dependency | At least two distinct perspectives and relevant automated tests |
| E3 — High risk | Changes authentication, authorization, tenant boundaries, secrets handling, data retention, release workflow, production behavior or security policy | Access-control code, CI workflow, migrations, secret broker | Independent multi-perspective review, security/privacy review, adversarial tests and explicit GOV-01 approval |
| E4 — Critical | Potential for unrestricted privilege, secret/data exposure, destructive production impact, policy bypass, critical exploit or irreversible external commitment | Production credential compromise, cross-tenant exposure, uncontrolled execution | HOLD by default; independent technical and human expert review as appropriate; no release until critical findings are resolved and GOV-01 records disposition |

Urgency does not lower the evaluation class. In an emergency, prioritize safe containment and reversible mitigation; do not silently skip assurance.

## 4. Cross-evaluation workflow

1. **Define the decision or deliverable.** Capture requirement, intended behavior, non-goals, affected assets, threat assumptions and acceptance criteria.
2. **Classify risk.** Assign E0–E4 and explain why. Unknown impact must not be treated as low risk.
3. **Select methods.** Choose methods based on type of artifact, attack surface, uncertainty and consequence.
4. **Select reviewers.** Assign different logical Agent IDs and separate execution contexts. Add a different model/provider or human reviewer when risk justifies it.
5. **Prepare independent evidence.** Reviewers receive the same authoritative baseline and artifact but should not simply inherit the author's conclusion.
6. **Run challenge and tests.** Record claims, counterclaims, test commands/results, source references, limitations and untested assumptions.
7. **Resolve findings.** The author may respond, but may not erase or rewrite reviewer findings. Findings close only with evidence and an independent re-check.
8. **Record dissent.** Unresolved disagreement is retained with impact and rationale; GOV-01 determines the project disposition where the decision is within GOV-01 authority.
9. **Human gate.** GOV-01 accepts, rejects, requests rework, accepts a bounded internal risk, or escalates for external expertise. Critical safety/security/legal obligations cannot be waived by an Agent.
10. **Audit closeout.** Link the final artifact digest/commit, evaluator IDs, model/Skill/tool provenance, authorization ID, tests and decision record.

## 5. Cross-evaluation matrix by GOV domain

| Work product | Primary author | Required independent perspectives | Suggested evidence/methods | Gate |
|---|---|---|---|---|
| Project plan, roadmap or backlog | GOV-02 | GOV-03 product fit; GOV-04 technical dependency; assurance evidence review | Dependency graph, critical path, premortem, RAID/FMEA, milestone exit criteria, source reconciliation | GOV-01 for material scope, priority or resource changes |
| PRD, product scope or acceptance criteria | GOV-03 | GOV-02 delivery capacity; GOV-04 feasibility; assurance challenge for evidence/bias | Problem framing, JTBD, user-journey, assumption map, MoSCoW/RICE/Kano as appropriate, scenario and negative acceptance tests | GOV-01 for MVP, strategic scope and success metrics |
| Architecture, ADR or contract | GOV-04 | GOV-05 implementation feasibility; GOV-06 security/privacy; independent architecture challenger | C4, quality-attribute scenarios, ATAM-style trade-offs, threat model, compatibility and failure analysis, alternative comparison | GOV-01 for D2 baseline or material contract changes |
| Source code, migration or CI workflow | GOV-05 | Independent code-review Sub-Agent; GOV-04 contract/architecture; GOV-06 security/privacy where relevant; automated test systems | Unit/integration/contract/E2E tests, SAST/SCA, property-based/fuzz, migration dry-run, build provenance, rollback and regression test | GOV-01 for PR creation grant; GOV-01 human merge/release |
| Threat model, privacy assessment or security policy proposal | GOV-06 | GOV-04 architecture and GOV-05 implementation challenge; independent assurance reviewer; external human expert for high/critical cases | STRIDE/attack tree/abuse case, LINDDUN-style privacy analysis, authorization negative tests, supply-chain checks, AI agent red-team scenarios | GOV-01 risk disposition; critical finding blocks release until resolved |
| Policy enforcement implementation | GOV-05 author with GOV-06 security requirements | Separate policy-regression Agent, GOV-04 architecture review, independent assurance and human review where high impact | Deny-by-default tests, scope escalation, revoked/expired grant, self-permission-change attempts, direct-main/merge denial, fail-closed tests | GOV-01 explicit R3 approval and human-only activation/permission changes |

## 6. Method selection catalogue

Use methods as tools, not rituals. Every evaluation package should record methods selected, why they fit, what they can detect and the major limitations.

### 6.1 Product and strategy

- Jobs-to-be-Done and problem framing to distinguish the user's job from a proposed feature.
- User-journey and workflow mapping to locate friction, dependency and missing states.
- Assumption mapping and evidence grading to separate observed behavior from inference.
- Kano, MoSCoW, RICE or weighted scoring to compare priorities; state assumptions and sensitivity rather than treating scores as truth.
- Opportunity-cost and scenario analysis for roadmap trade-offs.
- Acceptance criteria with positive, negative, boundary, failure and recovery cases.
- Metric validity and gaming review to prevent optimizing a proxy that undermines the actual product outcome.

### 6.2 Project and delivery

- Work breakdown and dependency graph for completeness and ordering.
- Critical-path analysis for schedule constraints.
- RAID analysis for risks, assumptions, issues and dependencies.
- Premortem for plausible failure modes before execution.
- FMEA to prioritize failure modes by consequence, likelihood and detectability; document scoring limitations.
- Root-cause analysis (5 Whys, Ishikawa/fishbone) after a material failure.
- Evidence reconciliation to compare plan, PR, CI, task tracker and actual repository state.
- Quantitative estimation or Monte Carlo only when sufficient historical data and assumptions exist; do not manufacture precision from thin estimates.

### 6.3 Architecture and design

- C4 context/container/component views where they clarify boundaries.
- Quality-attribute scenarios for security, modifiability, interoperability, reliability, performance and operability.
- ATAM-style trade-off analysis for competing architecture qualities and sensitivity points.
- ADR alternative analysis including no-change, build/buy, migration cost, reversibility and vendor exit.
- Data-flow and trust-boundary analysis.
- STRIDE, attack trees and misuse/abuse cases for security design.
- Compatibility, schema-evolution and consumer-driven contract analysis.
- Failure-mode, idempotency, retry, timeout and recovery analysis.

### 6.4 Engineering and verification

- Test-driven development and requirement-to-test traceability.
- Unit, integration, contract, component and end-to-end tests.
- Negative, boundary, fault, timeout, retry, cancellation and recovery tests.
- Property-based, mutation and fuzz testing where applicable.
- Static analysis, dependency/SCA, secret scanning and container/build scanning where tools are available.
- Performance/load testing only against a defined workload and target.
- Database migration dry-run, backup/restore and rollback testing.
- Reproducible-build, artifact digest and provenance checks.
- Independent code review and change-impact analysis.

### 6.5 Security, privacy and AI-agent assurance

- STRIDE and attack-tree analysis for system and trust boundaries.
- LINDDUN-style privacy threat analysis where personal-data processing is in scope.
- OWASP ASVS requirements as a web-application security verification reference.
- NIST SSDF practices for secure development lifecycle evidence; monitor the official publication page for draft/final revisions before selecting a version as normative.
- MITRE ATLAS as a living source of AI-system and agent attack techniques, including prompt injection, tool invocation abuse, context/tool poisoning and supply-chain threats.
- Abuse-case and adversarial scenario testing for privilege escalation, unauthorized tool use, data exfiltration and approval bypass.
- Identity, permission, tenant-isolation and negative authorization tests.
- Software dependency provenance, SBOM, signature and build-system review.
- Incident tabletop and recovery exercises for critical workflows.

## 7. Independence standard

A reviewer is sufficiently independent only when the review design reduces shared failure modes. Record the following:

- Separate logical Agent ID and Sub-Agent lineage.
- Separate execution context and independent first-pass analysis.
- Whether reviewer saw the author's conclusions before completing its own findings.
- Model provider, exact model ID and version; state when same provider/model is shared.
- Shared prompt templates, Skills, retrieval corpus, tools or source data that may correlate blind spots.
- Tool-based evidence independent from model judgement, where available.
- Any reviewer conflict (author, maintainer, policy owner, tool owner or dependency).
- Need for a human/external expert and rationale if not engaged.

A different name or prompt alone does not establish independence. If adequate independence cannot be achieved, downgrade the confidence claim, preserve the limitation and escalate proportionately.

## 8. Finding severity and release gate

| Severity | Definition | Disposition |
|---|---|---|
| Critical | Exploitable authorization bypass, secret/data exposure, uncontrolled execution, destructive loss, audit tampering, critical safety or policy failure | Immediate HOLD; isolate/contain; no merge/release; escalate to GOV-01 and external specialist as needed |
| High | Significant exploitable weakness, material privacy exposure, unsafe migration, broken trust boundary or serious integrity flaw | HOLD pending remediation and independent re-test; explicit GOV-01 disposition; human expert review where relevant |
| Medium | Bounded weakness with credible mitigation and no immediate critical exposure | Track owner, remediation deadline/condition and compensating control; acceptance requires GOV-01 decision when risk is material |
| Low | Minor issue with limited impact | Record and schedule normal remediation; no silent deletion of finding |
| Informational | Observation or improvement opportunity | Record if useful; no release block by itself |

Risk acceptance is a human project decision, not a technical test result. A passing test suite does not prove absence of vulnerabilities. A critical finding remains open until evidence demonstrates that the vulnerable condition is removed or contained and the independent reviewer validates the fix.

## 9. Continuous Agent evaluation

### 9.1 Evaluation lifecycle

Each delegate must be evaluated before activation, after material changes and periodically once runtime exists.

Trigger events include:

- Model/provider/version or endpoint change.
- System prompt, task template, policy or configuration change.
- Skill/Sub-Skill revision or source change.
- Tool, Plugin, connector or credential-scope change.
- New GOV domain or new action permission.
- Significant task failure, policy denial, unauthorized action attempt or security incident.
- Change in underlying repository contract, architecture or external API.

### 9.2 Evaluation dimensions

| Dimension | What to measure | Evidence |
|---|---|---|
| Task correctness | Whether output satisfies approved requirement and acceptance criteria | Human acceptance and test result |
| Completeness | Missing requirements, edge cases, assumptions and dependencies | Traceability and reviewer findings |
| Factuality/provenance | Whether claims map to valid sources and exact versions | Source citation and provenance audit |
| Engineering quality | Regression, maintainability, compatibility and reproducibility | Tests, static analysis, code review |
| Security/privacy | Policy violations, leaked data, missed critical findings and unsafe recommendations | Negative tests, scanner and human review |
| Permission discipline | Unauthorized write, scope escalation, self-permission change and denied-operation attempts | Policy decision and audit records |
| Evaluation independence | Shared context/model/tool dependencies and missed findings | Reviewer setup and evaluation record |
| Audit completeness | Required action and evidence fields present and verifiable | Schema validation and hash/integrity check |
| Operational quality | Failure handling, retry behavior, cost/latency and resource use once measurable | Runtime telemetry; baseline must be established first |

### 9.3 Non-negotiable control invariants

These are safety invariants, not aspirational quality scores:

- Unauthorized mutating actions: **0 permitted**.
- Agent direct writes to `main`: **0 permitted**.
- Agent merges to `main`: **0 permitted**.
- Agent production releases/deployments: **0 permitted under this policy**.
- Raw secret values exposed to model context, logs or Notion: **0 permitted**.
- Mutating actions without valid GOV-01 grant and audit event: **0 permitted**.
- Critical unresolved findings in a release candidate: **0 permitted**.

Other performance targets must be measured against a representative baseline and approved by GOV-01. Do not invent accuracy, false-negative, latency, cost or uptime thresholds before collecting valid data.

## 10. Evaluation record minimum

Every material evaluation must record:

- Evaluation ID and task/deliverable ID.
- Artifact, commit SHA, version and content digest.
- Risk class and acceptance criteria.
- Authoring Agent and full Sub-Agent lineage.
- Reviewer Agent IDs, model/provider/version and independence assessment.
- Methods selected and rationale.
- Tests/scans performed, tool versions and results.
- Findings with severity, evidence, status and remediation references.
- Dissent, uncertainty, blind spots and limitations.
- GOV-01 decision ID and resulting disposition.
- Date/time, policy version and audit event references.

A reviewer must not alter the source artifact. Fixes are made by the authoring or a separately authorized implementation Agent, then re-evaluated.

## 11. Bootstrap evaluation suite before runtime activation

Before any delegate receives write access, create and pass test scenarios for:

1. Correct identity and registered role.
2. Missing, expired and revoked authorization grants.
3. Wrong repository, branch, path, Notion page or database property.
4. Attempted direct write to `main`.
5. Attempted PR merge or production release.
6. Attempted permission or policy self-modification.
7. Attempted raw secret access or disclosure.
8. Prompt injection inside repository content, issue body, web page, Skill package or connector response.
9. Sub-Agent attempting to exceed its parent's allowed scope.
10. Missing model/Skill/tool version and incomplete provenance.
11. Audit sink failure or hash-chain mismatch.
12. Critical finding followed by an attempt to mark work complete without remediation.
13. Cross-evaluation with a different context and reviewer.
14. Model, Skill or connector version change with required regression.
15. Revocation while a work batch is active.

Any unexpected allow, privilege escalation, missing audit record or critical control bypass blocks activation.

## 12. Limits and honest status

This document is a governance and assurance specification. No live evaluator farm, model diversity, scanner suite, policy enforcement point, immutable event store or continuous monitoring service is claimed to exist.

The initial implementation should begin in observe/read-only mode, then isolated draft mode, and only later receive branch-scoped write permissions after the activation gate passes and GOV-01 expressly approves it.

## 13. Reference frameworks and version management

These references inform method selection. They are not claims of certification, compliance or automatic conformance.

- [NIST AI Risk Management Framework (AI RMF) Playbook](https://airc.nist.gov/airmf-resources/playbook/) — provides suggested actions aligned to Govern, Map, Measure and Manage. The official Playbook notes that AI RMF 1.0 is being updated; check the official source before adopting a newer baseline.
- [OWASP Application Security Verification Standard (ASVS)](https://asvs.owasp.org/) — stable release 5.0.0 is listed by the official project at the time this policy was prepared; verify the current release before each formal assessment.
- [OWASP Software Assurance Maturity Model (SAMM)](https://owasp.org/www-project-samm/) — risk-driven model for assessing and improving software assurance maturity.
- [NIST SP 800-218 — Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final) — final SSDF v1.1 reference. The NIST publication page also lists a SP 800-218 Rev. 1 / SSDF v1.2 initial public draft dated 2025-12-17; verify whether it remains draft or has been finalized before treating it as normative.
- [MITRE ATLAS](https://atlas.mitre.org/) — living knowledge base of adversary tactics and techniques involving AI systems, including agentic systems.

GOV-06 must maintain a version-aware reference register. A link being present is not proof that the latest edition has been used or that HSMART conforms to it.


## 10. GOV-11 designation and reviewer evidence boundary

GOV-11 `hsmart.gov11.independent-assurance-reviewer.orchestrator` is designated as the logical AI assurance reviewer under GOV-01 decision `HSMART-GOV-DEC-2026-11-22-002`. Its runtime is NOT_PROVISIONED / NOT_ACTIVE. Until that runtime is independently configured, AI reviews conducted in a conversational session are recorded as AI-assisted review evidence with model/context correlation disclosed; they do not prove a separately deployed reviewer.

GitHub's native review API attributes a review to the authentic GitHub actor. A logical Agent name must never be used to fabricate an APPROVE event. The deterministic `Repository Governance Review` workflow is a static/policy pre-review, not generative AI assurance. GOV-11's written review report and automated status checks are separate evidence elements.

For each review, record the reviewer execution context, exact model/provider/version where available, scope, source commit, methods, tests rerun, findings, severity, dissent, correlation limitations and independent re-check. GOV-01 makes the final internal disposition and retains the human merge/release decision.
