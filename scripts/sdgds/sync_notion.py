#!/usr/bin/env python3
"""Idempotent one-way GitHub registry -> Notion SDGDS mirror."""
from __future__ import annotations
import hashlib,json,os,sys,time
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"docs/glossary/terms.json"
API="https://api.notion.com/v1"
VERSION="2025-09-03"
TOKEN=os.getenv("NOTION_API_TOKEN","").strip()
DATA_SOURCE=os.getenv("NOTION_GLOSSARY_DATA_SOURCE_ID","").strip()
COMMIT=os.getenv("GITHUB_SHA","local-uncommitted")
def call(method: str,path: str,payload: dict|None=None)->dict:
    body=None if payload is None else json.dumps(payload,ensure_ascii=False).encode()
    req=Request(API+path,data=body,method=method,headers={"Authorization":f"Bearer {TOKEN}","Notion-Version":VERSION,"Content-Type":"application/json"})
    try:
        with urlopen(req,timeout=30) as res: return json.loads(res.read().decode())
    except HTTPError as exc:
        detail=exc.read().decode(errors="replace")
        raise RuntimeError(f"Notion API {method} {path}: HTTP {exc.code}: {detail}") from exc
    except URLError as exc: raise RuntimeError(f"Notion API network error: {exc}") from exc
def rt(value)->dict:
    if isinstance(value,list): value="; ".join(str(x) for x in value)
    value=str(value or "")
    chunks=[value[i:i+1800] for i in range(0,len(value),1800)] or [""]
    return {"rich_text":[{"type":"text","text":{"content":chunk}} for chunk in chunks]}
def record_hash(term: dict)->str:
    raw=json.dumps(term,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()
def build_properties(term: dict,digest: str)->dict:
    sources=term.get("sources",[])
    return {
      "Term":{"title":[{"type":"text","text":{"content":term["term"]}}]},
      "Term ID":rt(term["term_id"]),"Aliases":rt(term.get("aliases",[])),"Expansion":rt(term.get("expansion","")),
      "Term Type":{"select":{"name":term["term_type"]}},
      "Domain":{"multi_select":[{"name":x} for x in term["domains"]]},
      "Status":{"select":{"name":term["status"]}},
      "Language":{"multi_select":[{"name":x} for x in term.get("language",[])]},
      "Confidence":{"select":{"name":term["confidence"]}},
      "Verification":{"select":{"name":term["verification"]}},
      "Primary Source URL":{"url":sources[0]["url"] if sources else None},
      "Additional Sources":rt([x["url"] for x in sources[1:]]),
      "Etymology":rt(term.get("etymology")),"Terminological Definition":rt(term.get("terminological_definition")),
      "General Meaning":rt(term.get("general_meaning")),"Plain-language Explanation":rt(term.get("plain_language_explanation")),
      "Analogy":rt(term.get("analogy")),"Why This Term":rt(term.get("why_this_term")),
      "Operational Context":rt(term.get("operational_context")),"Usage Examples":rt(term.get("usage_examples")),
      "Boundaries / Non-examples":rt(term.get("boundaries")),"Expert Perspectives":rt(term.get("expert_perspectives")),
      "Related Term IDs":rt(term.get("related_term_ids",[])),"Version":rt(term.get("version")),
      "Last Reviewed":{"date":{"start":term.get("last_reviewed")}},
      "Content Hash":rt(digest),"Last Synced Commit":rt(COMMIT)
    }
def rich_text(page: dict,name: str)->str:
    prop=page.get("properties",{}).get(name,{})
    return "".join(x.get("plain_text","") for x in prop.get("rich_text",[]))
def load_existing()->dict:
    indexed={}; cursor=None
    while True:
        body={"page_size":100}
        if cursor: body["start_cursor"]=cursor
        result=call("POST",f"/data_sources/{DATA_SOURCE}/query",body)
        for page in result.get("results",[]):
            key=rich_text(page,"Term ID")
            if key: indexed[key]=page
        if not result.get("has_more"): break
        cursor=result.get("next_cursor")
        if not cursor: break
    return indexed
def main()->int:
    if not TOKEN or not DATA_SOURCE:
        print("SDGDS Notion sync SKIPPED: configure NOTION_API_TOKEN and NOTION_GLOSSARY_DATA_SOURCE_ID in repository Actions secrets.")
        return 0
    terms=json.loads(REGISTRY.read_text(encoding="utf-8"))["terms"]
    current=load_existing(); created=updated=unchanged=0
    for term in terms:
        old=current.get(term["term_id"]); digest=record_hash(term)
        if old and rich_text(old,"Content Hash")==digest:
            unchanged+=1; continue
        props=build_properties(term,digest)
        if old:
            call("PATCH",f"/pages/{old['id']}",{"properties":props}); updated+=1
        else:
            call("POST","/pages",{"parent":{"type":"data_source_id","data_source_id":DATA_SOURCE},"properties":props}); created+=1
        time.sleep(0.12)
    print(f"SDGDS Notion sync PASS: created={created}, updated={updated}, unchanged={unchanged}, commit={COMMIT[:12]}")
    return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print(f"SDGDS Notion sync FAILED: {exc}",file=sys.stderr); raise SystemExit(1)
