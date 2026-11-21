# ADR-005: Support Managed and Self-Hosted Runtimes

- Status: Accepted baseline
- Date: 2026-11-21

## Context
Managed cloud provides simplicity; self-hosted execution supports customer-controlled data, network, and operations.

## Decision
Support both modes through one runtime registration, deployment, job, artifact-verification, and telemetry contract.

## Consequences
- Use workload identity and scoped enrollment.
- Self-hosted runtime receives only authorized signed deployment intents.
- Customer-controlled hosts cannot be guaranteed uncompromised by HSMART.
- Feature parity may vary by runtime version and declared capabilities.
