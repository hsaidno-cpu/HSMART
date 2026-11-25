# HSAR — HSMART consumer integration contract

**Status:** proposed integration contract, not yet accepted into `main`  
**HSMART repository:** `hsaidno-cpu/HSMART`  
**HSO repository:** `hsaidno-cpu/Hypersystem-Orchestrator`

## 1. System boundary

HSAR is the technical anatomy/physiology registry serving HSO and explicitly authorized connected systems, including HSMART. HSMART remains a distinct platform with its own source repository, release lifecycle, data model, ownership and governance. HSO is not an alias for HSMART and must not absorb HSMART implementation.

## 2. Consumption model

HSMART may consume HSAR outputs through explicit documentation references or future versioned APIs/adapters. No direct shared-database ownership, runtime dependency or write-back authority is implied by documentation alone.

For each HSMART component documented in HSAR:
- Preserve the canonical HSMART repository and source owner.
- Capture exact branch, commit SHA, path, symbol and blob hash.
- Record whether the source is public, private, restricted or not assessed.
- Distinguish discovered, catalogued, source-verified, tested, host-tested and deployed states.
- Keep HSMART internal data, credentials and private instructions outside general HSO documentation.
- Track HSMART changes in the HSMART repository and link their PR/CI receipts into HSAR.

## 3. Improvement handoff

When HSAR identifies an improvement relevant to HSMART:
1. Capture positive findings, negative findings and negative-to-positive conversion separately.
2. Convert the approved candidate into a bounded HSMART work item with acceptance and rollback criteria.
3. Implement only on an authorized HSMART feature branch.
4. Preserve exact base/head SHAs and CI receipts.
5. Update the HSMART source documentation and HSAR cross-reference.
6. Do not auto-merge, deploy or change production without the required human approval.

## 4. Documentation synchronization

The target model is GitHub Actions/webhook event → source re-read → redacted normalized change record → Notion HSAR upsert → read-back verification → audit receipt.

This is not active by virtue of this contract. Activation requires a scoped Notion integration, GitHub Actions secrets, stable upsert keys, hash-based no-op handling, retries, reconciliation, redaction and tested end-to-end acceptance cases.

## 5. Canonical references

- HSO ecosystem control plane: https://github.com/hsaidno-cpu/Hypersystem-Orchestrator
- HSMART platform: https://github.com/hsaidno-cpu/HSMART
- HSAR Notion knowledge hub: https://app.notion.com/p/42399868397f81429e8ac321bdc33957