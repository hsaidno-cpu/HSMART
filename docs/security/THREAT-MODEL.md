# HSMART Threat Model

- Scope: Control Plane, Execution Plane, Data Plane, clients, publishers, marketplace, connectors, and self-hosted runtimes.
- Method: STRIDE plus supply-chain, multi-tenant, prompt-injection, and connector abuse scenarios.
- Status: Baseline threat model; review before production and after material architecture changes.

## Assets
1. Publisher identity and signing authority.
2. Capability source, immutable artifacts, manifests, SBOM, and provenance.
3. User identity, access tokens, API credentials, and OAuth clients.
4. Tenant data, invocation payloads, and execution outputs.
5. Runtime workloads, host infrastructure, and network egress.
6. Registry, desired/observed state, and deployment instructions.
7. Marketplace listings, licenses, entitlements, and billing records.
8. Audit evidence and encryption keys.

## Trust boundaries
- TB1: External AI clients and SDK consumers.
- TB2: Public gateway and protocol adapters.
- TB3: Authenticated Control Plane services.
- TB4: Execution workers and publisher code.
- TB5: Self-hosted customer environments.
- TB6: Third-party APIs, MCP servers, model providers, and artifact sources.
- TB7: Privileged publisher, operator, and Foundation administration.

## STRIDE register

| ID | Threat | Example | Required controls |
|---|---|---|---|
| TM-001 Spoofing | Impersonated publisher/runtime | Stolen token | OIDC, workload identity, verified publisher, rotation |
| TM-002 Tampering | Artifact changed after release | Replaced package | Digest, signature, immutable object version |
| TM-003 Repudiation | Actor denies release/change | Untracked admin action | Append-only audit, correlation, signed approval |
| TM-004 Disclosure | Secret or tenant data leaks | Token in log | Vault/KMS, redaction, tenant-scoped access |
| TM-005 DoS | Invocation flood/costly task | Recursive agent call | Rate limits, quotas, concurrency caps, timeouts |
| TM-006 Elevation | Skill gains host/admin access | Container escape | Sandbox, least privilege, default-deny |
| TM-007 SSRF | Connector reaches internal services | Cloud metadata endpoint | Egress proxy, IP/port and DNS/redirect validation |
| TM-008 Supply chain | Malicious dependency/build | Typosquatted package | Lockfiles, SBOM, scanning, provenance, signatures |
| TM-009 Prompt injection | Content manipulates tool use | Exfiltration instruction | Treat content as data, scoped tools, human approval |
| TM-010 Cross-tenant access | Tenant reads another tenant | Missing tenant filter | Tenant-scoped authorization, isolation tests |
| TM-011 Replay | Old request is replayed | Duplicate side effect | Expiry, nonce where relevant, idempotency |
| TM-012 Runtime compromise | Self-hosted node compromised | Stolen workload identity | Per-runtime identity, short-lived credentials, quarantine |
| TM-013 Marketplace abuse | Deceptive/malicious listing | Hidden permission | Publisher verification, disclosure, review, takedown |
| TM-014 Desynchronization | Partial or stale rollout | Version drift | Reconciliation, pinning, staged rollout, rollback |
| TM-015 Insider abuse | Operator misuses access | Unapproved release | Separation of duties, JIT access, audit |

## High-risk scenarios

### Malicious publisher
Verify identity and ownership; require signed release metadata, immutable artifact digest, provenance, SBOM where required, dependency/artifact scanning, permission disclosure, sandbox evaluation, human review for high-impact capabilities, quarantine, revocation, consumer notification, and appeal.

### SSRF through custom connectors
- Resolve and validate destination IP at connection time, not only at registration.
- Reject loopback, link-local, private, multicast, reserved, and cloud metadata ranges by default unless narrowly approved.
- Revalidate every redirect and DNS resolution; defend against DNS rebinding.
- Enforce host, port, protocol, response-size, timeout, and egress policies.
- Route outbound calls through a controlled egress proxy.
- Never forward inbound bearer tokens to upstream services.
- Inject upstream credentials only into isolated connector execution contexts.

### Prompt injection and agent misuse
Separate trusted policy from untrusted output/retrieved content. Treat model-generated plans as proposals. Authorize every tool invocation independently. Agents must not mint credentials, change their own scopes, approve releases, disable audit, or override quarantine. Require human approval for destructive, financial, external communication, data export, or privilege-changing actions according to tenant policy.

### Cross-tenant leakage
Derive tenant context from authenticated principal and verified grants, not an untrusted request field. Apply tenant scoping to every query and object access. Test APIs, search, cache, artifact storage, logs, and async workers.

## Severity response

| Severity | Default response |
|---|---|
| Critical | Contain; revoke/quarantine; block release/deployment |
| High | Stop rollout; investigate; require security approval |
| Medium | Restrict exposure; mitigate with deadline |
| Low | Remediate in planned maintenance |

No risk score can waive cryptographic verification, authentication, authorization, or isolation controls.

## Residual risks

Sandbox escapes remain a platform risk; use defense in depth and stronger isolation for high-risk workloads. A self-hosted customer controls its own host; HSMART cannot prove it is uncompromised. External clients may cache tools. Third-party model providers process data under their own terms, requiring data classification and contractual review.

Review before public marketplace launch, arbitrary third-party code execution, after incidents, and after changes to IAM, runtime, connectors, or synchronization.
