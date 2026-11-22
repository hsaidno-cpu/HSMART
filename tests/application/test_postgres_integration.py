"""Executed by the PostgreSQL CI service after Alembic upgrade head."""
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from hsmart_platform.models import Tenant, OutboxMessage
from hsmart_platform.outbox import enqueue

DATABASE_URL = os.getenv("HSMART_TEST_POSTGRES_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="PostgreSQL integration is executed only in the dedicated CI job")


def test_postgres_engine_and_migrated_schema():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as connection:
        assert connection.dialect.name == "postgresql"
        result = connection.execute(text("SELECT COUNT(*) FROM alembic_version"))
        assert result.scalar_one() == 1
        tables = connection.execute(text("SELECT to_regclass('public.tenants'), to_regclass('public.outbox_messages')")).one()
        assert tables[0] is not None and tables[1] is not None
    engine.dispose()


def test_postgres_tenant_scoped_idempotent_outbox_transaction():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    with Session(engine) as session:
        tenant_a = Tenant(slug="pg-tenant-a", display_name="Postgres Tenant A")
        tenant_b = Tenant(slug="pg-tenant-b", display_name="Postgres Tenant B")
        session.add_all([tenant_a, tenant_b])
        session.flush()
        event_a, created_a = enqueue(session, tenant_id=tenant_a.id, topic="test.registered", aggregate_id="a", payload={"version": 1}, idempotency_key="same-key")
        event_b, created_b = enqueue(session, tenant_id=tenant_b.id, topic="test.registered", aggregate_id="b", payload={"version": 1}, idempotency_key="same-key")
        retry_a, created_retry = enqueue(session, tenant_id=tenant_a.id, topic="test.registered", aggregate_id="a", payload={"version": 1}, idempotency_key="same-key")
        session.commit()
        assert created_a is True and created_b is True and created_retry is False
        assert event_a.id == retry_a.id and event_a.id != event_b.id
        assert session.scalar(select(OutboxMessage).where(OutboxMessage.id == event_a.id)).tenant_id == tenant_a.id
    engine.dispose()


def test_postgres_concurrent_duplicate_enqueue_is_idempotent():
    """Two independent transactions racing on one key converge on one row."""
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=4)
    with Session(engine) as setup:
        tenant = Tenant(slug="pg-concurrent", display_name="Concurrent Tenant")
        setup.add(tenant)
        setup.commit()
        tenant_id = tenant.id

    barrier = Barrier(2)

    def enqueue_from_independent_transaction(_):
        with Session(engine) as session:
            barrier.wait(timeout=10)
            with session.begin():
                message, created = enqueue(
                    session,
                    tenant_id=tenant_id,
                    topic="test.concurrent",
                    aggregate_id="aggregate-race",
                    payload={"value": "same"},
                    idempotency_key="same-concurrent-key",
                )
                return message.id, created

    with ThreadPoolExecutor(max_workers=2) as pool:
        first, second = list(pool.map(enqueue_from_independent_transaction, range(2)))

    assert first[0] == second[0]
    assert sorted([first[1], second[1]]) == [False, True]
    with Session(engine) as verify:
        rows = verify.scalars(
            select(OutboxMessage).where(
                OutboxMessage.tenant_id == tenant_id,
                OutboxMessage.idempotency_key == "same-concurrent-key",
            )
        ).all()
        assert len(rows) == 1
    engine.dispose()
