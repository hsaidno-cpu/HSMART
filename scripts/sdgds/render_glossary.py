#!/usr/bin/env python3
"""Render the concise HSMART glossary index from the canonical SDGDS JSON."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"docs/glossary/terms.json"
OUTPUT=ROOT/"docs/architecture/GLOSSARY.md"
def render(payload: dict)->str:
    terms=sorted(payload["terms"],key=lambda x:x["term"].casefold())
    lines=["# HSMART Glossary","","Generated index. Full definitions, aliases, evidence, relationships, and review metadata live in [SDGDS](../glossary/README.md) and [terms.json](../glossary/terms.json). Do not edit manually.","","| Term ID | Canonical term | Type | Domain | Concise definition | Status |","|---|---|---|---|---|---|"]
    for t in terms:
        d=t["terminological_definition"].replace("|","\\|").replace("\n"," ")
        if len(d)>220: d=d[:217].rstrip()+"..."
        label=t["term"].replace("|","\\|")
        domain=", ".join(t["domains"]).replace("|","\\|")
        lines.append(f'| {t["term_id"]} | {label} | {t["term_type"]} | {domain} | {d} | {t["status"]} |')
    lines += ["",f'_Generated from SDGDS dataset version {payload.get("dataset_version","unknown")}._',""]
    return "\n".join(lines)
def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    payload=json.loads(REGISTRY.read_text(encoding="utf-8"))
    generated=render(payload)
    if args.check:
        existing=OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if existing!=generated:
            print("Glossary index is stale. Run: python scripts/sdgds/render_glossary.py"); return 1
        print("Glossary render check PASS"); return 0
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(generated,encoding="utf-8")
    print(f"Rendered {len(payload['terms'])} terms to docs/architecture/GLOSSARY.md")
    return 0
if __name__=="__main__": raise SystemExit(main())
