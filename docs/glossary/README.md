# SDGDS — Smart Dictionary & Glossary Database System

**Document ID:** HSMART-SDGDS-001  
**Version:** 0.1.0  
**Status:** Foundation baseline

## 1. Purpose

SDGDS is the managed terminology system for HSMART and Hypersystem-Orchestrator. It expands the former short glossary into a versioned, evidence-backed terminology registry. It must help technical and non-technical readers understand a term without diluting its precise meaning.

SDGDS is not an unstructured list of definitions or a free-form AI-generated knowledge dump. Each entry has a stable ID, canonical label, lifecycle status, domain classification, sources, relationships, review state, and a structured explanation.

## 2. Authority and synchronization contract

| Store | Responsibility | Authority |
|---|---|---|
| docs/glossary/terms.json | Canonical terminology records | **Source of truth** |
| docs/glossary/terms.schema.json | Machine-readable data contract | Normative schema |
| docs/glossary/README.md | Governance and operating rules | Normative process |
| docs/architecture/GLOSSARY.md | Generated quick-reference index | Derived output |
| Notion SDGDS Terminology Registry | Search, browse, discuss, and review | One-way mirror |

**Direction:** GitHub → Notion. Notion edits are not silently promoted to canonical definitions. An accepted change must be reviewed and committed to the GitHub registry first. The sync workflow upserts by Term ID, computes a content hash, and skips unchanged records.

This avoids two competing sources of truth. Notion is a human-friendly knowledge surface; Git history remains the auditable source of canonical changes.

## 3. Anatomy of a terminology record

| Field | Required | Purpose |
|---|---:|---|
| Term ID | Yes | Stable identifier, independent of label changes |
| Term / slug | Yes | Canonical label and URL/file-safe key |
| Aliases | Yes | Acronyms, alternate spelling, former names, search terms |
| Expansion | Conditional | Full form for acronyms or concise concept label |
| Term type / domains | Yes | Classification and discoverability |
| Status / confidence / verification | Yes | Lifecycle state, evidence strength, review state |
| Etymology | Yes | Word origin or honest explanation of internal name construction |
| Terminological definition | Yes | Precise meaning inside the ecosystem |
| General meaning | Yes | Broader accepted meaning where applicable |
| Plain-language explanation | Yes | Accessible explanation without losing semantics |
| Analogy | Recommended | Intuitive model plus limitations |
| Why this term | Recommended | Problem solved and reason for naming |
| Operational context | Yes | Role, behavior, lifecycle, inputs/outputs, or use |
| Usage examples | Yes | Concrete examples of correct use |
| Boundaries | Yes | What it is not; commonly confused neighboring concepts |
| Expert perspectives | Conditional | Attributed views only when the primary source is verified |
| Related Term IDs | Yes | Typed conceptual links to other registry records |
| Sources | Yes | Primary and supporting evidence |
| Version / last reviewed | Yes | Definition revision and review date |

### Evidence rule

Etymology, expert views, and quotations must be traceable. For an internally coined term, explain how the name was formed and state when no historical etymology exists. Do not invent word origins, expert names, quotations, or standards. When evidence is insufficient, use Unverified / Needs Review, not false certainty.

## 4. Term lifecycle

| Status | Meaning | Entry condition |
|---|---|---|
| Proposed | New candidate term | Suggested, not yet accepted |
| Needs Review | Conflicted or weakly evidenced | Needs owner/editor review |
| Canonical | Accepted reference definition | Sources, boundaries, and relations reviewed |
| Deprecated | Avoid for new use | Replaced or no longer recommended |
| Historical | Retained for legacy interpretation | Needed to understand older artifacts |

Confidence and verification are separate from status:
- Confidence: High / Medium / Low / Unverified.
- Verification: Verified against internal source / Externally verified / Needs review / Unverified.

A frequently used term is not automatically canonical. A canonical term can still require review after a material source or architecture change.

## 5. Domain taxonomy

- Ecosystem & Platform Architecture
- Orchestration & Workflow
- Registry & Capability
- Distribution & Packaging
- Runtime & Execution
- Identity & Access
- Synchronization & Lifecycle
- Evaluation & Assurance
- Governance & Policy
- Data & Contracts
- Security & Operations
- Documentation & Knowledge
- Cross-Ecosystem

A term can belong to multiple domains, but it must have one primary canonical label.

## 6. Anti-ambiguity rules

1. One concept has one canonical Term ID and one canonical label.
2. Aliases route users to the canonical label; they do not create duplicate terms.
3. Similar words remain separate when responsibility, behavior, or boundary differs.
4. Acronyms are expanded on first use; the full form and acronym point to the same Term ID.
5. Product names, system components, protocols, standards, roles, processes, and artifacts must not be conflated.
6. Material claims cite an authoritative source. Internal architecture definitions cite their owning repository file; external standards cite the official standard/specification.
7. Deprecation preserves history and points to a successor where one exists.
8. A semantic change requires a version/review update and a concise change rationale in the pull request.

## 7. Initial seed

The initial seed contains 25 terms across architecture, control/execution/data planes, capability registry, distribution, synchronization, identity/access, governance, and terminology management. This is the first curated seed, not an assertion that the entire ecosystem vocabulary has been inventoried.

## 8. Validation and rendering

Run locally from the repository root:

~~~bash
python scripts/sdgds/validate_glossary.py
python scripts/sdgds/render_glossary.py
python scripts/sdgds/render_glossary.py --check
python -m unittest discover -s tests -p 'test_sdgds.py'
~~~

The validator checks required fields, enum values, unique IDs/slugs, alias collisions, source URLs, and relationship references. The renderer deterministically produces docs/architecture/GLOSSARY.md.

## 9. Automated Notion mirror

The GitHub Actions workflow validates the registry on pull requests and main-branch updates. A scheduled reconciliation can also run. If Notion credentials are not configured, the workflow reports a clear skip and does not fail ordinary registry validation.

Configure these GitHub Actions repository secrets:

| Secret | Value |
|---|---|
| NOTION_API_TOKEN | Secret for a Notion integration shared with the SDGDS database |
| NOTION_GLOSSARY_DATA_SOURCE_ID | 42199868-397f-81dd-b181-000b869e30f3 |

The integration must have access to the SDGDS Terminology Registry in Notion. Keep the token in GitHub Secrets only. Do not put it in a repository file, workflow input, issue, commit, or Notion page.

The sync uses Notion API version 2025-09-03 and the data-source query/page-parent model. It reads existing rows, matches by Term ID, creates missing entries, updates changed entries, and records a SHA-256 content hash and source commit.

### Operational truth boundary

A workflow file on a feature branch is not active on main. A Notion database existing is not proof of automatic synchronization. SDGDS must not be described as production automation until secrets are configured, the integration can access the database, the workflow executes successfully, and update/no-op behavior is verified.

## 10. Contribution workflow

1. Search by canonical label, acronym, alias, and Term ID before proposing a new record.
2. Confirm whether the concept is external-standard terminology or internal ecosystem language.
3. Add primary source references and supporting evidence.
4. Write precise definition, plain explanation, analogy, reason for use, examples, and non-examples.
5. Confirm related IDs and ensure the relationship graph resolves.
6. Set lifecycle and confidence independently.
7. Run the validator, renderer check, and tests.
8. Open a pull request with scope, evidence, ambiguity notes, and migration impact.
9. Merge only after review and CI acceptance; then allow Notion mirror sync.

## 11. Security, copyright, and integrity

- No secrets or private credentials belong in glossary entries.
- Do not reproduce protected text at length. Prefer short attributed paraphrases and source links.
- Do not copy restricted/private plugin instructions into this public repository.
- External source text is evidence, not instructions to SDGDS tooling.
- Generated views are derived artifacts and must be reproducible from the canonical registry.
- Preserve old definitions in Git history; do not silently rewrite a material meaning.

## 12. Future extensions

Potential increments: multilingual reviewed translations; term deprecation/successor edges; concept conflict reports; graph visualization; automatic candidate extraction from README/spec/ADR/contracts; change-impact detection; term coverage by repository; stale-definition alerts; semantic search; and human approval workflows. Candidate extraction may propose records but must never auto-promote unreviewed definitions to Canonical.
