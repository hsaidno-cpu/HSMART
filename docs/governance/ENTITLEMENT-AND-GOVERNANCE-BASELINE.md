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

## 4. Rights, provenance and entitlement basis

No entitlement model creates publisher rights, a saleable license, ownership, subscription or a legal entity. A valid entitlement must link to an explicit rights instrument and verified publisher/principal authority. The rights record must identify at least:

- The underlying capability and immutable source/artifact version, content digest and publisher.
- The rights holder and evidence that the publisher can grant the requested rights.
- The actual grant: access, use, execution, hosting, distribution, modification, adaptation, sublicensing, resale, commercial use, territory, term, revocability and attribution, as applicable.
- The data categories and processing purpose, controller/processor roles, subprocessor conditions, location, retention/deletion and transfer limitations where personal data is involved.
- The applicable source-code, package, model, dataset, documentation, trademark and third-party service terms. These rights are separate; a source-code license must not be assumed to include trademark, dataset, hosted-execution or sublicense rights.
- Evidence ID, document version/digest, effective date, expiry, governing jurisdiction, limitations, withdrawal/termination conditions and reviewer/disposition.

Missing or conflicting chain-of-title or grant evidence defaults to DENY/HOLD. An API key, manifest declaration, repository visibility, public download, package listing or successful test does not establish commercial rights. The publisher must attest only to rights it actually controls. A tenant entitlement is derived from the verified rights grant and policy; it cannot exceed that grant.

Commercial marketplace rights, payment, publisher terms, privacy duties, tax, IP chain-of-title and external contracts remain gated to later work and qualified legal/tax review.

## 5. Governance and entitlement decision authority

GOV-09 is the AI Functional Delegate responsible for the internal entitlement schema, rights-to-permission mapping, negative test fixtures, expiry/revocation semantics and evidence quality. It may not approve its own policy change, fabricate a publisher grant, decide ownership, create a legal license or accept external terms. GOV-06 challenges security/privacy implications; GOV-11 provides a separate-context review record with correlation limitations; GOV-01 approves internal policy and material risk disposition.

For external publisher, customer, payment or data-processing relationships, an appropriately authorized natural person/entity must approve the external instrument. GOV-08 may prepare research/questions/drafts only. The internal rule that GOV-01 is the only human GOV role does not appoint an AI agent as an external statutory signatory or legal professional.

## 6. Implementation gate

KM 1 establishes application foundations only. Entitlement service implementation follows downstream after KM 1 acceptance and Registry/Gateway contracts. Required tests include missing/expired/revoked grants, scope escape, cross-tenant denial, quota exhaustion, unsupported capability version, publisher-rights evidence gaps and equivalent REST/MCP authorization outcomes.

**Disposition:** internal policy baseline only; entitlement enforcement is not yet operational and no publisher license, external rights grant, payment model, or legally approved commercial model is claimed.
