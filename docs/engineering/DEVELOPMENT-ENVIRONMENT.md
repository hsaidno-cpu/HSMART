# HSMART Development Environment — Contract Tooling Baseline

**Document ID:** HSMART-ENG-DEV-001  
**Version:** 1.0.0  
**Prepared:** 2026-11-22  
**Status:** Contract-validation environment baseline; application stack still pending ADR-011 approval

## 1. Scope boundary

This environment makes the current canonical contracts testable from a clean checkout. It does not claim that the HSMART application backend, database, runtime, gateway or deployment environment exists.

The validation toolchain uses Python 3.12 for JSON Schema and OpenAPI contract tests. It does not decide the HSMART runtime backend framework. The application stack remains conditional on approval of ADR-011.

## 2. Prerequisites

- Python 3.12 (same minor line locally and in CI).
- Git.
- Network access to install the pinned development dependencies on first setup.
- No cloud account, API key, production database or provider credential is required for contract tests.

## 3. Bootstrap

### macOS / Linux

~~~bash
bash scripts/bootstrap-dev.sh
source .venv/bin/activate
make validate
~~~

### Windows PowerShell

~~~powershell
.\scripts\bootstrap-dev.ps1
.\.venv\Scripts\Activate.ps1
make validate
~~~

If GNU Make is unavailable on Windows, run:

~~~powershell
python -m pytest -q
~~~

## 4. Toolchain contract

- .python-version declares the Python minor line.
- requirements-dev.txt pins direct validation-tool dependencies.
- pyproject.toml defines pytest discovery and repository test paths.
- POSIX and PowerShell bootstrap scripts create a local virtual environment and install the same dependency set.
- Makefile exposes standard install, test and validate entry points.
- GitHub Actions runs the same dependency file and test command on pull requests and pushes to main.

Direct dependency pins are not a fully hermetic lock: transitive packages are not all hash-locked, the hosted runner image is managed by GitHub, and the Python patch release is not pinned. A hash-locked dependency artifact and pinned runner image may be added when the application stack and supply-chain policy are approved.

## 5. Validation layers

| Layer | Command / workflow | What it proves | What it does not prove |
|---|---|---|---|
| Syntax | Workflow JSON parse | JSON files are parseable | Schema correctness |
| JSON Schema | python -m pytest -q | Positive/negative fixtures match the declared schema | Registry implementation |
| OpenAPI | OpenAPI validator test | OpenAPI document conforms to validator-supported 3.1 rules | A live API exists |
| CI | GitHub Actions on exact commit | Configured checks ran and passed on that commit | Runtime, security or production readiness |
| Runtime | NOT IMPLEMENTED | No claim | Must be built and independently tested later |

## 6. Clean-run acceptance

A clean checkout must:
1. Provide the documented Python 3.12 minor line.
2. Create a new virtual environment.
3. Install the pinned direct dependency set without relying on a developer's global packages.
4. Run all contract tests with python -m pytest -q.
5. Return a non-zero exit code for malformed schema/fixture/OpenAPI documents.
6. Produce the CI result against the exact commit SHA.

## 7. Security and maintenance

- Do not store credentials, cloud config, .env secrets or production data in this repository.
- Keep .venv, caches and test artifacts out of Git.
- Review pinned dependencies for security updates before changing them.
- Dependency upgrades must update pins and run the complete test suite.
- Expand this environment into the application dev environment only after backend/database/infrastructure ADRs are accepted.
