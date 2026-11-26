"""Allowlisted in-process demo runtime. Uploaded package code is never executed."""
from __future__ import annotations

from typing import Any

from .errors import PilotError


def echo_v1(payload: dict[str, Any]) -> dict[str, Any]:
    message = payload.get("message")
    if not isinstance(message, str):
        raise PilotError("message_must_be_text", 422)
    if len(message) > 4000:
        raise PilotError("message_too_long", 422)
    return {"message": message, "runtime": "hsmart-builtin-v1"}


HANDLERS = {"builtin:hsmart.echo.v1": echo_v1}


def execute(entrypoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    handler = HANDLERS.get(entrypoint)
    if handler is None:
        raise PilotError("entrypoint_not_allowlisted", 403)
    return handler(payload)
