# Application foundation tests

These tests validate KM 1 only: FastAPI liveness/readiness, production database guardrails, tenant uniqueness, tenant-scoped outbox idempotency, durable claim/retry/dead-letter behavior, and safe handling of unknown event topics. The dedicated PostgreSQL 16 CI job additionally validates the Alembic migration and a transactional tenant-scoped outbox scenario. They do not implement or accept KM 2 Registry, public Gateway, arbitrary-code Runtime, entitlement commerce, full Evaluation service, or Synchronization Engine.
