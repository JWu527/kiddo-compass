# Kiddo Compass

Kiddo Compass is an OpenClaw / AgentSkills-compatible Positive Discipline parenting skill. It turns Chinese study notes, Adlerian psychology basics, 52 Positive Discipline tool cards, practical parenting scenarios, and a 30-day learning path into a local knowledge base an AI agent can load as needed.

This skill is for parents, caregivers, and educators who want responses that are warm, specific, kind and firm. It is not a medical, psychological, legal, or diagnostic tool.

[中文 README](README.md)

## What It Does

- Triggers a Positive Discipline parenting coach from `SKILL.md`.
- Builds a local child profile through a short onboarding conversation.
- Uses `references/methodology.md` as the internal six-step analysis framework.
- Adds `references/english-response-guide.md` for natural English and bilingual responses.
- Loads chapter notes, tool cards, scenario guides, learning plans, and FAQ files only when needed.
- Maintains local runtime files: `child-profile.md`, `practice-log.md`, and `learning-progress.md`.
- Preserves clear professional boundaries for self-harm, severe aggression, developmental concerns, trauma, and parent mental-health risk signals.

## Repository Layout

```text
kiddo-compass/
├── SKILL.md                         # OpenClaw / AgentSkills entrypoint
├── references/                      # On-demand knowledge base
├── references/english-response-guide.md
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
I want to use Positive Discipline when my child throws food from the high chair.
```

```text
Can you give me a bilingual Positive Discipline response I can share with my partner?
```

On first use, the agent checks whether `child-profile.md` exists and is complete. If not, it asks a short five-round onboarding sequence and writes the answers locally.

## Knowledge Base

| File | Purpose |
| --- | --- |
| `references/methodology.md` | Internal scenario analysis and output rules |
| `references/english-response-guide.md` | English and bilingual response style |
| `references/core-concepts.md` | Core Positive Discipline concepts |
| `references/adler-psychology.md` | Adlerian psychology and mistaken goals |
| `references/tool-cards.md` | 52 Positive Discipline tools |
| `references/scenario-guide.md` | Bedtime, meals, crying, and other practical scenarios |
| `references/grandparent-strategies.md` | Handling inconsistent grandparent discipline |
| `references/learning-map.md` | Learning map |
| `references/30-day-plan.md` | 30-day learning plan |
| `references/feedback-and-patrol.md` | Practice feedback loop |
| `references/faq.md` | FAQ |
| `references/chapter-*.md` | Chapter-by-chapter Chinese study notes |

Most long-form reference notes are currently Chinese. The English response guide helps the agent translate the method into natural English during conversation without duplicating the whole knowledge base.

## Maintenance Checks

```bash
git status --short
git ls-files child-profile.md practice-log.md learning-progress.md
rg -n "^---|^name:|^version:|^description:|^metadata:" SKILL.md
```

`git ls-files` should print nothing for the three private runtime files.

## Publishing

See [PUBLISHING.md](PUBLISHING.md). Before publishing, confirm that `.clawhubignore` excludes private runtime files and that `SKILL.md` version matches the release version.

## Privacy And Safety

See [SECURITY.md](SECURITY.md). This skill can store sensitive child and family context locally. Do not commit or publish runtime profile files.

## License

MIT-0. See [LICENSE](LICENSE).
