# HSMART AI Audit Trail and Evidence

**Document ID:** HSMART-GOV-AI-AUD-001  
**Version:** 1.0.0  
**Effective date:** 2026-11-22  
**Policy owner:** GOV-01 — Harysaidno  
**Schema:** [ai-agent-action-record.schema.json](../contracts/ai-agent-action-record.schema.json)  
**Status:** Audit requirements approved; append-only runtime store not yet implemented or verified

## 1. Purpose

This document defines the evidence required to reconstruct AI-assisted work across HSMART. It separates:

- **Request:** what GOV-01 or another authorized user asked for.
- **Authorization:** what GOV-01 explicitly permitted and within which boundaries.
- **Policy decision:** what the centralized enforcement component allowed, denied or held.
- **Execution:** which Agent, model, Skill, Sub-Agent and tool actually acted.
- **Change:** what resource, branch, page, path or artifact was affected.
- **Evaluation:** what tests and independent reviewers found.
- **Disposition:** what GOV-01 or another authorized human decided.

A chat transcript, Agent summary, successful API response or Git commit alone is not a complete audit record.

## 2. Non-negotiable evidence requirements

Every action that mutates GitHub, Notion, CI configuration, a runtime, a credential broker or another authoritative system must have:

1. A unique event ID and event timestamp in UTC.
2. The stable Agent ID, GOV role and full Sub-Agent lineage.
3. Actual model provider, model ID, model version/snapshot and runtime instance identifier where exposed.
4. System prompt, task template, policy, configuration, Skill and Sub-Skill version/revision or content digest.
5. Tool/Plugin/Connector name, version, operation and request/trace reference.
6. Original task and source references.
7. GOV-01 approval grant and approval evidence.
8. Central policy decision ID, policy version and ALLOW/DENY/HOLD result.
9. Target system, repository/page, branch, path/property and operation.
10. Before/after content hashes or immutable artifact identifiers where the operation changes content.
11. Commit SHA, pull request URL, CI run ID, Notion page ID or external operation ID where applicable.
12. Tests, independent evaluation, findings and final disposition.
13. Integrity metadata linking the event to the append-only sequence.

If a value is not exposed, record `unknown` and a reason. If a field does not apply, record `not_applicable` where the schema supports it. Do not guess model versions, infer that a Skill was loaded or invent a tool execution ID.

## 3. Event taxonomy

At minimum, capture these events:

| Event family | Examples | Required capture |
|---|---|---|
| Request and planning | task accepted, plan drafted, scope clarified | requester, source instruction, task ID, objective, context |
| Authorization | grant created, amended, revoked, expired | GOV-01 approver, grant scope, validity, decision reference |
| Policy enforcement | allow, deny, hold, emergency suspension | actor, target/action, policy version, decision ID, reason |
| Agent lifecycle | designated, provisioned, verified, activated, suspended, revoked | Agent ID, profile/model/Skill/tool versions, approver |
| Tool execution | GitHub read/write, Notion update, test/scan invocation | connector, tool, operation, request ID, target and outcome |
| Repository changes | branch create, commit, PR create/update, merge | base/head SHA, branch, file paths, content hashes, PR URL |
| Notion changes | page update, property update, task state change | page ID, exact operation, property/content diff, page URL |
| Evaluation | review started/completed, test result, finding created/closed | evaluator identity, independence, methods, evidence, finding status |
| Human decision | accept, reject, hold, risk disposition, approval | GOV-01 identity, authority basis, date, rationale and scope |
| Security incident | unauthorized attempt, secret exposure, audit gap, policy bypass | detection, containment, impact, evidence, response and recovery |
| Release/production | release proposal, human approval, deployment result | target environment, version/artifact digest, approver, rollback evidence |

Read-only events may be captured at a lower detail level based on sensitivity, but sensitive reads must remain attributable. Mutating events must never be omitted.

## 4. Provenance record

### 4.1 Actor and execution lineage

Record:

- Actor type: human, AI assistant, orchestrator, Sub-Agent or system.
- Stable actor ID and GOV role ID.
- Parent orchestrator and every Sub-Agent involved.
- Whether the action was directly requested, delegated or triggered automatically.
- Runtime instance, tenant/environment and connector identity.

### 4.2 Model and AI configuration

Record the actual values available at execution time:

- Provider or model host.
- Exact model identifier and version/snapshot; do not use a marketing family name when a specific runtime version is available.
- Endpoint/deployment ID and inference configuration references where available.
- System instruction and task prompt template ID/version/digest.
- Retrieval corpus, source snapshot or reference set when material to the result.
- Guardrail/policy configuration and revision.

Raw chain-of-thought or private reasoning is not an audit requirement. Capture the task input reference, concise decision rationale, sources, tool calls, findings and outcome. Do not log hidden reasoning or unnecessary personal data.

### 4.3 Skill, Sub-Skill, Plugin and Tool provenance

For each loaded Skill/Sub-Skill and invoked Plugin/Tool/Connector, record:

- Stable ID/name.
- Version, release, commit SHA or package digest.
- Publisher/source and retrieval reference.
- Permission scopes and enabled operations.
- Connector endpoint identity where safe to record.
- Invocation request ID, result and artifact digest.

An Agent profile that has only a name but no pinned Skill/tool revisions is not fully reproducible and must not be described as version-verified.

## 5. Authorization and decision lineage

Every mutating action must link to one specific authorization grant.

An approval grant must be reconstructible from its record: approver, authority basis, task, Agent IDs, target resources, branch/pages/paths, allowed operations, risk, expiry, limits, required tests, cross-evaluators and revocation conditions.

Store the grant ID, not just a natural-language statement that "approval was given". Record policy decision ID and exact policy version for each action. A single grant may authorize a finite work batch, but each mutating call must still generate a policy decision and event.

The authorization record and execution record are different things: GOV-01 approval authorizes an action; a policy decision evaluates whether the requested action fits that approval at execution time.

## 6. Change and evidence linkage

For GitHub:

- Repository full name, base ref/SHA and working branch.
- Exact file paths and operation type.
- Before/after blob SHA or content digest when available.
- Resulting commit SHA, PR number/URL, merge SHA if merged by a human.
- CI workflow ID/run ID, head SHA, job results and artifact references.
- Reviewer and approval references.

For Notion:

- Workspace/data source/page ID and canonical URL.
- Exact property names or content section changed.
- Operation type and summarized before/after state.
- GitHub source document/commit reference for normative information.
- Task state change and the evidence that justified it.

For external tools:

- Connector identity, endpoint/service identity, request/trace ID and response outcome.
- Safe request/response digests or redacted summaries.
- Do not store raw credential values or sensitive payloads merely to make the audit record look complete.

## 7. Append-only integrity architecture

The intended audit store must be append-only and independently verifiable.

Minimum requirements:

1. Events are written in sequence and cannot be edited in place by Agents.
2. Corrections are new events that reference the earlier event; do not rewrite the original record.
3. Each event includes the previous event hash and its own canonical event hash.
4. Use a well-defined canonical serialization and cryptographic hash algorithm.
5. Where feasible, sign events or batches using a protected signing service whose key is unavailable to Agents.
6. Store audit data in a restricted append-only/WORM-capable destination separate from the runtime being audited.
7. Restrict deletion and retention-policy changes to an authorized human process.
8. Back up audit records and periodically verify chain continuity, signatures, event counts and restore integrity.
9. Alert on missing events, sequence gaps, hash mismatch, clock anomalies or unauthorized access.
10. Maintain a read-only audit view for project review and incident reconstruction.

A Git repository is valuable for normative decision history but is not, by itself, a tamper-proof audit store. Repository administrators or compromised credentials may be able to rewrite or delete history. HSMART must not claim immutable runtime audit until a separate protected event store, signing/verification process, retention policy and recovery process are implemented and tested.

## 8. Privacy, data minimization and retention

Auditability does not justify indiscriminate data collection.

- Store the minimum information required to reconstruct action and authority.
- Never log passwords, API keys, tokens, private keys, recovery codes or raw secret values.
- Redact personal or confidential data from payloads and tool logs unless required and authorized.
- Prefer references, hashes and controlled evidence links over duplicate payload storage.
- Apply access controls to audit records; an Agent should access only records needed for its task.
- Define separate retention rules for operational events, security incidents, approval evidence and personal data.
- GOV-01 must approve retention, legal-hold, deletion and export policy after considering applicable law and actual operating context. No retention duration is invented in this specification.
- Record every access to sensitive audit evidence where the storage system supports it.

## 9. Audit and incident controls

The following events require immediate escalation to GOV-01 and suspension of affected mutating permissions:

- Any Agent performs or attempts an unauthorized write.
- A grant is missing, expired, revoked or outside the action scope.
- An Agent attempts to change its own policy, permissions, identity or parent registry.
- Direct write to `main`, merge, production release or deployment is attempted by an Agent.
- Secret material appears in model context, tool output, Notion, code, logs or audit evidence.
- An audit event is missing, rewritten, unverifiable or lacks required provenance.
- A critical cross-evaluation finding is omitted, downgraded without evidence or marked closed without independent re-test.

Preserve evidence, contain the affected identity, revoke credentials through the authorized human process, establish impact and root cause, and require an independently reviewed recovery plan.

## 10. Bootstrap decision and action records

These records document the initial establishment of the policy and the actions that created this governance baseline. They are historical project records, not proof that a production audit platform already exists.

### 10.1 PR #9 merge authorization and result

| Field | Record |
|---|---|
| Event ID | `HSMART-EVT-GOV01-20261122-PR9-MERGE` |
| Human authority | Harysaidno — GOV-01 |
| Source approval | Explicit instruction in the conversation: "merge PR #9" |
| Approved target | PR #9, exact head `4640029172ae66b74a3d1d7e27a74e020b0e25a4` |
| Pre-merge verification | GitHub Actions run #23, all four jobs successful |
| Executed action | PR #9 marked ready for review and merged using merge commit |
| Result | Merged: `5ad3bf612a886550ea5c78e7ba605886456e8ff6` |
| Evidence | [PR #9](https://github.com/hsaidno-cpu/HSMART/pull/9), [CI run #23](https://github.com/hsaidno-cpu/HSMART/actions/runs/44975788638) |
| Limitation | This action predates technical rollout of the present policy. It was directly authorized by GOV-01 and is being captured as a bootstrap record; no separate runtime policy decision ID or append-only event hash was emitted at execution time. |

### 10.2 AI Functional Delegation authorization

| Field | Record |
|---|---|
| Event ID | `HSMART-EVT-GOV01-20261122-AI-DELEGATION` |
| Approval grant | `HSMART-AUTH-GOV01-20261122-002` |
| Human authority | Harysaidno — GOV-01 |
| Source approval | Explicit instruction to designate AI Functional Delegates for GOV-02 through GOV-06 under centralized final decision authority and the five structural rules |
| Approved scope | Design and document AI delegate profiles, sub-agent/Skill/Sub-Skill/tool maps, permission policy, cross-evaluation, audit and controlled GitHub/Notion integration rules |
| Execution boundary | Governance documentation and approved branch work; no direct write to `main`, no production deployment, no secret mutation and no runtime Agent activation |
| Runtime state | Logical profiles designated; runtime provisioning and verification remain pending |
| Evidence | This policy package, its GitHub branch/PR and related Notion closeout entry |
| Limitation | Actual model version/Skill/tool runtime metadata for HSMART delegate instances remains unknown because those instances have not been provisioned. |

### 10.3 Execution trace and version limitation

Actions performed through conversation-connected GitHub and Notion tools must be recorded as assistant/tool-assisted operations, not falsely attributed to an HSMART runtime Agent. In the bootstrap phase, the exact internal connector implementation version and per-call model deployment metadata may not be exposed. Those fields must be marked `unknown` in any machine event export rather than fabricated.

## 11. Runtime implementation gate

Before HSMART may claim an immutable audit system is operational, implement and test:

- Schema validation for every event type.
- Per-action authorization and policy-decision linkage.
- Append-only/write-once storage and restricted write identities.
- Hash chain or signature verification with protected keys.
- Independent monitoring for missing, delayed or invalid events.
- Backup, restore and retention controls.
- Privacy redaction and secret-detection tests.
- A documented incident runbook and audit export.
- Independent evidence review and GOV-01 acceptance.

Until then, the repository/Notion records are a governance evidence trail, not a production-grade immutable runtime audit service.
