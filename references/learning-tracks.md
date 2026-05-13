# Learning Tracks

Use this file when the user asks for a practice plan or when `LearningTrack` state should be updated. Prefer goal-driven tracks over a fixed day-by-day course.

## Goal-driven tracks

| Track | Start when | Minimum route | Practice action | Review question |
| --- | --- | --- | --- | --- |
| `sleep` | Bedtime delay, night waking, repeated sleep conflict | routine visibility -> one boundary sentence -> review sleep/medical flags | Use one last-step script for 3 nights and record what changed. | Did requests shorten, shift, or escalate? |
| `feeding` | Food throwing, picky eating, mealtime pressure | responsive feeding check -> adult/child job split -> calm end-of-meal rule | Offer one safe food and one tiny new exposure without pressure. | Was the child calmer, safer, or more willing to stay at the table? |
| `toileting` | Potty resistance or accidents | readiness/pain check -> no-shame routine -> neutral cleanup | Try one predictable sit time without bargaining. | Any pain, fear, constipation, or pressure signs? |
| `aggression` | Hitting, biting, kicking, throwing | safety block -> replacement action -> repair later | Practice "stomp, squeeze, ask for help" while calm. | Did adults block harm quickly and repair later? |
| `separation` | Drop-off distress or clinginess | short goodbye ritual -> teacher handoff -> reconnection ritual | Repeat the same goodbye sentence for one week. | How long did recovery take after the caregiver left? |
| `grandparent-alignment` | Conflicting adult responses | one bottom-line rule -> shared sentence -> flexible areas | Send one family rule card. | Did adults use the same sentence? |
| `method-basics` | User wants positive-parenting foundations | connect before correct -> warm-and-firm boundary -> repair | Pick one recent conflict and rewrite the adult sentence. | Did the sentence respect both the child and the boundary? |

## State flow

Use `LearningTrack.progress_state` from `references/state-schema.md`:

- `not-started`: user asked about learning but has not picked a goal.
- `learning`: user is reading or discussing principles.
- `practicing`: user has one concrete practice action.
- `reviewing`: user reported an outcome and needs adjustment.
- `paused`: user chose to stop or a safety/health issue takes priority.
- `completed`: user reports the goal is stable enough for now.

## Recommendation rule

Recommend a track only after the current scene is answered. Tie learning to the user's live case: "Because you are working on bedtime delay, start with the sleep track." Do not require the old static 30-day sequence before helping with the current problem.
