#!/usr/bin/env python3
"""Validate the SDGDS canonical terminology registry using Python stdlib only."""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"docs/glossary/terms.json"
TERM_TYPES={"Acronym","Architecture Concept","Technical Term","Governance Term","System Component","Process","Artifact/Schema","Role/Actor"}
STATUSES={"Canonical","Proposed","Needs Review","Deprecated","Historical"}
CONFIDENCE={"High","Medium","Low","Unverified"}
VERIFICATION={"Verified against internal source","Externally verified","Needs review","Unverified"}
LANGUAGES={"English","Indonesian","Mixed"}
DOMAINS={"Ecosystem & Platform Architecture","Orchestration & Workflow","Registry & Capability","Distribution & Packaging","Runtime & Execution","Identity & Access","Synchronization & Lifecycle","Evaluation & Assurance","Governance & Policy","Data & Contracts","Security & Operations","Documentation & Knowledge","Cross-Ecosystem"}
REQUIRED={"term_id","slug","term","aliases","term_type","domains","status","language","confidence","verification","etymology","terminological_definition","general_meaning","plain_language_explanation","analogy","why_this_term","operational_context","usage_examples","boundaries","expert_perspectives","related_term_ids","sources","last_reviewed","version"}

def norm(value: str)->str:
    value=unicodedata.normalize("NFKD",value).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+"," ",value).strip()

def validate_terms(terms: list[dict])->list[str]:
    errors,ids,slugs,labels=[],{},{},{}
    for i,term in enumerate(terms):
        where=f"terms[{i}]"
        missing=REQUIRED-set(term)
        if missing: errors.append(f"{where}: missing fields: {', '.join(sorted(missing))}")
        tid,label,slug=term.get("term_id",""),term.get("term",""),term.get("slug","")
        if not tid: errors.append(f"{where}: empty term_id")
        elif tid in ids: errors.append(f"{where}: duplicate term_id {tid}")
        else: ids[tid]=label
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",slug or ""): errors.append(f"{where}: invalid slug {slug!r}")
        elif slug in slugs: errors.append(f"{where}: duplicate slug {slug}")
        else: slugs[slug]=label
        for value in [label,*term.get("aliases",[])]:
            key=norm(value)
            if not key: continue
            prior=labels.get(key)
            if prior and prior!=tid: errors.append(f"{where}: label/alias collision {value!r} between {prior} and {tid}")
            else: labels[key]=tid
        if term.get("term_type") not in TERM_TYPES: errors.append(f"{where}: invalid term_type")
        if term.get("status") not in STATUSES: errors.append(f"{where}: invalid status")
        if term.get("confidence") not in CONFIDENCE: errors.append(f"{where}: invalid confidence")
        if term.get("verification") not in VERIFICATION: errors.append(f"{where}: invalid verification")
        if not set(term.get("domains",[]))<=DOMAINS: errors.append(f"{where}: unknown domain")
        if not set(term.get("language",[]))<=LANGUAGES: errors.append(f"{where}: unknown language")
        if not term.get("terminological_definition"): errors.append(f"{where}: empty terminological_definition")
        if not term.get("plain_language_explanation"): errors.append(f"{where}: empty plain_language_explanation")
        if not term.get("sources"): errors.append(f"{where}: no evidence sources")
        for src in term.get("sources",[]):
            parsed=urlparse(src.get("url",""))
            if parsed.scheme not in {"http","https"} or not parsed.netloc: errors.append(f"{where}: invalid source URL {src.get('url')!r}")
    known=set(ids)
    for i,term in enumerate(terms):
        for related in term.get("related_term_ids",[]):
            if related not in known: errors.append(f"terms[{i}]: unresolved related term {related}")
    return errors

def main()->int:
    try: payload=json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"SDGDS registry could not be read: {exc}",file=sys.stderr); return 2
    if payload.get("dataset")!="HSMART-SDGDS" or not isinstance(payload.get("terms"),list):
        print("Invalid registry envelope",file=sys.stderr); return 2
    errors=validate_terms(payload["terms"])
    if errors:
        print("SDGDS validation FAILED:")
        for error in errors: print(f"- {error}")
        return 1
    print(f"SDGDS validation PASS: {len(payload['terms'])} terms; IDs, labels, aliases, enums, sources, and relationships are valid.")
    return 0
if __name__=="__main__": raise SystemExit(main())
