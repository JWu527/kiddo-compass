# Security Policy

Kiddo Compass 是本地运行的育儿知识 skill。它不需要 API key、外部账号或系统命令依赖，但它会引导 agent 维护孩子画像、实践日志和学习进度，因此隐私保护是主要安全边界。

## 支持版本

当前维护 `main` 分支和最新发布版本。

## 报告问题

如果你发现以下问题，请通过 GitHub issue 或私下联系维护者报告：

- 仓库或发布包中包含真实孩子、家庭、学校、地址、电话等私人信息。
- 说明中诱导 agent 泄露本地画像或实践日志。
- 文档绕过专业边界，替代医学诊断或心理治疗。
- 发布包包含不必要的脚本、可执行文件或隐藏依赖。
- ClawHub 元数据与实际能力不一致。

公开 issue 中请不要粘贴真实家庭数据。可以使用脱敏示例或 `.example.md` 模板字段。

## 隐私边界

以下文件必须只存在于用户本地的私有 state root（平台私有 storage 或 `.kiddo-compass-state/`）：

```text
.kiddo-compass-state/child-profile.md
.kiddo-compass-state/practice-log.md
.kiddo-compass-state/learning-progress.md
```

维护者和贡献者应只提交：

```text
child-profile.example.md
practice-log.example.md
learning-progress.example.md
```

## 专业边界

本项目不能替代儿科、儿童心理、精神健康或家庭治疗等专业服务。遇到 `SKILL.md` 中列出的自伤、严重攻击、发展迟缓、疑似神经发育问题、创伤、进食或睡眠障碍等信号时，agent 必须建议用户寻求专业帮助。

## 发布安全检查

发布前建议运行：

```bash
git status --short --ignored
python3 scripts/release_guardrails.py check
python3 scripts/release_guardrails.py list
python3 scripts/build_release_package.py --output dist/kiddo-compass.zip
python3 scripts/release_guardrails.py inspect dist/kiddo-compass.zip
rg -n "token|api[_ -]?key|password|secret|手机号|电话|地址|身份证|真实姓名" .
rg -n "child-profile.md|practice-log.md|learning-progress.md|.kiddo-compass-state" .gitignore .clawhubignore
```

如果使用 ClawHub 发布，请先通过 `skill-package-manifest.txt` 生成白名单包，确认私人运行期文件没有进入发布包。不要直接压缩整个工作区。
