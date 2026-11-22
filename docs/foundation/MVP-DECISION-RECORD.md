# HSMART MVP Boundary & Acceptance Decision Record

**Document ID:** HSMART-PRODUCT-MVP-001  
**Version:** 1.0.0  
**Prepared:** 2026-11-22  
**Status:** PROPOSED — accountable approval required  
**Decision class:** D2 (product scope and acceptance baseline)  
**Decision owner:** Project Sponsor / Accountable Owner and Product Owner — appointments pending  
**Related:** Project Charter v1.0.0; Implementation Roadmap; ADR-001 through ADR-010

> This record converts the Charter's broad MVP statement into a testable decision package. It is not a claim that the scope has been formally approved. Approval remains open until accountable project roles are appointed and explicitly adopt it.

## 1. Decision requested

Approve one narrow MVP: a repeatable, secure, observable end-to-end lifecycle for a deterministic capability named hsmart:demo:text-transformer.

The MVP demonstrates HSMART's infrastructure value. It is not an advanced AI product, a marketplace launch, or proof of universal compatibility.

## 2. Product outcome

A publisher/operator can register and validate a capability, publish an immutable version, make it discoverable to an authorized consumer, authorize and invoke it through both REST/HTTP and Remote MCP, execute it in a constrained managed worker, capture attributable evaluation/audit evidence, roll out a compatible update under policy, and demonstrate a denied request plus a failed-rollout recovery to a known-good version.

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

- Full external publisher marketplace, listing moderation, payment, billing, refunds and settlement.
- Self-hosted runtime fleet, runtime enrollment at scale and multi-region active-active deployment.
- Broad SDK coverage or a claim of compatibility with every AI client/platform.
- Bulk publication of the candidate 427 Skill Registry Records.
- First-party integration of A.S.F.R.E.E Canonical/Legacy, Skill Analyzer and Octa-Prompt; these remain KM 7.
- Arbitrary third-party code execution without the defined trust, quarantine and isolation controls.
- General-purpose model hosting, model training or guaranteed correctness of external model outputs.
- Kubernetes or microservices as prerequisites.
- Production SLO, throughput, latency, availability, RPO/RTO or unit-cost commitments before workload and infrastructure baselines exist.

## 5. Acceptance criteria

A criterion is accepted only when its test result and evidence locator are attached to the relevant build/PR/release record.

| AC | Observable acceptance condition | Required evidence |
|---|---|---|
| AC-01 | Every required manifest fixture is deterministically accepted or rejected; unknown fields and malformed identity/version are rejected | Schema test report |
| AC-02 | Duplicate active capability identity is rejected within the declared publisher namespace | Registry test and persisted uniqueness constraint |
| AC-03 | Published version metadata and artifact digest cannot be silently changed; a change creates a new version | Registry/artifact immutability test |
| AC-04 | Discovery returns only records visible to the authenticated principal and tenant | Positive and negative authorization tests |
| AC-05 | Expired, revoked, unauthorized, cross-tenant and over-quota invocations are denied | Policy test matrix with observed decisions |
| AC-06 | REST and Remote MCP produce equivalent authorization outcomes for equivalent principal/resource/action inputs | Cross-protocol contract test report |
| AC-07 | Demo executes in the managed worker under configured resource limits and default-deny/restricted egress | Runtime isolation and resource-limit report |
| AC-08 | Timeout, cancellation, execution failure and retry behavior follow the documented lifecycle and idempotency rules | Runtime failure/recovery tests |
| AC-09 | Every security-sensitive invocation and lifecycle action has a correlated audit record; secrets and restricted payloads are absent from ordinary logs | Audit completeness and log-redaction tests |
| AC-10 | Evaluation evidence identifies exact capability ID, version and artifact digest | Evidence-linkage test |
| AC-11 | Compatible update follows policy; high-risk/breaking update is held for approval; failed rollout restores a known-good artifact | Synchronization and rollback test report |
| AC-12 | All required MVP scenarios pass on a named commit and environment, with unresolved P0/P1 defects blocking acceptance | Test ledger, review and acceptance decision |

## 6. Initial success measures

These are finite MVP acceptance measures, not production service-level objectives.

- Contract determinism: all committed positive and negative schema fixtures produce their expected pass/fail result.
- Authorization correctness: 100% of the declared MVP positive/negative policy cases produce the expected allow/deny outcome.
- Protocol parity: REST and Remote MCP pass the same authorization decision matrix.
- Artifact integrity: every published test artifact has a recorded digest; no in-place mutation is accepted.
- Audit coverage: 100% of the enumerated security-sensitive MVP actions have a correlated audit record.
- Recovery: the defined failed-rollout test returns the target to the previously known-good version.
- Release discipline: no MVP acceptance decision is made with an unresolved P0/P1 defect or a required test marked NOT_RUN/BLOCKED.
- Reproducibility: a clean checkout can install the declared development tooling and run contract tests using the documented Python minor version and pinned direct dependencies.

Do not translate these criteria into production SLOs or financial ROI without workload, deployment, and cost evidence.

## 7. Dependency sequence

1. KM 0 governance: named decision owner, scope adoption, roles, initial risk acceptance and backlog.
2. KM 1 technical foundation: selected stack, reproducible development baseline, canonical contract and test harness.
3. KM 2 registry: stable identity, persistence, validation, publication and discovery.
4. KM 3 access/distribution: shared policy core, identity, API key lifecycle, REST and Remote MCP.
5. KM 4 managed execution: isolated worker and invocation lifecycle.
6. KM 5 assurance/observability: evidence, traces, metrics and release gates.
7. KM 6 minimal adaptive synchronization: desired/observed state, staged rollout and rollback.
8. MVP acceptance review: independent verification and signed decision.

## 8. Decision and approval record

| Decision field | Value |
|---|---|
| Proposed boundary | This document, sections 2–7 |
| Decision | PENDING |
| Project Sponsor / Accountable Owner | NOT APPOINTED |
| Product Owner | NOT APPOINTED |
| Approval date | NOT RECORDED |
| Conditions / exceptions | Must be recorded here before the baseline is treated as approved |

A proposed scope is not an approved scope. Record the named approver, date, decision, accepted exceptions and effective version before changing status to APPROVED.
