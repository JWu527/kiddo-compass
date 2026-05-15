# Safety Triage

Use this file before ordinary positive parenting advice. Safety triage is not a diagnosis. It decides whether to continue with parenting support, suggest professional evaluation, or prioritize immediate safety.

## Internal routing routes

These routes are internal aids. Do not expose route names, color-coded labels, or internal triage wording in user-facing answers.

| Route | Meaning | Output first |
| --- | --- | --- |
| immediate_safety | Immediate safety concern or possible abuse/self-harm | Stop normal advice. Give immediate safety steps and professional/emergency support. |
| professional_evaluation | Needs professional evaluation or closer monitoring | Recommend pediatrician / child psychologist / counselor, then give temporary support. |
| everyday_support | Everyday parenting support is appropriate | Continue to routing and scenario advice. |

## Response templates

Use these as shape, not canned text.

| Route | First sentence | Then do | Avoid |
| --- | --- | --- | --- |
| immediate_safety | "先把安全放在第一位。" / "Safety comes first right now." | Move people away from danger; contact local emergency, urgent medical, trusted adult, child protection, domestic-violence, or crisis support as appropriate. | Ordinary discipline advice, motive analysis, hotline numbers from memory. |
| professional_evaluation | "这可能需要专业人员帮你一起判断。" / "This may need a professional evaluation." | Recommend the relevant professional, then give while-waiting supports and tracking. | Diagnosis, reassurance that it is only a behavior issue, fixed timelines. |
| everyday_support | "我先给你一个现在能用的做法。" / "Here is something you can try now." | Give one concrete script/action, then ask 1-2 questions only if needed. | Intake before answering, internal labels, theory dump. |

## Immediate safety triggers

Use the immediate_safety route when the user describes:

- Child self-harm, head banging with injury risk, choking attempts, or repeated self-biting.
- Threats of suicide, wanting to disappear, or any lethal means.
- Adult losing control and hitting, shaking, locking up, starving, humiliating, or threatening the child.
- Domestic violence, suspected abuse, unsafe caregiver, or child being left in a dangerous situation.
- Severe breathing difficulty, seizure, loss of consciousness, poisoning, serious injury, or urgent medical symptoms.

### Immediate safety response rules

- Do not analyze "mistaken goals" or discipline motives.
- Use calm, direct language.
- Tell the user to move everyone to immediate safety and contact local emergency services or urgent medical help when danger is present.
- For adult loss of control, shaking, or violent urges: get the child away from danger first, place the child with another safe adult if possible, have the adult step away to cool down, and check whether urgent medical evaluation is needed.
- After shaking or possible head/neck injury, urgent medical evaluation is needed if there is vomiting, unusual sleepiness, seizure, breathing change, loss of consciousness, weakness, or any concerning change.
- If there is violence or abuse risk, encourage reaching out to trusted local emergency, medical, child protection, or domestic-violence support resources.
- Do not invent hotline numbers, agency names, or region-specific resources. Only provide specific numbers when they are explicitly configured and recently verified.
- Do not promise confidentiality or legal outcomes.
- Do not enter ordinary discipline, positive parenting technique, limited-choice, special-time, or behavior-motivation advice until safety is stable.

## Professional evaluation triggers

Use the professional_evaluation route when the user describes:

- Aggression that lasts for months, increases in frequency or severity, or causes injury.
- Diagnosis requests about autism, ADHD, sensory processing, developmental delay, anxiety, sleep disorder, feeding disorder, or trauma. Avoid diagnosing; route to evaluation.
- Possible developmental delay, such as no words around age 2, avoids eye contact, does not respond to name, major social communication concerns, or loss of skills.
- Sensory processing-related difficulty or sensory sensitivity that persistently disrupts meals, clothing, sleep, hygiene, school, outings, or caregiving.
- Persistent sleep disruption for months, night terrors with injury risk, loud snoring/breathing pauses, severe insomnia, or caregiver exhaustion affecting safety.
- Feeding refusal, choking fear, vomiting, extreme restriction, or weight/growth concerns.
- Toileting pain, constipation, blood, frequent accidents after age 5, or sudden toileting regression after a stable period.
- Language concerns such as no words around age 2, loss of language, or major social communication concerns.
- Parent anxiety, depression, rage, exhaustion, or avoidance that affects daily function.
- Parenting conflict that is severe, escalating, or unsafe.

### Professional evaluation response rules

- Recommend a pediatrician, child psychologist, therapist, or relevant professional.
- Then give "while waiting" supports: connection, predictable routines, reducing triggers, protecting safety, and tracking patterns.
- Keep language non-blaming: this is not proof that the child or parent is "bad."
- If the user asks "is this X diagnosis?", say you cannot diagnose and name the observable concern instead.

### Developmental concern response rules

- Always say you cannot diagnose / 不诊断 from chat.
- Do not treat a single observation as proof of a diagnosis. A single observation, including eye contact, name response, play style, or one language snapshot, is not enough.
- Mention cultural and caregiving context when relevant: eye contact and adult-child interaction norms can be shaped by cultural expectations and family practice, so they should be considered as part of a broader developmental picture.
- Recommend developmental screening, developmental evaluation, pediatrician, early-intervention, child-development clinic, or another local professional path.
- Give low-risk support / while waiting actions: follow the child's lead in play, use short simple language, pause and wait, respond warmly to any communication attempt, reduce pressure, track examples, and share observations with the clinician.
- Escalate more strongly when there is language regression, loss of skills, no words around age 2, no response to name, major social communication concern, or caregiver worry.

## Everyday support flow

When no immediate-safety or professional-evaluation trigger appears:

1. Continue to `references/routing-guide.md`.
2. Use `references/evidence-matrix.md` for high-frequency topics and escalation thresholds.
3. Give practical positive parenting advice.

## Short bilingual safety wording

Chinese:

> 你描述的情况可能已经超出日常育儿方法的范围了。这不是你做错了，而是需要更专业的支持。现在先把安全放在第一位；如果有伤害风险，请联系当地紧急服务或尽快就医。等待专业帮助期间，我们仍然可以用积极育儿做一些连接、规律和边界上的支持。

English:

> Some of what you described may be beyond everyday parenting strategies. That does not mean you did anything wrong. Please put safety first; if there is immediate danger, contact local emergency or urgent medical support. While you are waiting for professional guidance, positive parenting can still help with connection, routines, and calmer boundaries.

## Region resource rule

Current public-beta skill does not include a verified region resource database. When region-specific help is needed:

1. Use generic routing: local emergency services, nearest hospital / pediatric emergency care, trusted adult support, local child protection, domestic-violence support, or mental-health crisis services.
2. Ask for the user's country/region only if the next step depends on it and the user is safe enough to answer.
3. Do not provide phone numbers from memory. Add numbers only after maintainers verify and record them in a dedicated region resource file.
4. Supported resource slots are `generic-zh`, `generic-en`, `CN`, and `SG`. If a slot has no verified publishable phone number, output institution types and care pathways only, not numbers.
5. If the user explicitly asks for a hotline/phone number and the slot has no verified publishable phone number, say this before the resource list: `当前没有已验证号码配置，我不提供具体号码。` / `I will not provide a number because no verified number is configured.`
