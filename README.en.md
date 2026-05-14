# Kiddo Compass

Kiddo Compass is an OpenClaw / AgentSkills-compatible positive-parenting companion skill. It turns original practice cards, common parenting scenarios, safety triage, evidence calibration, and optional practice paths into a local knowledge base an AI agent can load as needed.

This skill is for parents, caregivers, and educators who want responses that are warm, specific, kind and firm. It is not a medical, psychological, legal, or diagnostic tool.

Current status: internal testing / public-beta candidate. Do not publish a public package until whitelist packaging, privacy scanning, and P0 regression checks pass.

[中文 README](README.md)

## What It Does

- Triggers a positive-parenting companion from `SKILL.md`.
- Runs safety triage first, then gives a temporary answer before optional onboarding.
- Uses `references/content-map.md` to separate runtime-core, support, study-private, and archive layers; ordinary first answers load only core runtime material.
- Adds age, scenario, caregiver routing and evidence calibration.
- Tracks deep research coverage so public-beta scope is not confused with full product scope.
- Adds `references/english-response-guide.md` for natural English and bilingual responses.
- Adds easy-read / TTS-friendly mode for overwhelmed caregivers.
- Loads safety, evidence, scenario, state, and language guides only when needed.
- Uses a goal-driven `LearningTrack` schema by default instead of a fixed 30-day course.
- Maintains local runtime state under platform-private storage or `.kiddo-compass-state/` after user-confirmed writes; the repository reference implementation uses `.kiddo-compass-state/state.json`, while host platforms may map the schema to private Markdown or database storage. If storage is unavailable, it keeps answering without claiming a write happened.
- Separates facts, hypotheses, interventions, outcomes, and consent flags before writing state.
- Keeps user data local-private, anonymized, and minimized by default; before writing, it must summarize the facts to record and wait for confirmation.
- Preserves clear professional boundaries for self-harm, severe aggression, developmental concerns, trauma, and parent mental-health risk signals.

## Repository Layout

```text
kiddo-compass/
├── SKILL.md                         # OpenClaw / AgentSkills entrypoint
├── PUBLIC_BETA_KANBAN.md            # Public beta roadmap board
├── PUBLIC_BETA_COVERAGE.md          # Deep research coverage matrix
├── references/                      # Runtime-core and necessary support knowledge base
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
├── study-private/                   # Private study notes; not runtime or public package material
├── archive/                         # Historical material; not runtime or public package material
├── scripts/beta_kpi_gate.py           # Beta readiness KPI gate
├── scripts/build_release_package.py   # Guarded whitelist release zip entrypoint
├── scripts/quality_dashboard.py       # Local beta dashboard generator
├── scripts/release_gate.py             # Unified public-beta release gate
├── scripts/release_guardrails.py       # Whitelist packaging and privacy scan
├── scripts/run_regression.py           # Hermes JSONL regression runner
├── scripts/semantic_score.py           # Regression report assertion summary
├── scripts/source_freshness.py         # Source and regional-resource freshness checks
├── scripts/state_service.py            # Local state-service reference implementation
├── scripts/weekly_quality_report.py    # Local weekly quality report generator
├── skill-package-manifest.txt          # Public package whitelist
├── examples/                          # Sanitized state templates, no real family data
│   ├── child-profile.example.md       # Private profile template
│   ├── practice-log.example.md        # Practice log template
│   └── learning-progress.example.md   # Learning progress template
├── README.md
├── README.en.md
├── CONTRIBUTING.md
├── SECURITY.md
├── OPS.md
├── PUBLISHING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── HERMES_TEST_CASES.md             # Hermes manual test cases
├── LICENSE
└── .clawhubignore
```

The following files are created in platform-private storage or `.kiddo-compass-state/` during use. They are not skill runtime release content, must not remain in the skill root, and must not enter Git or a ClawHub artifact. Public artifacts must be built with `make audit-bundle` / the `skill-package-manifest.txt` allowlist, never by zipping the whole workspace:

```text
.kiddo-compass-state/child-profile.md
.kiddo-compass-state/practice-log.md
.kiddo-compass-state/learning-progress.md
.kiddo-compass-state/state.json
```

They may contain private child and family information. This repository only tracks sanitized `examples/*.example.md` templates. Templates must use placeholders or fictional examples only; do not copy real child names, birthdays, schools, family structures, practice logs, or learning progress.

## Install

### OpenClaw workspace install

Clone this repository into your OpenClaw workspace `skills/` directory:

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/JWu527/kiddo-compass.git ~/.openclaw/workspace/skills/kiddo-compass
```

Start a new OpenClaw session so the skill snapshot reloads.

### ClawHub install

If the skill has been published to ClawHub:

```bash
openclaw skills search "kiddo compass"
openclaw skills install kiddo-compass
```

## Usage

Use English, Chinese, or ask for a bilingual response. Example prompts:

```text
Kiddo Compass, my 3-year-old keeps asking for more stories at bedtime and cries when I stop. What should I do?
```

```text
I want to use a positive-parenting approach when my child throws food from the high chair.
```

```text
Can you give me a bilingual positive-parenting response I can share with my partner?
```

On first use, the agent checks whether a private `child-profile.md` exists in the private state root and is complete. If not, it still gives temporary advice first, then asks only 1-2 necessary questions. The full five-round onboarding sequence is optional and only starts when the user wants to build a fuller local profile.

Default intake asks only for an optional nickname and age band. Exact birthday, phone, school, address, and similar sensitive information are not collected or persisted by default.

## Knowledge Base

| File | Purpose |
| --- | --- |
| `HERMES_TEST_CASES.md` | Hermes manual test cases and release sampling guide |
| `PUBLIC_BETA_KANBAN.md` | Public beta optimization board |
| `PUBLIC_BETA_COVERAGE.md` | Deep research coverage matrix |
| `references/content-map.md` | Layer map for runtime-core, support, study-private, and archive |
| `references/methodology.md` | Compact runtime behavior rules: action first, low theory, no labels |
| `references/safety-triage.md` | Red/yellow/green safety triage |
| `references/routing-guide.md` | Age, scene, and caregiver routing |
| `references/dialogue-modes.md` | Crisis, ordinary advice, deep learning, review, intake, family-sharing, and easy-read modes |
| `references/accessibility-i18n.md` | Chinese, English, bilingual, and TTS-friendly templates |
| `references/evidence-matrix.md` | Evidence calibration for sleep, feeding, toileting, aggression, separation |
| `references/source-registry.json` | Traceable source_id registry for official and internal sources |
| `references/scenario-template.md` | Standard scenario card template |
| `references/evaluation-set.md` | Lightweight public beta regression set |
| `references/evaluation-set.jsonl` | Executable regression data format |
| `references/english-response-guide.md` | English and bilingual response style |
| `references/state-schema.md` | Local state schema and error handling |
| `references/platform-integration.md` | Consent UI, data rights, account permissions, and storage contract for App / mini-program integration; platform UI/permissions are Spec-only |
| `references/feature-status.md` | Implemented / Spec-only / Deferred capability status so docs do not overstate behavior |
| `references/quality-monitoring.md` | Beta-quality events, feedback taxonomy, and sample review |
| `references/learning-tracks.md` | Goal-driven practice tracks |
| `references/deep-scenario-packs.md` | Deeper P1/P2 scenario packs, review prompts, and escalation boundaries |
| `references/regional-resources.json` | Reviewable regional safety-resource placeholder library |
| `references/scenario-guide.md` | Bedtime, meals, crying, and other practical scenarios |
| `references/grandparent-strategies.md` | Handling inconsistent grandparent discipline |
| `references/feedback-and-patrol.md` | Practice feedback loop |
| `OPS.md` | Release, content, privacy, source freshness, and incident operations |

Long-form reading notes, chapter-style materials, tool lists, and fixed-day plans live in `study-private/`; the older methodology frame lives in `archive/`. Those two layers are not runtime material and are excluded from the public package whitelist until copyright and positioning review says otherwise.

The old fixed 30-day course has moved to `archive/legacy-learning-path.md` as self-study reference only. The default learning-progress template is `examples/learning-progress.example.md` and uses `goal_type`, `baseline`, `practice_action`, `review_metric`, `progress_state`, `completion_rule`, and `last_reviewed_at`.

## Maintenance Checks

```bash
git status --short
git ls-files child-profile.md practice-log.md learning-progress.md
python3 scripts/release_guardrails.py check
python3 scripts/release_gate.py
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
rg -n "^---|^name:|^version:|^description:|^metadata:" SKILL.md
```

`git ls-files` should print nothing for the three private runtime files.

OpenClaw agent regression requires the skill to be installed or copied into that OpenClaw workspace at `skills/kiddo-compass/`. Avoid symlinks that point outside the configured skill root; OpenClaw skips those as `symlink-escape`.

## Publishing

See [PUBLISHING.md](PUBLISHING.md). Before publishing, confirm that `.clawhubignore` excludes private runtime files and that `SKILL.md` version matches the release version.

## Privacy And Safety

See [SECURITY.md](SECURITY.md). This skill can store sensitive child and family context locally. Do not commit or publish runtime profile files.

## License

MIT-0. See [LICENSE](LICENSE).
