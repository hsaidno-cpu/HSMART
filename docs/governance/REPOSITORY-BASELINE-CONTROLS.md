# HSMART Repository Governance — Main Branch Controls

**ID:** HSMART-GOV-REPO-001  
**Version:** 1.2.0  
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
- `AI Reviewer Evidence`

Also require up-to-date branch, resolved conversations, linear history and admin enforcement. Prohibit force pushes and branch deletion. Keep ruleset bypass actors empty. This is a personal repository. GitHub's branch-protection push-restriction list for named users/teams/apps is not available here; rely on required PRs, strict checks, admin enforcement and an empty bypass list.

Native GitHub approving-review count is intentionally zero. GOV-11's AI assurance report is verified by the `AI Reviewer Evidence` CI job, but neither the report nor that job is a GitHub-native approving review. GOV-01 retains final human merge authorization.

## 3. Administrative operation

`scripts/github-governance.py` supports:
- `status`: read current protection and ruleset status.
- `apply-branch-protection`: dry-run by default; apply only with `--apply --confirm-main`.
- `apply-ruleset`: dry-run by default; create/update the named HSMART ruleset.

A repository administrator must create a fine-grained token or GitHub App installation token with repository `Administration: write`, store it as the repository secret `HSMART_REPOSITORY_ADMIN_TOKEN`, and run the `Repository Main Protection` workflow. The workflow passes this secret transiently as `GH_TOKEN`; it never logs or writes the token. Never paste the token into ChatGPT, Notion or source files. Every write requires the current expected main SHA and a manual `workflow_dispatch` by `hsaidno-cpu`.

## 4. Verification

After apply, independently read back branch protection and rulesets. Prove all seven required contexts, admin enforcement, no bypass, no force-push/deletion and direct-push restrictions. Run a disposable negative-control PR/branch to prove missing checks and forbidden pushes are blocked. Until these results exist, status remains NOT_APPLIED / NOT_VERIFIED.
