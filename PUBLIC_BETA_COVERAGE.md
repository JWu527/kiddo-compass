# Deep Research Coverage Matrix

本矩阵用于区分两件事：

1. 当前仓库是否已经达到 **OpenClaw skill 公测版** 目标。
2. 是否已经覆盖 deep research 报告中的 **完整产品化目标**。

状态说明：

- `Covered for skill beta`：在当前 skill 仓库范围内已经可用。
- `Partial`：已有骨架或第一版内容，但距离报告验收标准仍有差距。
- `Deferred`：报告中有要求，但依赖 App / 小程序 / 账号 / 存储 / 支付 / 专家资源，当前版本不实现。
- `Not covered`：尚未在当前仓库中形成明确产出。

## High Priority

| ID | Report item | Current coverage | Evidence in repo | Remaining gap |
| --- | --- | --- | --- | --- |
| H-01 | 去种子化并清空真实家庭数据 | Covered for internal beta gate | `.gitignore` / `.clawhubignore` exclude runtime files; `.example.md` templates use privacy-friendly fields; `skill-package-manifest.txt` and `scripts/release_guardrails.py` enforce whitelist packaging and privacy scanning. | Public release still requires P0 conversation regression evidence. |
| H-02 | 监护人同意、隐私规则与数据权利闭环 | Deferred | `SKILL.md` and README document data minimization and local-only runtime files. | No consent UI, settings page, export/delete/revoke workflow, or opt-in controls. Requires product surface and legal copy review. |
| H-03 | 渐进式建档 | Covered for skill beta | `SKILL.md` now runs safety triage and temporary advice before optional five-round onboarding. | Future platform should measure first-answer time, completion rate, and satisfaction. |
| H-04 | 分离事实、推断、干预与结果的状态模型 | Partial | `references/state-schema.md` defines facts, hypotheses, interventions, outcomes, consent_flags, last_updated, and source_turn; examples now follow the schema. | No platform service, migration tool, or multi-user storage layer. |
| H-05 | 证据矩阵与内容校准层 | Covered for skill beta | `references/evidence-matrix.md` covers 30 high-frequency topics with age band, scene, evidence level, source category, reviewed_at, limits, and escalation thresholds. | Future work: deeper per-scenario traceability in long-form notes and ongoing source freshness checks. |
| H-06 | 年龄、场景与照护者三维路由 | Partial | `references/routing-guide.md` defines age bands, scenes, caregiver roles, and output modes. | Needs more route examples, stronger scene-to-card mapping, and regression checks proving different routes produce different advice. |
| H-07 | 安全分诊与升级机制前置 | Partial | `references/safety-triage.md` defines red/yellow/green triggers and response rules; `SKILL.md` loads it first. | Needs region-specific resource slots and an operations path for updating safety rules without changing core skill docs. |
| H-08 | 平台化状态层 | Deferred | Runtime file boundaries are documented for local use. | No `ProfileService`, `LogService`, `LearningService`, content IDs, storage failure handling, or platform-independent state interface. |
| H-09 | 埋点、质量评测与回归测试 | Covered for skill beta gate | `references/evaluation-set.jsonl` provides executable regression data; `scripts/release_guardrails.py` validates static P0 guardrails and regression schema; `scripts/beta_kpi_gate.py` checks evidence coverage, P0 count, language/mode coverage, red/yellow risk coverage, and privacy findings; `scripts/run_regression.py` can run Hermes forbidden-regex checks. | Platform work remains deferred: production events, BI dashboard, weekly quality report, and online replay sample process. |

## Medium Priority

| ID | Report item | Current coverage | Evidence in repo | Remaining gap |
| --- | --- | --- | --- | --- |
| M-01 | 扩充场景库并标准化深写样板 | Partial | `references/scenario-template.md` includes 20 public-beta scenario cards using the same fields. | Cards are public-beta operating cards, not full long-form content packs with source tags and tested variants. |
| M-02 | 可访问性与低认知负荷版本 | Covered for text beta | `references/dialogue-modes.md` and `references/accessibility-i18n.md` define ordinary, crisis, deep, review, full-intake, family-sharing, easy-read / TTS, Chinese, English, and bilingual templates. | UI accessibility checklist, large-touch controls, undo flows, and usability test records remain platform-dependent. |
| M-03 | 家庭协同能力产品化 | Partial | `scenario-template.md` includes family rule and grandparent communication cards; routing asks for shareable summaries. | No co-parent view, role permissions, share audit, or privacy-preserving collaboration workflow. |
| M-04 | 目标驱动学习路径 | Not covered | Existing `references/30-day-plan.md` and `learning-progress.example.md` remain static day-by-day plans. | Needs goal tracks such as sleep, feeding, separation, aggression, grandparent alignment, and method basics. |
| M-05 | 商业化包装与增长链路 | Deferred | Not in the current skill scope. | Requires product packaging, pricing, funnel analytics, trust page, payment/subscription capabilities. |

## Low Priority

| ID | Report item | Current coverage | Evidence in repo | Remaining gap |
| --- | --- | --- | --- | --- |
| L-01 | 专家网络与社区层扩展 | Deferred | Not in the current skill scope. | Requires vetted experts, moderation, credential display, legal review, and community governance. |

## Cross-Cutting Product Requirements

| Requirement | Current coverage | Gap |
| --- | --- | --- |
| KPI / events / dashboard | Covered for skill beta gate through `scripts/beta_kpi_gate.py`. | Production events, dashboards, weekly report, and retention/helpfulness metrics require a target platform. |
| Architecture diagrams | Partial through narrative routing docs. | No maintained architecture doc for orchestration, state service, evaluation service, and content service. |
| Legal and medical source freshness | Partial via reference links and publishing reminder. | Official materials should be rechecked before any public release or product implementation. |
| Public package safety | Covered for internal beta gate. | Public release must use the whitelist zip and pass P0 conversation regression; direct workspace zips remain unsafe. |

## Next Coverage Milestones

1. Add per-scenario evidence labels and escalation thresholds to all long-form scenario notes.
2. Replace static learning plan with goal-based tracks if learning paths enter public scope.
3. Draft a platform-state design before implementing any App / 小程序 / account-backed version.
4. Connect `references/evaluation-set.jsonl` to a semantic model-graded harness when available.
5. Add production KPI events only after a target platform and consent flow exist.
