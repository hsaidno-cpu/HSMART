# HSMART Implementation Roadmap

Estimates are planning ranges, not delivery commitments. Parallel work is possible only after dependencies and owners exist.

## Delivery principles
- Deliver a vertical slice before broad feature coverage.
- Keep MVP scope narrow.
- Build modularly; extract services only with evidence.
- Every phase ends with acceptance and security review.
- Do not claim production readiness from endpoint demos.
- Track work through issues, PRs, tests, and release evidence.

## Phase 0 — Architecture and governance foundation
**Planning range:** 2–3 weeks.
- Master architecture and ADR baseline.
- Domain boundaries and ownership.
- Canonical manifest and event envelope.
- Threat model and security baseline.
- Repository structure, branch protection, contribution policy.

Exit gate: architecture owner approves normative contracts; open decisions have owners.

## Phase 1 — Universal Registry
**Planning range:** 3–4 weeks.
- Organization/publisher identity minimum.
- Capability ID and version model.
- Manifest validation.
- Dependency declaration and basic resolver.
- Artifact metadata, digest, provenance.
- Discovery and visibility policy.

Exit gate: capability can be registered, validated, discovered, and versioned without duplicate identity.

## Phase 2 — Access and Connectivity
**Planning range:** 3–5 weeks.
- OIDC integration.
- API key lifecycle.
- Access policy enforcement.
- REST gateway and Remote MCP server.
- Request validation, rate limits, audit correlation.
- Connector security baseline.

Exit gate: authorized MCP and REST clients invoke allowed operations; negative authorization tests pass.

## Phase 3 — Managed Execution
**Planning range:** 3–5 weeks.
- Queue and worker lifecycle.
- Isolated cloud execution.
- Resource/time limits.
- Invocation status/result contract.
- Runtime telemetry.
- Quarantine and cancellation.

Exit gate: one signed capability artifact executes in isolation with traceable version and tenant context.

## Phase 4 — Adaptive Synchronization
**Planning range:** 4–6 weeks.
- Desired/observed state.
- Risk classification.
- Evaluation/release gates.
- Dependency and compatibility checks.
- Staged/canary rollout.
- Rollback and audit evidence.

Exit gate: compatible update propagates; breaking/high-risk update is approval-gated; failure restores a known-good state.

## Phase 5 — Self-hosted and cross-platform
**Planning range:** 4–6 weeks.
- Runtime enrollment and workload identity.
- Signed deployment instructions.
- Self-hosted runtime agent.
- Platform adapters based on supported client capabilities.
- Generic MCP and REST SDK.

Exit gate: same contract works through managed cloud and a self-hosted runtime; at least two independent client paths pass integration tests.

## Phase 6 — Marketplace
**Planning range:** 4–6 weeks.
- Publisher onboarding and verification.
- Listing lifecycle and permission disclosure.
- License and entitlement model.
- Usage metering and audit.
- Quarantine, appeal, takedown.

Exit gate: external publisher submits a capability and consumers invoke only with valid entitlement and permission.

## Phase 7 — Production hardening
**Planning range:** 3–5 weeks.
- Security assessment and remediation.
- Load/resilience tests.
- Backup/restore and DR drills.
- Operational runbooks.
- Alerting and incident response.
- Production readiness review.

Exit gate: security, operations, and governance owners approve production launch.

## MVP minimum scope

Canonical manifest and registry; stable identity and immutable version metadata; publisher identity and artifact integrity; REST invocation and Remote MCP; authentication, authorization, quota, audit; isolated managed runtime; basic evaluation gate; basic risk-adaptive desired/observed state; failure handling and rollback.

Defer full self-hosted fleet management, multi-region, billing settlement, complete marketplace automation, and autonomous self-healing.

## First vertical slice
1. Register a sample capability.
2. Validate manifest and publisher authorization.
3. Upload artifact and verify digest/signature.
4. Publish a stable version after tests.
5. Discover through Registry.
6. Invoke through REST and MCP.
7. Execute in isolated worker.
8. Publish a compatible patch.
9. Reconcile target runtime.
10. Demonstrate denied request, failed rollout, rollback, and audit trail.

## Workstream ownership

Assign accountable owners for Registry, Access, Gateway, Runtime, Synchronization, Evaluation/Security, and Marketplace. One person may hold multiple roles in an early team, but responsibilities remain explicit.

A feature is complete only when implementation, documentation, tests, operations, and acceptance evidence agree.
