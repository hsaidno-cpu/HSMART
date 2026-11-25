# HSMART Integration Contract: Human Approval & Action Notifications

**Document ID:** HSMART-GOV-HAP-01  
**Version:** 1.0.0-draft  
**Date:** 2026-11-25  
**Status:** Proposed integration requirement; must be accepted through the existing HSMART PR/KM gates.

## 1. Canonical procedure

HSMART adopts the shared ecosystem procedure defined in the HSO canonical governance document:

[HSO Human Approval, Manual Action & Notification Procedure (HAP-01)](https://github.com/hsaidno-cpu/Hypersystem-Orchestrator/blob/main/governance/HUMAN-APPROVAL-AND-ACTION-NOTIFICATION-PROCEDURE.md)

This HSMART document is an integration contract, not a duplicate policy source. If details differ, the canonical HSO HAP-01 document governs operational notification format, action records, approval receipts and lifecycle behavior, subject to GOV-01 approval and repository/KM acceptance.

## 2. Authority invariant

- GOV-01, the project owner, is the sole human decision authority for owner-level HSMART–HSO–UEDE decisions.
- No second human engineering reviewer or separate human security approver is introduced.
- AI review, tests, CI and security checks are technical evidence only; they never impersonate a human GitHub approval.
- Silence, green CI, draft PR state or an agent's own report does not constitute approval.
- HSMART services and workers cannot modify their own approval policy, grant themselves privilege or accept their own critical changes.

## 3. Events that must stop for owner action

HSMART adapters and UEDE must request explicit GOV-01 approval before protected-branch merge where required, identity/access/policy/secret/audit changes, production deployment, destructive migration/deletion, KM gate acceptance or advancement, PRE baseline/acceptance modification, and autonomy-tier expansion.

A separate manual-action request is required when a human must complete an external login, account-level setting, credential configuration or GitHub UI step that the connected tooling cannot safely complete. Never request that secrets be pasted into chat or Notion.

## 4. Action notification requirements

Each notice must include:

- Action ID and priority;
- distinction between approval and manual operation;
- project, repository, PR/issue, branch, base and exact head SHA;
- direct URL plus exact UI path/tab/panel/button;
- reason, risk and consequence of action/inaction;
- numbered steps and expected result;
- forbidden premature actions;
- stale conditions and approval validity;
- Notion Human Action Inbox record URL;
- exact owner response or evidence required to close the action.

The canonical Notion register is [UEDE Human Action & Approval Inbox](https://app.notion.com/p/42399868397f8152b2b7d1bf8cc15712).

## 5. HSMART-specific gates

- A green PR check does not accept a KM gate.
- PR merge does not itself accept KM 0/KM 1 or authorize KM 2+.
- HSMART foundation-service activation remains subject to the applicable KM, security, deployment and live acceptance gates.
- If a branch/commit, base, dependency graph, ruleset, approval policy or PRE revision changes, mark the existing action record Stale and require a fresh state snapshot.
- A branch must not be deleted while an open PR, stacked PR or recovery path depends on it.

## 6. Response and record contract

All HSMART project responses must close with:
1. actual result and status;
2. exact evidence and links;
3. HUMAN ACTION REQUIRED, AWAITING EVIDENCE, or NO HUMAN ACTION REQUIRED;
4. risks and stop conditions;
5. one dependency-aware next-work recommendation;
6. one ready-to-copy next prompt in Indonesian.

When a manual action is needed, the AI must explain the exact GitHub/Notion UI location and steps, not merely say "please approve" or paste an unexplained link.

## 7. Implementation boundary

The Notion Human Action & Approval Inbox has been created. This document does not claim that a GitHub webhook listener, event verifier, approval receipt verifier, automatic GitHub issue/comment dispatcher or push notification channel is already deployed. Until a live end-to-end test passes, the active notification path is the assistant's explicit response plus the Notion action record. Automated notification is NOT_CONFIGURED.

## 8. Acceptance criteria

- [ ] HSMART and HSO point to the same canonical HAP-01 procedure.
- [ ] Only GOV-01 can authorize owner-level decisions.
- [ ] Owner-action notices include exact links and human-operable steps.
- [ ] Notion action records are idempotent and bound to exact commit state.
- [ ] Stale approvals are rejected after target changes.
- [ ] HSMART KM/security/production gates remain intact.
- [ ] No notification or service is claimed live without delivery evidence.
- [ ] Every HSMART project response includes a next-work recommendation and ready-to-copy next prompt.
