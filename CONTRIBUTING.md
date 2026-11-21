# Contributing to HSMART

## Before contributing
- Read the Master Architecture Specification.
- Review Domain Boundaries and relevant ADRs.
- Identify the owning domain and affected contracts.
- Never include credentials, production data, or private customer payloads.

## Pull request requirements
- Explain the problem and intended outcome.
- Link an issue or ADR for material architecture changes.
- Describe backward compatibility and migration implications.
- Include tests or validation evidence.
- Update API/schema/event documentation where contracts change.
- Include security and data-handling implications.
- Do not claim a capability is implemented without executable evidence.

## Architecture changes
Changes to identity, tenancy, runtime trust, artifact integrity, synchronization risk, protocol contracts, or marketplace permissions require an ADR or amendment.

## Security-sensitive contributions
Report vulnerabilities privately through the repository's configured security contact when available. Do not publish exploit details or secrets in public issues. Until a private disclosure channel is configured, contact the repository owner through a trusted private channel.

## Engineering style
- Prefer explicit names and typed contracts.
- Keep domain ownership clear.
- Avoid direct cross-domain database access.
- Make asynchronous operations idempotent.
- Treat external content and model output as untrusted.
- Document operational failure behavior.

A change is ready only when required checks pass, reviewers approve it, and documentation reflects actual implementation status.
