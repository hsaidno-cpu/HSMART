# UEDE HSO Capability Discovery Adapter v1.0.0

**Status:** Draft read-only catalog adapter. It discovers HSO plugin and skill identities; it does not invoke them.  
**Branch:** `feat/hso-capability-discovery-adapter-20261125`, stacked on HSMART PR #34.

## Canonical source and inventory

The adapter pins HSO parent repository `hsaidno-cpu/Hypersystem-Orchestrator` at commit `9853bde6d8484b486aa4d163e65f834fa632410b` and reads six versioned catalog files:

- `catalog/plugins.json`
- `catalog/repositories.json`
- `catalog/instruction-snapshots.json`
- `catalog/distribution-registry.json`
- `catalog/hso-runtime-capabilities.json`
- `catalog/compatibility-matrix.json`

At catalog revision 2026-11-23, the parent catalog declares 23 plugins and 265 skill records. The discovery adapter emits one descriptor per plugin and one per skill (288 records). It also reports runtime capability IDs and plugin-to-plugin contract-test edges as separate metadata.

## Evidence is not execution

The HSO runtime catalog records two built-in sandbox operations, one test-only fault injector, and one enabled Remote MCP skill capability scoped to Skill Analyzer. The Remote MCP entry is restricted to one analysis tool, Streamable HTTP, approval policy ALWAYS, and probe status READY_WITH_LIMITATIONS. It does not establish that the current HSMART host is activated or that a real skill invocation has completed.

The adapter therefore never emits `ELIGIBLE`. It separates:

1. Catalog identity — plugin/skill exists in a pinned HSO catalog.
2. Source verification — the child repository and pinned content need independent verification.
3. Rights clearance — a real license identifier and distribution permission are required; non-commercial/private/unassessed rights remain blocked.
4. Instruction parity — source-vs-platform parity status from the HSO catalog is retained; snapshot count mismatch is a hard drift.
5. Interface contract — plugin-to-plugin handoff tests are not treated as MCP invocation tests.
6. Host/runtime — registration of an enabled adapter is not host activation or a real invocation receipt.

## Read-only transport

`HsoCatalogTransport` exposes one operation: `read_json(path, ref)`. There are no repository write, plugin publish, key rotation, runtime invoke, installation or merge methods.

A bound transport changes readiness only to `TRANSPORT_BOUND_NOT_VERIFIED`. It does not claim that the transport was authorized, that child sources were independently fetched, or that any HSO capability is callable from HSMART.

## Fail-closed behavior

- The adapter rejects catalog count mismatches, duplicate identities, missing instruction snapshots and inconsistent registry counts.
- Missing child source/commit yields `NOT_IDENTIFIED`; catalog-known source without direct child verification remains `CANDIDATE`, never `VERIFIED`.
- A catalog without an explicit license identifier and installable distribution status cannot claim `CLEARED`.
- `DRIFT_DETECTED` remains `DRIFT`; `NOT_COMPARED` remains `NOT_COMPARED`.
- `CONTRACT_TESTED` in the 15-edge plugin handoff matrix does not mean host activation, MCP contract success, or runtime verification.
- Every discovered plugin/skill remains `BLOCKED` until all requirements in HSMART `uede-capability-descriptor.schema.json` have independently passed with evidence.

## Live integration prerequisites

The current HSMART host has no injected HSO catalog transport. Before activation, a deployment adapter must fetch the exact pinned Git ref through read-only credentials, verify child repository commits/content digests, resolve license rights for the intended use, run instruction-parity checks, probe host activation, perform a scoped real invocation and attach exact runtime evidence. Do not grant broad repository or production permissions to the catalog reader.
