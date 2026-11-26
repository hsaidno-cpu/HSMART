"""Local first-party MCP host invoked over stdio by an explicitly configured client."""
from __future__ import annotations

import anyio
import json
import os
import sys

import mcp.types as types
from mcp.server import Server, ServerRequestContext
from mcp.server.stdio import stdio_server

from ..database import build_engine, build_session_factory
from ..settings import Settings
from .auth import authenticate_token
from .errors import PilotError
from .service import invoke_capability, list_capabilities


def build_server(settings: Settings | None = None) -> Server:
    config = settings or Settings.from_env()
    config.validate()
    engine = build_engine(config.database_url)
    factory = build_session_factory(engine)

    async def on_list_tools(
        ctx: ServerRequestContext,
        params: types.PaginatedRequestParams | None,
    ) -> types.ListToolsResult:
        return types.ListToolsResult(tools=[
            types.Tool(
                name="hsmart.list_capabilities",
                title="HSMART Capability Discovery",
                description="List capabilities granted to the authenticated tenant principal.",
                input_schema={"type": "object", "properties": {}, "additionalProperties": False},
            ),
            types.Tool(
                name="hsmart.invoke",
                title="HSMART Capability Invocation",
                description="Invoke an installed, rights-cleared and allowlisted HSMART capability.",
                input_schema={
                    "type": "object",
                    "required": ["capability_id", "version", "payload", "idempotency_key"],
                    "properties": {
                        "capability_id": {"type": "string", "minLength": 1, "maxLength": 120},
                        "version": {"type": "string", "minLength": 1, "maxLength": 80},
                        "payload": {"type": "object"},
                        "idempotency_key": {"type": "string", "minLength": 8, "maxLength": 200},
                    },
                    "additionalProperties": False,
                },
            ),
        ])

    async def on_call_tool(
        ctx: ServerRequestContext,
        params: types.CallToolRequestParams,
    ) -> types.CallToolResult:
        try:
            # A short-lived token is held in the MCP client's process environment,
            # never sent as a tool argument or echoed into the transcript.
            token = os.getenv("HSMART_PILOT_ACCESS_TOKEN", "")
            principal = authenticate_token(token, config)
            with factory() as session:
                if params.name == "hsmart.list_capabilities":
                    result = {"items": list_capabilities(session, principal)}
                elif params.name == "hsmart.invoke":
                    arguments = params.arguments or {}
                    result = invoke_capability(
                        session,
                        config,
                        principal,
                        capability_key=str(arguments.get("capability_id", "")),
                        version=str(arguments.get("version", "")),
                        payload=arguments.get("payload") or {},
                        idempotency_key=str(arguments.get("idempotency_key", "")),
                        host_id=config.pilot_host_id,
                    )
                else:
                    raise PilotError("unknown_mcp_tool", 404)
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=json.dumps(result, sort_keys=True))],
            )
        except PilotError as exc:
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=exc.code)],
                is_error=True,
            )

    return Server("hsmart-local-mcp-host", on_list_tools=on_list_tools, on_call_tool=on_call_tool)


async def _run() -> None:
    server = build_server()
    async with stdio_server() as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())


def main() -> None:
    # MCP stdio requires stdout to remain a clean JSON-RPC stream.
    anyio.run(_run)


if __name__ == "__main__":
    main()
