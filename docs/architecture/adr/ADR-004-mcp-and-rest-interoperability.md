# ADR-004: MCP-Native, REST-First-Class Interoperability

- Status: Accepted baseline
- Date: 2026-11-21

## Context
Some AI clients support MCP; others require HTTP APIs or SDK integration. A single protocol would limit reach and tie HSMART to client capabilities.

## Decision
Provide Remote MCP as a primary AI tool interface and versioned REST/HTTP APIs as a first-class general interface. SDKs, webhooks, and platform adapters are additive.

## Consequences
- Canonical operations are defined independently of protocol.
- Adapters share authentication, authorization, audit, and error semantics.
- MCP revisions are pinned and tested.
- HSMART cannot force external clients to refresh locally cached tool manifests.
