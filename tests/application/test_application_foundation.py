from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hsmart_platform.app import create_app
from hsmart_platform.database import Base
from hsmart_platform.models import Tenant, OutboxMessage
from hsmart_platform.outbox import enqueue, claim_one, mark_processed, mark_failed
from hsmart_platform.settings import Settings


def make_db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=__import__("sqlalchemy").pool.StaticPool)
    Base.metadata.create_all(engine)
    return engine


def test_health_and_database_readiness():
    engine = make_db()
    app = create_app(Settings(environment="test", database_url="sqlite://"), engine)
    with TestClient(app) as client:
        assert client.get("/v1/health").json()["status"] == "ok"
        assert client.get("/v1/ready").json() == {"status": "ready", "database": "reachable"}


def test_production_refuses_sqlite():
    settings = Settings(environment="production", database_url="sqlite:///unsafe.db")
    try:
        settings.validate()
    except ValueError as exc:
        assert "requires PostgreSQL" in str(exc)
    else:
        raise AssertionError("SQLite must not be accepted as a production database")


def test_tenant_slug_is_unique():
    engine = make_db()
    with Session(engine) as session:
        session.add(Tenant(slug="acme", display_name="Acme"))
        session.commit()
        session.add(Tenant(slug="acme", display_name="Duplicate"))
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
        else:
            raise AssertionError("duplicate tenant slug was accepted")


def test_outbox_idempotency_and_worker_claim():
    engine = make_db()
    with Session(engine) as session:
        tenant = Tenant(slug="northwind", display_name="Northwind")
        session.add(tenant)
        session.flush()
        event, created = enqueue(session, tenant_id=tenant.id, topic="capability.registered", aggregate_id="cap-1", payload={"v": 1}, idempotency_key="evt-1")
        session.commit()
        assert created is True
        duplicate, created = enqueue(session, tenant_id=tenant.id, topic="capability.registered", aggregate_id="cap-1", payload={"v": 1}, idempotency_key="evt-1")
        assert created is False
        assert duplicate.id == event.id
        claimed = claim_one(session, now=datetime.now(timezone.utc))
        assert claimed is not None and claimed.status == "processing" and claimed.attempts == 1
        mark_processed(session, claimed)
        session.commit()
        stored = session.scalar(select(OutboxMessage).where(OutboxMessage.id == event.id))
        assert stored.status == "processed"


def test_outbox_failed_message_retries_then_dead_letters():
    engine = make_db()
    with Session(engine) as session:
        tenant = Tenant(slug="retry", display_name="Retry")
        session.add(tenant)
        session.flush()
        message, _ = enqueue(session, tenant_id=tenant.id, topic="test.failure", aggregate_id="a-1", payload={}, idempotency_key="retry-1")
        session.flush()
        message.attempts = 5
        mark_failed(session, message, "permanent error")
        session.commit()
        assert message.status == "dead_letter"


def test_outbox_idempotency_is_scoped_to_tenant():
    engine = make_db()
    with Session(engine) as session:
        first_tenant = Tenant(slug="tenant-one", display_name="Tenant One")
        second_tenant = Tenant(slug="tenant-two", display_name="Tenant Two")
        session.add_all([first_tenant, second_tenant])
        session.flush()
        first, created_first = enqueue(session, tenant_id=first_tenant.id, topic="test.event", aggregate_id="a", payload={}, idempotency_key="same-key")
        second, created_second = enqueue(session, tenant_id=second_tenant.id, topic="test.event", aggregate_id="b", payload={}, idempotency_key="same-key")
        duplicate, created_duplicate = enqueue(session, tenant_id=first_tenant.id, topic="test.event", aggregate_id="a", payload={}, idempotency_key="same-key")
        session.commit()
        assert created_first is True and created_second is True
        assert created_duplicate is False
        assert first.id == duplicate.id and second.id != first.id


def test_worker_does_not_acknowledge_event_without_handler():
    from hsmart_platform.worker import run_once
    engine = make_db()
    with Session(engine) as session:
        tenant = Tenant(slug="worker-tenant", display_name="Worker Tenant")
        session.add(tenant)
        session.flush()
        message, _ = enqueue(session, tenant_id=tenant.id, topic="unhandled.topic", aggregate_id="a", payload={}, idempotency_key="worker-1")
        session.commit()
        assert run_once(session, handlers={}) is True
        stored = session.scalar(select(OutboxMessage).where(OutboxMessage.id == message.id))
        assert stored.status == "pending"
        assert stored.attempts == 1



def test_worker_handler_database_error_is_rolled_back_and_retried():
    from hsmart_platform.worker import run_once

    engine = make_db()
    with Session(engine) as session:
        tenant = Tenant(slug="worker-failure", display_name="Worker Failure")
        session.add(tenant)
        session.flush()
        message, _ = enqueue(
            session,
            tenant_id=tenant.id,
            topic="test.database_failure",
            aggregate_id="aggregate-1",
            payload={},
            idempotency_key="database-failure-1",
        )
        session.commit()
        message_id = message.id

        def failing_handler(_message):
            session.add(Tenant(slug="worker-failure", display_name="Duplicate tenant"))
            session.flush()  # UNIQUE violation invalidates the transaction.

        assert run_once(session, handlers={"test.database_failure": failing_handler}) is True
        stored = session.get(OutboxMessage, message_id)
        assert stored is not None
        assert stored.status == "pending"
        assert stored.attempts == 1
        assert stored.last_error == "handler_failed:IntegrityError"
    engine.dispose()
