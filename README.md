# Kiddo Compass

Kiddo Compass 是一个 OpenClaw / AgentSkills 兼容的正面管教育儿 skill。它把《正面管教》学习笔记、阿德勒心理学基础、52 个工具卡、常见育儿场景和 30 天练习计划组织成可被 AI agent 按需加载的本地知识库。

这个项目适合父母、照顾者和教育者在日常对话中获得更具体、更温和也更有边界的育儿回应。它不是医疗、心理诊断或治疗工具。

[English README](README.en.md)

## 功能

- 按 `SKILL.md` 触发正面管教育儿顾问能力。
- 首次使用时通过 5 轮问答建立本地孩子画像。
- 公测版默认先安全分诊、先给临时建议，再邀请用户补充画像。
- 按 `references/methodology.md` 的 6 步框架分析育儿场景。
- 增加年龄、场景、照护者路由和证据校准层。
- 支持英文和中英双语 Positive Discipline 回答。
- 根据用户意图按需读取章节笔记、工具卡、场景指南、学习计划和 FAQ。
- 自动维护本地 `child-profile.md`、`practice-log.md` 和 `learning-progress.md`。
- 对自伤、严重攻击、发展迟缓、疑似神经发育问题等高风险信号保留专业边界。

## 目录结构

```text
kiddo-compass/
├── SKILL.md                         # OpenClaw / AgentSkills 入口
├── PUBLIC_BETA_KANBAN.md            # 公测版优化看板
├── references/                      # 按需加载的知识库
├── references/safety-triage.md
├── references/routing-guide.md
├── references/evidence-matrix.md
├── references/scenario-template.md
├── references/evaluation-set.md
├── references/english-response-guide.md
├── child-profile.example.md         # 私人画像模板
├── practice-log.example.md          # 实践日志模板
├── learning-progress.example.md     # 学习进度模板
├── README.md
├── README.en.md
├── CONTRIBUTING.md
├── SECURITY.md
├── PUBLISHING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── LICENSE
└── .clawhubignore
```

运行期会生成下列本地私人文件，仓库通过 `.gitignore` 和 `.clawhubignore` 避免发布它们：

```text
child-profile.md
practice-log.md
learning-progress.md
```

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

在对话中提到 `Kiddo Compass`、`正面管教`、`孩子不听话`、`温和而坚定`、`睡前冲突`、`发脾气`、`打人`、`不分享` 等话题即可触发。

用户用英文提问时默认英文回答；明确要求双语时输出简短中英双语版本。

首次使用时，agent 会先检查 `child-profile.md` 是否存在且完整。如果没有，公测版不会强制用户先完整建档，而是先给临时建议，再只追问 1-2 个必要问题。用户愿意继续时，才按 `SKILL.md` 中定义的 5 轮问答初始化孩子画像和实践日志。初始化信息只应保存在本地私人文件中，不应提交到开源仓库或发布到 ClawHub。

示例问题：

```text
Kiddo Compass，我家 3 岁孩子睡前一直拖延，讲完故事还要继续讲，怎么办？
```

```text
我想用正面管教处理孩子吃饭时扔食物的问题。
```

```text
帮我做一个每天 15 分钟的正面管教学习计划。
```

```text
Kiddo Compass, my 3-year-old keeps asking for more stories at bedtime and cries when I stop. What should I do?
```

## 知识库导航

| 文件 | 用途 |
| --- | --- |
| `PUBLIC_BETA_KANBAN.md` | 公测版分阶段优化看板 |
| `references/safety-triage.md` | 红/黄/绿安全分诊 |
| `references/routing-guide.md` | 年龄、场景、照护者路由 |
| `references/evidence-matrix.md` | 睡眠、喂养、如厕、攻击、分离证据校准 |
| `references/scenario-template.md` | 高频场景卡片标准模板 |
| `references/evaluation-set.md` | 公测版轻量回归评测集 |
| `references/methodology.md` | 场景分析主框架和输出规则 |
| `references/english-response-guide.md` | 英文和中英双语回应风格 |
| `references/core-concepts.md` | 正面管教核心理念 |
| `references/adler-psychology.md` | 阿德勒心理学和四个错误目的 |
| `references/tool-cards.md` | 52 个正面管教工具卡 |
| `references/scenario-guide.md` | 睡前、吃饭、哭闹等场景实操 |
| `references/grandparent-strategies.md` | 祖辈管教不一致场景 |
| `references/learning-map.md` | 学习地图 |
| `references/30-day-plan.md` | 30 天学习计划 |
| `references/feedback-and-patrol.md` | 实践反馈和巡检闭环 |
| `references/faq.md` | 常见问题速查 |
| `references/chapter-*.md` | 《正面管教》逐章学习笔记 |

## 维护与验证

修改后建议执行：

```bash
git status --short
rg -n "child-profile.md|practice-log.md|learning-progress.md" .gitignore .clawhubignore README.md SKILL.md
rg -n "^---|^name:|^version:|^description:|^metadata:" SKILL.md
rg -n "真实姓名[:：]\\S|精确生日[:：]\\S|手机号[:：]?\\s*[0-9]|电话[:：]?\\s*[0-9]|地址[:：]\\S|学校[:：]\\S|token\\s*=|api[_-]?key\\s*=|password\\s*=|secret\\s*=" .
```

发布前还应确认：

- `SKILL.md` frontmatter 可以被 YAML 解析。
- 不包含真实孩子画像、家庭信息、联系方式或其他私人内容。
- 新增 reference 已在 `SKILL.md` 或 README 的导航中说明何时读取。
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
