# Routing Guide

Use this file after safety triage and before choosing tools or scripts. The goal is to avoid one-size-fits-all advice.

## Minimum needed fields

Ask only when the answer changes safety or the advice:

- Age band: 0-12 months, 12-24 months, 24-36 months, 3-5 years, 6+ years.
- Scene: sleep, feeding, toileting, separation, aggression, sharing/toys, screens, siblings, public meltdown, caregiver disagreement.
- Caregiver role: mom, dad, grandparent, teacher, nanny/other caregiver, multiple caregivers.
- Pattern: first time, repeated, escalating, already tried something.

If missing, give a temporary answer and ask one concise follow-up.

## Intent taxonomy

Use one primary intent and at most one secondary intent.

| Intent | Trigger | Default mode |
| --- | --- | --- |
| `safety_help` | harm, self-harm, shaking, abuse, severe regression, medical/development concern | `crisis-support` or professional-evaluation support |
| `scene_help` | a concrete parenting moment: sleep, feeding, aggression, separation, screens, toileting | `ordinary-advice` |
| `learning_mode` | asks why, principles, plan, or practice path | `deep-learning` |
| `tool_lookup` | asks for a specific script, card, or checklist | `ordinary-advice` or `family-sharing` |
| `family_alignment` | partner, grandparent, teacher, nanny, or multiple caregivers need consistency | `family-sharing` |
| `profile_manage` | asks to create, view, correct, export, delete, or anonymize records | `full-intake` or state operation |
| `feedback_update` | reports that a prior intervention helped, partly helped, or failed | `review` |

## Slot schema

| Slot | Values | Required when |
| --- | --- | --- |
| `age_band` | `0-12m`, `12-24m`, `24-36m`, `3-5y`, `6+y`, `unknown` | Advice would change by developmental expectation. |
| `scene_type` | `sleep`, `feeding`, `toileting`, `aggression`, `separation`, `screens`, `siblings`, `public-meltdown`, `caregiver-alignment`, `other` | Always infer if possible. |
| `caregiver_role` | `parent`, `grandparent`, `teacher`, `nanny`, `multi-caregiver`, `unknown` | Needed for tone and feasible action. |
| `risk_route` | `immediate_safety`, `professional_evaluation`, `everyday_support`, `unknown` | Always set after safety triage. |
| `pattern_frequency` | `first-time`, `repeated`, `escalating`, `already-tried`, `unknown` | Needed for escalation and review. |
| `language_mode` | `zh`, `en`, `bilingual`, `tts` | Needed for visible output shape. |

## Route precedence

1. `safety_help` beats every other intent.
2. `feedback_update` beats a fresh generic suggestion because the user already tried something.
3. `profile_manage` runs only after answering urgent scene or safety needs.
4. `family_alignment` changes output into a shareable card and omits private logs.
5. `learning_mode` can expand only after safety boundaries are handled.
6. `scene_help` is the default for everyday-support cases.

## Decision table

| Primary signal | Required slots | Load | Output rule |
| --- | --- | --- | --- |
| Immediate harm or adult may hurt child | `risk_route=immediate_safety` | `safety-triage.md` | Safety action first; no ordinary discipline advice. |
| Development, medical, or months-long escalating concern | `risk_route=professional_evaluation`, `scene_type` | `safety-triage.md`, `evidence-matrix.md` | Recommend evaluation; give while-waiting support. |
| Everyday concrete scene, missing age | `scene_type`, `age_band=unknown` | `evidence-matrix.md`, matching scenario file | Give temporary advice, then ask one age-band question. |
| User asks to build profile | `profile_manage`, `language_mode` | `state-schema.md` | Ask optional nickname and age band first; no exact birthday by default. |
| User reports tried advice | `feedback_update`, `pattern_frequency=already-tried` | `state-schema.md`, `feedback-and-patrol.md` | Name outcome, adjust intervention, ask one key detail. |
| Message for partner/grandparent/teacher | `family_alignment`, `caregiver_role` | `sharing-note.md`, `grandparent-strategies.md` when relevant | Share one rule and exact sentence; omit private records. |

## Age routing

| Age band | Default stance | Avoid |
| --- | --- | --- |
| 0-12 months | Attachment, responsive care, sleep/feeding safety, caregiver support | Discipline framing, compliance expectations |
| 12-24 months | Short scripts, physical safety, routines, redirection | Long reasoning, moral lectures, sharing demands |
| 24-36 months | Limited choices, visual routines, naming feelings, brief repair | Expecting stable impulse control |
| 3-5 years | Collaborative problem solving, practice, simple cause/effect | Shame, threats, complex negotiations |
| 6+ years | Family meetings, reflection, responsibility, repair plans | Talking down, removing all agency |

## Scene routing

| Scene | Load | First decision |
| --- | --- | --- |
| Sleep | `evidence-matrix.md`, `scenario-guide.md` | Is this routine/limit testing, fear, illness, or sleep debt? |
| Feeding / throwing food | `evidence-matrix.md`, `scenario-guide.md` | Is the child hungry, full, exploring, seeking reaction, or struggling medically? |
| Toileting | `evidence-matrix.md`, `scenario-template.md` | Is the child developmentally ready? Is there pain, fear, constipation, or pressure? |
| Aggression / hitting | `safety-triage.md`, `evidence-matrix.md`, `scenario-template.md` | Is anyone unsafe? Is this occasional or persistent/escalating? |
| Separation | `evidence-matrix.md`, `scenario-template.md` | Is this normal transition distress or extreme/persistent impairment? |
| Grandparent disagreement | `grandparent-strategies.md`, `scenario-template.md` | Is this preference difference or safety boundary? |
| Screens | `evidence-matrix.md`, `scenario-template.md` | Is the issue transition, limit, boredom, sleep, or adult inconsistency? |
| Siblings / sharing | `evidence-matrix.md`, `scenario-template.md` | Is this normal ownership development, rivalry, or safety risk? |

## Caregiver routing

- Parent alone: give one script the parent can use today.
- Two parents: include one alignment sentence to avoid conflicting limits.
- Grandparent: respect the relationship; focus on safety bottom lines and one shared rule.
- Teacher: use group routines, class meetings, safety, and repair language.
- Multiple caregivers: produce a shareable summary instead of exposing full logs.

## Output modes

- Crisis support: immediate safety concern. Safety action first, no ordinary discipline advice.
- Ordinary advice: default. Give a usable script/action first, then ask at most 1-2 needed questions.
- Deep learning: only when the user asks for analysis, learning, or a plan.
- Review: user tried something. Record outcome, adjust next intervention, avoid repeating a failed tool unchanged.
- Full intake: user explicitly wants a profile. Ask optional nickname + age band first; no exact birthday by default.
- Family sharing: short card for partner, grandparent, teacher, or multiple caregivers; do not include private logs.
- Easy-read / TTS: one action per line, short sentences, little theory, no mixed-language clutter.

## Routing examples

- "2-year-old throwing food" -> 24-36 months + feeding -> check responsive feeding and satiety; use calm limit and remove food if throwing continues.
- "4-year-old hits sister every day" -> 3-5 years + aggression -> safety first; if persistent/injuring, recommend professional evaluation.
- "Grandma gives candy after I say no" -> caregiver disagreement -> load grandparent strategy; set one safety/health rule and a respectful script.
