# HSMART Security Baseline

This document defines minimum implementation controls. It is not a certification claim.

## Identity and authentication
- Use an OIDC-compatible identity provider.
- Validate issuer, signature, expiry, audience, authorized party, and scopes.
- Use Authorization Code + PKCE for user-facing OAuth clients.
- Use client credentials or workload identity for machine-to-machine access where appropriate.
- Use short-lived access tokens and controlled refresh-token rotation.
- Validate exact redirect URIs.
- Support rapid credential revocation.

## Authorization
- Default deny and least privilege.
- Separate user, publisher, tenant, runtime, operator, and Foundation roles.
- Use resource- and tenant-scoped permissions.
- Distinguish listing visibility from invocation entitlement.
- Reauthorize every privileged tool action.
- Require separation of duties for high-risk release approval.

## API keys
- Generate high-entropy random keys.
- Show plaintext once at creation; store only a verifier/hash suitable for verification.
- Use a public key prefix or ID for identification; never log full keys.
- Support scopes, expiry, rotation, revocation, quotas, and owner binding.
- Do not use API keys as a replacement for workload identity.

## Secrets and encryption
- Store secret material in a managed secret manager/KMS-backed vault.
- Use envelope encryption for stored sensitive material.
- Store references and metadata in application databases, not raw secrets.
- Never place secrets in Git, manifests, artifacts, logs, prompts, telemetry, or URL query strings.
- Rotate keys and document break-glass recovery.

## MCP and protocol security
- Pin and test supported MCP protocol versions.
- Implement authorization according to the applicable MCP security specification.
- Bind access tokens to intended resource/audience.
- Never pass a token issued to HSMART through to an upstream MCP server.
- Validate tool inputs and authorize each tool independently.
- Treat tool output as untrusted data.

## Runtime isolation
- Execute publisher code in isolated environments.
- Run as non-root; drop unnecessary capabilities.
- Apply CPU, memory, disk, process, file-size, and wall-clock limits.
- Restrict filesystem mounts and network egress.
- Use read-only base images/filesystems where practical.
- Separate workloads by trust level.
- Verify artifact signature and digest before deployment and execution.

## Connector outbound security
- Use an egress proxy and destination policy.
- Reject private/reserved destinations by default.
- Validate DNS answers and redirects at connection time.
- Restrict schemes, ports, response sizes, and timeouts.
- Bind upstream credentials only to an approved connector identity.
- Do not permit arbitrary user-controlled URLs to access internal services.

## Supply-chain security
- Protect branches and release workflows.
- Require review and automated checks.
- Pin dependencies and use lockfiles.
- Scan dependencies, source, images, and artifacts.
- Produce SBOM and build provenance.
- Sign releases and verify signatures at consumption time.
- Separate build credentials from deployment credentials.
- Keep production secrets out of untrusted pull-request workflows.

## Logging and audit
- Record privileged actions, release events, access changes, invocation metadata, and deployment outcomes.
- Redact secrets and sensitive payloads.
- Restrict access and retention.
- Use append-only or tamper-evident storage for security audit records.
- Correlate request, execution, tenant, release, and runtime IDs.

## Release blockers
Do not promote if signature verification fails, critical security tests fail, required approval is missing, mandatory permissions are undeclared, or provenance cannot be established.
