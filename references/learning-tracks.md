# Learning Tracks

Use this file when the user asks for a practice plan or when `LearningTrack` state should be updated. The default path is goal-driven, tied to the user's current scene and review data. Do not use a fixed day-by-day course as the product default.

Legacy note: the old fixed 30-day course has been moved to `archive/legacy-learning-path.md`. It is self-study reference only, not the default onboarding, practice, or progress model.

## Goal-driven schema

Each `LearningTrack` record uses:

- `goal_type`: one of the supported track ids.
- `baseline`: current scene, frequency, safety flags, and caregiver context in minimized form.
- `practice_action`: one small action to try before the next review.
- `review_metric`: includes one `count_metric` and one `experience_metric`.
- `progress_state`: `not-started`, `learning`, `practicing`, `reviewing`, `paused`, `completed`.
- `completion_rule`: the goal-specific rule for marking the track stable enough for now.
- `last_reviewed_at`: `YYYY-MM-DD` or empty until first review.

## Goal-driven tracks

| goal_type | baseline | practice_action | review_metric | progress_state | completion_rule | last_reviewed_at |
| --- | --- | --- | --- | --- | --- | --- |
| `sleep` | Bedtime delay, night waking, repeated sleep conflict; note nights/week and medical flags. | Use one predictable final-step script and one calm boundary for 3 nights. | count_metric: number of extra requests/night; experience_metric: caregiver stress 1-5 and child settling ease 1-5. | `not-started`, `learning`, `practicing`, `reviewing`, `paused`, `completed` | Complete when extra requests and caregiver stress are both lower for 5 of 7 nights, with no safety or health flags. | `YYYY-MM-DD` |
| `feeding` | Food throwing, picky eating, screen pressure, or mealtime conflict; note meals/week and choking/weight concerns. | Split adult job and child job; offer one safe food plus one tiny no-pressure exposure. | count_metric: meals with throwing/screen conflict per week; experience_metric: mealtime tension 1-5 and child willingness 1-5. | `not-started`, `learning`, `practicing`, `reviewing`, `paused`, `completed` | Complete when meals are calmer for one week and pressure/shame is not used. | `YYYY-MM-DD` |
| `toileting` | Potty resistance, accidents, regression, or fear; note accidents/week and pain/constipation signs. | Use one predictable sit time and neutral cleanup, without bargaining or shame. | count_metric: accidents or resisted sits per week; experience_metric: child anxiety 1-5 and adult frustration 1-5. | `not-started`, `learning`, `practicing`, `reviewing`, `paused`, `completed` | Complete when routine is accepted most days and pain/regression flags are absent or medically checked. | `YYYY-MM-DD` |
| `aggression` | Hitting, biting, kicking, throwing, or unsafe grabbing; note incidents/week and injury risk. | Block harm quickly, name the limit, practice one replacement action while calm, and repair later. | count_metric: unsafe incidents/week; experience_metric: repair quality 1-5 and adult calm 1-5. | `not-started`, `learning`, `practicing`, `reviewing`, `paused`, `completed` | Complete when harm is blocked reliably and incidents decrease or repair improves for two review cycles. | `YYYY-MM-DD` |
| `separation` | Drop-off distress, clinginess, or transition panic; note recovery time after separation. | Use one short goodbye ritual, a clear handoff, and a reconnection ritual after return. | count_metric: minutes to recover after goodbye; experience_metric: child confidence 1-5 and caregiver confidence 1-5. | `not-started`, `learning`, `practicing`, `reviewing`, `paused`, `completed` | Complete when recovery time shortens and the ritual feels predictable for one week. | `YYYY-MM-DD` |
| `method-basics` | User wants positive-parenting foundations or a reset after repeated conflict; note one live scene. | Rewrite one adult sentence into connection plus boundary, then try it once. | count_metric: number of practice attempts/week; experience_metric: respect-for-child 1-5 and boundary-clarity 1-5. | `not-started`, `learning`, `practicing`, `reviewing`, `paused`, `completed` | Complete when the user can produce an action-first, no-label response in two different scenes. | `YYYY-MM-DD` |
| `grandparent-alignment` | Conflicting adult responses; note one shared rule and which parts can stay flexible. | Send one short shared rule card and agree on one common sentence. | count_metric: times adults used the shared sentence/week; experience_metric: adult alignment 1-5 and conflict heat 1-5. | `not-started`, `learning`, `practicing`, `reviewing`, `paused`, `completed` | Complete when the core boundary is consistent for two review cycles, even if style differs. | `YYYY-MM-DD` |

## Review protocol

When the user reports back, output four parts:

1. `结果`: what changed, using the user's words when possible.
2. `可能原因`: 1-2 likely factors, without diagnosing or blaming.
3. `只调整一个变量`: change only one thing in the practice action.
4. `下次观察指标`: name the next count metric and subjective experience metric.

If the report includes safety, pain, regression, adult loss of control, or health flags, pause the learning track and route to safety or professional evaluation first.

## Recommendation rule

Recommend a track only after the current scene is answered. Tie learning to the user's live case: "Because you are working on bedtime delay, start with the sleep track." Do not require any static day-by-day sequence before helping with the current problem.
