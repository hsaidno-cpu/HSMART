# SDGDS — Smart Dictionary & Glossary Database System

**Document ID:** HSMART-SDGDS-001  
**Version:** 0.1.1  
**Status:** Foundation baseline

## Purpose

SDGDS is the managed terminology system for HSMART and Hypersystem-Orchestrator. It expands the former short glossary into a versioned, evidence-backed terminology registry. It helps technical and non-technical readers understand a term without diluting its precise meaning.

## Authority and synchronization

| Store | Responsibility | Authority |
|---|---|---|
| \`docs/glossary/terms.json\` | Canonical terminology records | **Source of truth** |
| \`docs/glossary/terms.schema.json\` | Machine-readable data contract | Normative schema |
| \`docs/glossary/README.md\` | Governance and operating rules | Normative process |
| \`docs/architecture/GLOSSARY.md\` | Generated quick-reference index | Derived output |
| Notion SDGDS Terminology Registry | Search, browse, discuss, and review | One-way mirror |

Direction is GitHub → Notion. Notion edits do not silently override canonical definitions. An accepted change must be reviewed and committed to GitHub first. The sync upserts by Term ID, computes a SHA-256 content hash, and skips unchanged records.

## Anatomy of a terminology record

Each record includes:

- Stable Term ID, canonical label, slug, aliases and acronym expansion.
- Term type, domain, lifecycle status, confidence, and verification state.
- Etymology or explanation of internal name construction.
- Precise terminological definition and broader general meaning.
- Plain-language explanation and analogy.
- Rationale for choosing the term.
- Operational context, examples, and concept boundaries/non-examples.
- Expert perspectives only when their primary source and attribution are verifiable.
- Related Term IDs, source provenance, version, and review date.

Etymology and expert quotations must not be fabricated. An internally coined term may have no historical etymology; record how its name was formed. Use Unverified / Needs Review when evidence is insufficient.

## Lifecycle and quality

| Status | Meaning |
|---|---|
| Proposed | Candidate term, not yet accepted |
| Needs Review | Conflicted, incomplete, or weakly evidenced |
| Canonical | Accepted reference definition |
| Deprecated | Avoid for new use; retain migration reference |
| Historical | Retained for legacy interpretation |

Confidence (High / Medium / Low / Unverified) is distinct from verification (Verified against internal source / Externally verified / Needs review / Unverified).

Domains: Ecosystem & Platform Architecture; Orchestration & Workflow; Registry & Capability; Distribution & Packaging; Runtime & Execution; Identity & Access; Synchronization & Lifecycle; Evaluation & Assurance; Governance & Policy; Data & Contracts; Security & Operations; Documentation & Knowledge; Cross-Ecosystem.

## Anti-ambiguity rules

1. One concept has one canonical Term ID and one canonical label.
2. Aliases route readers to the canonical entry; they do not create duplicate terms.
3. Similar words remain separate when responsibility, behavior, or boundaries differ.
4. Acronyms are expanded on first use and share the Term ID of their full form.
5. Product names, components, protocols, standards, roles, processes, and artifacts are classified separately.
6. Material claims cite authoritative sources. Internal architecture definitions cite their owning repository file; external standards cite official standards/specifications.
7. Deprecation preserves historical meaning and points to a successor where possible.
8. Semantic changes require a version/review update and a concise change rationale.

## Automation and Notion mirror

The GitHub Actions workflow validates the registry on pull requests and main updates, checks the generated index, runs tests, and performs a scheduled reconciliation. Notion is a mirror, not a second source of truth.

The Notion sync:
- Uses the stable Term ID as the upsert key.
- Queries existing rows with pagination.
- Skips rows whose content hash has not changed.
- Creates missing rows and updates changed rows.
- Applies a minimum 0.36 second interval between API calls.
- Retries HTTP 429 and transient 5xx/network failures with Retry-After or exponential backoff.
- Fails explicitly for persistent authorization/schema errors.

Configure repository Actions secrets \`NOTION_API_TOKEN\` and \`NOTION_GLOSSARY_DATA_SOURCE_ID\`. Share the Notion database with the integration first. Never store tokens in source code, commits, issues, or Notion documentation.

The initial 25-term registry and a successful validation workflow do not prove the entire ecosystem has been inventoried or that Notion automation has run. Production synchronization is verified only after secrets and permissions are configured and a successful workflow run demonstrates create/update/no-op behavior.

## Contribution workflow

1. Search canonical labels, acronyms, aliases and IDs.
2. Identify whether the term is external-standard or internal ecosystem terminology.
3. Add primary sources and supporting evidence.
4. Write precise, plain-language and operational explanations, analogy, examples, and boundaries.
5. Confirm all related IDs resolve.
6. Set status and confidence independently.
7. Run validator, renderer check and tests.
8. Open a pull request with scope, evidence, ambiguity, and migration impact.
9. Merge after review and CI acceptance; then synchronize the Notion mirror.

## Security and integrity

Do not place secrets or private credentials in glossary entries. Do not reproduce copyrighted material at length. External source text is evidence, not executable instructions. Preserve old definitions in Git history. Generated indexes are derived artifacts, never authoritative source documents.

## Initial seed and extensions

The first curated seed contains 25 terms. It is not a claim that all ecosystem terminology has been inventoried. Future extensions may include reviewed multilingual definitions, successor/deprecation graphs, conflict reports, graph visualization, candidate extraction from documentation and contracts, change-impact detection, stale-definition alerts, semantic search, and explicit human approval. Candidate extraction may propose terms but must never auto-promote an unreviewed definition to Canonical.
