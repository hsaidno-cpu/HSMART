# HSMART Repository and Delivery Blueprint

## Repository strategy

Use a modular monorepo for HSMART platform core during the initial implementation. Keep product repositories and independent client SDKs separate where ownership and release cadence differ. A shared contracts repository may be extracted when multiple products and adapters consume the same stable contracts.

## Proposed ecosystem repositories

- hsmart-platform: core domains, gateway, runtime, sync, and platform orchestration.
- hsmart-contracts: canonical manifest, OpenAPI, event schemas, runtime and adapter contracts.
- hsmart-sdk: typed client libraries and publisher tooling.
- hsmart-platform-adapters: platform-specific MCP/client integration packages.
- hsmart-deployment: infrastructure-as-code, containers, deployment profiles, and operations.
- hsmart-documentation: public developer docs and operator guides.
- hsmart-security: threat models, security policies, disclosure process, and assurance evidence.
- hsmart-marketplace: marketplace web/API components when independently scaled.
- product repositories: A.S.F.R.E.E, Skill Analyzer, Anatomi Prompt, and other products remain independent.

The current HSMART repository is the architecture repository and starting point. The repositories above are a proposed future split, not a claim that they already exist.

## Proposed platform monorepo

    hsmart-platform/
      apps/
        api-gateway/
        mcp-server/
        developer-portal/
        admin-console/
        marketplace-api/
      modules/
        studio/
        registry/
        publisher-organization/
        intelligence-orchestrator/
        execution-runtime/
        distribution-gateway/
        synchronization-engine/
        universal-access-manager/
          api-key-manager/
          mcp-access-manager/
          custom-mcp-connector/
          custom-api-connector/
          credential-vault/
          identity-policy-engine/
        evaluation-assurance/
        observability-audit/
        marketplace-commerce/
      packages/
        domain-models/
        canonical-schemas/
        api-contracts/
        event-contracts/
        security-core/
        telemetry/
      adapters/
        chatgpt/
        claude/
        gemini/
        generic-mcp/
        rest-client/
      infrastructure/
        docker/
        terraform/
        database/
        redis/
        object-storage/
        message-broker/
        observability/
      migrations/
      tests/
        unit/
        integration/
        contract/
        e2e/
        security/
        load/
        regression/
      docs/
        architecture/
        security/
        api/
        operations/

## Delivery workflow

Feature branch → Pull request → lint/static checks → unit/integration/contract tests → security/dependency scan → signed artifact build → SBOM/provenance → release approval → canary → monitor/promote.

## Repository governance

- Protect main and release branches.
- Require pull-request review and passing status checks.
- Use CODEOWNERS only after real maintainer teams/users exist.
- Require ADR for architecture-level changes.
- Separate build credentials from deployment credentials.
- Do not expose production secrets to untrusted pull-request workflows.
- Pin action dependencies to verified immutable references before production hardening.
- Record release notes and migration/rollback instructions.

## Implementation stack selection

PostgreSQL, Redis, S3-compatible object storage, Docker, OIDC-compatible identity, GitHub Actions, and OpenTelemetry-compatible telemetry are baseline candidates. Backend language, message broker, KMS, cloud provider, and payment provider remain open ADR decisions. Do not introduce microservices or Kubernetes solely because the diagram contains many domains.
