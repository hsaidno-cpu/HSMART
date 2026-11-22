# HSMART Entitlement and Governance Baseline

**ID:** HSMART-GOV-ENT-001  
**Version:** 1.0.0  
**Status:** INTERNAL POLICY BASELINE — TECHNICAL ENFORCEMENT AND EXTERNAL LEGAL TERMS PENDING  
**Policy owner:** GOV-01; functional steward GOV-09

## 1. Purpose

Separate capability visibility, rights entitlement, authentication, authorization and execution. A Registry listing never grants invocation. A valid identity or API key never grants unrestricted access. A publisher's release never automatically becomes a deployment instruction.

## 2. Required entitlement decision tuple

Every future entitlement decision resolves: principal, tenant/organization, capability ID and immutable version/digest, verified publisher, rights basis and supporting evidence, exact operation, resource/scope, environment, validity period, quota, current policy version, risk class and GOV-01 approval grant where required.

Decisions are ALLOW, DENY or HOLD. Unknown/unverifiable rights default to DENY; material unresolved uncertainty is HOLD. Expired/revoked grants must fail at invocation time.

## 3. Lifecycle and enforcement

Lifecycle: DRAFT → VERIFIED → GRANTED → ACTIVE → RESTRICTED/SUSPENDED → EXPIRED/REVOKED. Every transition records actor, authority, timestamp, target, reason, evidence, policy version and audit event. Reauthorize each operation; enforce tenant boundaries and quotas in the control plane, not merely in prompts.

GOV-09 may propose policy and run entitlement fixtures but cannot approve its own changes, grant itself entitlements or create commercial rights. GOV-06 challenges security/privacy impact. GOV-11 performs separate-context assurance. GOV-01 approves internal policy.

## 4. Rights and external terms

No entitlement model creates publisher rights, a saleable license, ownership, subscription or a legal entity. Commercial marketplace rights, payment, publisher terms, privacy duties, tax, IP chain-of-title and external contracts remain gated to later work and qualified legal/tax review.

## 5. Implementation gate

KM 1 establishes application foundations only. Entitlement service implementation follows downstream after KM 1 acceptance and Registry/Gateway contracts. Required tests include missing/expired/revoked grants, scope escape, cross-tenant denial, quota exhaustion, unsupported capability version, publisher-rights evidence gaps and equivalent REST/MCP authorization outcomes.

**Disposition:** normative internal baseline; no operational entitlement service or legally approved commercial model is claimed.
