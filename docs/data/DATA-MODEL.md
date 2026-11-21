# HSMART Logical Data Model

This is a logical model, not a production migration or physical schema. Tables, indexes, partitioning, retention, and row-level policies must be designed and tested during implementation.

## Data ownership and storage

| Data | Authoritative domain | Storage guidance |
|---|---|---|
| Users, organizations, memberships | Publisher & Organization / Identity | PostgreSQL |
| Capability IDs, manifests, versions | Registry | PostgreSQL |
| Artifacts, SBOM, provenance, reports | Registry / Artifact Manager | Immutable object storage + digest metadata |
| Grants, scopes, credential metadata | Access & Identity | PostgreSQL |
| Secret material | Vault/KMS | Dedicated secret manager |
| Runtime registration and observed state | Runtime / Synchronization | PostgreSQL |
| Jobs and results | Execution Runtime | PostgreSQL + object storage by size/retention |
| Test runs and evidence | Evaluation | PostgreSQL + object storage |
| Audit events | Observability & Audit | Append-only/tamper-evident store |
| Listings, subscriptions, entitlements | Marketplace & Commerce | PostgreSQL |
| Cache and short-lived coordination | Relevant domain | Redis; never source of truth |

## Core entities

### Organization and identity
- users: user_id, issuer, subject, status, created_at
- organizations: organization_id, slug, status, created_at
- organization_members: organization_id, user_id, role, status
- publishers: publisher_id, organization_id, namespace, verification_status
- tenants: tenant_id, organization_id, environment, status
- service_accounts: service_account_id, organization_id, workload_identity, status

External identity subject is unique within its issuer. Email is not a stable identity key.

### Registry
- capabilities: capability_id, publisher_id, name, kind, visibility, lifecycle_status
- capability_versions: capability_id, version, manifest_digest, release_channel, status, created_at
- capability_artifacts: artifact_id, capability_id, version, digest, media_type, storage_ref, signature_ref
- capability_dependencies: capability_id, version, dependency_id, version_range, optional
- capability_interfaces: capability_id, version, protocol, schema_ref
- capability_permissions: capability_id, version, permission, risk_level
- capability_provenance: capability_id, version, source_ref, commit_ref, build_ref, sbom_ref

The capability_id/version pair is unique. Published artifacts are immutable; a correction requires a new version.

### Runtime and execution
- runtime_instances: runtime_id, organization_id, environment, runtime_version, identity_ref, status
- runtime_deployments: deployment_id, runtime_id, capability_id, desired_version, observed_version, status
- invocations: invocation_id, tenant_id, principal_id, capability_id, resolved_version, request_digest, status, correlation_id
- execution_jobs: execution_id, invocation_id, runtime_id, started_at, completed_at, status
- execution_results: execution_id, result_ref, result_digest, retention_class

Avoid retaining raw prompts or payloads by default. Apply data classification and explicit retention policy.

### Synchronization
- sync_policies: policy_id, owner_id, channel, risk_rules, approval_rules
- desired_states: target_id, capability_id, desired_version, policy_id, updated_at
- observed_states: target_id, capability_id, observed_version, health, observed_at
- sync_operations: sync_id, target_id, capability_id, from_version, to_version, strategy, status
- deployment_rollouts: rollout_id, sync_id, stage, percentage, outcome

Desired and observed state are separate. Reconciliation is idempotent and auditable.

### Access and connectors
- api_credentials: credential_id, owner_id, key_prefix, verifier_hash, scopes, expires_at, revoked_at
- oauth_clients: client_id, owner_id, redirect_uris, grant_types, status
- access_grants: grant_id, principal_id, resource_id, scopes, constraints, expires_at
- identity_policies: policy_id, subject_selector, resource_selector, effect, conditions
- connector_registrations: connector_id, owner_id, protocol, endpoint_ref, status
- secret_references: secret_ref_id, vault_path, owner_id, rotation_state

Secret values are not stored in relational records.

### Evaluation, audit, and marketplace
- test_suites: suite_id, capability_id, version_constraint, suite_version
- evaluation_runs: run_id, capability_id, version, suite_id, result, started_at, completed_at
- evaluation_evidence: evidence_id, run_id, artifact_ref, digest, classification
- risk_assessments: assessment_id, release_id, risk_class, findings, disposition
- release_approvals: approval_id, release_id, approver_id, decision, evidence_ref
- audit_events: event_id, actor, organization_id, action, resource, outcome, occurred_at, correlation_id
- marketplace_listings: listing_id, capability_id, publisher_id, listing_status, license_ref
- subscriptions: subscription_id, tenant_id, listing_id, status, period
- entitlements: entitlement_id, tenant_id, capability_id, scope, valid_from, valid_until
- usage_records: usage_id, tenant_id, invocation_id, meter, quantity, occurred_at

## Relationship rules
- One publisher owns multiple capabilities.
- One capability has multiple immutable versions.
- Each version can have artifacts and dependencies.
- One tenant can hold multiple entitlements.
- An invocation is bound to one authenticated tenant and resolved capability version.
- A runtime can host many deployments subject to policy and quota.
- A synchronization operation reconciles one target/capability desired state.
- Marketplace listing does not itself grant execution rights.

## Data governance

Every entity has owner and retention class. Tenant-scoped queries require verified tenant context. Use foreign keys and uniqueness constraints. Retire without erasing historical evidence where required. Never reuse retired capability IDs. Audit events are append-only; corrections are compensating events. Classify payloads and support applicable deletion/export obligations. Document residency and processor relationships before production.
