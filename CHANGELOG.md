# Changelog

本项目遵循 semver。面向 ClawHub 发布时，每个版本都应记录主要变化和迁移注意事项。

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
- `references/english-response-guide.md`，支持自然英文和中英双语 Positive Discipline 回答。
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
