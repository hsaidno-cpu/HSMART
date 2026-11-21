# HSMART Hybrid Runtime Specification

## Runtime modes

### Managed cloud
The HSMART operator provisions and operates isolated worker capacity. HSMART controls deployment, resource quotas, security policy, health checks, and runtime lifecycle.

### Self-hosted
A customer operates the worker in its own infrastructure. The runtime establishes workload identity, registers with the Control Plane, receives signed and scoped desired-state instructions, verifies artifacts, executes approved workloads, and reports observed state.

Both modes implement one canonical runtime contract. Deployment topology may differ; identity, release verification, job lifecycle, telemetry, and authorization semantics remain compatible.

## Runtime responsibilities
- Authenticate as a workload, not a human user.
- Bind runtime identity to organization, environment, and runtime instance.
- Advertise supported runtime version and execution capabilities.
- Receive only authorized deployment intents.
- Verify signatures and artifact digests.
- Execute in an isolated worker/sandbox.
- Apply CPU, memory, process, filesystem, network, and time limits.
- Report job lifecycle and observed artifact/version.
- Support cancellation, health checks, and controlled shutdown.
- Revoke credentials and quarantine on integrity or policy failure.

## Registration lifecycle
enrolling → registered → healthy → degraded → quarantined → revoked.

Enrollment must be short-lived and scoped. Registration does not grant broad Control Plane access.

## Job lifecycle
accepted → queued → running → completed / failed / cancelled / timed_out.

Each job records invocation ID, tenant, capability ID, resolved version, artifact digest, runtime ID, resource usage, timestamps, and outcome.

## Isolation baseline
- Non-root execution and minimal runtime image.
- Drop unnecessary Linux capabilities.
- Read-only filesystem where practical.
- Explicit writable temporary directories.
- CPU, memory, PID, disk, and wall-clock limits.
- Restricted network egress through policy-controlled proxy.
- No host Docker socket or privileged host mounts.
- Per-job or per-trust-level isolation.
- No shared writable workspace between tenants.
- Secure cleanup after job completion.

For untrusted third-party code, evaluate stronger isolation such as microVM or sandbox runtime rather than treating a standard container as a complete security boundary.

## Runtime-to-control-plane protocol
- Runtime initiates outbound authenticated connection.
- Control Plane authenticates workload identity and checks authorization.
- Deployment intent is signed and includes target, release digest, policy revision, expiry, and nonce.
- Runtime acknowledges receipt and reports verified observed state.
- Heartbeats are bounded and contain no secrets or customer payloads.
- Revocation/quarantine prevents future deployment and execution.

## Data handling
Default to not retaining raw input/output payloads. Apply tenant-configured classification, retention, residency, and deletion. Telemetry should use identifiers and digests where possible.

## Runtime acceptance tests
- Invalid or revoked workload identity is rejected.
- Cross-organization runtime access is denied.
- Unsigned, expired, replayed, or digest-mismatched deployment intent is rejected.
- Resource limits and egress policy are enforced.
- Job state is idempotent under duplicate delivery.
- Observed version is verified against artifact digest.
- Quarantine stops new execution.
- Runtime recovers after disconnection without accepting stale or revoked instructions.
