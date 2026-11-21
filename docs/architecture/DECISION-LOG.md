# HSMART Architecture Decision Log

| ADR | Decision | Status |
|---|---|---|
| ADR-001 | Modular monolith first; extract services by evidence | Accepted baseline |
| ADR-002 | Logical separation of Control, Execution, and Data Planes | Accepted baseline |
| ADR-003 | Canonical Universal Capability Manifest | Accepted baseline |
| ADR-004 | MCP-native with REST/SDK interoperability | Accepted baseline |
| ADR-005 | Hybrid managed-cloud and self-hosted runtime | Accepted baseline |
| ADR-006 | Risk-adaptive desired/observed-state synchronization | Accepted baseline |
| ADR-007 | Zero Trust and workload identity | Accepted baseline |
| ADR-008 | Tenant isolation and domain-owned data | Accepted baseline |
| ADR-009 | Governed multi-publisher marketplace | Accepted baseline |
| ADR-010 | Immutable release artifacts and provenance | Accepted baseline |

## Open decisions

- Backend language and framework.
- Concrete message broker.
- OIDC provider and KMS/secret manager.
- Cloud provider and production region.
- Artifact/container signing service.
- Marketplace payment provider and financial/legal model.
- Public/private licensing and trademark policy.
- Initial SLO and support commitments.

Open decisions require a new ADR or explicit amendment. Do not silently overwrite accepted decisions.
