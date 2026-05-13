# Contributing

感谢你愿意改进 Kiddo Compass。这个仓库是一个 OpenClaw / AgentSkills 兼容的 skill，贡献重点是让 agent 在真实育儿对话里更具体、更温和、更有边界。

## 贡献范围

欢迎提交：

- 更清晰的 `SKILL.md` 触发描述和工作流说明。
- 新增或修正 `references/` 下的正面管教笔记、场景指南和工具卡。
- 英文或中英双语回应指南，但要优先保持自然表达，不做生硬逐句直译。
- 更好的示例模板。
- 隐私、安全、专业边界相关改进。
- 拼写、结构和可读性修复。

不接受：

- 真实孩子、家庭、学校或联系方式等私人信息。
- 将正面管教包装成医学诊断、心理治疗或保证有效的方案。
- 与 `SKILL.md` 中专业边界冲突的建议。
- 大段未经授权复制的版权材料。

## 开发原则

1. 保持 `SKILL.md` 精简。核心流程放在入口文件，细节放进 `references/`。
2. 每个 reference 都要有明确用途，并能被 `SKILL.md` 或 README 导航到。
3. 回答风格应贴近日常父母对话，少用术语堆砌。
4. 场景建议必须具体，不写泛泛的“多陪伴、多沟通”。
5. 涉及高风险信号时，优先建议专业帮助。

## 本地私人文件

以下文件是运行期私人数据，只能本地存在，不得提交：

```text
child-profile.md
practice-log.md
learning-progress.md
```

如果需要展示结构，请修改对应的 `.example.md` 模板。

## 提交前检查

```bash
git status --short
rg -n "真实|姓名|出生日期|手机号|电话|地址|token|api[_ -]?key|password|secret" .
rg -n "^---|^name:|^version:|^description:|^metadata:" SKILL.md
```

如果修改了发布相关内容，也请检查：

```bash
rg -n "child-profile.md|practice-log.md|learning-progress.md" .gitignore .clawhubignore
```

## 文档风格

- 默认使用中文，必要时保留英文术语。
- 文件名使用小写字母、数字和连字符。
- Markdown 表格用于速查，不要让主流程被大表格淹没。
- 新增章节请补充“一句话总结”或“适用场景”，方便 agent 按需读取。

## Pull Request 清单

- [ ] 没有提交真实私人数据。
- [ ] `SKILL.md` frontmatter 仍然有效。
- [ ] 新增 reference 已被导航到。
- [ ] 专业边界没有被弱化。
- [ ] `CHANGELOG.md` 已更新。
