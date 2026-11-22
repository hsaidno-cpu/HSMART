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
| ADR-011 | MVP application stack and infrastructure direction | Recommended baseline; formal acceptance pending team, security, operations, budget and accountable-role evidence |

## Recommended MVP direction

Python 3.12 + FastAPI; PostgreSQL; SQLAlchemy 2.x + Alembic subject to proof-of-fit; PostgreSQL-backed transactional outbox with a separate worker; S3-compatible immutable/versioned artifact storage; external OIDC; managed secret manager/KMS; OCI containers; one-region managed container deployment; OpenTelemetry-compatible observability.

These are recommended defaults for a reversible engineering spike, not an accepted procurement decision or deployed stack. See ADR-011 for conditions and proof-of-fit requirements.

## Open decisions

- Team capability confirmation and backend vertical-slice result.
- Concrete message broker (deferred unless workload evidence requires one).
- OIDC provider and KMS/secret manager.
- Cloud provider and production region.
- Artifact/container signing service.
- Infrastructure-as-code tool after provider selection.
- Public domain, DNS/TLS and network topology.
- Marketplace payment provider and financial/legal model.
- Public/private licensing and trademark policy.
- Initial SLO and support commitments.

Open decisions require a new ADR or explicit amendment. Do not silently overwrite accepted decisions or interpret a recommendation as an approval.
