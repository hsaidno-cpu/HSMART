# HSAR v0.3.0 — HSMART Consumer Integration Contract

**Contract version:** 0.3.0  
**Status:** Proposed integration contract; PR remains unmerged  
**HSMART repository:** hsaidno-cpu/HSMART  
**HSO repository:** hsaidno-cpu/Hypersystem-Orchestrator

## 1. System boundary and ownership

HSAR is the technical anatomy/physiology registry and forensic knowledge layer serving HSO, HSMART and explicitly authorized connected components in the HSO plugin ecosystem.

HSMART remains a distinct platform with its own source repository, release lifecycle, data model, ownership and governance. HSO is not an alias for HSMART and must not absorb HSMART implementation. No direct shared-database ownership, runtime dependency or write-back authority is implied by documentation alone.

GitHub is canonical for engineering source, tests, schemas, workflows, PRs and releases. Notion HSAR is a knowledge/navigation/evidence projection. SDGDS remains the canonical terminology registry.

## 2. Six primary HSAR forensic spearheads

For HYPERDEEP_FORENSIC and EXTREME_HYPERDEEP modes, the six primary plugin spearheads are:

1. SKILL ANALYZER — forensic analysis, methodology selection, source/evidence audit, root cause and negative findings.
2. ANATOMI PROMPT v3.0 — OCTA-PROMPT — eight-pillar instruction and requirement architecture; exact version must be resolved.
3. ASFREE — artifact inventory, provenance, atomic deconstruction and authorized reconstruction.
4. AI Workflow Systems Orchestrator — workflow/system design, modularization, integration, evaluation and optimization.
5. Evaluator Team — adversarial challenge, counterevidence, cross-evaluation and acceptance assessment.
6. Skill Developer Orchestrator — controlled implementation, regression, packaging and release assurance.

Every role must carry an explicit execution state: INVOKED, PROCEDURE_APPLIED, UNAVAILABLE or NOT_USED. INVOKED requires a distinct observable invocation receipt. Requested and observed versions are separate. A fallback based on a lower-version instruction is not equivalent to exact v3.0 invocation without compatibility evidence.

Other HSO ecosystem plugins and skills may be engaged conditionally when the target, evidence or a discovered gap requires distinct specialist expertise. Examples include roadmap/dependency evaluation, database/schema/policy inspection, security, observability, workflow automation, compatibility or legal/licensing boundaries. Resolve canonical identity, current source/version, ownership, permission, capability and invocation evidence before routing. Catalogue presence does not prove executability.

## 3. Adaptive methodology intelligence

HSAR maintains an open-ended methodology registry. First Principles, Systems Thinking, MECE, Functional Decomposition, Root Cause Analysis, 5 Whys, Ishikawa, SWOT, PESTLE, FMEA/FMECA, Fault Tree, Bow-tie, STRIDE, dependency analysis, reliability engineering, architecture fitness functions and test-pyramid are starter methods, not an exhaustive whitelist.

New or more effective methods may be discovered and evaluated when an analytical gap exists. Method lifecycle:
CANDIDATE → SCREENED → PILOTED → VALIDATED → ADOPTED
with REJECTED, DEFERRED, RETIRED and SUPERSEDED dispositions.

A new method is not automatically better. Adoption requires an authoritative source, domain-fit assessment, repeatable procedure, matched pilot against a baseline, evidence of value, limitations, resource cost, decision record and versioning. Conflicting methods preserve assumptions and dissent; they are not averaged away.

## 4. Analysis output contract: four tables plus two comparative tables

Every substantive analysis produces four separate core tables:
1. Cross-method analysis.
2. Positive analysis.
3. Negative/root-cause analysis.
4. Negative-to-positive conversion.

When the user explicitly requests comparison, benchmarking, ranking, alternative assessment or feature comparison, HSAR adds:
5. Comparative scorecard comparing the four analysis dimensions across all target objects.
6. Feature-gap and evaluative recommendation table.

The 4+2 mode measures qualitative and quantitative evidence with an anchored 0–5 score, classification, value, confidence and evidence coverage. Unknown, inaccessible, untested or non-comparable evidence is N/A, not zero. Composite scores are not aggregated by default; a hard P0/P1 gate cannot be offset by a high average. Comparison requires matched scope, version, baseline, sample and scan depth.

## 5. L1–L4 forensic depth

| Level | Scope | Evidence boundary |
|---|---|---|
| L1 | Documentation, manifests, contracts, policies, plugins/skills, versions, ownership and exact baselines | Documentation-level claims only |
| L2 | Recursive structure, modules, interfaces, schemas, data stores, components, scripts/functions inventory and dependency DAG | Source-verified/inferred graph edges clearly distinguished |
| L3 | Source/script/function algorithms, control/data flow, state, security, errors, retries, recovery and tests | Static analysis distinguished from actual executed tests |
| L4 | Named-host/runtime invocation, permissions, side effects, logs, end-to-end and recovery tests | Explicit authorization and actual receipts required |

No L4 runtime claim can be inferred from L1-L3 inspection or a passing static CI job.

## 6. HSMART component documentation and source evidence

For each HSMART component documented in HSAR:
- Preserve the canonical HSMART repository and source owner.
- Capture exact branch, commit SHA, path, symbol and blob hash.
- Record whether source is public, private, restricted or not assessed.
- Distinguish discovered, catalogued, source-verified, tested, host-tested, executable and deployed states.
- Keep HSMART internal data, credentials and private instructions outside general HSO documentation.
- Track HSMART changes in the HSMART repository and link PR/CI receipts into HSAR.

## 7. Improvement handoff

When HSAR identifies an improvement relevant to HSMART:
1. Capture the four core analysis tables and, for comparative work, tables 5 and 6.
2. Convert accepted candidates into bounded HSMART work items with acceptance, rollback, source ownership and evidence requirements.
3. Use a feature branch and PR for authorized engineering changes.
4. Preserve exact base/head SHAs, CI receipts, tests and remaining caveats.
5. Update HSMART source documentation and HSAR cross-references.
6. Do not merge, deploy, change production or modify permissions without the appropriate human decision and authority gate.

## 8. GitHub-to-Notion synchronization

The target model is GitHub event → canonical source re-read → redacted normalized change record → stable-key/content-hash Notion upsert → read-back verification → audit receipt.

This is not active by virtue of this contract or plugin installation. Activation requires a scoped Notion integration, protected GitHub Actions secrets, stable upsert keys, hash-based no-op handling, idempotency, retries/backoff, reconciliation, redaction, dead-letter recovery and end-to-end acceptance tests for create/update/no-op/duplicate/stale/auth/permission/timeout/rate-limit/read-back cases.

No credentials belong in model context, Git commits, PR comments or Notion text. If permissions/secrets are not configured, synchronization remains NOT_CONFIGURED, PARTIAL or BLOCKED.

## 9. Checkpoint and recovery

Long-running forensic work preserves an immutable verified checkpoint with case/roadmap revision, exact source baselines, component/method versions, output hashes, stage status and next action. Keep latest verified checkpoint separate from latest incomplete attempt.

Specialist failure is classified as transient, permanent, permission, version conflict, integrity or unknown. Retry only bounded transient failures. Resume from a verified checkpoint, re-read source revisions and replay idempotently. Integrity mismatches are quarantined. Restore is first tested in isolation and verified by hashes, schema, counts and relationship integrity before promotion. Do not invent RPO/RTO; report only measured recovery.

## 10. Current implementation and verification boundary

This PR proposes the HSMART consumer contract. It does not install HSAR into HSMART runtime, establish a direct shared database, provision the six plugin runtimes, activate event-driven Notion sync or authorize production writes.

For the PR itself, review evidence must bind to the exact code-reviewed SHA. GOV-11 is currently a designated logical role whose separate runtime is not provisioned; any AI-generated assurance must disclose the actual execution context and correlation limitation. It is not independent certification, native GitHub approval or merge authorization.

## 11. Canonical references

- HSO ecosystem control plane: https://github.com/hsaidno-cpu/Hypersystem-Orchestrator
- HSMART platform: https://github.com/hsaidno-cpu/HSMART
- HSAR private plugin: https://chatgpt.com/plugins/plugins_6b07184f648081918f51a8495b59deac
- HSAR Notion knowledge hub: https://app.notion.com/p/42399868397f81429e8ac321bdc33957
