# Changelog

本项目遵循 semver。面向 ClawHub 发布时，每个版本都应记录主要变化和迁移注意事项。

## Unreleased

### Added

- `HERMES_TEST_CASES.md`：Hermes 手动测试案例，覆盖冒烟、路由、安全、隐私、双语和措辞红线。
- `skill-package-manifest.txt`、`scripts/release_guardrails.py`、`scripts/beta_kpi_gate.py` 和 `scripts/run_regression.py`：公开包白名单打包、隐私扫描、beta KPI gate、JSONL 回归 schema 检查和 Hermes forbidden-regex runner。
- `references/state-schema.md`：本地状态 facts / hypotheses / interventions / outcomes / consent_flags 结构和错误处理规则。
- `references/evaluation-set.jsonl`：P0/P1 可执行回归数据格式。
- `references/dialogue-modes.md` 和 `references/accessibility-i18n.md`：对话模式、中文/英文/双语和 TTS 友好模板。
- `scripts/build_release_package.py`：统一白名单 release zip 入口，并在打包后检查实际 artifact。
- `references/quality-monitoring.md`、`references/learning-tracks.md` 和 `OPS.md`：补齐质量事件、目标驱动学习、owner、来源巡检和事故处置流程。
- `.github/workflows/public-beta.yml`：把单元测试、release guardrails、beta KPI、白名单打包、artifact inspect 和 regression scoring 接入 GitHub Actions。
- `references/platform-integration.md`、`scripts/state_service.py`：补 App / 小程序 consent UI、数据权利、角色权限和本地状态服务参考实现。
- `references/regional-resources.json`、`scripts/source_freshness.py`：补地区安全资源占位库和来源巡检门禁。
- `references/deep-scenario-packs.md`、`scripts/semantic_score.py`、`scripts/quality_dashboard.py`：补 P1/P2 深场景包、回归报告断言汇总和本地 beta dashboard。
- `scripts/run_regression.py`：增加 OpenClaw infer / OpenClaw agent runner，支持 profile、model、agent 和逐 case session 前缀，作为 Hermes 不可用时的 P0 回归 fallback。
- `references/feature-status.md`：用 Implemented / Spec-only / Deferred 标注真实能力状态，避免把平台契约写成已上线功能。
- `scripts/weekly_quality_report.py`：从 beta KPI 和 OpenClaw 回归 JSON 生成本地 Markdown 周度质量报告。
- `references/methodology.md`：新增压缩 runtime 方法论，只保留先安全、先行动、最少追问、不诊断不贴标签等行为规则。
- `archive/legacy-learning-path.md`：迁移旧固定 30 天课程，明确仅作自学参考，不是默认学习路径。
- `references/source-registry.json`：新增官方和内部来源注册表，为 evidence matrix 的 `source_id` 提供可追溯 URL 或内部引用。
- `scripts/release_gate.py` 和 `make release-gate`：新增 public-beta 统一发布门禁，串联单元测试、guardrails、source freshness、P0 regression、semantic score、audit bundle 构建、inspect 和白名单比对。
- `references/source-registry.json`：新增 WHO 育儿干预指南、Quail & Ward 2022/2023 研究综述、CEBC 项目证据评估、PDEP 第四版手册五条独立证据来源；独立证据与 Positive Discipline 品牌方法来源分流，PDEP 标注为独立项目。
- `references/evidence-matrix.md` + `scripts/beta_kpi_gate.py`：证据分类新增 `research-review`、`evidence-clearinghouse`，并补一条可追溯的“非暴力管教方法选择”方法级行。
- `references/scenario-template.md`：新增“家庭问题解决会议”场景卡；`references/learning-tracks.md`：新增 `family-problem-solving` 目标驱动 track。
- `references/evaluation-set.jsonl` + `scripts/run_regression.py`：新增 7 条确定性行为回归用例（表扬情境、变相惩罚、照护者修复、幼儿家庭会议、青少年自主、动机假设、感官过载）及对应 case 指引。
- `scripts/release_guardrails.py`：打包黑名单增加 `.handoff/` 与 `.pdf`，防止本地研究资料或 PDF 进入发布包。

### Changed

- `SKILL.md` description 压缩到 prompt 预算内，长触发词改由 README 和 routing docs 承接。
- 渐进式建档默认只问可选昵称和年龄段，不再询问出生时间；精确生日仅在发育阈值判断确有需要且用户主动提供时使用。
- 运行态数据边界改为平台私有 storage 或 `.kiddo-compass-state/`，skill 根目录只保留示例模板。
- `references/state-schema.md` 升级为 Household / ChildProfile / Case / Intervention / Outcome / ConsentLog / LearningTrack schema，并补充查看、导出、更正、删除和匿名化操作。
- `references/routing-guide.md` 增加 intent taxonomy、slot schema、route precedence 和 decision table。
- `scripts/run_regression.py` 默认加载当前仓库路径的 skill，避免误测已安装副本；同时识别 provider/API 失败、支持 required regex 和 JSON 报告。
- `references/evidence-matrix.md` 扩展到 30 个高频主题，并补充年龄段、证据等级、source_id、source_title、issuer、source_ref、reviewed_at、next_review_at、适用边界和升级阈值。
- `study-private/chapter-03-birth-order.md` 与 `study-private/chapter-04-misbehavior.md` 将高风险定性表述改成非诊断、非定型的启发式镜头。
- `references/scenario-template.md` 的 20 个公测场景卡补充显式 `Evidence:` 标签，并由 `scripts/beta_kpi_gate.py` 检查证据、风险、升级阈值和低负荷字段。
- `archive/methodology.md` 明确默认骨架为安全、发展/身体/环境校准、关系与边界、技能训练，并把“四个错误目的”降级为学习或深度复盘的可选解释层。
- `references/accessibility-i18n.md` 增加 one-sentence、easy-read / TTS、standard、deep mode 的低认知负荷验收标准。
- 安全分诊补充诊断请求、攻击/自伤、睡眠、语言和如厕退行阈值；HEARTBEAT 巡检降级为可选集成。
- README 和发布文档明确当前为内部测试 / public-beta candidate，公开发布必须通过白名单包和 P0 回归。
- `scripts/beta_kpi_gate.py` 扩展为检查 CI、平台契约、深场景包、地区资源、状态服务、dashboard 和来源巡检脚本。
- `.github/workflows/public-beta.yml` 收敛为调用 `scripts/release_gate.py`，避免 CI 与本地发布检查分叉。
- `PUBLIC_BETA_COVERAGE.md` 和 `PUBLIC_BETA_KANBAN.md` 将剩余缺口重新区分为 skill beta 已覆盖、平台契约已覆盖和真实 App / 小程序延期项。
- `references/evaluation-set.jsonl` 增强英文诊断、中文建档和热线红线断言，拦截内部过程话术、中文混入英文答案和未验证热线号码。
- `archive/methodology.md` 保留旧长篇内部框架；runtime 不再使用强制称呼、固定结尾符号或单一照护者角色话术。
- `references/learning-tracks.md` 和 `examples/learning-progress.example.md` 统一为目标驱动 `LearningTrack` schema，复盘输出固定为结果、可能原因、只调整一个变量、下次观察指标。
- `references/safety-triage.md`、`references/evidence-matrix.md`、`references/scenario-template.md` 和 `references/evaluation-set.jsonl` 强化发展疑虑与成人失控场景边界：不诊断、不暴露内部分诊标签、不输出未验证号码，并按 generic-zh / generic-en / CN / SG 资源槽位给出本地路径。
- `references/methodology.md`、`references/accessibility-i18n.md`、`references/dialogue-modes.md`、`references/scenario-guide.md`、`references/grandparent-strategies.md` 和 `references/evaluation-set.jsonl` 收敛硬编码称呼、亲昵称谓和装饰符号依赖，补齐多照护者、formal、one-sentence、TTS 与危机场景风格门禁。
- `scripts/state_service.py`、`references/state-schema.md`、`references/platform-integration.md` 和 `references/feature-status.md` 对齐本地状态参考实现：支持 ChildProfile / Case / Intervention / Outcome / ConsentLog、写入确认摘要和 view/export/correct/delete/anonymize 数据权利操作，并明确平台级 UI、权限和账号能力仍为 Spec-only。
- `references/methodology.md`：强化先校准再用工具、动机只是假设、赞美看情境、后果要够格、内部术语不外露五条运行规则。
- `references/routing-guide.md`：`6+y` 区分学龄与青少年，仅在用户给出明确年龄或情境时按青少年引导，不改动持久年龄段取值。
- `references/scenario-template.md`：修订撒娇/重复要求、说谎/隐瞒、作业/练习抗拒、照护者吼叫与修复四张卡，去除固定动机归因，补充具体正向反馈与不强迫原谅。

## 0.4.2 - 2026-05-13

### Changed

- `SKILL.md` 和 `references/safety-triage.md` 增加地区资源红线：未验证前不提供具体热线、机构或电话号码，避免安全场景中凭记忆生成资源。

## 0.4.1 - 2026-05-13

### Changed

- `SKILL.md` 前置证据与措辞红线，禁止固定天数见效、"一定有效"和单一归因式话术。
- `archive/methodology.md` 增加默认输出的结果承诺禁区，适配 Hermes one-shot 测试发现的问题。

## 0.4.0 - 2026-05-13

### Added

- `PUBLIC_BETA_COVERAGE.md`：按 deep research 报告逐项记录 Covered / Partial / Deferred / Not covered。
- `references/scenario-template.md` 扩展为 20 个公测版高频场景卡。

### Changed

- `PUBLIC_BETA_KANBAN.md` 状态从全量 `Done` 校准为 `Done (skill beta)`、`Partial` 和 `Deferred`。
- `SKILL.md` 版本更新为 `0.4.0`，并要求补档后先让用户确认事实。
- 清理旧 reference 中部分保证效果、绝对化和过强承诺式表述。
- `PUBLISHING.md` 发布命令与检查清单同步更新到 `0.4.0`。

## 0.3.0 - 2026-05-13

### Added

- 公测版优化看板 `PUBLIC_BETA_KANBAN.md`。
- `references/safety-triage.md`：红/黄/绿安全分诊。
- `references/routing-guide.md`：年龄、场景、照护者三维路由。
- `references/evidence-matrix.md`：睡眠、喂养、如厕、攻击、分离的证据校准层。
- `references/scenario-template.md`：高频场景四层卡片模板和家庭协同卡片骨架。
- `references/evaluation-set.md`：中英文路由、安全分诊、渐进建档轻量评测集。

### Changed

- `SKILL.md` 主流程改为安全分诊优先、先答后补档、再反馈记录。
- 示例孩子画像模板改为隐私友好字段，默认使用昵称和年龄段。
- 发布检查清单增加 YAML、链接、隐私扫描和评测集抽样。

## 0.2.0 - 2026-05-13

### Added

- 英文 README，方便海外父母和 ClawHub 浏览者理解安装、使用和隐私边界。
- `references/english-response-guide.md`，支持自然英文和中英双语 positive parenting 回答。
- `SKILL.md` 语言模式规则：中文提问中文答，英文提问英文答，明确要求时双语答。

### Changed

- 发布示例版本更新为 `0.2.0`。

## 0.1.0 - 2026-05-13

### Added

- 初始公开 skill 文档集。
- `SKILL.md` OpenClaw metadata 和版本号。
- README、贡献指南、安全策略、发布流程、行为准则和 MIT-0 许可证。
- `.clawhubignore`，避免运行期私人文件进入发布包。

### Notes

- 运行期私人文件为 `child-profile.md`、`practice-log.md` 和 `learning-progress.md`，只应保存在本地。
