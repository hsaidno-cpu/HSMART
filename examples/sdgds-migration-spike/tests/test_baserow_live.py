from __future__ import annotations

import json
import os
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request

import pytest

BASE_URL = os.getenv("BASEROW_BASE_URL", "").rstrip("/")
pytestmark = pytest.mark.skipif(not BASE_URL, reason="BASEROW_BASE_URL not configured")


def request(method: str, path: str, body=None, authorization: str | None = None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if authorization:
        headers["Authorization"] = authorization
    req = urllib.request.Request(
        f"{BASE_URL}{path}", data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = response.read()
            if not payload:
                parsed = None
            else:
                text = payload.decode("utf-8", errors="replace")
                try:
                    parsed = json.loads(text)
                except json.JSONDecodeError:
                    # Health endpoints may return plain text or an empty body.
                    parsed = text
            return response.status, parsed
    except urllib.error.HTTPError as exc:
        payload = exc.read()
        try:
            parsed = json.loads(payload.decode("utf-8")) if payload else None
        except ValueError:
            parsed = payload.decode("utf-8", errors="replace")
        return exc.code, parsed


def wait_for_baserow(timeout_seconds: int = 360):
    deadline = time.time() + timeout_seconds
    last = None
    while time.time() < deadline:
        try:
            status, payload = request("GET", "/api/_health/")
            if status == 200:
                return payload
            last = (status, payload)
        except Exception as exc:  # service boot can take a little while
            last = repr(exc)
        time.sleep(3)
    raise AssertionError(f"Baserow health endpoint did not become ready: {last!r}")


def results_array(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if isinstance(payload.get("results"), list):
            return payload["results"]
        if isinstance(payload.get("data"), list):
            return payload["data"]
    raise AssertionError(f"Unexpected list response: {payload!r}")


def test_baserow_ose_real_api_scoped_database_token_and_row_acl():
    wait_for_baserow()

    suffix = uuid.uuid4().hex[:12]
    email = f"sdgds-ci-{suffix}@example.test"
    password = f"CI-{uuid.uuid4().hex}-{uuid.uuid4().hex}-Aa9!"

    # Create disposable test identity.
    status, created_user = request(
        "POST",
        "/api/user/",
        {"name": "SDGDS CI Synthetic", "email": email, "password": password},
    )
    assert status in (200, 201), f"user registration failed: {status} {created_user!r}"

    # Obtain a short-lived administrative JWT for provisioning test resources.
    status, auth = request(
        "POST",
        "/api/user/token-auth/",
        {"username": email, "password": password},
    )
    assert status == 200 and auth and auth.get("token"), f"JWT login failed: {status} {auth!r}"
    jwt = auth["token"]

    # A newly registered local user is provisioned with a starter workspace.
    status, workspace_response = request("GET", "/api/workspaces/", authorization=f"JWT {jwt}")
    assert status == 200, f"list workspaces failed: {status} {workspace_response!r}"
    workspaces = results_array(workspace_response)
    if workspaces:
        workspace_id = int(workspaces[0]["id"])
    else:
        # API-created users may not receive the frontend's initial workspace.
        status, created_workspace = request(
            "POST",
            "/api/workspaces/",
            {"name": f"SDGDS Synthetic {suffix}"},
            authorization=f"JWT {jwt}",
        )
        assert status == 200 and created_workspace and created_workspace.get("id"), (
            f"create workspace failed: {status} {created_workspace!r}"
        )
        workspace_id = int(created_workspace["id"])

    # Create a real database application and a small synthetic table.
    status, application = request(
        "POST",
        f"/api/applications/workspace/{workspace_id}/",
        {"name": "SDGDS Synthetic Projection", "type": "database", "init_with_data": False},
        authorization=f"JWT {jwt}",
    )
    assert status == 200 and application and application.get("id"), (
        f"create database application failed: {status} {application!r}"
    )
    database_id = int(application["id"])

    status, table = request(
        "POST",
        f"/api/database/tables/database/{database_id}/",
        {
            "name": "Synthetic Terms",
            "data": [["Term"], ["seed-row"]],
            "first_row_header": True,
        },
        authorization=f"JWT {jwt}",
    )
    assert status == 200 and table and table.get("id"), (
        f"create database table failed: {status} {table!r}"
    )
    table_id = int(table["id"])

    # Mint a database token restricted to this one table, and only create/read.
    status, database_token = request(
        "POST",
        "/api/database/tokens/",
        {"name": "SDGDS synthetic one-table token", "workspace": workspace_id},
        authorization=f"JWT {jwt}",
    )
    assert status in (200, 201) and database_token and database_token.get("key"), (
        f"create DB token failed: {status} {database_token!r}"
    )
    token_id = int(database_token["id"])
    token_key = database_token["key"]

    status, updated_token = request(
        "PATCH",
        f"/api/database/tokens/{token_id}/",
        {
            "permissions": {
                "create": [["table", table_id]],
                "read": [["table", table_id]],
                "update": False,
                "delete": False,
            }
        },
        authorization=f"JWT {jwt}",
    )
    assert status == 200, f"set table-scoped token permissions failed: {status} {updated_token!r}"

    status, check = request("GET", "/api/database/tokens/check/", authorization=f"Token {token_key}")
    assert status == 200, f"database token check failed: {status} {check!r}"

    # Prove write/read access against a live Baserow table using only the DB token.
    query = urllib.parse.urlencode({"user_field_names": "true"})
    status, row = request(
        "POST",
        f"/api/database/rows/table/{table_id}/?{query}",
        {"Term": f"HSMART-SYNTHETIC-{suffix}"},
        authorization=f"Token {token_key}",
    )
    assert status == 200 and row and row.get("id"), f"scoped row create failed: {status} {row!r}"
    row_id = int(row["id"])

    status, rows = request(
        "GET",
        f"/api/database/rows/table/{table_id}/?{query}",
        authorization=f"Token {token_key}",
    )
    assert status == 200, f"scoped row read failed: {status} {rows!r}"
    assert any(int(item["id"]) == row_id for item in results_array(rows))

    # The same key must not be allowed to delete a row because delete=False.
    denied_status, denied_body = request(
        "DELETE",
        f"/api/database/rows/table/{table_id}/{row_id}/",
        authorization=f"Token {token_key}",
    )
    assert denied_status in (401, 403), (
        f"database token unexpectedly had delete access: {denied_status} {denied_body!r}"
    )
