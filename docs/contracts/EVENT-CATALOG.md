# HSMART Event Catalog

Events are integration contracts, not informal log strings. Every event uses event-envelope.schema.json.

## Delivery guarantees
- Assume at-least-once delivery; consumers must be idempotent.
- Use an outbox pattern to avoid losing events between database commit and message publish.
- Preserve event ID, aggregate ID, correlation ID, and causation ID.
- Version event schemas independently.
- Use dead-letter queues and observable retry policies.
- Do not publish credentials or sensitive invocation payloads.

## Core event types

| Event | Producer | Consumers / purpose |
|---|---|---|
| organization.created | Organization | Registry, Marketplace |
| publisher.verified | Organization | Registry, Marketplace, Governance |
| capability.registered | Registry | Search, Studio |
| capability.version.created | Registry | Evaluation, Synchronization |
| release.submitted | Studio/Registry | Evaluation |
| release.validated | Evaluation | Registry, Governance |
| release.approved | Governance | Registry, Synchronization |
| release.published | Registry | Synchronization, Marketplace, Notifications |
| release.quarantined | Governance | Registry, Gateway, Runtime |
| invocation.accepted | Gateway | Runtime, Observability |
| execution.started | Runtime | Observability |
| execution.completed | Runtime | Billing, Observability |
| execution.failed | Runtime | Observability, Reliability |
| runtime.registered | Runtime | Synchronization, Observability |
| runtime.health.changed | Runtime | Synchronization, Operations |
| sync.requested | Synchronization | Runtime |
| sync.completed | Synchronization | Registry, Observability |
| sync.failed | Synchronization | Operations, Observability |
| access.revoked | Access & Identity | Gateway, Runtime, Connector Manager |
| connector.quarantined | Access & Identity | Gateway, Operations |
| listing.published | Marketplace | Discovery |
| entitlement.changed | Marketplace | Access & Identity |

## Payload rules
1. Include only fields needed by consumers.
2. Include stable resource IDs instead of copying full resources.
3. Re-fetch authoritative state when necessary.
4. Include schema version and producer identity.
5. Make handlers safe under duplicate and out-of-order delivery.
6. Guarantee ordering only where explicitly implemented per aggregate.
7. A replay must not repeat irreversible external side effects.

## Example event

    {
      "eventId": "evt_example_001",
      "eventType": "release.published",
      "eventVersion": "1.0",
      "occurredAt": "2026-11-21T12:00:00Z",
      "producer": "registry",
      "organizationId": "org_example",
      "aggregateId": "hsmart:publisher:capability",
      "correlationId": "corr_example",
      "data": {
        "capabilityId": "hsmart:publisher:capability",
        "version": "1.2.0",
        "channel": "stable",
        "artifactDigest": "sha256:..."
      }
    }
