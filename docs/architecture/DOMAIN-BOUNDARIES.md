# HSMART Domain Boundaries

This document defines bounded contexts, authoritative data ownership, public contracts, and forbidden dependencies. Domains may be modules in the MVP; boundaries remain normative before service extraction.

## Domain catalogue

| ID | Domain | Owns | Must not own |
|---|---|---|---|
| D01 | Studio & Developer Experience | Drafts, builds, local tests, publish workflow | Production policy, execution secrets |
| D02 | Universal Registry | Capability identity, manifests, versions, dependencies, provenance metadata | Runtime execution, user authentication |
| D03 | Publisher & Organization | Organizations, members, publisher profiles, tenant ownership | Secret material, artifact execution |
| D04 | Intelligence Orchestrator | Plans, routing decisions, workflow state, agent coordination | Policy bypass, direct credential reads |
| D05 | Execution Runtime | Jobs, workers, sandbox state, execution results, resource usage | Publishing or changing immutable releases |
| D06 | Distribution Gateway | Protocol sessions, request translation, client adapter state | Canonical capability metadata |
| D07 | Synchronization Engine | Desired/observed state, rollout plans, reconciliation jobs | Signing authority, security-gate bypass |
| D08 | Access & Identity | Principals, grants, scopes, API credential metadata, policies, secret references | Capability source or execution results |
| D09 | Evaluation & Assurance | Test definitions, runs, evidence, risk findings, release gate decisions | Altering publisher source or post-run evidence |
| D10 | Observability & Audit | Metrics, traces, logs, audit records and retention metadata | Business source-of-truth mutations |
| D11 | Marketplace & Commerce | Listings, subscriptions, entitlements, usage, billing references | Implicit runtime permission |
| D12 | Infrastructure & Operations | Deployment definitions, environment health, backup/restore | Publisher business ownership |

## Domain contracts

- Studio calls Registry to manage drafts and submit releases; it never writes Registry storage directly.
- Registry emits capability and release lifecycle events.
- Publisher/Organization provides verified publisher and tenant context.
- Gateway authenticates with Access & Identity, resolves capability via Registry, authorizes invocation, then delegates to Orchestrator/Runtime.
- Orchestrator requests authorization for each protected tool/action; it cannot mint scopes or elevate privileges.
- Runtime verifies signed deployment instructions and artifact digest before execution.
- Synchronization consumes release/evaluation events and requests deployments through Runtime's deployment contract.
- Evaluation consumes immutable artifacts and emits evidence and gate decisions.
- Marketplace reads Registry publication metadata and checks entitlement on every invocation.
- Observability consumes events; it is not an alternate business database.
- Infrastructure operations use workload identities and narrowly scoped administrative permissions.

## Forbidden dependencies

1. Direct cross-domain database writes.
2. Marketplace listing status treated as execution authorization.
3. Gateway or Orchestrator bypassing Access & Identity.
4. Runtime mutating published capability versions.
5. Synchronization activating a release that failed mandatory gates.
6. Publisher reading another publisher's secret material.
7. Self-hosted runtime receiving general Control Plane administrator privileges.
8. Logs containing raw tokens, private keys, or unredacted sensitive payloads.
9. An AI agent granting itself permission, approving its own high-risk release, or disabling audit.

## Event ownership

| Event family | Authoritative producer |
|---|---|
| Organization/member/publisher changes | Publisher & Organization |
| Capability/version/release lifecycle | Registry |
| Invocation/job lifecycle | Runtime |
| Plan/routing state | Orchestrator |
| Deployment/reconciliation state | Synchronization |
| Grants/credential revocation | Access & Identity |
| Evaluation/risk/release gate | Evaluation & Assurance |
| Listing/entitlement/billing state | Marketplace |

## Service extraction rule

A domain is eligible for independent service extraction when there is evidence of independent scaling, fault isolation, security boundary, deployment cadence, or team ownership. Extraction requires an ADR and migration plan; it must not create duplicated sources of truth.
