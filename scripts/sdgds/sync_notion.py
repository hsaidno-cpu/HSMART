#!/usr/bin/env python3
"""Idempotent one-way GitHub registry -> Notion SDGDS mirror."""
from __future__ import annotations
import hashlib
import json
import os
import sys
import time
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/glossary/terms.json"
API = "https://api.notion.com/v1"
VERSION = "2025-09-03"
TOKEN = os.getenv("NOTION_API_TOKEN", "").strip()
DATA_SOURCE = os.getenv("NOTION_GLOSSARY_DATA_SOURCE_ID", "").strip()
COMMIT = os.getenv("GITHUB_SHA", "local-uncommitted")
MIN_REQUEST_INTERVAL = 0.36
MAX_ATTEMPTS = 6
LAST_REQUEST_AT = 0.0

def wait_for_rate_limit() -> None:
    global LAST_REQUEST_AT
    now = time.monotonic()
    remaining = MIN_REQUEST_INTERVAL - (now - LAST_REQUEST_AT)
    if LAST_REQUEST_AT and remaining > 0:
        time.sleep(remaining)
    LAST_REQUEST_AT = time.monotonic()

def retry_delay(exc: HTTPError, attempt: int) -> float:
    retry_after = exc.headers.get("Retry-After", "")
    if retry_after:
        try:
            return max(0.0, min(float(retry_after), 60.0))
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(retry_after)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                return max(0.0, min(retry_at.timestamp() - time.time(), 60.0))
            except Exception:
                pass
    return min(2 ** attempt, 30.0)

def call(method: str, path: str, payload: dict | None = None) -> dict:
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    for attempt in range(MAX_ATTEMPTS):
        wait_for_rate_limit()
        request = Request(
            API + path,
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Notion-Version": VERSION,
                "Content-Type": "application/json"
            }
        )
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            retryable = exc.code == 429 or 500 <= exc.code <= 599
            if not retryable or attempt == MAX_ATTEMPTS - 1:
                raise RuntimeError(f"Notion API {method} {path}: HTTP {exc.code}: {detail}") from exc
            delay = retry_delay(exc, attempt)
            print(f"Notion API returned HTTP {exc.code}; retrying in {delay:.1f}s (attempt {attempt + 1}/{MAX_ATTEMPTS}).", file=sys.stderr)
            time.sleep(delay)
        except URLError as exc:
            if attempt == MAX_ATTEMPTS - 1:
                raise RuntimeError(f"Notion API network error after {MAX_ATTEMPTS} attempts: {exc}") from exc
            delay = min(2 ** attempt, 30.0)
            print(f"Notion API network error; retrying in {delay:.1f}s (attempt {attempt + 1}/{MAX_ATTEMPTS}).", file=sys.stderr)
            time.sleep(delay)
    raise RuntimeError("Notion API request exhausted retry attempts")

def rich_text(value) -> dict:
    if isinstance(value, list):
        value = "; ".join(str(x) for x in value)
    value = str(value or "")
    chunks = [value[i:i + 1800] for i in range(0, len(value), 1800)] or [""]
    return {"rich_text": [{"type":"text","text":{"content":chunk}} for chunk in chunks]}

def record_hash(term: dict) -> str:
    raw = json.dumps(term, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def build_properties(term: dict, digest: str) -> dict:
    sources = term.get("sources", [])
    return {
        "Term":{"title":[{"type":"text","text":{"content":term["term"]}}]},
        "Term ID":rich_text(term["term_id"]),
        "Aliases":rich_text(term.get("aliases", [])),
        "Expansion":rich_text(term.get("expansion", "")),
        "Term Type":{"select":{"name":term["term_type"]}},
        "Domain":{"multi_select":[{"name":value} for value in term["domains"]]},
        "Status":{"select":{"name":term["status"]}},
        "Language":{"multi_select":[{"name":value} for value in term.get("language", [])]},
        "Confidence":{"select":{"name":term["confidence"]}},
        "Verification":{"select":{"name":term["verification"]}},
        "Primary Source URL":{"url":sources[0]["url"] if sources else None},
        "Additional Sources":rich_text([source["url"] for source in sources[1:]]),
        "Etymology":rich_text(term.get("etymology")),
        "Terminological Definition":rich_text(term.get("terminological_definition")),
        "General Meaning":rich_text(term.get("general_meaning")),
        "Plain-language Explanation":rich_text(term.get("plain_language_explanation")),
        "Analogy":rich_text(term.get("analogy")),
        "Why This Term":rich_text(term.get("why_this_term")),
        "Operational Context":rich_text(term.get("operational_context")),
        "Usage Examples":rich_text(term.get("usage_examples")),
        "Boundaries / Non-examples":rich_text(term.get("boundaries")),
        "Expert Perspectives":rich_text(term.get("expert_perspectives")),
        "Related Term IDs":rich_text(term.get("related_term_ids", [])),
        "Version":rich_text(term.get("version")),
        "Last Reviewed":{"date":{"start":term.get("last_reviewed")}},
        "Content Hash":rich_text(digest),
        "Last Synced Commit":rich_text(COMMIT)
    }

def get_rich_text(page: dict, name: str) -> str:
    prop = page.get("properties", {}).get(name, {})
    return "".join(item.get("plain_text", "") for item in prop.get("rich_text", []))

def load_existing() -> dict:
    indexed = {}
    cursor = None
    while True:
        body = {"page_size":100}
        if cursor:
            body["start_cursor"] = cursor
        result = call("POST", f"/data_sources/{DATA_SOURCE}/query", body)
        for page in result.get("results", []):
            term_id = get_rich_text(page, "Term ID")
            if term_id:
                indexed[term_id] = page
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
        if not cursor:
            break
    return indexed

def main() -> int:
    if not TOKEN or not DATA_SOURCE:
        print("SDGDS Notion sync SKIPPED: configure NOTION_API_TOKEN and NOTION_GLOSSARY_DATA_SOURCE_ID in repository Actions secrets.")
        return 0
    terms = json.loads(REGISTRY.read_text(encoding="utf-8"))["terms"]
    current = load_existing()
    created = updated = unchanged = 0
    for term in terms:
        existing = current.get(term["term_id"])
        digest = record_hash(term)
        if existing and get_rich_text(existing, "Content Hash") == digest:
            unchanged += 1
            continue
        properties = build_properties(term, digest)
        if existing:
            call("PATCH", f"/pages/{existing['id']}", {"properties":properties})
            updated += 1
        else:
            call("POST", "/pages", {
                "parent":{"type":"data_source_id","data_source_id":DATA_SOURCE},
                "properties":properties
            })
            created += 1
    print(f"SDGDS Notion sync PASS: created={created}, updated={updated}, unchanged={unchanged}, commit={COMMIT[:12]}")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"SDGDS Notion sync FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
