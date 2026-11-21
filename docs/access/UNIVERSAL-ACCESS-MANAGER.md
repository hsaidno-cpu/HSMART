# HSMART Universal Access Manager

## Purpose

Universal Access Manager (UAM) is the access and connector governance capability inside HSMART Access & Identity (D08). It centralizes credential lifecycle, MCP/API connection authorization, secret references, identity policy, scopes, quotas, and audit.

UAM is a logical module group. The six subskills below are required functional boundaries; they may ship as modules within the initial monolith and do not need six independent services.

## Required subskills

| Subskill | Required responsibilities | Security boundary |
|---|---|---|
| api-key-manager | Generate, validate, rotate, revoke, scope, expire, and meter HSMART API keys | Store only a verifier/hash; show secret once; never log plaintext |
| mcp-access-manager | Authenticate and authorize inbound MCP clients and MCP tool calls | OAuth/OIDC, resource/audience binding, per-tool scopes, no token passthrough |
| custom-mcp-connector | Register, configure, validate, monitor, and revoke outbound MCP connections | Egress policy, SSRF controls, upstream identity, permission review |
| custom-api-connector | Register and operate external REST/HTTP integrations | Destination allowlist, DNS/redirect validation, bounded requests, scoped credentials |
| credential-vault | Store and retrieve secrets through secure vault references, rotate and revoke credentials | KMS/secret-manager integration; no plaintext in registry or logs |
| identity-policy-engine | Resolve principals, tenant scopes, grants, roles, permissions, quotas, and conditional access | Default deny, least privilege, explicit policy evaluation and audit |

## Responsibility boundaries

- UAM does not own capability source code, release artifacts, or marketplace listing content.
- The Registry supplies capability identity and declared permission requirements.
- Marketplace supplies current entitlement state; UAM enforces entitlement at invocation.
- Gateway and Orchestrator must call UAM authorization interfaces and cannot bypass them.
- Runtime receives only the minimum short-lived credentials or secret references needed for a job.
- Connector modules cannot access arbitrary internal networks or metadata endpoints.
- The Credential Vault is an adapter to managed secret infrastructure; it is not a reason to store encryption keys in application tables.

## Core operations

### API key lifecycle
1. Authorize key creation for an owner and tenant.
2. Generate high-entropy random secret material.
3. Return the secret once and store only a verification hash plus non-secret prefix/metadata.
4. Attach scopes, expiration, quota, and environment.
5. Support rotation with controlled overlap and revocation.
6. Record all privileged operations.

### Inbound MCP authorization
1. Identify client and user/service principal.
2. Validate issuer, signature, expiry, audience/resource, and scopes.
3. Resolve organization, tenant, and capability entitlement.
4. Authorize each tool call independently.
5. Apply quota, rate limit, and audit correlation.
6. Reject invalid, stale, over-scoped, or revoked credentials.

### External MCP/API connectors
1. Require an owner and business purpose.
2. Validate protocol, endpoint, host, port, TLS, and declared permissions.
3. Resolve DNS and validate destination IP at connection time.
4. Revalidate redirects and DNS answers to mitigate rebinding.
5. Reject loopback/private/link-local/reserved/cloud metadata ranges by default.
6. Store credentials in the vault and bind them to connector identity.
7. Enforce egress proxy, request timeout, response size, and rate limit.
8. Record connector health and revoke/quarantine on risk.

## Canonical permission scopes

Illustrative scope families:
- capability.read
- capability.invoke
- registry.publish
- registry.manage
- runtime.register
- runtime.deploy
- synchronization.request
- synchronization.approve
- connector.manage
- credential.manage
- marketplace.list
- marketplace.entitlement.read
- audit.read
- organization.admin

Scope names are policy identifiers, not a substitute for resource-level authorization. The same scope may be constrained by organization, tenant, capability, environment, and time.

## Policy evaluation contract

Input:
- authenticated principal and identity issuer;
- organization and tenant context;
- target resource and operation;
- requested scopes;
- current entitlement;
- runtime and environment attributes;
- risk signals and policy revision.

Output:
- allow or deny;
- effective scopes and constraints;
- policy revision;
- reason code safe for caller disclosure;
- audit correlation reference.

The policy engine must fail closed when critical authorization dependencies are unavailable. A policy decision may not grant permissions absent from the caller's authenticated identity or explicit grants.

## Required data records

- API credential ID, owner, prefix, verifier hash, scopes, expiry, revocation, last-used metadata.
- OAuth client ID, owner, redirect URIs, grant types, status.
- Connector ID, owner, protocol, endpoint reference, declared permissions, egress policy, health, quarantine status.
- Secret reference, vault path, owner, rotation status; never raw secret material.
- Policy ID, subject/resource selectors, effect, conditions, version, approval.
- Access grant, principal, resource, scope, constraints, expiry.

## Acceptance criteria

- API keys are never recoverable from stored verifier records.
- Key rotation/revocation takes effect within the documented propagation objective.
- MCP access tokens are audience-bound and not forwarded upstream.
- Cross-tenant and over-scoped requests are denied.
- Connector SSRF tests cover private, loopback, link-local, metadata IPs, redirects, DNS rebinding, and IPv6.
- Secret values never appear in manifest, logs, traces, error messages, or ordinary database records.
- Every privileged operation and policy decision is correlated to audit evidence.
