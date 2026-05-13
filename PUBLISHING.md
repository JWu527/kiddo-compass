# Publishing

本文档记录 Kiddo Compass 作为 OpenClaw / ClawHub skill 的发布流程。

## 发布前检查

1. 确认 `SKILL.md` 存在，并包含 `name`、`description`、`version` 和 `metadata.openclaw`。
2. 确认 `child-profile.md`、`practice-log.md`、`learning-progress.md` 没有被 Git 跟踪。
3. 更新 `CHANGELOG.md`。
4. 检查 `.clawhubignore` 是否覆盖运行期私人文件。
5. 检查没有真实孩子、家庭、联系方式或密钥信息。
6. 抽样跑 `references/evaluation-set.md`，确认安全分诊、渐进建档和中英文路由符合预期。
7. 对照 `PUBLIC_BETA_COVERAGE.md`，确认本次发布没有把 `Partial` 或 `Deferred` 项误写成已完成。

```bash
git status --short --ignored
git ls-files child-profile.md practice-log.md learning-progress.md
ruby -ryaml -e 's=File.read("SKILL.md"); fm=s.match(/\A---\n(.*?)\n---/m)[1]; data=YAML.safe_load(fm); abort("missing skill metadata") unless data["name"] && data["description"] && data["version"] && data.dig("metadata","openclaw","skillKey"); puts "frontmatter ok"'
ruby -e 'Dir["**/*.md"].each { |f| File.read(f).scan(/\[[^\]]+\]\(([^)]+)\)/).flatten.each { |link| next if link =~ /\Ahttps?:/; target=link.split("#",2)[0]; next if target.empty?; path=File.expand_path(target, File.dirname(f)); abort("missing #{target} referenced from #{f}") unless File.exist?(path) } }; puts "markdown local links ok"'
rg -n "真实姓名[:：]\\S|精确生日[:：]\\S|手机号[:：]?\\s*[0-9]|电话[:：]?\\s*[0-9]|地址[:：]\\S|学校[:：]\\S|token\\s*=|api[_-]?key\\s*=|password\\s*=|secret\\s*=" .
```

`git ls-files` 对私人文件应无输出。隐私扫描命令如有输出，需要逐条确认是否为真实私人数据；发布检查命令本身、隐私说明文字不算泄露。

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
