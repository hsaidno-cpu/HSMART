# HSMART Production Readiness Checklist

This is a release gate template. An item is complete only when evidence is linked.

## Architecture and ownership
- [ ] Domain and operational owners assigned.
- [ ] ADRs approved for stack, identity, data, runtime, messaging, deployment.
- [ ] Foundation/operator responsibilities and legal instruments reviewed.
- [ ] Data controller/processor, retention, and residency responsibilities documented.
- [ ] Support escalation and incident ownership established.

## Identity and security
- [ ] OIDC issuer and client configuration reviewed.
- [ ] Audience, issuer, signature, expiry, scopes, and redirect validation tested.
- [ ] API key generation, verifier storage, rotation, revocation, and quotas tested.
- [ ] Workload identity and runtime enrollment tested.
- [ ] Tenant isolation tests pass.
- [ ] SSRF, egress, redirect, DNS rebinding, and connector tests pass.
- [ ] Sandbox boundary and resource-limit tests pass.
- [ ] Secret/dependency scanning, SBOM, provenance, signature verification enabled.
- [ ] No sensitive tokens or payloads in logs.

## Registry and release
- [ ] Canonical manifest validation enforced.
- [ ] Capability IDs and versions are unique and immutable.
- [ ] Artifact digest and signature verified on publish and deploy.
- [ ] Dependency resolution and compatibility tests pass.
- [ ] Quarantine and revocation paths tested.
- [ ] Release approval is evidence-backed and auditable.

## Execution and synchronization
- [ ] Invocation idempotency and duplicate delivery tested.
- [ ] Timeout, cancellation, retry, and dead-letter behavior tested.
- [ ] Desired and observed state reconciled.
- [ ] Canary health thresholds defined.
- [ ] Rollback tested against known-good artifact.
- [ ] Self-hosted runtime cannot access unauthorized Control Plane resources.
- [ ] Runtime disconnect and stale desired-state handling tested.

## Marketplace
- [ ] Publisher verification and ownership claims reviewed.
- [ ] Permission and data-use disclosure visible.
- [ ] License and entitlement checks enforced at invocation.
- [ ] Abuse report, quarantine, takedown, and appeal procedures operational.
- [ ] Billing and payout flows tested where enabled.

## Operations
- [ ] SLOs and alerts defined.
- [ ] Dashboards cover gateway, registry, runtime, sync, queue, and identity.
- [ ] Backup/restore and DR drills completed.
- [ ] Capacity, load, soak, and failure-injection tests passed.
- [ ] Runbooks and on-call escalation available.
- [ ] Vulnerability disclosure and incident response procedures published.
- [ ] Retention, deletion, export, and data residency reviewed.

For each item retain owner, evidence link, date, environment, version, result, and exceptions with approver and expiry. A checkbox without evidence is not acceptance.
