# State Schema

Use this file before reading or writing local runtime state. Missing, corrupted, or unwritable state must not block the first helpful answer.

The current repository provides a local JSON reference implementation in `scripts/state_service.py`. It is not a complete SaaS data platform.

## Storage boundary

- Prefer the platform-provided private storage directory.
- If no platform storage exists, use `.kiddo-compass-state/` in the local workspace.
- Do not place live runtime state in the skill root.
- Migrate any legacy root-level `child-profile.md`, `practice-log.md`, or `learning-progress.md` into `.kiddo-compass-state/` before release checks.
- The repository may keep only sanitized `examples/*.example.md` templates; templates must use placeholders or fictional examples, not real child or family data.

## Write policy

- Give the user-facing answer first unless the user explicitly asked only to edit state.
- Store only information the user has confirmed.
- Do not convert model guesses into facts.
- Prefer age band over exact birthday.
- Do not persist real name, exact birthday, phone, school, address, or medical identifiers by default.
- If a precise date is necessary for a developmental threshold, explain why and let the user provide it voluntarily. Store the derived age band unless the user explicitly asks to save the exact date.
- Before writing, show a short confirmation summary and wait for confirmation.
- A confirmation summary must include: fields to write, whether direct identifiers are present, whether the payload is desensitized, and whether user confirmation is required.

## Entities

Use these entities even when the physical file format is Markdown with YAML blocks.

```yaml
Household:
  schema_version: "1"
  household_id: "local generated id"
  locale: "zh-CN|en-US|other"
  storage_scope: "platform-private|local-private"

ChildProfile:
  schema_version: "1"
  child_id: "local generated id"
  household_id: "Household.household_id"
  nickname: "optional nickname"
  age_band: "0-12m|12-24m|24-36m|3-5y|6+y|unknown"
  caregiver_mode: "parent|grandparent|teacher|multi-caregiver|unknown"
  facts:
    - value: "user-confirmed fact"
      source_type: "user_confirmed"
      source_turn: "turn reference"
      last_updated: "YYYY-MM-DD"
  hypotheses:
    - value: "assistant interpretation, not fact"
      source_type: "assistant_inferred"
      confidence: "low|medium"
      source_turn: "turn reference"
      last_updated: "YYYY-MM-DD"

Case:
  schema_version: "1"
  case_id: "local generated id"
  child_id: "ChildProfile.child_id"
  scene_type: "sleep|feeding|toileting|aggression|separation|screens|siblings|caregiver-alignment|other"
  risk_route: "immediate_safety|professional_evaluation|everyday_support|unknown"
  pattern_frequency: "first-time|repeated|escalating|unknown"
  source_type: "user_confirmed|assistant_inferred|observed_feedback"
  created_at: "YYYY-MM-DD"

Intervention:
  schema_version: "1"
  intervention_id: "local generated id"
  case_id: "Case.case_id"
  recommendation_type: "script|routine|safety-step|professional-evaluation|family-card|learning-practice"
  evidence_label: "official-consensus|method-source|practice-pattern|needs-evaluation|experience-only"
  action: "what was suggested or tried"
  source_type: "user_confirmed|assistant_inferred|observed_feedback"
  delivered_at: "YYYY-MM-DD"

Outcome:
  schema_version: "1"
  outcome_id: "local generated id"
  intervention_id: "Intervention.intervention_id"
  result_type: "helped|partly-helped|not-helpful|unknown"
  notes: "user-confirmed outcome summary"
  source_type: "user_confirmed|observed_feedback"
  updated_at: "YYYY-MM-DD"

ConsentLog:
  schema_version: "1"
  consent_id: "local generated id"
  action_type: "store_profile|store_case|store_intervention|store_outcome|correct|delete|anonymize|export|share_family_card"
  confirmed_at: "YYYY-MM-DD"
  scope: "what the user allowed"
  confirmation_summary:
    entity: "ChildProfile|Case|Intervention|Outcome|State"
    action_type: "same action as above"
    fields_to_write: ["field names only"]
    contains_identifying_info: false
    desensitized: true
    requires_user_confirmation: true

LearningTrack:
  schema_version: "1"
  track_id: "local generated id"
  child_id: "ChildProfile.child_id"
  goal_type: "sleep|feeding|toileting|aggression|separation|grandparent-alignment|method-basics"
  baseline:
    scene: "minimized current scene"
    frequency_count: "countable starting point"
    safety_flags: "none reported|needs evaluation|paused"
    caregiver_context: "generalized caregiver setup"
  practice_action: "one small action to try"
  review_metric:
    count_metric: "number or frequency to count"
    experience_metric: "subjective 1-5 or short user-reported experience"
  progress_state: "not-started|learning|practicing|reviewing|paused|completed"
  completion_rule: "goal-specific stability rule"
  last_reviewed_at: "YYYY-MM-DD or empty"
  practice_ref: "Case.case_id or Intervention.intervention_id"
  updated_at: "YYYY-MM-DD"
```

## Source types

| Source type | Meaning | Write rule |
| --- | --- | --- |
| `user_confirmed` | The user explicitly confirmed the statement. | May be written to facts or outcomes. |
| `assistant_inferred` | The assistant inferred a possible pattern. | Keep in hypotheses only. |
| `observed_feedback` | The user reported what happened after trying something. | May update outcomes after confirmation. |

## Operations

Support these user rights in text-only form until a product UI exists: `view/export/correct/delete/anonymize`.

| User asks | Behavior |
| --- | --- |
| View | Summarize stored facts, current cases, interventions, outcomes, and consent logs. |
| Export | Provide a compact Markdown/JSON-style dump with sensitive fields minimized. |
| Correct | Show the old value and proposed new value; write only after confirmation. |
| Delete | Remove the requested field, case, or full profile after confirmation; add a ConsentLog delete entry if a log is kept. |
| Anonymize | Replace direct identifiers with nickname/age band/scene labels and remove exact dates or locations. |

## Local reference implementation

`scripts/state_service.py` stores `.kiddo-compass-state/state.json` and supports:

- `prepare_write(entity, fields, action_type)` / CLI `prepare-write`
- `create_profile(...)` for ChildProfile
- `create_case(...)` for Case
- `create_intervention(...)` for Intervention
- `create_outcome(...)` for Outcome
- `view_state()` / CLI `view`
- `export_state()` / CLI `export`
- `correct_field(...)` / CLI `correct`
- `delete_entity(...)` or `delete_state()` / CLI `delete`
- `anonymize()` / CLI `anonymize`

This is a local reference implementation for tests and host-platform mapping. Account UI, role-based permissions, sync, backups, and production audit logs remain platform responsibilities.

## Error handling

| Problem | Behavior |
| --- | --- |
| File missing | Continue with temporary advice; offer optional profile creation after the answer. |
| File corrupted or unreadable | Say the local record cannot be trusted, continue from the current message, and ask before overwriting. |
| File unwritable | Continue the conversation; offer a short summary the user can save later. |
| Conflicting facts | Ask the user which fact to keep before writing. |
| Sensitive detail supplied | Minimize it, avoid repeating it, and ask whether to store a less identifying version. |

## Atomic write rule

When a tool can edit files, write to a temporary file in the same private state directory, validate required fields and `schema_version`, then rename into place. If the platform provides file locks or transactions, use them.
