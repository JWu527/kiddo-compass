# Platform Integration Contract

Use this file when embedding Kiddo Compass in an App, mini program, web app, or account-backed assistant.

The current skill repository is a reference implementation, not a complete SaaS data platform. `scripts/state_service.py` demonstrates local JSON storage and data-rights operations. Consent UI, account permissions, multi-user isolation, sync, backups, and production audit trails are Spec-only until implemented by a host platform.

## Consent UI

Any product surface must show explicit choices before writing state:

| Toggle | Default | Meaning |
| --- | --- | --- |
| Store minimal profile | off | Save nickname, age band, caregiver mode, and active scene. |
| Store sensitive detail | off | Save a precise detail only after explaining why it is needed. |
| Share family card | off | Generate a shareable note without private logs. |

The UI must never make exact birthday, school, phone, address, or medical identifiers required for ordinary advice.

Before any write, the platform should display the same confirmation summary shape used by `StateStore.prepare_write`:

```yaml
confirmation_summary:
  entity: "ChildProfile|Case|Intervention|Outcome|State"
  action_type: "store_profile|store_case|store_intervention|store_outcome|correct|delete|anonymize"
  fields_to_write: ["field names only"]
  contains_identifying_info: false
  desensitized: true
  requires_user_confirmation: true
```

## Data Rights UI

The platform data-rights UI is Spec-only in this repository. A host product must expose these actions before claiming platform-level data rights:

- View: show stored profile, cases, interventions, outcomes, and consent logs.
- Export: download a JSON or Markdown dump.
- Correct: edit one field after confirmation.
- Delete: remove selected fields or the full local profile.
- Anonymize: replace direct identifiers with nickname, age band, and scene labels.

The local reference implementation is `scripts/state_service.py`; it provides command-line `view`, `export`, `correct`, `delete`, and `anonymize` operations for local JSON state only.

## Account And Permission Model

- `household_id`: owns profiles and consent logs.
- `child_id`: scoped to one household.
- `caregiver_id`: optional actor id for parent, grandparent, teacher, or nanny.
- `role`: `owner`, `editor`, `viewer`, or `family-card-only`.

Only `owner` should be allowed to delete or export full state. `family-card-only` should be able to view shareable cards but not private logs. This role enforcement is Spec-only here and requires platform auth/storage.

## Storage Interface

Platform services should map to these methods:

```text
create_profile(nickname, age_band, caregiver_mode, consent_scope)
prepare_write(entity, fields, action_type)
create_case(child_id, scene_type, risk_route, pattern_frequency, source_type)
create_intervention(case_id, recommendation_type, evidence_label, action, source_type)
create_outcome(intervention_id, result_type, notes, source_type)
view_state()
export_state()
correct_field(entity, field, value)
anonymize()
delete_state()
```

Every write must append a ConsentLog entry with `confirmation_summary` or be rejected.
