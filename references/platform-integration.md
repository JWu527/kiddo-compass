# Platform Integration Contract

Use this file when embedding Kiddo Compass in an App, mini program, web app, or account-backed assistant.

## Consent UI

Any product surface must show three explicit choices before writing state:

| Toggle | Default | Meaning |
| --- | --- | --- |
| Store minimal profile | off | Save nickname, age band, caregiver mode, and active scene. |
| Store sensitive detail | off | Save a precise detail only after explaining why it is needed. |
| Share family card | off | Generate a shareable note without private logs. |

The UI must never make exact birthday, school, phone, address, or medical identifiers required for ordinary advice.

## Data Rights UI

The platform must expose these actions:

- View: show stored profile, cases, interventions, outcomes, and consent logs.
- Export: download a JSON or Markdown dump.
- Correct: edit one field after confirmation.
- Delete: remove selected fields or the full local profile.
- Anonymize: replace direct identifiers with nickname, age band, and scene labels.

The local reference implementation is `scripts/state_service.py`.

## Account And Permission Model

- `household_id`: owns profiles and consent logs.
- `child_id`: scoped to one household.
- `caregiver_id`: optional actor id for parent, grandparent, teacher, or nanny.
- `role`: `owner`, `editor`, `viewer`, or `family-card-only`.

Only `owner` can delete or export full state. `family-card-only` can view shareable cards but not private logs.

## Storage Interface

Platform services should map to these methods:

```text
create_profile(nickname, age_band, caregiver_mode, consent_scope)
view_state()
export_state()
correct_field(entity, field, value)
anonymize()
delete_state()
```

Every write must append a ConsentLog entry or be rejected.
