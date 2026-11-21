# ADR-003: Adopt a Canonical Universal Capability Manifest

- Status: Accepted baseline
- Date: 2026-11-21

## Context
Skills and plugins use different file formats and platform-specific metadata. HSMART needs a neutral contract for identity, version, dependencies, interfaces, permissions, runtime, security, and compatibility.

## Decision
Use a versioned JSON-compatible canonical manifest validated against JSON Schema. Platform-specific adapters translate this contract without changing canonical identity or capability semantics.

## Consequences
- IDs are stable and never reused.
- Versions and artifacts are immutable after publication.
- Credentials and private operational secrets are forbidden in manifests.
- Schema evolution requires compatibility tests and a version policy.
