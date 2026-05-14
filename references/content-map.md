# Kiddo Compass Content Map

This map defines what the runtime may load, what can be packaged for public audit, and what must remain private or historical. When a file is not listed here, treat it as support at most until it is explicitly classified.

## Layer Rules

| Layer | Runtime Access | Public Package | Purpose |
| --- | --- | --- | --- |
| runtime-core | Allowed in ordinary first answers | Allowed | Minimal instructions needed for safe, short, privacy-aware replies. |
| support | Load only for a specific user or maintainer task | Allowed only when explicitly whitelisted | Optional references for deeper scenario work, product governance, and regression operations. |
| study-private | Not runtime | Not allowed | Personal study notes, long-form reading notes, fixed-day learning drafts, and copyright-positioning review material. |
| archive | Not runtime | Not allowed | Historical or migration-era material kept for traceability, not active behavior. |

`SKILL.md` may directly reference only runtime-core files. Support files are discovered through this map and loaded only when a task explicitly needs them. `study-private/` and `archive/` must never be referenced by runtime instructions or included in release bundles.

## Runtime-Core

| File | Role |
| --- | --- |
| `references/content-map.md` | Layer boundary and runtime loading policy. |
| `references/methodology.md` | Compact behavior rules for short, action-first, non-theoretical answers. |
| `references/safety-triage.md` | Safety triage and professional boundary handling. |
| `references/routing-guide.md` | Age, scene, and caregiver routing. |
| `references/dialogue-modes.md` | Response modes and compact output behavior. |
| `references/accessibility-i18n.md` | Easy-read, TTS, Chinese, English, and bilingual output constraints. |
| `references/evidence-matrix.md` | Evidence calibration and escalation thresholds for common scenes. |
| `references/scenario-template.md` | Minimal scenario-card structure for user-facing advice. |
| `references/english-response-guide.md` | English and bilingual wording guardrails. |
| `references/state-schema.md` | Private state schema, consent, and write-confirmation rules. |

## Support

| File | Load Only When |
| --- | --- |
| `references/scenario-guide.md` | User asks for a specific low-risk scene that needs more concrete examples than the template. |
| `references/grandparent-strategies.md` | User asks about grandparent or multi-caregiver alignment. |
| `references/sharing-note.md` | User asks for a family-shareable note. |
| `references/faq.md` | User asks a common operational or expectation-setting question. |
| `references/feedback-and-patrol.md` | Maintainer or host platform is implementing an explicit feedback loop. |
| `references/feature-status.md` | Maintainer checks implemented vs spec-only capability claims. |
| `references/quality-monitoring.md` | Maintainer runs beta-quality review or incident sampling. |
| `references/source-registry.json` | Maintainer audits source_id traceability, source URLs/refs, and review cadence. |
| `references/learning-tracks.md` | User explicitly asks for a learning path, not an ordinary first answer. |
| `references/deep-scenario-packs.md` | User explicitly asks for deeper P1/P2 scenario planning or review. |
| `references/platform-integration.md` | Product integration work for consent UI, storage, accounts, or data rights. |
| `references/regional-resources.json` | Maintainer reviews regional safety-resource placeholders; do not invent numbers from memory. |
| `references/evaluation-set.md` | Human-readable regression set. |
| `references/evaluation-set.jsonl` | Machine-readable regression set used by CI and local checks. |

## Study-Private

These files are retained for private study and copyright-positioning review. They are not runtime material and must not enter a public package:

- `study-private/learning-map.md`
- `study-private/tool-cards.md`
- `study-private/adler-psychology.md`
- `study-private/core-concepts.md`
- `study-private/practice-diary.md`
- `study-private/chapter-01-positive-methods.md`
- `study-private/chapter-02-basic-concepts.md`
- `study-private/chapter-03-birth-order.md`
- `study-private/chapter-04-misbehavior.md`
- `study-private/chapter-05-logical-consequences.md`
- `study-private/chapter-06-problem-solving.md`
- `study-private/chapter-07-encouragement.md`
- `study-private/chapter-08-class-meetings.md`
- `study-private/chapter-09-family-meetings.md`
- `study-private/chapter-10-personality.md`
- `study-private/chapter-11-integration.md`
- `study-private/chapter-12-love-and-joy.md`

## Archive

| File | Reason |
| --- | --- |
| `archive/methodology.md` | Older broad method frame. Kept for traceability, but ordinary runtime should use runtime-core routing, evidence, and scenario templates instead. |
| `archive/legacy-learning-path.md` | Former fixed 30-day course. Kept only as self-study reference; default learning is goal-driven. |

## Release Boundary

The public audit bundle is built from `skill-package-manifest.txt`. It may include runtime-core and necessary support files only. It must not include `study-private/`, `archive/`, local state directories, generated `dist/` content, VCS metadata, or machine-local files.
