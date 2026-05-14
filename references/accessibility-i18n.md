# Accessibility And I18n Templates

Use this file with `references/dialogue-modes.md` and `references/english-response-guide.md`.

## Chinese ordinary answer

- Target length: 120-220 Chinese characters for routine everyday-support cases.
- Short paragraphs, no dense bullet walls unless the user asks for a checklist.
- First give one concrete script/action, then ask at most 1-2 questions.
- Avoid theory labels, mixed-language jargon, decorative emoji, and forced intimate child nicknames.
- Use the role the user gives. If no role is given, use neutral words such as "你" and "孩子".

Template:

```text
先稳住一句话：[script]。

现在你做 [action]。下次提前 [prevention]。

我只需要再确认一个点：[question]
```

## English ordinary answer

- Write natural English independently; do not translate Chinese sentence order.
- Target length: 150-250 words for ordinary everyday-support cases.
- Avoid "defiant", "manipulative", "naughty", and diagnostic certainty.
- Do not import Chinese caregiver terms into English answers.

Template:

```text
Try this first: "[script]"

Then [action]. For next time, [prevention].

One thing I would check: [question]
```

## Bilingual sharing

- Use paired short scripts or a compact note.
- Do not paste two full complete essays.
- Keep private child logs out.

Template:

```text
中文：今晚我们只守一个规则：[rule]。我们一起说：[script]。

English: Tonight we keep one rule: [rule]. We both say: "[script]"
```

## Easy-read / TTS

- One action per line.
- 3-6 lines.
- No parenthetical theory.
- No mixed Chinese-English unless requested.
- Prefer verbs: "抱开", "蹲下", "说", "等", "记录".
- Keep the critical action even when compressing the answer.
- In one-sentence mode, include exactly one script or one next action, not a slogan.
- In standard mode, include one script, one action, and one prevention cue.
- In formal mode, be restrained and practical: no cute tone, no decorative emoji, no forced kinship labels.
- In deep mode, explain the reason only after the user has a usable action.

Acceptance checks:

| Mode | Length target | Must contain |
| --- | --- | --- |
| one-sentence mode | 1 sentence, 30 Chinese characters or fewer when possible | critical action or exact script |
| easy-read / TTS | 3-6 lines | one action per line, no theory labels |
| standard mode | 120-220 Chinese characters or 150-250 English words | script, next action, one check |
| formal mode | compact, restrained paragraphs | practical action, respectful wording |
| deep mode | user-requested only | reason, boundary, example |

Template:

```text
先把孩子带到安全边上。
蹲下来。
说："[script]"
少解释。
等哭声变小，再走下一步。
```
