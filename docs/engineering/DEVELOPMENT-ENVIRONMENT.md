# HSMART Development Environment — Contract Tooling Baseline

**Document ID:** HSMART-ENG-DEV-001  
**Version:** 1.2.0  
**Prepared:** 2026-11-22  
**Status:** CONTRACT TOOLING + KM 1 APPLICATION FOUNDATION IMPLEMENTED — POSTGRESQL CI AND INDEPENDENT EXIT REVIEW PENDING

## 1. Scope boundary

This document describes the existing contract-validation toolchain and the accepted KM 1 application-foundation environment. The application foundation contains a FastAPI process, SQLAlchemy persistence model, Alembic migration and PostgreSQL-backed outbox worker scaffold. It is not yet the Registry, public REST/MCP Gateway, arbitrary-code Runtime, Evaluation service, Synchronization Engine or a production deployment.

The toolchain uses the Python 3.12 minor line for JSON Schema and OpenAPI contract tests. It does not by itself approve the application backend framework.

## 2. Supported prerequisites

- Python 3.12.x (keep the same major/minor line locally and in CI; apply the latest security patch available for the platform).
- Git.
- Network access to install pinned development dependencies and the hash-locked application runtime from `requirements-dev.txt` and `requirements-app.lock` on first setup.
- Bash on macOS/Linux; PowerShell on Windows.
- No cloud account, API key, production database or provider credential is required for contract tests.

The Python 3.12 branch is in security-fixes-only maintenance. Python.org records 3.12.16 as the latest 3.12 security release on 2026-10-25 and notes that 3.12 installers ended at 3.12.10; therefore this project pins the minor line rather than pretending every operating system can install the same patch binary. CI records the actual patch version used. See https://www.python.org/downloads/release/python-31216/.

## 3. Bootstrap

### macOS / Linux

~~~bash
bash scripts/bootstrap-dev.sh
.venv/bin/python scripts/validate-json.py
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
~~~

### Windows PowerShell

~~~powershell
.\scripts\bootstrap-dev.ps1
.\.venv\Scripts\python.exe scripts\validate-json.py
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -q
~~~

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

**Dependency-lock boundary:** requirements-app.txt is the direct-pin input for the application runtime. requirements-app.lock is the generated transitive lock, including package hashes, and is consumed with pip's `--require-hashes` mode by the application image and PostgreSQL CI. The lock is compiled with pip-tools 7.7.0 under Python 3.12. requirements-dev.txt remains a direct-pin developer/test dependency file; this does not claim the complete development toolchain is hermetic or bit-for-bit reproducible. GitHub-hosted runner images are also mutable.

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


## 8. Accepted KM 1 application environment

ADR-011 v1.2.0 was accepted by GOV-01 on 2026-11-22. The application foundation uses Python 3.12.x, FastAPI/Uvicorn, PostgreSQL 16, SQLAlchemy 2.0/Alembic, PostgreSQL transactional outbox, OCI packaging, environment-driven settings and a separate worker process.

Files:
- `requirements-app.txt` — direct application dependency constraints used to compile the runtime lock.
- `requirements-app.lock` — generated transitive runtime lock with hashes; the container installs it using `pip --require-hashes`.
- `src/hsmart_platform/` — health/readiness API, database/session factory, tenant and outbox models, outbox functions and worker.
- `alembic/` and `alembic.ini` — versioned migration.
- `Dockerfile`, `compose.yaml`, `.env.example` — local container topology; no production credentials or endpoints included.
- `.github/workflows/km1-application.yml` — PostgreSQL 16 integration job.

The outbox enforces idempotency within a tenant, supports claim/retry/dead-letter behavior, and never acknowledges an unhandled topic as processed. KM 1 intentionally defines no business event handlers.

### Local verification record

- `PYTHONPATH=src python -m pytest -q`: **11 passed, 2 skipped**.
- Both skipped tests require a real PostgreSQL connection and run in the dedicated CI job.
- `alembic upgrade head` migration smoke passed on SQLite only.
- `python scripts/repository-governance-review.py`: PASS for deterministic policy/secret-pattern checks only.
- Local runtime was Python 3.13.5, not the supported Python 3.12 line. No Docker/PostgreSQL service was available locally.

This is local implementation evidence, not proof that hosted Python 3.12/PostgreSQL 16 CI passed.

### Clean application bootstrap (Python 3.12)

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install --require-hashes -r requirements-app.lock
python -m pip check
export PYTHONPATH=src
export DATABASE_URL=postgresql+psycopg://<user>:<password>@localhost:5432/<database>
alembic upgrade head
python -m pytest -q
```

On Windows, activate `.venv\\Scripts\\Activate.ps1` and set `$env:PYTHONPATH="src"`. Use a local secret store or environment variable for credentials; never commit them.

### Disposable database migration lifecycle

Run the following only against a disposable local development database. `alembic downgrade base` removes the schema managed by this application; never point it at a shared, staging or production database.

```bash
alembic upgrade head
alembic downgrade base
alembic upgrade head
alembic current
```

The PostgreSQL 16 CI job runs this apply → rollback → re-apply sequence before the application tests. A successful `upgrade head` after the rollback is required before the tests execute.

## 9. KM 1 boundary and non-claims

This foundation does **not** implement or accept the Capability Registry, external REST/Remote MCP Gateway, OIDC or production API-key issuance, arbitrary publisher code execution, hardened sandbox runtime, production Evaluation/Observability, WORM audit, synchronization/rollback engine, production hosting, backup restoration, disaster recovery or security certification.

KM 2 Registry may start only after PostgreSQL 16 CI, independent KM 1 evaluation and explicit GOV-01 KM 1 acceptance are complete.
