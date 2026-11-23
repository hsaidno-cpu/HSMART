# HSMART

**Hypersystem Synchronization & Management Architecture for Revolutionary Technology**

HSMART is a universal AI ecosystem infrastructure platform for registering, governing, distributing, executing, evaluating, and synchronizing AI capabilities across compatible platforms and deployment environments.

> Build Once. Connect Everywhere. Evolve Continuously.

## Architecture baseline

This repository currently contains the architecture and implementation contracts. It is **not yet a deployed platform**. Runtime services, authentication, marketplace transactions, synchronization workers, and production controls must be implemented and independently verified.

| Decision | Baseline |
|---|---|
| Ownership | Hybrid Foundation + Commercial Operator |
| Execution | Hybrid managed cloud + self-hosted runtime |
| Distribution | Universal, protocol- and adapter-based |
| Synchronization | Adaptive, risk-based |
| Ecosystem | Governed multi-publisher marketplace |
| Architecture | Modular, API-first, MCP-native |
| Initial implementation | Modular monolith with separable workers |

## Platform domains

- Universal Capability Registry: stable identities, manifests, versions, provenance, dependencies, and release channels.
- Distribution Gateway: Remote MCP, REST/HTTP, SDKs, webhooks, and platform adapters.
- Execution Runtime: isolated managed-cloud and self-hosted execution.
- Adaptive Synchronization: desired/observed state reconciliation, risk classification, staged rollout, and rollback.
- Access & Identity: OIDC/OAuth, API credentials, connector authorization, workload identity, and policy enforcement.
- Evaluation & Assurance: contract, compatibility, security, regression, and release-gate evidence.
- Marketplace: governed publisher onboarding, discovery, licensing, entitlement, and usage metering.
- Observability & Governance: auditability, tracing, quotas, incident response, and operational controls.

## Documentation map

| Path | Purpose |
|---|---|
| docs/foundation/ | Project Charter, ratification record, MVP boundary and acceptance decision |
| docs/planning/ | Progressive completion roadmap, prioritized KM 0–KM 2 backlog and dependencies |
| docs/engineering/ | Contract tooling and KM 1 application development environment |
| tests/ | JSON Schema fixtures, OpenAPI contract tests and governance policy tests |
| src/hsmart_governance/ | Local reference policy evaluator; not a production authorization gateway |
| src/hsmart_platform/ | KM 1 FastAPI/SQLAlchemy/Alembic application foundation; not KM 2 services |
| docs/architecture/ | Master architecture, domains, ADRs, ecosystem integration, repository blueprint |
| docs/access/ | Universal Access Manager and its six required subskills |
| docs/security/ | Threat model and security baseline |
| docs/data/ | Logical data model and governance |
| docs/glossary/ | SDGDS terminology registry, schema, curation policy and synchronization tooling |
| docs/contracts/ | JSON Schema, OpenAPI, event contracts |
| docs/synchronization/ | Adaptive synchronization policy |
| docs/runtime/ | Hybrid runtime contracts and GOV-02..GOV-12 activation/evidence plan |
| docs/governance/ | Ownership, human authority, AI Functional Delegation Charter, delegate registry, permission/approval policy, cross-evaluation and audit governance |
| docs/roadmap/ | Implementation phases and acceptance criteria |
| docs/operations/ | Production-readiness and operations |

## First implementation milestone

Prove one complete vertical slice: register a capability; validate publisher identity, manifest, digest and signature; publish an immutable version; discover and invoke it through MCP and REST; execute it in a constrained cloud runtime; propagate a compatible release; and demonstrate authorization denial, audit evidence, failure handling and rollback.

A successful HTTP response alone is not acceptance evidence.

## Status and non-goals

- Current status: **KM 1 application foundation implemented on PR #28 branch; PR #13 canonical; main protection and KM 0/KM 1 exit gates remain open**.
- No production endpoint, cloud account, database, OAuth issuer, marketplace payment provider, or runtime is claimed to exist.
- The baseline does not require microservices, Kubernetes, multi-region deployment, or autonomous code modification in the MVP.
- External clients may need adapter refresh or reconnection for changed tool manifests. HSMART cannot force an independently managed client to refresh.

## Repository protection operation

**First-time bootstrap:** because the workflow itself is still on PR #28, it is not yet available from the default branch. Apply the initial protection from a local checkout using the exact commands in `docs/governance/REPOSITORY-BASELINE-CONTROLS.md` and a local-only token with repository **Administration: write**. After PR #28 merges, use **Actions → Repository Main Protection → Run workflow** for status, dry-run and later changes; that workflow is restricted to `hsaidno-cpu`, reads `HSMART_REPOSITORY_ADMIN_TOKEN` from repository Secrets and requires the current full `main` SHA. Never put the token in ChatGPT, Notion, source files or workflow inputs. Installing a workflow does not itself protect `main`; verify GitHub's API read-back and negative test.

## Contributing

See CONTRIBUTING.md. Normative architecture or contract changes require an ADR, validation evidence, and compatibility assessment. Project scope and governance changes must follow the Project Charter.

## License

The repository currently contains an Apache License 2.0 file. Review licensing and ownership policy for each separately distributed artifact, marketplace listing, trademark, and third-party contribution before commercial release.


## Historical implementation snapshot — 22 November 2026 (superseded by PR #28 current snapshot above)

- PR #13 is merged to `main` at `17c78dcd2ea59c6d40f9a07d188bab6f829f0596`.
- GOV-01 is the sole human authority in the internal governance model; GOV-02 through GOV-12 are AI Functional Delegate profiles designated but not provisioned/active.
- ADR-011 v1.2.0 is accepted as the internal KM 1 technology baseline; cloud provider, region, OIDC vendor, secret manager, artifact-store vendor and spending remain separate decisions.
- KM 1 foundation code and PostgreSQL 16 CI workflow are implemented on a working branch. Local tests report 11 passed and 2 PostgreSQL tests skipped locally; hosted PostgreSQL CI is pending.
- GitHub still reports `main` unprotected. A dry-run/apply operator is included; applying requires a repository Administration: write token supplied locally by an authorized administrator.
- KM 0/KM 1 are not yet closed. KM 2 Registry and later Gateway, Runtime, Evaluation and Synchronization services remain gated.
- No production endpoint, production deployment, real backup/restore, DR exercise, WORM audit store or production security certification is claimed.
