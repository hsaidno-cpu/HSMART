# HSMART Glossary

| Term | Meaning |
|---|---|
| Capability | Registerable unit of AI functionality: skill, plugin, agent, tool, workflow, or orchestrator |
| Canonical Manifest | Platform-neutral metadata contract for a capability |
| Capability ID | Stable global identity that does not change with version |
| Release | Immutable, validated version of a capability |
| Artifact | Executable or distributable package associated with a release |
| Publisher | Verified person or organization authorized to publish a capability |
| Tenant | Security and billing boundary for a consumer organization/environment |
| Control Plane | Identity, governance, registry, release, and synchronization control |
| Execution Plane | Runtime workers and isolated task execution |
| Data Plane | Controlled transfer of artifacts and invocation data |
| Desired State | Version/configuration a target is intended to run |
| Observed State | Version/configuration verified as actually running |
| Adaptive Sync | Risk- and policy-aware reconciliation of desired/observed state |
| MCP | Model Context Protocol, an interface for tools and context |
| Adapter | Translation layer for platform-specific protocol or client behavior |
| Workload Identity | Machine identity assigned to a runtime or service |
| Entitlement | Current right for a tenant/principal to invoke a capability |
| Quarantine | State preventing a capability, release, or connector from use pending review |
| Provenance | Evidence of source, build process, and artifact origin |
| SBOM | Software Bill of Materials describing artifact dependencies |
| ADR | Architecture Decision Record documenting decision and consequences |
