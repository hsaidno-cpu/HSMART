# ADR-002: Separate Control, Execution, and Data Planes

- Status: Accepted baseline
- Date: 2026-11-21

## Context
HSMART manages untrusted third-party capabilities while maintaining central identity, release, and policy governance. Running publisher code inside privileged control services creates a trust collision.

## Decision
Define three logical planes: Control Plane for identity, registry, policy, lifecycle, release, and synchronization; Execution Plane for workers, sandbox, jobs, and results; Data Plane for controlled artifact and request/response transfer.

They may share deployment infrastructure in the MVP, but must preserve separate permissions, network paths, and data ownership.

## Consequences
- Runtime cannot mutate registry or release state.
- Control services do not execute publisher code.
- Data movement is governed and observable.
- Deployment can evolve independently.
