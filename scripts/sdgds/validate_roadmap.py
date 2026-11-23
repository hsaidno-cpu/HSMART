#!/usr/bin/env python3
"""Validate the SDGDS roadmap/progress ledger with Python stdlib only."""
from __future__ import annotations
import json,re,sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[2]
FILE=ROOT/"docs/roadmap/SDGDS-PROGRESS.json"
STATUSES={"NOT_STARTED","PLANNED","IN_PROGRESS","BLOCKED","IMPLEMENTED","VERIFIED","ACCEPTED","MERGED","DEFERRED","CANCELLED"}
GATES={"NOT_RUN","NOT_ASSESSED","PASS","PASS_WITH_CAVEATS","HOLD","FAIL","BLOCKED","NOT_APPLICABLE"}
PRIORITIES={"P0","P1","P2","P3"}
STAGES={"R0 Intake","R1 Strategy & Baseline","R2 Roadmap Design","R3 Approval & Baseline Freeze","R4 Iteration Execution","R5 Formative Check","R6 Milestone Acceptance","R7 Outcome & Impact","R8 Adaptation","R9 Closure & Learning"}
TYPES={"Milestone","Work Item","Evaluation","Risk","Decision","Dependency"}
def validate(data:dict)->list[str]:
    errors=[]
    try:
        date.fromisoformat(data.get("snapshot_date","")); date.fromisoformat(data.get("last_evaluated",""))
    except Exception: errors.append("snapshot_date and last_evaluated must be valid ISO dates")
    if data.get("status") not in {"DRAFT","PROPOSED_NOT_FROZEN","APPROVED","ACTIVE","CLOSED","RETIRED"}:
        errors.append("invalid roadmap status")
    measurement=data.get("progress_measurement",{})
    if "overall_completion" not in measurement: errors.append("overall_completion must be explicitly present (null allowed)")
    if measurement.get("overall_completion") is not None and not measurement.get("overall_completion_reason"):
        errors.append("numeric overall_completion requires an approved denominator and method")
    items=data.get("work_items",[])
    if not isinstance(items,list): return errors+["work_items must be a list"]
    ids=set()
    for i,item in enumerate(items):
        where=f"work_items[{i}]"
        if not isinstance(item,dict): errors.append(f"{where} must be an object"); continue
        tid=item.get("id","")
        if not re.fullmatch(r"SDGDS-[A-Z0-9-]+",tid): errors.append(f"{where}: invalid ID {tid!r}")
        if tid in ids: errors.append(f"{where}: duplicate ID {tid}")
        ids.add(tid)
        if item.get("type") not in TYPES: errors.append(f"{where}: invalid type")
        if item.get("stage") not in STAGES: errors.append(f"{where}: invalid PRE stage")
        if item.get("status") not in STATUSES: errors.append(f"{where}: invalid delivery status")
        if item.get("gate") not in GATES: errors.append(f"{where}: invalid evaluation gate")
        if item.get("priority") not in PRIORITIES: errors.append(f"{where}: invalid priority")
        if not item.get("title") or not item.get("acceptance"): errors.append(f"{where}: title and acceptance are required")
        try: date.fromisoformat(item.get("last_evaluated",""))
        except Exception: errors.append(f"{where}: invalid last_evaluated date")
        for url in item.get("evidence",[]):
            parsed=urlparse(url)
            if parsed.scheme not in {"http","https"} or not parsed.netloc or any(c.isspace() for c in url):
                errors.append(f"{where}: invalid evidence URL {url!r}")
    for i,item in enumerate(items):
        if not isinstance(item,dict): continue
        for dep in item.get("deps",[]):
            if dep not in ids: errors.append(f"work_items[{i}]: unresolved dependency {dep}")
    return errors
def main()->int:
    try: data=json.loads(FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Cannot read SDGDS progress ledger: {exc}",file=sys.stderr); return 2
    errors=validate(data)
    if errors:
        print("SDGDS roadmap validation FAILED:")
        for error in errors: print(f"- {error}")
        return 1
    print(f"SDGDS roadmap validation PASS: {len(data['work_items'])} records; IDs, states, dependencies, evidence and progress discipline valid.")
    return 0
if __name__=="__main__": raise SystemExit(main())
