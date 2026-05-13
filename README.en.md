# Kiddo Compass

Kiddo Compass is an OpenClaw / AgentSkills-compatible positive-parenting companion skill. It turns original practice cards, common parenting scenarios, safety triage, evidence calibration, and optional practice paths into a local knowledge base an AI agent can load as needed.

This skill is for parents, caregivers, and educators who want responses that are warm, specific, kind and firm. It is not a medical, psychological, legal, or diagnostic tool.

Current status: internal testing / public-beta candidate. Do not publish a public package until whitelist packaging, privacy scanning, and P0 regression checks pass.

[中文 README](README.md)

## What It Does

- Triggers a positive-parenting companion from `SKILL.md`.
- Runs safety triage first, then gives a temporary answer before optional onboarding.
- Uses `references/methodology.md` internally, without exposing theory labels or the six-step structure in ordinary answers.
- Adds age, scenario, caregiver routing and evidence calibration.
- Tracks deep research coverage so public-beta scope is not confused with full product scope.
- Adds `references/english-response-guide.md` for natural English and bilingual responses.
- Adds easy-read / TTS-friendly mode for overwhelmed caregivers.
- Loads safety, evidence, scenario, state, and language guides only when needed.
- Maintains local runtime files: `child-profile.md`, `practice-log.md`, and `learning-progress.md`.
- Separates facts, hypotheses, interventions, outcomes, and consent flags before writing state.
- Preserves clear professional boundaries for self-harm, severe aggression, developmental concerns, trauma, and parent mental-health risk signals.

## Repository Layout

```text
kiddo-compass/
├── SKILL.md                         # OpenClaw / AgentSkills entrypoint
├── PUBLIC_BETA_KANBAN.md            # Public beta roadmap board
├── PUBLIC_BETA_COVERAGE.md          # Deep research coverage matrix
├── references/                      # On-demand knowledge base
├── references/safety-triage.md
├── references/routing-guide.md
├── references/dialogue-modes.md
├── references/accessibility-i18n.md
├── references/evidence-matrix.md
├── references/scenario-template.md
├── references/evaluation-set.md
├── references/evaluation-set.jsonl
├── references/english-response-guide.md
├── references/state-schema.md
├── scripts/beta_kpi_gate.py           # Beta readiness KPI gate
├── scripts/release_guardrails.py       # Whitelist packaging and privacy scan
├── scripts/run_regression.py           # Hermes JSONL regression runner
├── skill-package-manifest.txt          # Public package whitelist
├── child-profile.example.md         # Private profile template
├── practice-log.example.md          # Practice log template
├── learning-progress.example.md     # Learning progress template
├── README.md
├── README.en.md
├── CONTRIBUTING.md
├── SECURITY.md
├── PUBLISHING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── HERMES_TEST_CASES.md             # Hermes manual test cases
├── LICENSE
└── .clawhubignore
```

The following files are created locally during use and must not be published:

```text
child-profile.md
practice-log.md
learning-progress.md
```

They may contain private child and family information. This repository only tracks the `.example.md` templates.

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

On first use, the agent checks whether `child-profile.md` exists and is complete. If not, it still gives temporary advice first, then asks only 1-2 necessary questions. The full five-round onboarding sequence is optional and only starts when the user wants to build a fuller local profile.

Default intake asks only for an optional nickname and age band. Exact birthday, phone, school, address, and similar sensitive information are not collected or persisted by default.

## Knowledge Base

| File | Purpose |
| --- | --- |
| `HERMES_TEST_CASES.md` | Hermes manual test cases and release sampling guide |
| `PUBLIC_BETA_KANBAN.md` | Public beta optimization board |
| `PUBLIC_BETA_COVERAGE.md` | Deep research coverage matrix |
| `references/safety-triage.md` | Red/yellow/green safety triage |
| `references/routing-guide.md` | Age, scene, and caregiver routing |
| `references/dialogue-modes.md` | Crisis, ordinary advice, deep learning, review, intake, family-sharing, and easy-read modes |
| `references/accessibility-i18n.md` | Chinese, English, bilingual, and TTS-friendly templates |
| `references/evidence-matrix.md` | Evidence calibration for sleep, feeding, toileting, aggression, separation |
| `references/scenario-template.md` | Standard scenario card template |
| `references/evaluation-set.md` | Lightweight public beta regression set |
| `references/evaluation-set.jsonl` | Executable regression data format |
| `references/methodology.md` | Internal scenario analysis and output rules |
| `references/english-response-guide.md` | English and bilingual response style |
| `references/state-schema.md` | Local state schema and error handling |
| `references/scenario-guide.md` | Bedtime, meals, crying, and other practical scenarios |
| `references/grandparent-strategies.md` | Handling inconsistent grandparent discipline |
| `references/feedback-and-patrol.md` | Practice feedback loop |

Long-form reading notes, chapter-style materials, tool lists, and fixed-day plans are kept out of the public package whitelist until copyright and positioning review is complete.

## Maintenance Checks

```bash
git status --short
git ls-files child-profile.md practice-log.md learning-progress.md
python3 scripts/release_guardrails.py check
python3 scripts/beta_kpi_gate.py
python3 scripts/run_regression.py --priority P0
python3 -m unittest tests/test_release_guardrails.py
rg -n "^---|^name:|^version:|^description:|^metadata:" SKILL.md
```

`git ls-files` should print nothing for the three private runtime files.

## Publishing

See [PUBLISHING.md](PUBLISHING.md). Before publishing, confirm that `.clawhubignore` excludes private runtime files and that `SKILL.md` version matches the release version.

## Privacy And Safety

See [SECURITY.md](SECURITY.md). This skill can store sensitive child and family context locally. Do not commit or publish runtime profile files.

## License

MIT-0. See [LICENSE](LICENSE).
