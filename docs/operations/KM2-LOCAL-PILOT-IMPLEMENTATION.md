# HSMART KM2 Local Registry, Signed Installer and MCP Host Pilot

**Implementation status:** feature branch, awaiting CI and review.
**Pilot scope:** one first-party capability, one tenant, one local host, one explicit publisher trust policy.
**Not claimed:** public-cloud deployment, marketplace, production OIDC provisioning, arbitrary package-code execution, production WORM, production DR or commercial distribution of third-party plugins.

## 1. Architecture of the first working slice

1. A publisher builds a deterministic tar.gz release from a canonical source tree and immutable 40-character Git commit SHA.
2. The builder signs canonical release metadata using Ed25519 and records SHA-256 for every package file.
3. The installer verifies package size, archive paths, no symlinks, file digests, signature, signer fingerprint, publisher identity, source repository and source commit allowlist, capability allowlist, license allowlist, rights evidence and byte-identical LICENSE file.
4. The installer copies the verified package into a SHA-256 content-addressed local artifact store and registers its immutable capability version.
5. A tenant/subject entitlement and an ACTIVE installation on the named host are both mandatory before invocation.
6. REST and MCP stdio use the same invocation service, idempotency checks and audit trail.
7. The local demo runtime accepts only the built-in entrypoint builtin:hsmart.echo.v1. Package files are not imported or executed.

## 2. Bootstrap a local PostgreSQL and API environment

Copy .env.example to .env and set a strong local-only POSTGRES_PASSWORD. Do not commit .env.

Install Python dependencies in a dedicated virtual environment using requirements-app.txt and requirements-dev.txt, then start Docker Compose:

    docker compose up --build -d
    docker compose run --rm migrate

API health:

    curl http://127.0.0.1:8000/v1/health
    curl http://127.0.0.1:8000/v1/ready

Only loopback ports are published by the default compose file. The MCP service is a stdio process behind the optional mcp profile and has no TCP listener.

## 3. Create a local/test OIDC signing key

These keys are for local testing only. Production requires an externally operated OIDC issuer, an HTTPS JWKS endpoint, issuer and audience validation, and managed secret/key rotation.

    PYTHONPATH=src python tools/hsmart_pilot_admin.py oidc-test-keygen --output-dir .local/keys

The public key is mounted read-only into local containers. The private key must remain outside Git and outside any package artifact. Issue short-lived test tokens only when required by the local operator.

## 4. Create a package-signing key and trust policy

Create a separate Ed25519 package-signing key pair:

    PYTHONPATH=src python tools/hsmart_package.py keygen --output-dir .local/package-keys

Copy config/pilot-publisher-trust.example.json to config/pilot-publisher-trust.local.json. Replace the signer SHA-256 with the exact public_key_sha256 printed by keygen. Replace the source commit placeholder with the reviewed full source commit being packaged. Do not broaden the publisher, capability or license lists for convenience.

The example trust policy is an intentionally unusable template until the operator pins the actual signer fingerprint and exact source commit. It permits only:

- publisher hsmart-first-party
- capability hsmart.echo
- source repository https://github.com/hsaidno-cpu/HSMART
- license Apache-2.0 with the repository LICENSE as the exact license evidence
- one explicitly approved immutable source commit. The installer rejects a package whose source SHA is not in allowed_source_commits.

Other Plugin Creator packages, including USER/PRIVATE packages, are not authorized by this policy and cannot be installed with it.

## 5. Build and verify the signed demonstration package

Use the full SHA of the reviewed commit that contains the manifest, package payload and built-in handler:

    PYTHONPATH=src python tools/hsmart_package.py build --private-key .local/package-keys/package-signing-private.pem --signer-key-id hsmart-dev-ed25519-1 --source-commit FULL_40_CHARACTER_SHA --license-file LICENSE --output dist/hsmart-echo-0.1.0.tar.gz

Then verify against the public key and explicit trust policy:

    PYTHONPATH=src python tools/hsmart_package.py verify --bundle dist/hsmart-echo-0.1.0.tar.gz --public-key .local/package-keys/package-signing-public.pem --trust-policy config/pilot-publisher-trust.local.json

The package includes LICENSE, README and input.schema.json, but no executable plugin source. The only executable behavior is the reviewed HSMART built-in handler in the platform.

## 6. Tenant, install, entitlement and activation

Load local environment variables into the shell (or configure equivalent environment variables in PowerShell):

    set -a; . ./.env; set +a

Create the local tenant and record the returned UUID:

    PYTHONPATH=src python tools/hsmart_pilot_admin.py seed-tenant --slug hsmart-local --display-name 'HSMART Local Pilot'

Install the package after signing and trust checks pass:

    PYTHONPATH=src python tools/hsmart_package.py install --bundle dist/hsmart-echo-0.1.0.tar.gz --public-key .local/package-keys/package-signing-public.pem --trust-policy config/pilot-publisher-trust.local.json --tenant-id TENANT_UUID --host-id hsmart-local-mcp-host-v1 --installer-subject local-publisher

Record the returned installation ID. Activate it:

    PYTHONPATH=src python tools/hsmart_package.py transition --installation-id INSTALLATION_UUID --state ACTIVE --actor local-operator

Grant invocation permission with an evidence reference:

    PYTHONPATH=src python tools/hsmart_pilot_admin.py grant --tenant-id TENANT_UUID --capability-id hsmart.echo --subject pilot-user --permission capability.invoke --evidence-ref local-approval-ticket

The grant CLI writes an audit event. The REST endpoint POST /v1/registry/grants requires scope entitlement.grant. Grant revocation uses POST /v1/registry/grants/{grant_id}/revoke and records the evidence reference. A revoked entitlement is checked before idempotent invocation replay, so stored results are not returned after access has been withdrawn.

## 7. Obtain a short-lived local token and launch the MCP stdio host

Mint a short-lived token with tenant_id, issuer, audience and only the required scopes:

    PYTHONPATH=src python tools/hsmart_pilot_admin.py mint-test-token --private-key .local/keys/oidc-test-private.pem --issuer https://issuer.hsmart.test --audience hsmart-api --subject pilot-user --tenant-id TENANT_UUID --scope capability.read capability.invoke

Set the returned token in HSMART_PILOT_ACCESS_TOKEN in the local process environment. Never place tokens in the source tree, command history, PR body, Notion or audit payloads.

Launch the MCP stdio host:

    PYTHONPATH=src python -m hsmart_platform.pilot.mcp_pilot

An MCP-compatible client starts this command as a child process and communicates over stdin/stdout. It exposes:

- hsmart.list_capabilities
- hsmart.invoke

The host validates the token and calls the same service used by REST. It does not accept tenant_id from tool arguments.

## 8. Installer lifecycle

Supported transitions:

- INSTALLED → ACTIVE, REVOKED or UNINSTALLED
- ACTIVE → DISABLED, REVOKED or UNINSTALLED
- DISABLED → ACTIVE, REVOKED or UNINSTALLED
- UNINSTALLED is terminal for that installation record, but the same immutable release can be installed again after signature/trust/rights re-verification. REVOKED is terminal for both the installation and the capability version; all installations of that version are moved to REVOKED.

Revoking a release marks all installations of that capability version REVOKED. A revoked release cannot be reinstalled or activated. Content-addressed artifacts are retained for provenance and are not deleted when a single installation is uninstalled.

## 9. Security boundaries and production gaps

Implemented in the pilot:
- issuer/audience/time/signature JWT verification and asymmetric algorithm allowlist
- explicit tenant/subject scopes and persisted capability grants with expiry/revocation
- immutable package metadata, Ed25519 release signing, signer key fingerprint pinning and file SHA-256
- publisher/source/capability/license/rights allowlists and exact LICENSE-file check
- explicit host activation and idempotency
- per-tenant hash-linked audit records with testable chain verification
- actual MCP stdio client/server integration test

Not yet production-ready:
- a managed OIDC issuer, production clients, workload identity and automatic JWKS key rotation
- KMS/HSM-backed signer custody and rotation; the local PEM key is only a dev/test mechanism
- a policy service/network enforcement point and independent tenant isolation review
- durable object storage with retention/object lock; local file storage is not WORM
- external immutable audit sink, OpenTelemetry metrics/traces, alert routing and SLOs
- hosted container environment, public DNS/TLS, budget, backup/restore and DR test
- malware scanning, SBOM, build attestation and security review before accepting external publisher artifacts

Production promotion remains fail-closed until those gates are separately evidenced and accepted by GOV-01.