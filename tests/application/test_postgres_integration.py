"""Executed by the PostgreSQL CI service after Alembic upgrade head."""
import os
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
