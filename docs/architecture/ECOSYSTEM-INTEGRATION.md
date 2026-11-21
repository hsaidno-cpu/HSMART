# HSMART Internal Ecosystem Integration

## Purpose

This document defines how existing and planned products integrate with HSMART without making the platform core depend on their internal implementation details. HSMART manages their discovery, access, distribution, execution, synchronization, and evaluation through canonical contracts.

## Product integration matrix

| Product | HSMART role | Integration domains | Migration posture |
|---|---|---|---|
| A.S.F.R.E.E Canonical | First-party evaluation capability | Registry, Runtime, Evaluation, Distribution | Primary supported product |
| A.S.F.R.E.E Legacy | Compatibility target | Registry, compatibility adapter, controlled runtime | Preserve explicit legacy identity; do not silently replace canonical |
| Skill Analyzer | Skill discovery, forensic analysis, comparison, reconstruction | Registry, Orchestrator, Runtime, Evaluation | Register its capability contract and tool schemas |
| Anatomi Prompt v3 / Octa-Prompt | Prompt engineering and decomposition capability | Registry, Orchestrator, Runtime | Integrate as a separately versioned product |
| Universal AI Invocation Gateway | Earlier remote invocation and routing concept | Gateway, Access & Identity, Runtime, Observability | Consolidate into HSMART platform domains; avoid duplicate gateway stacks |
| External publisher skills/plugins | Third-party ecosystem products | Registry, Marketplace, Evaluation, Runtime, Access | Governed publisher onboarding |

## Integration invariants

1. Each product retains its own repository, release lifecycle, ownership, and product roadmap.
2. HSMART consumes canonical manifests, artifacts, dependency declarations, signatures, and evaluation evidence.
3. HSMART does not need to understand internal implementation details beyond declared interfaces and contracts.
4. Product identity is stable; platform adapters do not create duplicate capability identities.
5. Product releases remain immutable and independently versioned.
6. Marketplace listing does not automatically authorize execution.
7. Product-specific secrets remain in scoped secret stores and are never copied into shared manifests.
8. HSMART platform failure must not silently mutate a product's source repository.

## A.S.F.R.E.E Canonical and Legacy

A.S.F.R.E.E Canonical is the primary integration target. Legacy remains separately identifiable and is exposed only through an explicit compatibility path.

Required metadata:
- distinct capability IDs;
- explicit version and lifecycle status;
- compatibility declaration;
- dependency and schema version;
- migration/retirement notice where relevant;
- evaluation evidence.

Canonical and Legacy must not share a version namespace or be treated as interchangeable without contract tests.

## Skill Analyzer

Skill Analyzer should use HSMART Registry for capability and skill discovery, Orchestrator for delegated workflows, and Evaluation for evidence-backed analysis. Its own analysis methods remain product-owned capabilities. HSMART owns routing, access, audit, and lifecycle integration.

## Anatomi Prompt

Anatomi Prompt is a specialized prompt-engineering capability. HSMART should register its canonical interface and dependencies while leaving Octa-Prompt logic and domain methodology in its own repository. It must not become a mandatory dependency of unrelated HSMART services.

## Universal AI Invocation Gateway consolidation

The prior Gateway concept contributes:
- remote MCP and HTTP invocation;
- centralized routing;
- OIDC/OAuth;
- API key management;
- Redis-backed rate limiting/cache where appropriate;
- controlled logging and observability.

These responsibilities are assigned to D06 Distribution Gateway, D08 Access & Identity, D04 Intelligence Orchestrator, D05 Runtime, and D10 Observability. Build one HSMART gateway path rather than maintaining parallel gateways with duplicated authentication and audit logic.

## Registry migration and bulk ingestion

A previous planning requirement identified 427 individual Skill Registry Records as a migration workload. Treat 427 as a planning inventory count from that earlier project context, not as proof that 427 validated records currently exist in HSMART.

Bulk migration must:
1. inventory source records and provenance;
2. preserve source IDs and paths as provenance fields;
3. normalize names, domains, categories, triggers, inputs, outputs, and workflow;
4. map references, scripts, assets, commands, agents, dependencies, and permissions;
5. detect duplicates and broken references;
6. identify missing or contradictory metadata;
7. validate against the canonical manifest;
8. import into a non-public staging state;
9. run compatibility/security evaluation;
10. publish only after approval.

Migration statuses: discovered, imported, normalized, validation_failed, validated, approved, published, deprecated, retired.

No bulk import should automatically make an artifact executable or publicly discoverable.

## Integration sequence

1. Register one internal sample capability.
2. Integrate A.S.F.R.E.E Canonical through Registry and Runtime.
3. Add Skill Analyzer as an independent capability.
4. Integrate Anatomi Prompt with explicit dependency boundaries.
5. Migrate Universal AI Invocation Gateway responsibilities into HSMART platform domains.
6. Preserve A.S.F.R.E.E Legacy through a compatibility adapter.
7. Prepare external publisher onboarding only after trust controls are implemented.
