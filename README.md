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
| docs/foundation/ | Project Charter, decision rights, scope, success measures, and adoption record |
| docs/architecture/ | Master architecture, domains, ADRs, ecosystem integration, repository blueprint |
| docs/access/ | Universal Access Manager and its six required subskills |
| docs/security/ | Threat model and security baseline |
| docs/data/ | Logical data model and governance |
| docs/contracts/ | JSON Schema, OpenAPI, event contracts |
| docs/synchronization/ | Adaptive synchronization policy |
| docs/runtime/ | Hybrid runtime and execution contracts |
| docs/governance/ | Ownership, publisher, marketplace governance |
| docs/roadmap/ | Implementation phases and acceptance criteria |
| docs/operations/ | Production-readiness and operations |

## First implementation milestone

Prove one complete vertical slice: register a capability; validate publisher identity, manifest, digest and signature; publish an immutable version; discover and invoke it through MCP and REST; execute it in a constrained cloud runtime; propagate a compatible release; and demonstrate authorization denial, audit evidence, failure handling and rollback.

A successful HTTP response alone is not acceptance evidence.

## Status and non-goals

- Current status: **Architecture and project governance baselines / implementation not yet established**.
- No production endpoint, cloud account, database, OAuth issuer, marketplace payment provider, or runtime is claimed to exist.
- The baseline does not require microservices, Kubernetes, multi-region deployment, or autonomous code modification in the MVP.
- External clients may need adapter refresh or reconnection for changed tool manifests. HSMART cannot force an independently managed client to refresh.

## Contributing

See CONTRIBUTING.md. Normative architecture or contract changes require an ADR, validation evidence, and compatibility assessment. Project scope and governance changes must follow the Project Charter.

## License

The repository currently contains an Apache License 2.0 file. Review licensing and ownership policy for each separately distributed artifact, marketplace listing, trademark, and third-party contribution before commercial release.
