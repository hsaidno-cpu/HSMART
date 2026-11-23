# HSMART Repository Governance — Main Branch Controls

**Document ID:** HSMART-GOV-REPO-001  
**Version:** 1.0.0  
**Prepared:** 2026-11-22  
**Status:** TARGET CONTROL SPECIFICATION — CONFIGURATION NOT YET APPLIED  
**Authority:** Project Charter v1.0.2 and GOV-01 internal project authority  
**Target:** hsaidno-cpu/HSMART, branch main

---

## 1. Verified current state

At the inspected baseline main @ e796b5842f98277716fc5d81026ac175d0591f36, GitHub reported:
- main protected = false;
- branch protection enabled = false;
- required status checks = not enforced.

The repository currently has a Specification Validation workflow with these job names:
- Contract tests (ubuntu-24.04)
- Contract tests (windows-2025)
- Contract tests (macos-15)
- OpenAPI and required repository files

A green workflow run is evidence only for the exact commit and jobs that ran. The workflow is not a replacement for repository-level merge restrictions.

## 2. Required ruleset for main

Create an active branch ruleset targeting only main with the following controls:

| Control | Required setting | Reason |
|---|---|---|
| Pull request before merge | Required | No direct-to-main changes |
| Required approvals | At least 1 independent human approval | Separate author from reviewer |
| Dismiss stale approvals | Enabled | New commits invalidate old approval context |
| Latest push approval | Required where supported | Reviewer must examine the latest change |
| Required status checks | All four job names listed above | Contract and repository validation |
| Branch up to date | Required | Validate against current main |
| Conversation resolution | Required | No unresolved review discussions |
| Force pushes | Prohibited | Preserve branch history and review trace |
| Branch deletion | Prohibited for main | Preserve canonical branch |
| Bypass list | Empty or tightly controlled and human-only | No AI/delegate bypass around review gates |
| Administrator enforcement | Include administrators where supported | Avoid silent owner bypass |

Do not add an AI delegate, GitHub App or automation identity to the bypass list. AI profiles may prepare a branch or PR only within an explicit task-scoped authorization. They may not merge main or alter repository governance.

## 3. Independent reviewer prerequisite

A required approval cannot be supplied by the PR author. Before enforcing one required approval, ensure that at least one trusted, qualified human reviewer has repository review access and accepts the responsibility.

If no independent reviewer is available:
- Keep main protected against direct pushes, force pushes and deletion where those controls can be enforced.
- Do not pretend the independent-review gate is satisfied.
- Keep material governance/security PRs on HOLD until an acceptable review path exists.
- Do not use self-approval, an AI delegate, or a second account controlled by the author as a substitute for independent review.

## 4. Configuration procedure

A repository administrator should:
1. Open repository Settings.
2. Open Rules → Rulesets (or Branches → Branch protection rules where rulesets are unavailable).
3. Create an active ruleset targeting branch main.
4. Enable required pull requests, independent approval, stale approval dismissal, latest-push approval, required status checks, up-to-date branch, conversation resolution, and force-push/deletion prevention.
5. Add the four exact status-check job names from section 1.
6. Remove broad bypass permissions and include administrators in enforcement where supported.
7. Save the ruleset.
8. Re-fetch main branch/ruleset settings and test with a disposable PR that intentionally lacks one required check or approval.
9. Record ruleset identifier, configuration read-back, test PR URL and result.

## 5. Verification and change control

A control is VERIFIED only after GitHub itself reports it active and the negative enforcement test proves it blocks the prohibited operation.

A screenshot or written checklist alone is not enough if GitHub configuration read-back is available. If ruleset mutation/read-back capability is unavailable to the connected tooling, the status must remain NOT_APPLIED / NOT_VERIFIED until a repository administrator performs the procedure.

Any change to required checks must first inspect the live workflow job names. Do not copy names from a stale workflow version.

---

**Current disposition:** NOT_APPLIED / NOT_VERIFIED. This document describes the intended control; it does not claim that GitHub settings have been changed.
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

**Initial bootstrap before PR #28 is merged:** the workflow file is not yet on the default branch, so first apply must be run locally from a checkout of this branch. Create a fine-grained token or GitHub App installation token with repository `Administration: write`, store it in a local environment variable `GH_TOKEN`, and run:

```bash
export GH_TOKEN='<token entered locally, never into chat or source files>'
MAIN_SHA=$(git ls-remote origin refs/heads/main | cut -f1)
python scripts/github-governance.py apply-branch-protection --apply --confirm-main --expected-main-sha "$MAIN_SHA"
python scripts/github-governance.py apply-ruleset --apply --confirm-main --expected-main-sha "$MAIN_SHA"
unset GH_TOKEN
```

Then read back protection and rulesets and execute the negative-control verification in section 4. **After PR #28 merges**, store an appropriately scoped token as repository secret `HSMART_REPOSITORY_ADMIN_TOKEN` and run the `Repository Main Protection` `workflow_dispatch` workflow for subsequent status/dry-run/apply changes. It passes the secret transiently as `GH_TOKEN`; it never logs or writes the token. Never paste the token into ChatGPT, Notion or source files. Every write requires the current expected main SHA and a manual run by `hsaidno-cpu`.

## 4. Verification

After apply, independently read back branch protection and rulesets. Prove all seven required contexts, admin enforcement, no bypass, no force-push/deletion and pull-request-only updates. Personal-repository user/team/app push-restriction lists are not available. Run a disposable negative-control PR/branch to prove missing checks and forbidden pushes are blocked. Until these results exist, status remains NOT_APPLIED / NOT_VERIFIED.
