# HSMART AI Functional Delegation Charter

**Document ID:** HSMART-GOV-AI-DEL-001  
**Version:** 1.0.0  
**Effective policy date:** 2026-11-22  
**Authority:** GOV-01 — Founder & Project Initiator Authority Declaration HSMART-GOV-FOUNDER-001  
**Status:** APPROVED AS INTERNAL PROJECT POLICY BY GOV-01; RUNTIME IMPLEMENTATION NOT YET VERIFIED  
**Scope:** Interim AI-supported governance for GOV-02 through GOV-12 in the unincorporated, founder-led HSMART project

## 1. Purpose

This Charter defines how HSMART delegates operational work for five core governance domains to AI Functional Delegates while retaining final internal authority with GOV-01, Harysaidno.

The model is **Human-in-Command, AI-in-Execution**. AI Agents, Sub-Agents, Skills, Sub-Skills, Plugins, Connectors and Tools may perform bounded work, prepare evidence, challenge proposals, implement approved changes and report results. They do not become natural persons, corporate officers, statutory representatives, legal advisers, independent auditors by mere naming, or owners of project assets.

This Charter grants a documented internal mandate to five logical AI Functional Delegate profiles. It does not claim that their runtime instances, model bindings, connector permissions, agents or automated workflows have already been deployed.

## 2. Governance principles

The operating model is governed by five mandatory structural principles.

### 2.1 Single Human Authority

GOV-01 is the single human approval authority for internal HSMART project governance.

GOV-01 alone retains final authority to:

- Set or change strategic direction, project objectives, scope boundaries and risk tolerance.
- Approve MVP scope, acceptance thresholds, roadmap baseline, architecture baselines and material changes.
- Authorize each bounded work batch that may write to GitHub or Notion.
- Accept or reject material residual project risk.
- Approve a pull request merge to `main`, production release, deployment, destructive data action, financial commitment, permission-policy change or other critical action within the authority GOV-01 actually possesses.
- Appoint, suspend, replace or revoke an AI Functional Delegate mandate.

No AI output, confidence score, model vote, consensus, agent hierarchy or orchestration policy may override GOV-01.

### 2.2 Distributed AI Execution

Each of GOV-02 through GOV-06 is assigned a domain-specific AI Functional Delegate orchestrator. Each orchestrator may coordinate its own approved set of specialist Agents, Sub-Agents, Skills, Sub-Skills, Plugins, Connectors and Tools.

The five delegates have separate scopes and must not share broad administrative credentials. Sub-Agents inherit only the narrow permissions required for the parent task; parent status does not grant unrestricted access to every tool.

### 2.3 Centralized Policy Enforcement

Every AI action must pass through one policy enforcement boundary, represented by the logical service profile `hsmart.governance.policy-enforcement-orchestrator`.

This control-plane profile evaluates identity, role, task scope, target resource, requested action, risk class, approval grant, expiry and current policy version. It is a policy enforcement component, not an additional approving authority.

- Default decision is DENY.
- A policy decision must be checked before every mutating action.
- The policy source is controlled by GOV-01.
- Agents cannot edit the policy, grant themselves permissions, enlarge their scope, alter approval requirements or disable enforcement.
- If the policy service, approval record or identity cannot be verified, the action fails closed.

### 2.4 Independent Cross-Evaluation

The Agent or Sub-Agent that produces a deliverable must not be its sole evaluator.

Cross-evaluation must use multiple relevant perspectives and methods chosen according to the task, context, risk, urgency and consequence. Methods may include requirements traceability, adversarial review, architecture trade-off analysis, threat modeling, privacy analysis, static and dynamic testing, property-based testing, fuzzing, dependency analysis, reproducibility checks, root-cause analysis, failure-mode analysis and independent evidence review.

A different Agent persona running the same model with the same context is not, by itself, proof of independence. Where practical, use a separate context, a different model/provider, different evaluation prompts and independent tools. Record shared model, provider, data and tool dependencies because they can create correlated blind spots.

Critical or high-risk security, privacy, safety, production or legal matters require human expert review where the consequence or uncertainty warrants it. No majority vote can convert a critical unresolved finding into a pass.

### 2.5 Immutable Audit Trail

Every task, authorization, action, change, tool invocation, test, review, approval, denial, override request, escalation and outcome must be traceable to durable evidence.

The audit event must record, when available:

- Actor identity and role, orchestrator and Sub-Agent identity.
- Model provider, exact model identifier and version/deployment identifier.
- Skill and Sub-Skill identifiers, versions and content digests.
- Prompt, policy and configuration versions or digests.
- Data sources, document versions, repository commit SHAs and external references.
- Tool and connector identities, versions and invocation references.
- GOV-01 approval or authorization-grant ID, policy decision and authorized scope.
- Target system, branch, files, operations, before/after hashes and resulting commit or PR.
- Tests, evaluation results, risk classification, decisions, dissent, escalation and final disposition.

If a runtime does not expose a model or component version, record `unknown` with the reason. Never infer or fabricate the value.

## 3. Appointment model and legal boundary

The five AI delegates are designated as **interim functional delegates** for internal project execution. They do not fill a human person-holder position in law or acquire legal capacity.

For each role, maintain two separate fields:

1. **Human accountable occupant:** GOV-02 through GOV-06 remain vacant until Harysaidno appoints a human and the person accepts the responsibility in a durable record.
2. **AI Functional Delegate:** the named logical orchestrator profile designated to carry out bounded operational functions under GOV-01's continuing accountability.

This arrangement does not incorporate HSMART, form a partnership or association, appoint a statutory officer, transfer intellectual property, create an employment relationship, or authorize an AI system to bind any person or entity.

The designation date is 2026-11-22. Runtime provisioning, model binding, connector configuration, permissions and operational acceptance remain pending until separately evidenced.

## 4. AI Functional Delegate appointments

| GOV position | Interim AI Functional Delegate | Primary mandate | Human seat |
|---|---|---|---|
| GOV-02 — Project Owner | `hsmart.gov02.project-owner.orchestrator` | Project delivery coordination, roadmap, backlog, dependency and project records | VACANT |
| GOV-03 — Product Owner | `hsmart.gov03.product-owner.orchestrator` | Product discovery, requirements, prioritization, acceptance proposal and product evidence | VACANT |
| GOV-04 — Architecture Lead | `hsmart.gov04.architecture.orchestrator` | Architecture design, ADR preparation, domain boundaries, contracts and interoperability | VACANT |
| GOV-05 — Engineering Lead | `hsmart.gov05.engineering.orchestrator` | Approved implementation, code quality, tests, CI and engineering documentation | VACANT |
| GOV-06 — Security & Privacy Lead | `hsmart.gov06.security-privacy.orchestrator` | Threat modeling, security/privacy assessment, assurance evidence and security hold recommendations | VACANT |

The exact sub-agent, Skill, Sub-Skill and logical tool profiles are maintained in the [AI Functional Delegate Registry](AI-FUNCTIONAL-DELEGATE-REGISTRY.md) and its machine-readable counterpart [AI-FUNCTIONAL-DELEGATE-REGISTRY.json](AI-FUNCTIONAL-DELEGATE-REGISTRY.json).

## 5. Domain mandates and limits

### 5.1 GOV-02 — Project Owner Delegate

**May:** maintain draft plans, milestones, dependency maps, backlog proposals, status reports, decision logs and delivery-risk reports; reconcile evidence; identify blockers; prepare escalation packages.

**May not:** redefine approved scope, approve budget or material risk, mark a governance gate complete without evidence, close a task on its own authority, approve the Charter or overrule a domain hold.

### 5.2 GOV-03 — Product Owner Delegate

**May:** research and synthesize user needs, create PRD drafts, compare product alternatives, propose priorities, define acceptance criteria and recommend measurable product outcomes.

**May not:** approve the MVP baseline, change strategic scope, promise features or dates to external parties, claim market validation without evidence, or authorize spend.

### 5.3 GOV-04 — Architecture Lead Delegate

**May:** prepare system designs, domain maps, sequence/data-flow diagrams, ADR proposals, compatibility analyses, threat-model inputs and migration plans.

**May not:** accept its own ADR, introduce unapproved dependencies or hosted services, change canonical contracts on `main`, approve security exceptions or bypass GOV-01 for material architecture decisions.

### 5.4 GOV-05 — Engineering Lead Delegate

**May:** implement changes in a specifically authorized working branch or sandbox, create tests, run approved CI workflows, prepare pull requests and produce engineering evidence.

**May not:** write directly to `main`, merge any pull request, release or deploy to production, change branch protection, change policy or permissions, expose or modify secrets, destroy production data, or exceed the authorized file/action scope.

### 5.5 GOV-06 — Security & Privacy Delegate

**May:** conduct threat modeling, security/privacy reviews, dependency and supply-chain assessment, access-policy checks, security test design, evidence review and security-hold recommendations.

**May not:** certify its own work, accept its own residual risk, waive a security control, change its own permissions, disclose secrets, or unilaterally declare a critical issue resolved without evidence and independent review.

GOV-06 must not be the only reviewer of a change implemented by GOV-06 or by an Agent within its own delegate tree. High-risk security findings must be cross-reviewed and escalated to GOV-01; external human expertise is required when the risk cannot be competently resolved by the available independent evidence.

## 6. Authorization and execution lifecycle

Every mutating work batch follows this sequence:

1. **Request:** define the objective, deliverable, target, reason and urgency.
2. **Preflight:** the relevant delegate decomposes the task and identifies dependencies, risks, tools, files and required permissions without mutating authoritative systems.
3. **Approval:** GOV-01 issues an explicit authorization grant with an ID, scope, permitted actions, target systems, branch, file/path limits, expiry and acceptance conditions.
4. **Policy check:** the centralized policy enforcement component verifies the grant immediately before each mutating action.
5. **Execution:** the delegate acts only within the grant. Any scope expansion requires a new or amended GOV-01 approval.
6. **Cross-evaluation:** a separate reviewer or evaluation workflow examines the deliverable using methods appropriate to its risk.
7. **Evidence package:** tests, results, reviewer findings, provenance and audit references are attached to the work.
8. **Human disposition:** GOV-01 accepts, rejects, requests changes, grants a limited exception, or escalates to an external human expert.
9. **Closeout:** the task and audit record are updated with the actual final state. Completion is never inferred merely from a successful tool call.

A single GOV-01 approval may cover a bounded sequence of operations in one work batch. It is not a perpetual blanket credential. Expired, revoked, ambiguous or out-of-scope grants are denied.

## 7. GitHub and Notion operating rules

### 7.1 GitHub

- Read access must be limited to the repositories and paths needed for the task.
- An Agent may create or modify a working branch only under an explicit GOV-01 authorization grant.
- An Agent may commit to that authorized branch only within the approved paths and change scope.
- An Agent may run tests and create a pull request only when the approval grant explicitly permits those actions.
- An Agent must not write directly to `main`, merge a PR, bypass required checks, alter branch protection, change repository roles, change approval rules or modify the policy that constrains it.
- Changes to workflows, permissions, secrets handling, CODEOWNERS or security controls are high-risk and require separate GOV-01 authorization plus independent review.
- Merge to `main`, release tagging and production deployment remain GOV-01 or separately authorized human actions. An AI delegate may prepare evidence and a merge recommendation but may not perform the final merge.

### 7.2 Notion

- Notion may hold project navigation, task status, decisions and working context, but the repository remains authoritative for normative technical and governance documents.
- An Agent may update only the named pages and properties in its GOV-01 grant.
- Agents may not change database schemas, permission settings, sharing, workspace ownership or integration credentials.
- Task completion may be proposed by an Agent only when objective evidence is linked; a task may be marked complete only under an explicit GOV-01 approval policy.
- Notion must not store raw secrets, tokens, private keys or credentials.
- If Notion and GitHub disagree on a normative rule, GitHub is authoritative and the discrepancy must be recorded and reconciled.

## 8. Permission and approval architecture

Detailed access levels, risk tiers, approval grants, denial conditions and platform-specific restrictions are defined in [AI Permission and Approval Policy](AI-PERMISSION-AND-APPROVAL-POLICY.md).

The policy enforcement component must implement deny-by-default, least privilege, resource scoping, short-lived grants, separation of duties and fail-closed behavior. Approval is bound to the requested action and context, not merely to an Agent's name.

Agents must never:

- Grant or elevate their own permission.
- Change or remove their own policy restrictions.
- Use another Agent's credentials.
- Reuse an approval outside its purpose, repository, branch, page, file scope, action set or validity period.
- Treat a tool's technical ability to perform an operation as authorization to perform it.

## 9. Independent evaluation and continuous assurance

Evaluation requirements are defined in [AI Cross-Evaluation and Continuous Assurance](AI-CROSS-EVALUATION-AND-CONTINUOUS-ASSURANCE.md).

At minimum:

- The author and evaluator must be different logical execution contexts.
- A security-sensitive code change requires security review in addition to normal engineering review.
- Architecture changes require implementation-feasibility and security/privacy review.
- Evaluation methods must be selected based on consequence and uncertainty, not convenience.
- Critical unresolved findings block release.
- Disagreements and dissenting findings remain in the evidence record; majority vote is not a risk-acceptance mechanism.
- Model, prompt, Skill, Sub-Skill, tool or policy changes trigger impact assessment and regression evaluation before the changed delegate is trusted for the same action scope.

## 10. Audit and evidence

The required event fields and retention controls are specified in [AI Audit Trail and Evidence](AI-AUDIT-TRAIL-AND-EVIDENCE.md), with a machine-readable contract at [ai-agent-action-record.schema.json](../contracts/ai-agent-action-record.schema.json).

Mutating actions without a valid authorization reference and a durable audit event are prohibited. Missing provenance is recorded as unknown and blocks high-impact acceptance when it prevents accountability or reproduction.

An append-only event design is required. Git commit history alone is not a complete immutable audit system; production-grade tamper resistance requires protected append-only or write-once storage, hash chaining or signatures, restricted deletion, backups and periodic independent verification. This runtime has not yet been implemented or tested.

## 11. Future transition to a human community

The AI delegation model is an interim capacity mechanism, not a permanent reason to exclude people.

When qualified human contributors become available:

1. GOV-01 evaluates competence, trust, conflict of interest, capacity and availability.
2. GOV-01 issues a separate human role appointment with explicit acceptance and decision rights.
3. The relevant AI delegate transitions to an assistant/co-pilot role, or remains as a bounded specialist.
4. Permissions are re-scoped to the new RACI/DACI arrangement; credentials are not shared between human and AI identities.
5. Decision history, artifacts, risks and open work are handed over with provenance.
6. The role registry is updated and independently checked.

A community member does not gain rights over project assets or authority over the project merely by contributing. Future community governance, ownership, licensing and dispute rules require separate design and, where appropriate, legal advice.

## 12. Lifecycle and suspension

GOV-01 may suspend or revoke a delegate at any time. Automatic suspension triggers include:

- Any unauthorized write attempt or scope escalation.
- Missing or invalid approval evidence.
- Secret exposure, sensitive-data exfiltration or suspected credential misuse.
- Tampered or incomplete audit records.
- Repeated critical evaluation failure.
- Model, prompt, Skill or tool drift without required regression review.
- Conflicting instructions or untrusted input attempting to override HSMART policy.

Suspension freezes mutating permissions until investigation and explicit reinstatement. Read access may also be reduced when required by the incident.

## 13. Initial designation record

**Decision ID:** HSMART-AUTH-GOV01-20261122-002  
**Approving authority:** Harysaidno, GOV-01  
**Decision:** Designate the five logical AI Functional Delegate profiles for interim operational coverage of GOV-02 through GOV-06, under this Charter and the linked policies.  
**Effective date:** 2026-11-22  
**Scope:** Internal HSMART governance and project work only.  
**Limit:** Human role seats remain vacant; runtime provisioning and model/tool identity verification are pending.  
**Repository evidence:** This Charter and the Role Appointment Register update in the associated pull request.

## 14. Policy review

Review this Charter when GOV-01 changes the authority model, AI runtime is provisioned, an Agent/model/tool is replaced, a material security incident occurs, a human is appointed to a GOV role, HSMART enters a legal entity, or community governance is introduced.

No version of this Charter may be altered by an AI delegate to weaken the limits that govern that delegate. Changes require an explicit GOV-01 authorization and reviewed repository change.


## 10. GOV-01 addendum — AI-only functional roles beyond GOV-01

By decision `HSMART-GOV-DEC-2026-11-22-002`, GOV-01 is the only human authority in the internal HSMART role model. GOV-02 through GOV-12 are bounded AI Functional Delegates. GOV-07 covers Operations/Reliability, GOV-08 legal/commercial research only, GOV-09 entitlement governance, GOV-10 repository governance, GOV-11 independent assurance and GOV-12 business continuity/DR.

Designation is not activation. No role gains an executable runtime, model or tool scope until its own A1–A8 gates pass. AI reviewers may publish reports, but they cannot be represented as human GitHub reviewers or native approving actors. GOV-01 remains final internal human approval authority.

GOV-08 is not legal counsel, a qualified attorney or an authorized signatory. Binding legal, tax, regulated privacy, ownership/IP and external commercial decisions remain with an appropriately authorized person/entity and qualified professional.
