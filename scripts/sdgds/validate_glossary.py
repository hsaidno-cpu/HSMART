#!/usr/bin/env python3
"""Validate the SDGDS canonical terminology registry using Python stdlib only."""
from __future__ import annotations
import json, re, sys, unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/glossary/terms.json"
TERM_TYPES = {"Acronym","Architecture Concept","Technical Term","Governance Term","System Component","Process","Artifact/Schema","Role/Actor"}
STATUSES = {"Canonical","Proposed","Needs Review","Deprecated","Historical"}
CONFIDENCE = {"High","Medium","Low","Unverified"}
VERIFICATION = {"Verified against internal source","Externally verified","Needs review","Unverified"}
LANGUAGES = {"English","Indonesian","Mixed"}
DOMAINS = {
    "Ecosystem & Platform Architecture","Orchestration & Workflow","Registry & Capability",
    "Distribution & Packaging","Runtime & Execution","Identity & Access",
    "Synchronization & Lifecycle","Evaluation & Assurance","Governance & Policy",
    "Data & Contracts","Security & Operations","Documentation & Knowledge","Cross-Ecosystem"
}
REQUIRED = {
    "term_id","slug","term","aliases","term_type","domains","status","language",
    "confidence","verification","etymology","terminological_definition","general_meaning",
    "plain_language_explanation","analogy","why_this_term","operational_context",
    "usage_examples","boundaries","expert_perspectives","related_term_ids","sources",
    "last_reviewed","version"
}
TERM_ID_RE = re.compile(r"^[A-Z][A-Z0-9]+-[0-9]{4,}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

def validate_terms(terms: list[dict]) -> list[str]:
    errors: list[str] = []
    ids: dict[str,str] = {}
    slugs: dict[str,str] = {}
    labels: dict[str,str] = {}

    if not isinstance(terms, list):
        return ["terms must be a list"]

    for i, term in enumerate(terms):
        where = f"terms[{i}]"
        if not isinstance(term, dict):
            errors.append(f"{where}: record must be an object")
            continue

        missing = REQUIRED - set(term)
        if missing:
            errors.append(f"{where}: missing fields: {', '.join(sorted(missing))}")

        tid = term.get("term_id", "")
        label = term.get("term", "")
        slug = term.get("slug", "")

        if not isinstance(tid, str) or not TERM_ID_RE.fullmatch(tid):
            errors.append(f"{where}: invalid term_id {tid!r}")
        elif tid in ids:
            errors.append(f"{where}: duplicate term_id {tid}")
        else:
            ids[tid] = label if isinstance(label, str) else ""

        if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
            errors.append(f"{where}: invalid slug {slug!r}")
        elif slug in slugs:
            errors.append(f"{where}: duplicate slug {slug}")
        else:
            slugs[slug] = label if isinstance(label, str) else ""

        if not isinstance(label, str) or not label.strip():
            errors.append(f"{where}: term must be a non-empty string")
        else:
            for value in [label, *(term.get("aliases", []) if isinstance(term.get("aliases", []), list) else [])]:
                key = norm(value) if isinstance(value, str) else ""
                if not key:
                    continue
                prior = labels.get(key)
                if prior and prior != tid:
                    errors.append(f"{where}: label/alias collision {value!r} between {prior} and {tid}")
                else:
                    labels[key] = tid

        aliases = term.get("aliases", [])
        if not isinstance(aliases, list) or any(not isinstance(x, str) or not x.strip() for x in aliases):
            errors.append(f"{where}: aliases must be a list of non-empty strings")

        if term.get("term_type") not in TERM_TYPES:
            errors.append(f"{where}: invalid term_type")
        if term.get("status") not in STATUSES:
            errors.append(f"{where}: invalid status")
        if term.get("confidence") not in CONFIDENCE:
            errors.append(f"{where}: invalid confidence")
        if term.get("verification") not in VERIFICATION:
            errors.append(f"{where}: invalid verification")

        domains = term.get("domains")
        if not isinstance(domains, list) or not domains or not set(domains) <= DOMAINS:
            errors.append(f"{where}: domains must contain one or more recognized domains")
        languages = term.get("language")
        if not isinstance(languages, list) or not languages or not set(languages) <= LANGUAGES:
            errors.append(f"{where}: language must contain one or more recognized languages")

        for field in ("terminological_definition", "plain_language_explanation", "version"):
            value = term.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{where}: {field} must be a non-empty string")

        reviewed = term.get("last_reviewed")
        try:
            if not isinstance(reviewed, str):
                raise ValueError("not a string")
            date.fromisoformat(reviewed)
        except ValueError:
            errors.append(f"{where}: last_reviewed must be a valid ISO date (YYYY-MM-DD)")

        sources = term.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{where}: no evidence sources")
        else:
            for source_index, src in enumerate(sources):
                if not isinstance(src, dict):
                    errors.append(f"{where}: source[{source_index}] must be an object")
                    continue
                url = src.get("url", "")
                role = src.get("role", "")
                parsed = urlparse(url) if isinstance(url, str) else None
                if (
                    not parsed or parsed.scheme not in {"http", "https"} or not parsed.netloc
                    or any(char.isspace() for char in url) or "](" in url or url.endswith(")")
                ):
                    errors.append(f"{where}: invalid source URL {url!r}")
                if not isinstance(role, str) or not role.strip():
                    errors.append(f"{where}: source[{source_index}] must have a non-empty role")

    known = set(ids)
    for i, term in enumerate(terms):
        if not isinstance(term, dict):
            continue
        relations = term.get("related_term_ids", [])
        if not isinstance(relations, list):
            errors.append(f"terms[{i}]: related_term_ids must be a list")
            continue
        for related in relations:
            if related not in known:
                errors.append(f"terms[{i}]: unresolved related term {related}")

    return errors

def main() -> int:
    try:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"SDGDS registry could not be read: {exc}", file=sys.stderr)
        return 2
    if payload.get("dataset") != "HSMART-SDGDS" or not isinstance(payload.get("terms"), list):
        print("Invalid registry envelope", file=sys.stderr)
        return 2
    errors = validate_terms(payload["terms"])
    if errors:
        print("SDGDS validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"SDGDS validation PASS: {len(payload['terms'])} terms; IDs, aliases, dates, enums, sources and relationships are valid.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
