# UEDE Core Contracts v1.0.0

**Status:** Proposed contract baseline, stacked on HSMART PR #32. Not merged, deployed, or approved as an operational authority.  
**Scope:** Read-only PRE intake, HSO capability discovery, and factual execution receipts.  
**Canonical repositories:** hsaidno-cpu/HSMART for shared cross-system schemas; hsaidno-cpu/Hypersystem-Orchestrator for HSO capability catalog and workflow-plan ownership.

## 1. Contract boundaries

| Contract | Authority | Consumer | Direction | Mutating authority |
|---|---|---|---|---|
| Roadmap Snapshot | PRE | UEDE planner | PRE → UEDE | None; snapshot is read-only |
| Capability Descriptor | HSO catalog and source evidence | UEDE capability selector | HSO → UEDE | None; discovery is not invocation |
| Execution Receipt | Verified worker/CI evidence | HSO, PRE evidence reconciliation | UEDE → evidence stores | Factual evidence only; cannot apply PRE stage transitions |

The contracts are separate from HSMART's future Capability Registry API. This PR does not implement KM 2, add registry persistence, provision a live PRE endpoint, or activate HSO skill invocation.

## 2. Existing plan contract is reused, not forked

The HSO repository owns the plan-only schema contracts/hso-workflow-plan.schema.json (schema version 1.0.0). UEDE consumes that schema for decomposition, owner assignment, dependency order, write scope, capability state, and approval declaration. HSMART must not maintain a competing planner schema.

A valid plan is still not a dispatch grant. Runtime re-checks permissions, source freshness, exact target and approval policy before any write.

## 3. Schema inventory

- uede-roadmap-snapshot.schema.json: binds PRE roadmap ID/revision, source locator, authority disposition, pagination/completeness, digest, freshness, dependencies, gates, and acceptance criteria. COMPLETE requires complete pagination, fresh evidence, and no missing references. An APPROVED/FROZEN baseline must include its decision reference and approval timestamp.
- uede-capability-descriptor.schema.json: records owner, immutable source pointer, rights, instruction parity, interface contract tests, named host activation, runtime invocation, permissions, and blockers. ELIGIBLE is invalid unless every required evidence plane passes.
- uede-execution-receipt.schema.json: binds one attempt to plan digest, repository, branch, base/head SHA, changed files, PR, CI runs, and verification. A PASS receipt must reference the exact verified commit and contain successful CI evidence. The standard JSON Schema checks shape and CI success; src/hsmart_platform/uede_contracts.py enforces cross-field equality between target HEAD, verified SHA and a successful exact-head CI run. Canonical PRE stage mutation is structurally forbidden.

## 4. Versioning and compatibility

- Each schema uses an immutable $id and an explicit semver-style contract version. Breaking changes require a new major version and a compatibility migration note.
- Unknown fields are rejected (additionalProperties: false). Additive fields therefore require a deliberate schema-version decision, not silent producer drift.
- Digests are SHA-256 prefixed as sha256:<lowercase-hex>. A digest is evidence only when the consumer independently recomputes it from the referenced canonical bytes.
- URLs are locators, not proof of trust. Consumers must resolve allowlisted sources, validate provenance, and record observation time and freshness.
- Unknown, unavailable, stale, partial, unverified, or unlicensed states must stay explicit. They never become PASS by default.

## 5. Readiness is multi-dimensional

A capability is not dispatchable because it exists in a catalog or has an instruction snapshot. Dispatch requires all of: verified canonical source with repository/ref/commit/digest, declared usage rights, instruction parity, passing interface contract tests, named-host activation, and a passing real runtime invocation with evidence. JSON Schema enforces local fields; src/hsmart_platform/uede_contracts.py enforces cross-field consistency, including parity counts and readiness conditions. An "active" catalog state is not a substitute for host evidence. If any dimension is unknown or blocked, eligibility is BLOCKED or NOT_ASSESSED.

## 6. Execution and authority rules

1. PRE remains the sole authority for roadmap baseline and stage decisions.
2. HSO remains the owner of capability identities, source pointers, and rights metadata.
3. HSMART owns platform security, policy enforcement, runtime and audit services only after their own acceptance gates.
4. UEDE may prepare plans and coordinate bounded workers; it cannot change its own permissions, policy, acceptance criteria, source rights, or approval rules.
5. Execution workers may record branch, commit, pull request, CI, test and artifact facts. They cannot self-accept a milestone or mutate canonical PRE Stage.
6. Merge, release, protected-branch, identity, secrets, production, destructive migration and baseline/acceptance changes remain under the designated human authority.

## 7. Minimum contract test matrix

- Valid and invalid PRE source revision, baseline authority, pagination completeness, freshness and missing-reference combinations.
- Capability descriptor eligibility: reject missing source, undeclared/restricted rights, instruction drift, untested interface, absent host, and mock-only invocation.
- Execution receipt: reject missing exact commit evidence, CI on a different SHA, PASS without a verification receipt, and any canonical roadmap mutation.
- Unknown fields, wrong schema versions, malformed digests, invalid URI/date-time, duplicate dependencies and empty identifiers.
- Snapshot and receipts remain read-only data; schema validity does not grant tool permissions.

## 8. Explicit non-claims

This contract proposal does not claim that PRE's shared runtime/API is deployed, that HSO generic skill invocation works, that a capability is host-live, that HSMART has a deployed Registry/Gateway, or that an autonomous worker can run against production. The current implementation is schema + local tests only; adapters and live acceptance are future gated deliverables.
