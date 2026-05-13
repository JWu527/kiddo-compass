# Publishing

本文档记录 Kiddo Compass 作为 OpenClaw / ClawHub skill 的发布流程。

## 发布前检查

1. 确认 `SKILL.md` 存在，并包含 `name`、`description`、`version` 和 `metadata.openclaw`。
2. 确认公开包使用 `skill-package-manifest.txt` 白名单打包，不直接发布整个工作区。
3. 确认 `child-profile.md`、`practice-log.md`、`learning-progress.md` 没有被 Git 跟踪，也不在 manifest 中。
4. 更新 `CHANGELOG.md`。
5. 检查 `.gitignore`、`.clawhubignore` 和 manifest 是否覆盖 `.git/`、`__MACOSX/`、`._*`、`.env*`、`*.log`、`*.private.md`。
6. 运行发布前隐私与红线扫描。
7. 抽样跑 `references/evaluation-set.md` 或用 `references/evaluation-set.jsonl` 接入回归 harness，确认 P0 对话用例 100% 通过。
8. 对照 `PUBLIC_BETA_COVERAGE.md`，确认本次发布没有把 `Partial` 或 `Deferred` 项误写成已完成。

```bash
git status --short --ignored
git ls-files child-profile.md practice-log.md learning-progress.md
python3 scripts/release_guardrails.py check
python3 scripts/beta_kpi_gate.py
python3 scripts/release_guardrails.py list
python3 scripts/run_regression.py --priority P0
ruby -ryaml -e 's=File.read("SKILL.md"); fm=s.match(/\A---\n(.*?)\n---/m)[1]; data=YAML.safe_load(fm); abort("missing skill metadata") unless data["name"] && data["description"] && data["version"] && data.dig("metadata","openclaw","skillKey"); puts "frontmatter ok"'
ruby -e 'Dir["**/*.md"].each { |f| File.read(f).scan(/\[[^\]]+\]\(([^)]+)\)/).flatten.each { |link| next if link =~ /\Ahttps?:/; target=link.split("#",2)[0]; next if target.empty?; path=File.expand_path(target, File.dirname(f)); abort("missing #{target} referenced from #{f}") unless File.exist?(path) } }; puts "markdown local links ok"'
python3 scripts/release_guardrails.py package --output dist/kiddo-compass.zip
```

`git ls-files` 对私人文件应无输出。`release_guardrails.py` 会从白名单生成包文件列表，扫描隐私过采集、近诊断词、固定天数承诺、未验证热线和单因果标签。失败时不要发布。

当前仓库可保留本地运行期文件供维护者测试，但公开 artifact 必须来自白名单 zip，而不是直接压缩整个目录。

## 版本规则

使用 semver：

- `patch`: 修正错别字、细节说明、非行为性文档调整。
- `minor`: 新增 reference、工具卡、场景或兼容性 metadata。
- `major`: 改变初始化流程、输出协议或运行期文件结构。

`SKILL.md` 中的 `version` 应与发布命令使用的版本保持一致。

## ClawHub 发布

安装并登录 ClawHub CLI：

```bash
npm i -g clawhub
clawhub login
```

官方当前文档使用 `clawhub skill publish`。如果本机 CLI 较旧，`clawhub skill publish --help` 不存在时，使用兼容命令 `clawhub publish`。

发布单个 skill（新版 CLI）：

```bash
clawhub skill publish . \
  --slug kiddo-compass \
  --name "Kiddo Compass" \
  --version 0.4.2 \
  --changelog "Add safety guardrails against unverified region-specific hotline or agency numbers." \
  --tags latest,parenting,positive-parenting,bilingual,public-beta
```

发布单个 skill（旧版 CLI）：

```bash
clawhub publish . \
  --slug kiddo-compass \
  --name "Kiddo Compass" \
  --version 0.4.2 \
  --changelog "Add safety guardrails against unverified region-specific hotline or agency numbers." \
  --tags latest,parenting,positive-parenting,bilingual,public-beta
```

如果只想预览本地会被扫描到的 skill，可使用：

```bash
clawhub sync --dry-run --all
```

某些旧版 CLI 即使 dry run 也要求先登录。如果看到 `Not logged in. Run: clawhub login`，先登录后再重试。

## OpenClaw 用户安装命令

发布后，用户可以通过 OpenClaw 原生命令安装：

```bash
openclaw skills search "kiddo compass"
openclaw skills install kiddo-compass
```

更新：

```bash
openclaw skills update --all
```

## 发布后检查

- 打开 ClawHub 页面检查 `description`、tag、版本号和文件列表。
- 确认安全扫描没有报告 metadata mismatch。
- 从一个干净工作区安装并开启新会话，确认触发词和首次初始化流程正常。
- 检查 README 中的安装命令仍然准确。
