# HSMART Repository Governance — Main Branch Controls

**ID:** HSMART-GOV-REPO-001  
**Version:** 1.1.0  
**Target:** `hsaidno-cpu/HSMART`, branch `main`  
**Status:** TARGET CONFIGURATION — NOT APPLIED / NOT VERIFIED  
**Authority:** GOV-01; preparation and drift checks delegated to GOV-10

## 1. Verified baseline

After PR #13 merge, main was read back at `17c78dcd2ea59c6d40f9a07d188bab6f829f0596`; GitHub returned `protected=false`. The connected GitHub connector exposes GET reads for protection/rulesets but no write operation. This record does not claim the protection has been applied.

## 2. Required controls

Require a PR for main changes; strict required status checks for:
- `Contract tests (ubuntu-24.04)`
- `Contract tests (windows-2025)`
- `Contract tests (macos-15)`
- `OpenAPI and required repository files`
- `KM1 application integration (PostgreSQL 16)`
- `Repository Governance Review`

Also require up-to-date branch, resolved conversations, linear history and admin enforcement. Prohibit force pushes and branch deletion. Keep ruleset bypass actors empty. Restrict direct push access to the repository owner account `hsaidno-cpu` where branch-protection restrictions permit.

Native GitHub approving-review count is intentionally zero. GOV-11 and domain reviewers provide separate AI reports; they cannot be represented as native GitHub human approvals. GOV-01 retains final human merge authority.

## 3. Administrative operation

`scripts/github-governance.py` supports:
- `status`: read current protection and ruleset status.
- `apply-branch-protection`: dry-run by default; apply only with `--apply --confirm-main`.
- `apply-ruleset`: dry-run by default; create/update the named HSMART ruleset.

A repository administrator must provide `GH_TOKEN` or `GITHUB_TOKEN` with repository `Administration: write` in a local secure environment. Never paste the token into ChatGPT, Notion or Git. Every write requires the current expected main SHA.

## 4. Verification

After apply, independently read back branch protection and rulesets. Prove the six required contexts, admin enforcement, no bypass, no force-push/deletion and direct-push restrictions. Run a disposable negative-control PR/branch to prove missing checks and forbidden pushes are blocked. Until these results exist, status remains NOT_APPLIED / NOT_VERIFIED.
