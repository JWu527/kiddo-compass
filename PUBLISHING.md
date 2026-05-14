# Publishing

本文档记录 Kiddo Compass 作为 OpenClaw / ClawHub skill 的发布流程。

## 发布前检查

public-beta candidate 必须通过下面的统一门禁生成：

```bash
python3 scripts/release_gate.py
```

该命令会先清理旧的 regression report 和旧 audit bundle，随后依次运行单元测试、release guardrails、beta KPI、source freshness、P0 regression、semantic score、audit bundle 构建、artifact inspect 和白名单内容比对。只有所有 hard-fail 检查通过后，`audit-bundle/kiddo-compass-audit-bundle.zip` 才可作为 public-beta candidate。

只需要构建白名单 audit bundle 时，也可以运行：

```bash
make audit-bundle
```

不要直接压缩整个工作目录，也不要把 `dist/`、`.git/`、根目录 live state、`.kiddo-compass-state/` 或其他 ignored 文件夹作为外发包。`scripts/release_gate.py` 和 `make audit-bundle` 都会使用 `skill-package-manifest.txt` 白名单生成 `audit-bundle/kiddo-compass-audit-bundle.zip`，并对实际 artifact 运行 `python3 scripts/release_guardrails.py inspect`。

1. 确认 `SKILL.md` 存在，并包含 `name`、`description`、`version` 和 `metadata.openclaw`。
2. 确认公开包使用 `skill-package-manifest.txt` 白名单打包，不直接发布整个工作区。
3. 确认根目录没有 `child-profile.md`、`practice-log.md`、`learning-progress.md`；真实数据只保存在 `.kiddo-compass-state/` 或平台私有 storage。
4. 更新 `CHANGELOG.md`。
5. 检查 `.gitignore`、`.clawhubignore` 和 manifest 是否覆盖 `.git/`、`__MACOSX/`、`._*`、`.env*`、`*.log`、`*.private.md`。
6. 运行发布前隐私、红线扫描和来源巡检；`references/evidence-matrix.md` 的 `source_id` 必须能在 `references/source-registry.json` 中找到。
7. 抽样跑 `references/evaluation-set.md` 或用 `references/evaluation-set.jsonl` 接入回归 harness，确认 P0 对话用例 100% 通过。
8. 确认 `.github/workflows/public-beta.yml` 与本地检查命令一致。
9. 对照 `PUBLIC_BETA_COVERAGE.md`，确认本次发布没有把平台依赖项误写成完整产品已完成。

```bash
git status --short --ignored
git ls-files child-profile.md practice-log.md learning-progress.md
test ! -e child-profile.md && test ! -e practice-log.md && test ! -e learning-progress.md
python3 scripts/release_guardrails.py check
python3 scripts/release_gate.py
python3 scripts/beta_kpi_gate.py
python3 scripts/source_freshness.py
python3 scripts/release_guardrails.py list
python3 scripts/run_regression.py --priority P0
python3 scripts/run_regression.py --priority P0 --report dist/regression-p0.json
python3 scripts/run_regression.py --runner openclaw-agent --openclaw-profile kiddo-regression --openclaw-model zai/glm-5.1 --openclaw-agent main --openclaw-session-prefix kiddo-p0 --priority P0 --timeout 180 --report dist/regression-p0-openclaw.json
python3 scripts/semantic_score.py --report dist/regression-p0.json
python3 scripts/semantic_score.py --report dist/regression-p0-openclaw.json
ruby -ryaml -e 's=File.read("SKILL.md"); fm=s.match(/\A---\n(.*?)\n---/m)[1]; data=YAML.safe_load(fm); abort("missing skill metadata") unless data["name"] && data["description"] && data["version"] && data.dig("metadata","openclaw","skillKey"); puts "frontmatter ok"'
ruby -e 'Dir["**/*.md"].each { |f| File.read(f).scan(/\[[^\]]+\]\(([^)]+)\)/).flatten.each { |link| next if link =~ /\Ahttps?:/; target=link.split("#",2)[0]; next if target.empty?; path=File.expand_path(target, File.dirname(f)); abort("missing #{target} referenced from #{f}") unless File.exist?(path) } }; puts "markdown local links ok"'
python3 scripts/build_release_package.py --output dist/kiddo-compass.zip
python3 scripts/release_guardrails.py inspect dist/kiddo-compass.zip
python3 scripts/beta_kpi_gate.py --json > dist/beta-kpi.json
python3 scripts/quality_dashboard.py --metrics dist/beta-kpi.json --regression dist/regression-p0-openclaw.json --output dist/quality-dashboard.html
python3 scripts/weekly_quality_report.py --metrics dist/beta-kpi.json --regression dist/regression-p0-openclaw.json --output dist/weekly-quality-report.md
make audit-bundle
```

`git ls-files` 对私人文件应无输出；根目录 live state 文件存在时，`release_guardrails.py check` 会直接失败。仓库中只允许保留 `examples/*.example.md` 脱敏模板，模板不得包含真实儿童姓名、生日、学校、家庭结构、练习日志或学习进度。`release_guardrails.py` 会从白名单生成包文件列表，扫描 frontmatter、隐私过采集、近诊断词、固定天数承诺、未验证热线、单因果标签和 live state 内容；`inspect` 会对实际 zip artifact 再扫一遍。失败时不要发布。

维护者本地运行期文件只能保存在 `.kiddo-compass-state/` 或平台私有 storage，公开 artifact 必须来自 `make audit-bundle` 生成的白名单 zip，而不是直接压缩整个目录。

GitHub Actions 中的 `Public Beta Gate` 直接调用 `python3 scripts/release_gate.py`，与本地 public-beta release gate 是同一入口。它不是线上监控替代品；线上 dashboard、真实用户反馈闭环和账号权限执行仍属于 App / 小程序平台层。

OpenClaw agent 回归是 Hermes 不可用时的本地 fallback。运行前把当前 skill 复制到目标 profile 的 workspace，例如 `~/.openclaw/workspace-kiddo-regression/skills/kiddo-compass/`。不要使用指向仓库外部的 symlink；OpenClaw 会因为 `symlink-escape` 跳过该 skill。

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
