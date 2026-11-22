# HSMART Development Environment — Contract Tooling Baseline

**Document ID:** HSMART-ENG-DEV-001  
**Version:** 1.1.0  
**Prepared:** 2026-11-22  
**Status:** IMPLEMENTED CONTRACT-TOOLING BASELINE — APPLICATION ENVIRONMENT DEPENDS ON ACCEPTED ADR-011

## 1. Scope boundary

This environment makes the current canonical contracts testable from a clean checkout. It is a repeatable contract-validation environment, not the HSMART application runtime. It does not claim that the backend, database, Registry, REST/MCP gateway, worker, synchronization service or deployment environment exists.

The toolchain uses the Python 3.12 minor line for JSON Schema and OpenAPI contract tests. It does not by itself approve the application backend framework.

## 2. Supported prerequisites

- Python 3.12.x (keep the same major/minor line locally and in CI; apply the latest security patch available for the platform).
- Git.
- Network access to install the exact direct development dependencies in requirements-dev.txt on first setup.
- Bash on macOS/Linux; PowerShell on Windows.
- No cloud account, API key, production database or provider credential is required for contract tests.

The Python 3.12 branch is in security-fixes-only maintenance. Python.org records 3.12.16 as the latest 3.12 security release on 2026-10-25 and notes that 3.12 installers ended at 3.12.10; therefore this project pins the minor line rather than pretending every operating system can install the same patch binary. CI records the actual patch version used. See https://www.python.org/downloads/release/python-31216/.

## 3. Bootstrap

### macOS / Linux

\`\`\`bash
bash scripts/bootstrap-dev.sh
.venv/bin/python scripts/validate-json.py
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
\`\`\`

### Windows PowerShell

\`\`\`powershell
.\\scripts\\bootstrap-dev.ps1
.\\.venv\\Scripts\\python.exe scripts\\validate-json.py
.\\.venv\\Scripts\\python.exe -m pip check
.\\.venv\\Scripts\\python.exe -m pytest -q
\`\`\`

The bootstrap scripts create a project-local virtual environment and install requirements-dev.txt into that environment. They do not upgrade pip to an unbounded latest version during every setup. GNU Make is optional; it is a convenience on platforms where it is available.

## 4. Toolchain contract

- .python-version declares the supported Python 3.12 minor line.
- requirements-dev.txt pins the direct contract-validation dependencies.
- pyproject.toml defines pytest discovery and repository test paths.
- POSIX and PowerShell bootstrap scripts create a local virtual environment and install the same direct dependency set.
- scripts/validate-json.py performs strict JSON syntax checks while excluding virtual environments and generated directories.
- Makefile exposes standard validation entry points.
- GitHub Actions exercises the bootstrap and test suite on Ubuntu 24.04, Windows Server 2025 and macOS 15.
- CI reports the actual Python and pip versions, runs pip check, runs pytest, and performs repository/OpenAPI structural checks.

**Dependency-lock limitation:** requirements-dev.txt is a direct-pin file, not a transitive hash-locked artifact. Dependency resolution for transitive packages may therefore change as package indexes evolve. Do not use the words hermetic, bit-for-bit reproducible or fully locked for this baseline. A hashed transitive lock remains a separate engineering task and must be generated and verified in a network-enabled environment before it is adopted.

**Runner limitation:** versioned runner labels prevent accidental drift to a different OS major label, but GitHub-hosted runner images are updated over time. CI logs record the environment used; exact image immutability requires a maintained, pinned container/runner image and is not claimed here. Current supported labels are documented by GitHub's runner-images project: https://github.com/actions/runner-images.

## 5. Validation layers

| Layer | Command / workflow | What it proves | What it does not prove |
|---|---|---|---|
| Strict JSON syntax | python scripts/validate-json.py | Committed JSON documents parse, contain no duplicate object keys or non-finite values | Schema correctness |
| JSON Schema | python -m pytest -q | Positive/negative fixtures match the declared schema | Registry implementation |
| OpenAPI | OpenAPI validator test and Ruby structural check | OpenAPI document conforms to validator-supported rules and required project paths exist | A live API exists |
| Dependency consistency | python -m pip check | Installed packages have no declared dependency conflicts | Package supply-chain integrity or vulnerability absence |
| Cross-platform bootstrap | GitHub Actions OS matrix | Setup scripts and contract tests run on declared OS labels | All developer machines or arbitrary OS versions |
| CI | GitHub Actions on exact commit | Configured checks ran and passed on that commit | Runtime, security or production readiness |
| Runtime | NOT IMPLEMENTED | No claim | Must be built and independently tested later |

## 6. Clean-run acceptance

A clean checkout meets this tooling baseline when it:

1. Uses Python 3.12.x.
2. Creates a new project-local virtual environment.
3. Installs the declared direct dependency set without relying on global developer packages.
4. Passes strict JSON validation.
5. Passes pip check.
6. Runs all contract tests with python -m pytest -q.
7. Returns a non-zero exit code for malformed JSON/schema/fixture/OpenAPI documents.
8. Produces successful GitHub Actions evidence against the exact PR head SHA on all three declared operating-system labels.

## 7. Security and maintenance

- Do not store credentials, cloud config, .env secrets or production data in this repository.
- Keep .venv, caches and test artifacts out of Git.
- Review pinned direct dependencies for security updates before changing them.
- Dependency upgrades must update direct pins and pass the full cross-platform validation suite.
- Add a transitive hash lock before the toolchain becomes part of a production software-supply-chain assurance claim.
- Expand this environment into the application development environment only after backend/database/infrastructure ADRs are accepted.
