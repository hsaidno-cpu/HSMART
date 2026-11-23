#!/usr/bin/env python3
"""Idempotent GitHub SDGDS progress ledger -> Notion roadmap database sync."""
from __future__ import annotations
import hashlib,json,os,sys,time
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[2]
FILE=ROOT/"docs/roadmap/SDGDS-PROGRESS.json"
API="https://api.notion.com/v1"
VERSION="2025-09-03"
TOKEN=os.getenv("NOTION_API_TOKEN","").strip()
DATA_SOURCE=os.getenv("NOTION_SDGDS_ROADMAP_DATA_SOURCE_ID","").strip()
COMMIT=os.getenv("GITHUB_SHA","local-uncommitted")
MIN_INTERVAL=0.36
MAX_ATTEMPTS=6
LAST_CALL=0.0
def pace():
    global LAST_CALL
    if LAST_CALL:
        delay=MIN_INTERVAL-(time.monotonic()-LAST_CALL)
        if delay>0: time.sleep(delay)
    LAST_CALL=time.monotonic()
def retry_wait(exc:HTTPError,attempt:int)->float:
    value=exc.headers.get("Retry-After","")
    if value:
        try:return max(0.0,min(float(value),60.0))
        except ValueError:
            try:
                point=parsedate_to_datetime(value)
                if point.tzinfo is None:point=point.replace(tzinfo=timezone.utc)
                return max(0.0,min(point.timestamp()-time.time(),60.0))
            except Exception:pass
    return min(2**attempt,30.0)
def api_call(method:str,path:str,payload:dict|None=None)->dict:
    body=None if payload is None else json.dumps(payload,ensure_ascii=False).encode()
    for attempt in range(MAX_ATTEMPTS):
        pace()
        req=Request(API+path,data=body,method=method,headers={"Authorization":f"Bearer {TOKEN}","Notion-Version":VERSION,"Content-Type":"application/json"})
        try:
            with urlopen(req,timeout=30) as response:return json.loads(response.read().decode())
        except HTTPError as exc:
            detail=exc.read().decode(errors="replace")
            if (exc.code!=429 and not 500<=exc.code<=599) or attempt==MAX_ATTEMPTS-1:
                raise RuntimeError(f"Notion API {method} {path}: HTTP {exc.code}: {detail}") from exc
            delay=retry_wait(exc,attempt); print(f"Notion API HTTP {exc.code}; retry in {delay:.1f}s.",file=sys.stderr); time.sleep(delay)
        except URLError as exc:
            if attempt==MAX_ATTEMPTS-1:raise RuntimeError(f"Notion network failure after {MAX_ATTEMPTS} attempts: {exc}") from exc
            delay=min(2**attempt,30.0); print(f"Notion network failure; retry in {delay:.1f}s.",file=sys.stderr); time.sleep(delay)
    raise RuntimeError("Notion API retry attempts exhausted")
def rich(value)->dict:
    if isinstance(value,list):value="; ".join(str(x) for x in value)
    value=str(value or "")
    chunks=[value[i:i+1800] for i in range(0,len(value),1800)] or [""]
    return {"rich_text":[{"type":"text","text":{"content":chunk}} for chunk in chunks]}
def digest(item:dict)->str:
    raw=json.dumps(item,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()
def properties(item:dict,content_hash:str)->dict:
    return {
      "Work Item":{"title":[{"type":"text","text":{"content":item["title"]}}]},
      "Work Item ID":rich(item["id"]),
      "Work Type":{"select":{"name":item["type"]}},
      "PRE Stage":{"select":{"name":item["stage"]}},
      "Delivery Status":{"select":{"name":item["status"]}},
      "Evaluation State":{"select":{"name":item["gate"]}},
      "Priority":{"select":{"name":item["priority"]}},
      "Owner Role":rich(item.get("owner")),
      "Dependencies":rich([*item.get("deps",[]),*item.get("external",[])]),
      "Acceptance Criteria":rich(item.get("acceptance")),
      "Evidence URL":{"url":item["evidence"][0] if item.get("evidence") else None},
      "Next Action":rich(item.get("next")),
      "date:Last Evaluated:start":item.get("last_evaluated",""),
      "date:Last Evaluated:is_datetime":0,
      "Source Commit":rich(COMMIT),
      "Content Hash":rich(content_hash),
      "Notes":rich(item.get("notes"))
    }
def get_text(page:dict,name:str)->str:
    prop=page.get("properties",{}).get(name,{})
    return "".join(x.get("plain_text","") for x in prop.get("rich_text",[]))
def load_existing()->dict:
    indexed={}; cursor=None
    while True:
        body={"page_size":100}
        if cursor:body["start_cursor"]=cursor
        response=api_call("POST",f"/data_sources/{DATA_SOURCE}/query",body)
        for page in response.get("results",[]):
            key=get_text(page,"Work Item ID")
            if not key:continue
            if key in indexed:raise RuntimeError(f"Duplicate Work Item ID already exists in Notion: {key}")
            indexed[key]=page
        if not response.get("has_more"):break
        cursor=response.get("next_cursor")
        if not cursor:break
    return indexed
def main()->int:
    if not TOKEN or not DATA_SOURCE:
        print("SDGDS roadmap sync SKIPPED: configure NOTION_API_TOKEN and NOTION_SDGDS_ROADMAP_DATA_SOURCE_ID in GitHub Actions secrets.")
        return 0
    data=json.loads(FILE.read_text(encoding="utf-8")); entries=data["work_items"]
    time.sleep(1.0)
    existing=load_existing(); created=updated=unchanged=0
    for item in entries:
        page=existing.get(item["id"]); content_hash=digest(item)
        if page and get_text(page,"Content Hash")==content_hash:
            unchanged+=1;continue
        values=properties(item,content_hash)
        if page:
            api_call("PATCH",f"/pages/{page['id']}",{"properties":values});updated+=1
        else:
            api_call("POST","/pages",{"parent":{"type":"data_source_id","data_source_id":DATA_SOURCE},"properties":values});created+=1
    print(f"SDGDS roadmap Notion sync PASS: created={created}, updated={updated}, unchanged={unchanged}, source_commit={COMMIT[:12]}")
    return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except Exception as exc:
        print(f"SDGDS roadmap sync FAILED: {exc}",file=sys.stderr);raise SystemExit(1)
