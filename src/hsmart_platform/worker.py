"""Restartable allowlisted worker; unhandled events are never silently acknowledged."""
from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from collections.abc import Callable
from sqlalchemy.orm import Session

from .database import build_engine, build_session_factory
from .models import OutboxMessage
from .outbox import claim_one, mark_failed, mark_processed
from .settings import Settings

logger = logging.getLogger("hsmart.worker")
EventHandler = Callable[[OutboxMessage], None]


def run_once(session: Session, handlers: dict[str, EventHandler] | None = None) -> bool:
    """Process one event using an explicit topic allowlist. Return False when idle."""
    message = claim_one(session)
    if message is None:
        session.rollback()
        return False

    message_id = message.id
    topic = message.topic
    handler = (handlers or {}).get(topic)
    if handler is None:
        # Do not mark a message processed when no business handler exists yet.
        mark_failed(session, message, "no_handler_registered")
        session.commit()
        logger.warning("outbox event deferred: no handler registered", extra={"message_id": message.id})
        return True

    try:
        handler(message)
    except Exception as exc:  # noqa: BLE001 - worker boundary records safe error class only
        # A handler may fail after a database error has invalidated the current
        # transaction. Roll back the claim, reload the durable row and record
        # the failed attempt in a fresh transaction. If storage itself is down,
        # leave the claim rolled back so the message remains retryable.
        session.rollback()
        try:
            failed_message = session.get(OutboxMessage, message_id)
            if failed_message is None:
                logger.error("outbox event disappeared during handler failure", extra={"message_id": message_id})
                return True
            failed_message.status = "processing"
            failed_message.attempts += 1
            failed_message.available_at = datetime.now(timezone.utc)
            mark_failed(session, failed_message, f"handler_failed:{type(exc).__name__}")
            session.commit()
        except Exception:
            session.rollback()
            logger.exception("could not persist outbox handler failure", extra={"message_id": message_id})
            return True
        logger.exception("outbox handler failed", extra={"message_id": message_id, "topic": topic})
        return True

    mark_processed(session, message)
    session.commit()
    logger.info("outbox event processed", extra={"message_id": message_id, "topic": topic})
    return True


def main() -> None:
    settings = Settings.from_env()
    settings.validate()
    engine = build_engine(settings.database_url)
    factory = build_session_factory(engine)
    # KM 1 intentionally registers no business handlers. KM 2+ adds domain
    # handlers explicitly; unknown topics remain pending/retryable and are never dropped.
    handlers: dict[str, EventHandler] = {}
    while True:
        with factory() as session:
            worked = run_once(session, handlers)
        if not worked:
            time.sleep(1)


if __name__ == "__main__":
    main()
