# Kiddo Compass

Kiddo Compass 是一个 OpenClaw / AgentSkills 兼容的积极育儿陪伴 skill。它把原创实践卡、常见育儿场景、安全分诊、证据校准和可选练习路径组织成可被 AI agent 按需加载的本地知识库。

这个项目适合父母、照顾者和教育者在日常对话中获得更具体、更温和也更有边界的育儿回应。它不是医疗、心理诊断或治疗工具。

当前仓库处于内部测试 / public-beta candidate 阶段。未通过白名单打包、隐私扫描和 P0 回归前，不应公开发布。

[English README](README.en.md)

## 功能

- 按 `SKILL.md` 触发积极育儿陪伴能力。
- 公测版默认先安全分诊、先给临时建议，再邀请用户补充画像；完整 5 轮建档是可选路径。
- 按 `references/content-map.md` 区分 runtime-core、support、study-private 和 archive，普通首答只读取核心运行资料。
- 增加年龄、场景、照护者路由和证据校准层。
- 维护 deep research 覆盖矩阵，明确哪些已覆盖、部分覆盖或延期。
- 支持英文和中英双语积极育儿回答。
- 增加 easy-read / TTS 友好模式，适合崩溃现场和朗读。
- 根据用户意图按需读取安全、证据、场景、状态和语言指南。
- 默认学习路径使用目标驱动 `LearningTrack` schema，不再使用固定 30 天课程作为主路径。
- 在用户确认后，按平台私有 storage 或 `.kiddo-compass-state/` 维护本地状态；仓库内的参考实现使用 `.kiddo-compass-state/state.json`，宿主平台也可以映射为私有 Markdown/数据库结构。不可写时继续回答，不声称已记录。
- 写状态前区分 facts、hypotheses、interventions、outcomes 和 consent_flags。
- 用户数据默认本地私有、匿名化和最小化记录；任何写入前必须先复述将记录的事实并等待确认。
- 对自伤、严重攻击、发展迟缓、疑似神经发育问题等高风险信号保留专业边界。

## 目录结构

```text
kiddo-compass/
├── SKILL.md                         # OpenClaw / AgentSkills 入口
├── PUBLIC_BETA_KANBAN.md            # 公测版优化看板
├── PUBLIC_BETA_COVERAGE.md          # deep research 覆盖矩阵
├── references/                      # runtime-core 和必要 support 知识库
├── references/content-map.md
├── references/methodology.md
├── references/safety-triage.md
├── references/routing-guide.md
├── references/dialogue-modes.md
├── references/accessibility-i18n.md
├── references/evidence-matrix.md
├── references/source-registry.json
├── references/scenario-template.md
├── references/evaluation-set.md
├── references/evaluation-set.jsonl
├── references/english-response-guide.md
├── references/state-schema.md
├── references/platform-integration.md
├── references/regional-resources.json
├── references/deep-scenario-packs.md
├── study-private/                   # 私人学习笔记，不进入 runtime 或公开包
├── archive/                         # 历史材料，不进入 runtime 或公开包
├── scripts/beta_kpi_gate.py           # beta readiness KPI gate
├── scripts/build_release_package.py   # 白名单 release zip 入口
├── scripts/quality_dashboard.py       # 本地 beta dashboard 生成器
├── scripts/release_gate.py             # public-beta 统一发布门禁
├── scripts/release_guardrails.py       # 白名单打包和隐私扫描
├── scripts/run_regression.py           # Hermes JSONL 回归 runner
├── scripts/semantic_score.py           # 回归报告语义/断言结果汇总
├── scripts/source_freshness.py         # 来源和地区资源巡检
├── scripts/state_service.py            # 本地状态服务参考实现
├── scripts/weekly_quality_report.py    # 本地周度质量报告生成器
├── skill-package-manifest.txt          # 公开包文件白名单
├── examples/                          # 脱敏状态模板，不含真实家庭数据
│   ├── child-profile.example.md       # 私人画像模板
│   ├── practice-log.example.md        # 实践日志模板
│   └── learning-progress.example.md   # 学习进度模板
├── README.md
├── README.en.md
├── CONTRIBUTING.md
├── SECURITY.md
├── OPS.md
├── PUBLISHING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── manual-testing/HERMES_TEST_CASES.md # Hermes 非发布手动测试案例
├── LICENSE
└── .clawhubignore
```

运行期会在平台私有 storage 或 `.kiddo-compass-state/` 中生成下列私人文件。它们不是 skill runtime 的发布内容，不应留在仓库根目录，也不能进入 Git 或 ClawHub artifact。公开 artifact 必须通过 `make audit-bundle` / `skill-package-manifest.txt` 白名单生成，不能直接压缩整个工作区：

```text
.kiddo-compass-state/child-profile.md
.kiddo-compass-state/practice-log.md
.kiddo-compass-state/learning-progress.md
.kiddo-compass-state/state.json
```

仓库中只保留 `examples/*.example.md` 脱敏模板。模板只能使用占位符或虚构示例，不得复制真实儿童姓名、生日、学校、家庭结构、实践日志或学习进度。

## 安装

### OpenClaw 工作区安装

把本仓库放入 OpenClaw 工作区的 `skills/` 目录：

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/JWu527/kiddo-compass.git ~/.openclaw/workspace/skills/kiddo-compass
```

然后开启一个新的 OpenClaw 会话，让技能快照重新加载。

### ClawHub 安装

如果该 skill 已发布到 ClawHub，可使用 OpenClaw 原生命令安装：

```bash
openclaw skills search "kiddo compass"
openclaw skills install kiddo-compass
```

## 使用

在对话中提到 `Kiddo Compass`、`积极育儿`、`孩子不听话`、`温和而坚定`、`睡前冲突`、`发脾气`、`打人`、`不分享` 等话题即可触发。

用户用英文提问时默认英文回答；明确要求双语时输出简短中英双语版本。

首次使用时，agent 会先检查私有 state root 里的 `child-profile.md` 是否存在且完整。如果没有，公测版不会强制用户先完整建档，而是先给临时建议，再只追问 1-2 个必要问题。用户愿意继续时，才按 `SKILL.md` 中定义的 5 轮问答初始化孩子画像和实践日志。初始化信息只应保存在本地私人文件中，不应提交到开源仓库或发布到 ClawHub。

默认只问可选昵称和年龄段。精确生日、电话、学校、地址等敏感信息不会默认采集或持久化。

示例问题：

```text
Kiddo Compass，我家 3 岁孩子睡前一直拖延，讲完故事还要继续讲，怎么办？
```

```text
我想用积极育儿的方法处理孩子吃饭时扔食物的问题。
```

```text
帮我做一个每天 15 分钟的积极育儿练习路径。
```

```text
Kiddo Compass, my 3-year-old keeps asking for more stories at bedtime and cries when I stop. What should I do?
```

## 知识库导航

| 文件 | 用途 |
| --- | --- |
| `manual-testing/HERMES_TEST_CASES.md` | Hermes 非 runtime、非发布手动测试案例与发布前抽样建议 |
| `PUBLIC_BETA_KANBAN.md` | 公测版分阶段优化看板 |
| `PUBLIC_BETA_COVERAGE.md` | deep research 报告覆盖矩阵 |
| `references/content-map.md` | 内容分层地图，定义 runtime-core、support、study-private 和 archive |
| `references/methodology.md` | 压缩后的 runtime 行为规则：先行动、少理论、不贴标签 |
| `references/safety-triage.md` | 红/黄/绿安全分诊 |
| `references/routing-guide.md` | 年龄、场景、照护者路由 |
| `references/dialogue-modes.md` | 危机、普通建议、深度学习、复盘、intake、家庭共享和 easy-read 模式 |
| `references/accessibility-i18n.md` | 中文、英文、双语和 TTS 友好模板 |
| `references/evidence-matrix.md` | 睡眠、喂养、如厕、攻击、分离证据校准 |
| `references/source-registry.json` | 官方来源和内部来源的可追溯 source_id 注册表 |
| `references/scenario-template.md` | 高频场景卡片标准模板 |
| `references/evaluation-set.md` | 公测版轻量回归评测集 |
| `references/evaluation-set.jsonl` | 可执行回归数据格式 |
| `references/english-response-guide.md` | 英文和中英双语回应风格 |
| `references/state-schema.md` | 本地状态 schema 与错误处理 |
| `references/platform-integration.md` | App / 小程序接入的 consent UI、数据权利、账号权限和存储接口契约；平台 UI/权限为 Spec-only |
| `references/feature-status.md` | Implemented / Spec-only / Deferred 能力状态表，避免文档夸大 |
| `references/quality-monitoring.md` | 公测质量事件、反馈分类和周报抽样 |
| `references/learning-tracks.md` | 目标驱动学习路径 |
| `references/deep-scenario-packs.md` | P1/P2 深层场景包、复盘问题和升级边界 |
| `references/regional-resources.json` | 可巡检的地区安全资源占位库 |
| `references/scenario-guide.md` | 睡前、吃饭、哭闹等场景实操 |
| `references/grandparent-strategies.md` | 祖辈管教不一致场景 |
| `references/feedback-and-patrol.md` | 实践反馈和巡检闭环 |
| `OPS.md` | release owner、content owner、privacy owner、来源巡检和事故处置 |

仓库中保留的读书/学习笔记、章节式资料、工具清单和固定天数计划位于 `study-private/`，旧方法论材料位于 `archive/`。这两层不进入 runtime，也不进入公开发布白名单；需完成版权与定位审查后再决定是否公开。

旧固定 30 天课程已迁移到 `archive/legacy-learning-path.md`，只作为自学参考；默认学习进度模板位于 `examples/learning-progress.example.md`，使用 `goal_type`、`baseline`、`practice_action`、`review_metric`、`progress_state`、`completion_rule` 和 `last_reviewed_at`。

## 维护与验证

修改后建议执行：

```bash
git status --short
python3 scripts/release_guardrails.py check
python3 scripts/release_gate.py
python3 scripts/release_gate.py --regression-runner openclaw-agent --openclaw-profile kiddo-regression --openclaw-model zai/glm-5.1 --openclaw-agent main --openclaw-session-prefix kiddo-p0
python3 scripts/beta_kpi_gate.py
python3 scripts/run_regression.py --priority P0
python3 scripts/run_regression.py --priority P0 --report dist/regression-p0.json
python3 scripts/run_regression.py --runner openclaw-agent --openclaw-profile kiddo-regression --openclaw-model zai/glm-5.1 --openclaw-agent main --openclaw-session-prefix kiddo-p0 --priority P0 --timeout 180 --report dist/regression-p0-openclaw.json
python3 scripts/semantic_score.py --report dist/regression-p0.json
python3 scripts/semantic_score.py --report dist/regression-p0-openclaw.json
python3 scripts/source_freshness.py
make audit-bundle
python3 scripts/release_guardrails.py inspect audit-bundle/kiddo-compass-audit-bundle.zip
python3 scripts/beta_kpi_gate.py --json > dist/beta-kpi.json
python3 scripts/quality_dashboard.py --metrics dist/beta-kpi.json --regression dist/regression-p0-openclaw.json --output dist/quality-dashboard.html
python3 scripts/weekly_quality_report.py --metrics dist/beta-kpi.json --regression dist/regression-p0-openclaw.json --output dist/weekly-quality-report.md
python3 -m unittest tests/test_release_guardrails.py
rg -n "child-profile.md|practice-log.md|learning-progress.md|.kiddo-compass-state" .gitignore .clawhubignore README.md SKILL.md
rg -n "^---|^name:|^version:|^description:|^metadata:" SKILL.md
```

OpenClaw agent 回归需要先把 skill 安装或复制到对应 OpenClaw workspace 的 `skills/kiddo-compass/` 下。不要用指向仓库外部的 symlink；OpenClaw 会因 `symlink-escape` 跳过该 skill。

发布前还应确认：

- `SKILL.md` frontmatter 可以被 YAML 解析。
- 公开包不包含真实孩子画像、家庭信息、联系方式或其他私人内容。
- P0 JSONL/Hermes 回归 100% 通过。
- 新增 reference 已在 `SKILL.md` 或 README 的导航中说明何时读取。
- `PUBLIC_BETA_COVERAGE.md` 中的 `Partial` / `Deferred` 项没有被误标为已完成。
- `references/evaluation-set.md` 中的安全场景和渐进建档场景人工抽样通过。
- 变更记录已写入 `CHANGELOG.md`。

## 发布

发布到 ClawHub 的流程见 [PUBLISHING.md](PUBLISHING.md)。OpenClaw 官方文档说明，ClawHub 技能包以 `SKILL.md` 和支持文件为核心，发布时使用 semver 版本、tag 和 changelog 管理版本。

## 贡献

欢迎提交改进建议。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，尤其是隐私、专业边界和引用来源要求。

## 安全与隐私

请阅读 [SECURITY.md](SECURITY.md)。这个 skill 会在本地维护家庭和孩子相关的私人上下文，但这些文件不应该进入 Git 或 ClawHub 发布包。

## 许可证

本项目使用 [MIT-0](LICENSE) 许可证。ClawHub 当前对已发布 skills 使用 MIT-0 授权模型，因此仓库采用相同许可证以避免授权冲突。
