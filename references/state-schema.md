# State Schema

Use this file before writing any local runtime state. Missing, corrupted, or
unwritable state files must not block the first helpful answer.

## Write policy

- Give the user-facing answer first unless the user explicitly asked only to edit state.
- Store only information the user has confirmed.
- Do not convert model guesses into facts.
- Prefer age band over exact birthday.
- Do not persist real name, exact birthday, phone, school, address, or medical identifiers by default.
- If a precise date is necessary for a developmental threshold, explain why and let the user provide it voluntarily. Store the derived age band unless the user explicitly asks to save the exact date.

## Schema

Use these sections in `child-profile.md` and related local files:

```yaml
facts:
  - value: "optional nickname or age band"
    source_turn: "user-confirmed turn reference"
    last_updated: "YYYY-MM-DD"
hypotheses:
  - value: "possible explanation, not fact"
    confidence: "low|medium"
    source_turn: "turn reference"
    last_updated: "YYYY-MM-DD"
interventions:
  - scene: "sleep|feeding|toileting|aggression|separation|screens|siblings|caregiver-alignment|other"
    action: "what the caregiver tried"
    evidence_basis: "official-consensus|method-source|practice-pattern|experience-only"
    source_turn: "turn reference"
    last_updated: "YYYY-MM-DD"
outcomes:
  - intervention_ref: "short label"
    result: "helped|partly-helped|not-helpful|unknown"
    notes: "user-confirmed summary"
    source_turn: "turn reference"
    last_updated: "YYYY-MM-DD"
consent_flags:
  store_profile: "yes|no|unknown"
  store_sensitive_detail: "no by default"
  share_with_family: "yes|no|unknown"
last_updated: "YYYY-MM-DD"
```

## Error handling

| Problem | Behavior |
| --- | --- |
| File missing | Continue with temporary advice; offer optional profile creation after the answer. |
| File corrupted or unreadable | Say the local record cannot be trusted, continue from the current message, and ask before overwriting. |
| File unwritable | Continue the conversation; offer a short summary the user can save later. |
| Conflicting facts | Ask the user which fact to keep before writing. |
| Sensitive detail supplied | Minimize it, avoid repeating it, and ask whether to store a less identifying version. |

## Fact vs hypothesis examples

Fact: "Age band: 3-5 years" after the user confirms it.

Hypothesis: "Bedtime delay may be partly about transition difficulty" because the model inferred it.

Intervention: "One last story, then lights out; parent sits quietly for two minutes."

Outcome: "Partly helped; crying shortened but requests continued."
