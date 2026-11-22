# HSMART Initial Risk Register

**Register ID:** HSMART-RISK-001  
**Version:** 1.0.0  
**Prepared:** 2026-11-22  
**Status:** Initial risk baseline; risk owners and likelihood assessments pending  
**Related:** docs/security/THREAT-MODEL.md; docs/security/SECURITY-BASELINE.md; Project Charter v1.0.0

## 1. Assessment rules

- Severity describes consequence if the risk occurs; likelihood is not scored until evidence and exposure are available.
- P0 is a stop/decision gate; P1 requires control before the dependent implementation/release gate; P2 requires planned treatment and monitoring; P3 is monitored.
- A documented control is not an implemented control. Status distinguishes control design from tested operation.
- Risk owners are role-based placeholders until appointments are made. No individual is assigned by inference.
- Risk acceptance must be made by the authority defined in the Charter; an AI-generated register cannot accept risk on behalf of the project.

## 2. Register

| ID | Risk event / cause | Consequence | Severity | Likelihood | Existing design/control | Required treatment / trigger | Owner | Status |
|---|---|---|---:|---|---|---|---|---|
| R-HS-001 | Sponsor/Project Owner and control roles remain unappointed | Decisions stall; scope, review and accountability become ambiguous | P0 | NOT ASSESSED | Charter defines roles and decision classes | Appoint accountable people; trigger: any D2/D3 decision or KM 0 exit | Sponsor / Project Owner | OPEN |
| R-HS-002 | MVP boundary and acceptance remain unapproved | Scope drift and disputes over what “done” means | P0 | NOT ASSESSED | Charter and proposed MVP decision record | Ratify boundary and acceptance matrix before implementation expands | Product Owner | OPEN |
| R-HS-003 | Charter baseline is treated as formally adopted without evidence | Authority and governance claims exceed actual adoption | P0 | NOT ASSESSED | Ratification record explicitly separates merged from adopted | Record approver, authority, effective date and conditions; trigger: governance action | Sponsor / Project Owner | OPEN |
| R-HS-004 | Stack/cloud choices are made without team, workload, budget or data-residency inputs | Lock-in, avoidable cost, unsuitable operations or migration | P1 | NOT ASSESSED | Stack and infrastructure ADR proposed, vendor-neutral choices preferred | Approve ADR with alternatives, cost envelope, region and exit criteria before procurement | Architecture Lead / Sponsor | OPEN |
| R-HS-005 | Authorization is implemented as “valid token means allowed” | Unauthorized capability/action or cross-tenant access | P0 | NOT ASSESSED | Zero Trust, default deny, per-invocation policy described | Test principal × tenant × resource × operation × scope × entitlement × quota; trigger: any authorization change | Security Lead | DESIGN_ONLY |
| R-HS-006 | Tenant context is taken from an untrusted request field or omitted in secondary stores | Cross-tenant disclosure or mutation | P0 | NOT ASSESSED | Threat model calls for identity-derived tenant scope and layered isolation | Test API, DB, cache, queue, artifact storage, logs and workers; trigger: new data path | Security Lead / Engineering Lead | DESIGN_ONLY |
| R-HS-007 | External MCP/API connector can reach private or metadata endpoints | SSRF, credential theft or internal network access | P0 | NOT ASSESSED | UAM specifies allowlists, DNS/redirect revalidation and egress controls | Negative tests for IPv4/IPv6, redirects, DNS rebinding, link-local and metadata ranges; trigger: connector implementation | Security Lead | DESIGN_ONLY |
| R-HS-008 | Imported capability/artifact or publisher identity is malicious or misrepresented | Supply-chain compromise, unsafe execution, IP dispute | P0 | NOT ASSESSED | Quarantine, provenance, digest/signature, publisher identity and review specified | Enforce source verification, signature/digest, SBOM/scan as risk dictates; trigger: import/publication | Security Lead / Publisher Owner | DESIGN_ONLY |
| R-HS-009 | Runtime isolation/resource/east-west network control is weaker than threat model assumes | Workload escape, resource exhaustion, tenant compromise | P0 | NOT ASSESSED | Managed isolated worker, limits and restricted egress specified | Threat-model chosen isolation boundary and run adversarial tests before untrusted code execution | Engineering Lead / Security Lead | DESIGN_ONLY |
| R-HS-010 | Published artifact can be modified or evaluation evidence detached from it | Reproducibility and trust failure; rollback cannot identify exact binary | P1 | NOT ASSESSED | Immutable release and digest-linked evaluation are specified | Enforce append-only version/digest linkage and read-back verification | Architecture Lead / Engineering Lead | DESIGN_ONLY |
| R-HS-011 | REST and MCP implement separate authorization semantics | Protocol-dependent privilege bypass | P1 | NOT ASSESSED | Shared authorization core is specified | Shared policy test vectors and cross-protocol parity suite; trigger: gateway implementation | Architecture Lead / Security Lead | DESIGN_ONLY |
| R-HS-012 | CI passes document checks but is interpreted as platform/runtime verification | False release confidence and premature stage advancement | P1 | OBSERVED SCOPE LIMITATION | Existing workflow validates JSON syntax, YAML structure and required files | Expand CI to schema/OpenAPI tests; explicitly separate static, contract, integration and runtime layers | Engineering Lead | IN_PROGRESS |
| R-HS-013 | Observability captures credentials, personal data or sensitive invocation payloads | Confidentiality/privacy breach and incident-response exposure | P1 | NOT ASSESSED | Data minimization, redaction and access controls are specified | Redaction tests, field allowlists, retention and access policy; trigger: logging/trace implementation | Security & Privacy Lead | DESIGN_ONLY |
| R-HS-014 | Synchronization races, retries or partial rollout create divergent target state | Broken clients, broad outage or unrecoverable version drift | P1 | NOT ASSESSED | Desired/observed reconciliation, idempotency, staged rollout and rollback specified | Test stale state, duplicate events, partial failures, canary abort and rollback; trigger: sync implementation | Operations / Engineering Lead | DESIGN_ONLY |
| R-HS-015 | 427 candidate records are treated as verified/publishable because the count exists | Invalid, duplicated, unlicensed or unsafe capabilities enter registry | P1 | NOT ASSESSED | Staging/provenance/schema/dedup/approval requirement documented | Establish source inventory and record-level evidence before migration; trigger: registry import | Registry Owner / Security Lead | OPEN |
| R-HS-016 | Legal entity, IP, licensing, privacy or publisher terms are assumed from technical documentation | Dispute, takedown, regulatory or commercial liability | P0 before external commercial operation | NOT ASSESSED | Charter explicitly leaves legal structure and contracts open | Obtain qualified legal/tax review and signed agreements before commercial/marketplace activity | Sponsor / Legal Advisor | OPEN |
| R-HS-017 | Project advances to KM 2–10 while KM 0/1 gates remain unresolved | Rework, uncontrolled scope and weak evidence chain | P1 | OBSERVED PLAN GAP | Stage-gated roadmap exists | Enforce exit evidence and no stage promotion by elapsed time or document count | Project Owner | OPEN |

## 3. Threat model review

### 3.1 Strengths retained

The existing threat model has a useful starting structure:
- Assets and trust boundaries cover identity, publisher authority, artifacts, tenant data, runtime, registry, marketplace and audit evidence.
- STRIDE is supplemented by supply-chain, multi-tenant, SSRF, prompt-injection, replay, runtime compromise, desynchronization and insider scenarios.
- The model describes meaningful controls such as OIDC/workload identity, immutable digests, vault/KMS, egress policy, default-deny, tenant scoping, quarantine and separation of duties.
- Residual risks are acknowledged rather than hidden.

### 3.2 Gaps to close before implementation/release

1. No accountable threat-model owner or approval record. The document is a baseline, not a completed security review.
2. No system-specific data-flow diagrams or deployment trust-boundary evidence. The current model is architecture-level.
3. No threat/control/test traceability. Most control statements do not yet map to test IDs, owners, implementation paths and evidence.
4. No likelihood/exposure assessment. This is intentionally unscored until runtime, provider and deployment choices exist.
5. No abuse-case coverage of policy decision composition. Add explicit tests for resource ownership, tenant, publisher, entitlement, scopes, quota, environment and policy-version changes.
6. No evidence that connector controls are enforced at connection time. DNS/redirect validation and egress controls remain design requirements.
7. No operational incident exercises. Quarantine, token/key revocation, audit reconstruction, backup/restore and incident escalation are not yet demonstrated.
8. No independent security review. Required before arbitrary third-party execution, marketplace launch and production.

### 3.3 Required next threat-model review

When the Security & Privacy Lead is appointed:
- Confirm assets, data classifications, entry points and trust boundaries for the selected stack.
- Create data-flow diagrams for registration, authentication, invocation, connector egress, artifact publication and synchronization.
- Link each threat to controls, source files, negative tests, owners, detection signals, response and recovery.
- Assess likelihood/exposure with actual deployment assumptions; preserve unknowns where evidence is missing.
- Record accepted residual risks and expiry/review triggers.
- Re-review after any material identity, tenancy, runtime, connector, artifact-signing or synchronization change.

## 4. Review cadence and triggers

Review at each KM exit gate and after:
- New external trust boundary, protocol, connector or identity provider.
- Changes to tenant isolation, key/secret lifecycle, artifact signing or execution isolation.
- Security incident, data exposure, unexpected side effect or failed rollout.
- Marketplace/publisher onboarding or new legal/data-processing arrangement.
- Major dependency or cloud/provider change.

## 5. Closure conditions

This is an initial risk register and documentary review, not evidence of controls operating. Risk identification/review task may close as a baseline deliverable; risk ownership, likelihood, treatment completion and residual risk acceptance remain open items and must be tracked separately.
