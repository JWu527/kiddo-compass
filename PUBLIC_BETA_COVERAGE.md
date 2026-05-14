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
| H-01 | 去种子化并清空真实家庭数据 | Covered for internal beta gate | `.gitignore` / `.clawhubignore` exclude runtime files and `.kiddo-compass-state/`; `.example.md` templates use privacy-friendly fields; `skill-package-manifest.txt`, `scripts/build_release_package.py`, and `scripts/release_guardrails.py inspect` enforce whitelist packaging and artifact scanning. | Public release still requires P0 conversation regression evidence. |
| H-02 | 监护人同意、隐私规则与数据权利闭环 | Covered for skill beta contract | `SKILL.md`, README, `references/state-schema.md`, `references/platform-integration.md`, and `scripts/state_service.py` document and exercise data minimization, consent logging, and view/export/correct/delete/anonymize operations. | Real consent UI, settings page, revoke toggle, and legal copy review require a target App / 小程序 surface. |
| H-03 | 渐进式建档 | Covered for skill beta | `SKILL.md` now runs safety triage and temporary advice before optional five-round onboarding. | Future platform should measure first-answer time, completion rate, and satisfaction. |
| H-04 | 分离事实、推断、干预与结果的状态模型 | Covered for skill beta contract | `references/state-schema.md` defines Household, ChildProfile, Case, Intervention, Outcome, ConsentLog, LearningTrack, `schema_version`, source types, operations, and state-root boundary; `scripts/state_service.py` provides a local reference implementation. | File locking, migrations, account-backed storage, and multi-user authorization remain platform implementation work. |
| H-05 | 证据矩阵与内容校准层 | Covered for skill beta gate | `references/evidence-matrix.md` covers 30 high-frequency topics with age band, scene, evidence_level, source_id, source_title, issuer, source_ref, reviewed_at, next_review_at, limits, and escalation thresholds; `references/source-registry.json` maps source_id to official URLs or internal refs; the 20 public-beta scenario cards carry explicit `Evidence:` labels; `scripts/source_freshness.py` checks source traceability and review freshness. | Future work: deeper per-scenario traceability in long-form notes and production content review tooling. |
| H-06 | 年龄、场景与照护者三维路由 | Covered for skill beta gate | `references/routing-guide.md` defines age bands, scenes, caregiver roles, intent taxonomy, slot schema, route precedence, and a decision table; `scripts/run_regression.py` and `scripts/semantic_score.py` provide route assertion hooks. | Stronger model-graded semantic comparisons still depend on a target model provider or evaluation service. |
| H-07 | 安全分诊与升级机制前置 | Covered for skill beta gate | `references/safety-triage.md` defines red/yellow/green triggers; `SKILL.md` loads it first; `references/regional-resources.json`, `scripts/source_freshness.py`, and `OPS.md` define resource hygiene and update operations. | Verified region-specific directories and platform-specific emergency-resource UI remain product work. |
| H-08 | 平台化状态层 | Covered for local reference | `references/platform-integration.md` defines the platform contract and `scripts/state_service.py` demonstrates the local service methods. | Real `ProfileService`, `LogService`, `LearningService`, content IDs, storage failure handling, and account-backed multi-user isolation remain platform implementation work. |
| H-09 | 埋点、质量评测与回归测试 | Covered for skill beta gate | `references/evaluation-set.jsonl` provides executable regression data; `.github/workflows/public-beta.yml` runs CI; `scripts/release_guardrails.py`, `scripts/beta_kpi_gate.py`, `scripts/run_regression.py`, `scripts/semantic_score.py`, `scripts/quality_dashboard.py`, and `scripts/weekly_quality_report.py` cover local gate, machine-readable reports, static dashboard, and Markdown weekly report; `references/quality-monitoring.md` defines beta review events and feedback taxonomy. | Production events, BI dashboard, and online replay sample process still require a platform telemetry stack and consent flow. |

## Medium Priority

| ID | Report item | Current coverage | Evidence in repo | Remaining gap |
| --- | --- | --- | --- | --- |
| M-01 | 扩充场景库并标准化深写样板 | Covered for skill beta | `references/scenario-template.md` includes 20 public-beta scenario cards; `references/deep-scenario-packs.md` adds deeper packs for sleep, feeding, toileting, aggression, separation, and grandparent alignment. | More variant testing and localization can continue after the first beta. |
| M-02 | 可访问性与低认知负荷版本 | Covered for text beta | `references/dialogue-modes.md` and `references/accessibility-i18n.md` define ordinary, crisis, deep, review, full-intake, family-sharing, easy-read / TTS, Chinese, English, bilingual templates, and low-load acceptance checks such as one-sentence and 3-6 line targets. | UI accessibility checklist, large-touch controls, undo flows, and usability test records remain platform-dependent. |
| M-03 | 家庭协同能力产品化 | Partial | `scenario-template.md` includes family rule and grandparent communication cards; routing asks for shareable summaries. | No co-parent view, role permissions, share audit, or privacy-preserving collaboration workflow. |
| M-04 | 目标驱动学习路径 | Covered for skill beta | `references/learning-tracks.md` defines goal-driven tracks for sleep, feeding, toileting, aggression, separation, grandparent alignment, and method basics with `LearningTrack.progress_state`; `references/deep-scenario-packs.md` supplies the first deeper practice content. | Real progress UI and reminders depend on platform storage and notification support. |
| M-05 | 商业化包装与增长链路 | Deferred | Not in the current skill scope. | Requires product packaging, pricing, funnel analytics, trust page, payment/subscription capabilities. |

## Low Priority

| ID | Report item | Current coverage | Evidence in repo | Remaining gap |
| --- | --- | --- | --- | --- |
| L-01 | 专家网络与社区层扩展 | Deferred | Not in the current skill scope. | Requires vetted experts, moderation, credential display, legal review, and community governance. |

## Cross-Cutting Product Requirements

| Requirement | Current coverage | Gap |
| --- | --- | --- |
| KPI / events / dashboard | Covered for skill beta gate through `scripts/beta_kpi_gate.py`, `scripts/quality_dashboard.py`, `scripts/weekly_quality_report.py`, and `references/quality-monitoring.md`. | Production events, dashboards, and retention/helpfulness metrics require a target platform. |
| Architecture diagrams | Covered for skill beta contract through routing, state, and `references/platform-integration.md`. | Full deployment diagrams remain platform-specific. |
| Legal and medical source freshness | Covered for skill beta gate via `references/source-registry.json`, `references/evidence-matrix.md`, `references/regional-resources.json`, `scripts/source_freshness.py`, and `OPS.md`. | Official materials should still be rechecked before public release or product implementation. |
| Public package safety | Covered for internal beta gate. | Public release must use the whitelist zip and pass P0 conversation regression; direct workspace zips remain unsafe. |

## Next Coverage Milestones

1. Connect `references/evaluation-set.jsonl` to a model-graded semantic harness when a target provider is chosen.
2. Implement real App / 小程序 consent UI, settings page, data-rights screens, and role enforcement.
3. Add production KPI events only after a target platform and consent flow exist.
4. Replace placeholder regional resources with reviewed region-specific directories before launching in any named market.
