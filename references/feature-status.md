# Feature Status

Use this file when README, coverage, Kanban, release notes, or user-facing descriptions might overstate what the current skill can actually do.

## Status Vocabulary

| Status | Meaning |
| --- | --- |
| Implemented | Enforced by `SKILL.md`, references, tests, scripts, CI, or release packaging in this repository. |
| Spec-only | Defined as a contract or operating rule, but requires a host App, mini program, OpenClaw setup, or manual maintainer action. |
| Deferred | Out of scope for the current skill beta. Do not imply it exists. |

## Current Status Map

| Capability | Status | Evidence / boundary |
| --- | --- | --- |
| Whitelist release packaging | Implemented | `skill-package-manifest.txt`, `scripts/build_release_package.py`, `scripts/release_guardrails.py inspect`. |
| Runtime private-file exclusion | Implemented | `.gitignore`, `.clawhubignore`, release guardrails, package inspect. |
| Safety triage before advice | Implemented | `SKILL.md`, `references/safety-triage.md`, P0 regression cases. |
| Gradual profile intake | Implemented | `SKILL.md`, `references/evaluation-set.jsonl`; default first round asks nickname + age band. |
| OpenClaw agent regression | Implemented | `scripts/run_regression.py --runner openclaw-agent` and `dist/regression-p0-openclaw.json` when generated locally. |
| Consent UI and data-rights UI | Spec-only | Contract in `references/platform-integration.md`; no real App or mini-program screen in this repo. |
| View/export/correct/delete/anonymize service | Implemented locally | `scripts/state_service.py` is a local reference implementation, not a production account service. |
| Account roles and multi-user isolation | Spec-only | Role model exists in `references/platform-integration.md`; enforcement requires platform storage and auth. |
| HEARTBEAT patrol | Spec-only | `references/feedback-and-patrol.md` defines optional behavior only when a host platform explicitly supports it. |
| Online monitoring / BI dashboard | Deferred | Local static dashboard exists; no production telemetry or real-user feedback loop. |
| Commercialization, expert network, community | Deferred | Not part of the current skill beta. |

## Writing Rule

When describing a capability, use this vocabulary:

- Implemented: "runs", "checks", "blocks", "generates", or "is enforced".
- Spec-only: "defines a contract", "requires platform support", or "is available as a local reference".
- Deferred: "out of current scope" or "requires a future product surface".

Avoid vague claims such as "自动维护", "完整支持", or "已接入线上监控" unless the capability is listed as Implemented above.
