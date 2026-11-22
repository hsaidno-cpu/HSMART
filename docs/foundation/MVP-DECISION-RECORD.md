# HSMART MVP Boundary & Acceptance Decision Record

**Document ID:** HSMART-PRODUCT-MVP-001  
**Version:** 1.1.0  
**Prepared:** 2026-11-22  
**Status:** APPROVAL-READY — PENDING ACCOUNTABLE DECISION  
**Decision class:** D2 (product scope and acceptance baseline)  
**Decision owner:** Project Sponsor / Accountable Owner and Product Owner — appointments pending  
**Related:** Project Charter v1.0.0; Implementation Roadmap; ADR-001 through ADR-011

> This record is a complete decision package, not evidence of approval. It becomes an approved product baseline only after the appointed accountable people record their decisions below.

## 1. Decision requested

Approve one narrow MVP: a secure, observable, repeatable end-to-end lifecycle for one deterministic demonstration capability, \`hsmart:demo:text-transformer\`, exposed through both REST/HTTP and Remote MCP.

The MVP is intended to prove HSMART's infrastructure and governance proposition. It is not a marketplace launch, a universal compatibility claim, or a production-scale service.

## 2. MVP operating envelope

| Dimension | MVP boundary |
|---|---|
| Capability | One deterministic demonstration capability: \`hsmart:demo:text-transformer\` |
| Publisher | One first-party test publisher |
| Control plane | One logical HSMART control-plane deployment |
| Execution | One isolated managed worker class |
| Protocols | REST/HTTP and Remote MCP |
| Tenancy | At least two test tenants to verify isolation; no multi-region tenancy claim |
| Clients | At least one authorized client and one denied client |
| Lifecycle | Register → validate → publish immutable version → discover → authorize → invoke → evaluate/audit → update → rollback |
| Environments | Local development, CI test, and one non-production hosted acceptance environment |
| Release objective | Verified vertical slice, not general availability |

The MVP may use synthetic test data only. No production customer data, production secret, or real publisher workload is required to prove the slice.

## 3. In-scope capabilities

| ID | Capability | Minimum MVP behavior | Primary domain |
|---|---|---|---|
| MVP-01 | Canonical manifest | Validate required fields, identity, version, interfaces, runtime and security declarations | D02 |
| MVP-02 | Publisher/capability identity | Stable publisher namespace and capability ID; reject duplicate active identity | D02/D03 |
| MVP-03 | Registry lifecycle | Register, validate, publish, list versions and discover visible capability metadata | D02 |
| MVP-04 | Artifact integrity | Bind immutable published version to digest and provenance metadata; prevent silent mutation | D02/D09 |
| MVP-05 | Access policy | Authenticate caller and evaluate tenant, resource, operation, scope and quota before invocation | D08 |
| MVP-06 | API credential minimum | Create, scope, expire, rotate and revoke an API credential through a safe lifecycle | D08 |
| MVP-07 | Distribution | Invoke the same capability through REST/HTTP and Remote MCP using equivalent policy decisions | D06/D08 |
| MVP-08 | Managed execution | Run the deterministic demo in an isolated worker with enforceable time/resource and network-egress boundaries | D05 |
| MVP-09 | Invocation lifecycle | Record accepted, queued, running, completed, failed, cancelled and timed-out states as applicable | D04/D05 |
| MVP-10 | Evaluation and evidence | Link test/evaluation evidence to capability version and artifact digest | D09 |
| MVP-11 | Observability/audit | Correlate security-sensitive lifecycle events from request through result without logging secrets | D10 |
| MVP-12 | Minimal synchronization | Demonstrate compatible update, gated high-risk update, failed rollout and rollback | D07 |
| MVP-13 | Negative controls | Demonstrate malformed manifest, expired/revoked/unauthorized/cross-tenant/over-quota denial and controlled execution failure | D08/D09 |

## 4. Explicit non-goals

- External publisher marketplace, listing moderation, payment, billing, refunds and settlement.
- Self-hosted runtime fleet, runtime enrollment at scale and multi-region active-active deployment.
- Broad SDK coverage or a claim of compatibility with every AI client/platform.
- Bulk publication of the candidate 427 Skill Registry Records.
- First-party integration of A.S.F.R.E.E Canonical/Legacy, Skill Analyzer and Octa-Prompt; these remain KM 7.
- Arbitrary third-party code execution without the defined trust, quarantine and isolation controls.
- General-purpose model hosting, model training or guaranteed correctness of external model outputs.
- Kubernetes or microservices as prerequisites.
- Production SLO, throughput, latency, availability, RPO/RTO or unit-cost commitments before workload and infrastructure baselines exist.

## 5. Acceptance criteria and test oracles

A criterion is accepted only when its test result and evidence locator are attached to the exact build/PR/release record.

| AC | Observable acceptance condition | Required evidence |
|---|---|---|
| AC-01 | Every required manifest fixture is deterministically accepted or rejected; missing required fields, invalid identity/version and undeclared extra fields are rejected | Positive/negative JSON Schema test report |
| AC-02 | Duplicate active capability identity is rejected within the declared publisher namespace, including a concurrent-create test | Registry test and persisted uniqueness constraint |
| AC-03 | Published version metadata and artifact digest cannot be silently changed; mutation is rejected and a legitimate change creates a new version | Registry/artifact immutability and digest-verification tests |
| AC-04 | Discovery returns only records visible to the authenticated principal and tenant | Positive and cross-tenant negative authorization tests |
| AC-05 | Valid permission is allowed; expired, revoked, insufficient-scope, unauthorized, cross-tenant and over-quota requests are denied | Policy test matrix with observed allow/deny decisions |
| AC-06 | REST and Remote MCP produce equivalent authorization outcomes for every case in the same AC-05 matrix | Cross-protocol parity report with shared test vectors |
| AC-07 | Demo executes in an isolated worker with a default-deny network-egress policy and enforceable resource limits; the exact limits are recorded in the runtime profile before execution | Runtime isolation, egress and resource-limit report |
| AC-08 | Timeout, cancellation, execution failure, duplicate request and retry behavior follow documented lifecycle and idempotency rules | Runtime failure/recovery and idempotency tests |
| AC-09 | Every enumerated security-sensitive action has a correlated audit record; automated checks find no test credential or token in ordinary logs | Audit completeness and log-redaction test report |
| AC-10 | Evaluation evidence identifies exact capability ID, version, artifact digest and source build | Evidence-linkage test |
| AC-11 | Compatible update succeeds; a breaking/high-risk update is held for approval; a failed rollout restores the exact known-good artifact | Synchronization, policy-gate and rollback report |
| AC-12 | All required acceptance scenarios pass on a named commit and environment; unresolved P0/P1 defects or required tests marked NOT_RUN/BLOCKED prevent acceptance | Test ledger, independent review and signed acceptance decision |

**Runtime limit rule:** CPU, memory, execution timeout, payload size and egress values must be selected in the accepted runtime profile and verified against the chosen worker. They must not be invented from this document or silently presented as production SLOs.

## 6. Initial success measures

These are binary/countable MVP acceptance measures, not production service-level objectives.

1. **Contract determinism:** 100% of committed positive and negative fixtures produce their expected result.
2. **Authorization correctness:** 100% of the declared allow/deny policy matrix produces the expected decision.
3. **Protocol parity:** 100% of the shared policy matrix has equivalent REST and Remote MCP outcomes.
4. **Artifact integrity:** 100% of published test versions have a recorded digest; every deliberate test mutation is rejected.
5. **Audit coverage:** 100% of enumerated security-sensitive MVP actions have correlated audit records, with no secret/token leakage in ordinary logs.
6. **Recovery:** the defined failed-rollout scenario restores the exact previous known-good artifact and records the recovery evidence.
7. **Reproducibility:** a clean checkout on the supported Python 3.12 minor line installs the declared contract-tool dependencies and passes the contract suite on the supported CI operating systems.
8. **Release discipline:** zero unresolved P0/P1 defects and zero required tests marked NOT_RUN/BLOCKED at the acceptance decision.

No throughput, latency percentile, availability, unit-cost, ROI or production support commitment is implied by these measures. Those require representative workload and deployment evidence.

## 7. Dependency sequence

1. KM 0 governance: named decision owner, scope adoption, roles, initial risk acceptance and backlog.
2. KM 1 technical foundation: accepted stack/infrastructure baseline, reproducible development baseline and canonical contract/test harness.
3. KM 2 registry: stable identity, persistence, validation, publication and discovery.
4. KM 3 access/distribution: shared policy core, identity, API key lifecycle, REST and Remote MCP.
5. KM 4 managed execution: isolated worker and invocation lifecycle.
6. KM 5 assurance/observability: evidence, traces, metrics and release gates.
7. KM 6 minimal adaptive synchronization: desired/observed state, staged rollout and rollback.
8. MVP acceptance review: independent verification and signed decision.

## 8. Approval and decision record

| Decision field | Value |
|---|---|
| Proposed boundary | This document, sections 2–7 |
| Decision | PENDING |
| Project Sponsor / Accountable Owner | NOT APPOINTED |
| Product Owner | NOT APPOINTED |
| Approval date | NOT RECORDED |
| Conditions / exceptions | Must be recorded here before the baseline is treated as approved |
| Effective version | 1.1.0 only after approval |

A proposed scope is not an approved scope. Record the named approver, authority, date, decision, accepted exceptions and effective version before changing status to APPROVED.
