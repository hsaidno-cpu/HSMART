"""Durable outbox primitives; dispatch policy is deliberately kept out of API handlers."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import OutboxMessage


def enqueue(
    session: Session,
    *,
    tenant_id: str,
    topic: str,
    aggregate_id: str,
    payload: dict,
    idempotency_key: str,
) -> tuple[OutboxMessage, bool]:
    existing = session.scalar(
        select(OutboxMessage).where(
            OutboxMessage.tenant_id == tenant_id,
            OutboxMessage.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        return existing, False
    message = OutboxMessage(
        tenant_id=tenant_id,
        topic=topic,
        aggregate_id=aggregate_id,
        payload=payload,
        idempotency_key=idempotency_key,
        status="pending",
    )
    try:
        # A savepoint preserves the caller's outer transaction if another
        # transaction wins the same tenant/idempotency-key race.
        with session.begin_nested():
            session.add(message)
            session.flush()
    except IntegrityError:
        existing = session.scalar(
            select(OutboxMessage).where(
                OutboxMessage.tenant_id == tenant_id,
                OutboxMessage.idempotency_key == idempotency_key,
            )
        )
        if existing is None:
            raise
        return existing, False
    return message, True


def claim_one(session: Session, *, now: datetime | None = None, stale_after_seconds: int = 300) -> OutboxMessage | None:
    """Claim one pending or stale message; PostgreSQL uses SKIP LOCKED under concurrency."""
    now = now or datetime.now(timezone.utc)
    stale = now - timedelta(seconds=stale_after_seconds)
    statement = (
        select(OutboxMessage)
        .where(
            or_(
                (OutboxMessage.status == "pending") & (OutboxMessage.available_at <= now),
                (OutboxMessage.status == "processing") & (OutboxMessage.available_at <= stale),
            )
        )
        .order_by(OutboxMessage.created_at, OutboxMessage.id)
        .limit(1)
        .with_for_update(skip_locked=True)
    )
    message = session.scalar(statement)
    if message is None:
        return None
    message.status = "processing"
    message.attempts += 1
    message.available_at = now
    session.flush()
    return message


def mark_processed(session: Session, message: OutboxMessage, *, now: datetime | None = None) -> None:
    message.status = "processed"
    message.processed_at = now or datetime.now(timezone.utc)
    message.last_error = None
    session.flush()


def mark_failed(
    session: Session,
    message: OutboxMessage,
    error: str,
    *,
    now: datetime | None = None,
    max_attempts: int = 5,
) -> None:
    now = now or datetime.now(timezone.utc)
    message.last_error = error[:2000]
    if message.attempts >= max_attempts:
        message.status = "dead_letter"
    else:
        message.status = "pending"
        message.available_at = now + timedelta(seconds=min(2 ** message.attempts, 300))
    session.flush()
