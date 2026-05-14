---
tags: [积极育儿, 反馈闭环, 可选巡检]
created: 2026-05-10
---

# 反馈闭环与可选巡检协议

## 实践反馈闭环（每次互动时执行）

### 触发条件
1. 用户反馈了某个工具/方法的实际使用效果（"昨晚试了XX"）
2. 用户描述了一个新的场景（追加到"当前关注"）
3. 用户纠正了画像中的信息

### 更新规则
- **用户说管用** → 用户确认后，可写入 Outcome: `helped`
- **用户说不管用** → 先追问"当时具体怎么说的/做的"，用户确认后，可写入 Outcome: `not-helpful`
- **用户说部分有效** → 用户确认后，可写入 Outcome: `partly-helped`，再建议只调整一个变量
- **用户描述了新场景** → 先给当前回答；用户确认后，可写入 Case

写入前先读 `references/state-schema.md`，用 confirmation summary 说明将写入哪些字段、是否含可识别信息、是否已降敏，以及是否需要用户确认。用户确认的信息写入 facts / Case / Intervention / Outcome；模型判断只能写入 hypotheses。状态文件缺失、损坏或不可写时，不阻断当前回答。

### 建议前必查
如果本地状态可读，给出新建议前可以参考最近实践记录：
- 最近 7 天内 ❌ → 不再推荐同一个,换工具
- 最近 7 天内 ✅ → 强化使用,可以进阶
- 最近 7 天内 ⚠️ → 调整使用方式后再推荐

### 反馈追问
用户只描述场景没反馈效果时,温和地问问：
> "上次一起探索的那个方法,你有试过吗？想听听你的感受。"

---

## 可选 HEARTBEAT 巡检协议

Status: Spec-only。HEARTBEAT 只是可选集成，不是核心流程依赖。只有用户明确开启，并且目标平台支持时，才在用户的 HEARTBEAT.md 中注册巡检项。

### 巡检 1: 每周学习进度（每周日 20:00）

1. 读取 `learning-progress.md`
2. 如果用户正在练习某个 goal-driven track：
   - 检查 `goal_type`、`practice_action`、`review_metric` 和 `last_reviewed_at`
   - 超过约定复盘时间 → 温和提醒：
     > "积极育儿练习小提醒：你上次在练 [goal_type]。
     > 不着急，今晚有空的话可以用 5 分钟看一下：结果、可能原因、要不要只调一个变量。"
   - 还在约定观察期内 → 不打扰
3. 用户还没开始学习 → 不提醒（不强迫）

### 巡检 2: 每月实践回顾草案（每月 1 日）

Status: Spec-only。当前 `scripts/state_service.py` 不会定时生成或写入月度回顾。若宿主平台实现 HEARTBEAT，可在用户明确开启后读取本地 state export，生成草案，并在用户确认后再写入 Outcome 或 LearningTrack 相关字段。

草案可以包含：

- 本月用户确认过的练习次数
- 哪个 Intervention 反馈较好
- 哪个 Outcome 仍需调整
- 下个月只建议关注的一个变量

### 巡检 3: 场景关注更新（每两周）

Status: Spec-only。当前仓库不自动更新"当前关注"。若宿主平台实现该巡检，必须先生成 confirmation summary，并在用户确认后写入 Case / Outcome / LearningTrack。

---

## 本地档案更新规则

Status: Implemented locally through `scripts/state_service.py` as a reference implementation; actual product storage still requires a host platform. If storage is missing, damaged, or unsupported, continue answering and do not claim a write happened.

| 用户行为 | 更新动作 |
|---------|---------|
| 提到孩子长大或年龄段变化 | 用户确认后，更新 ChildProfile.age_band；不默认保存精确生日 |
| 描述了育儿场景 | 用户确认后，写入 Case |
| 给出一个建议或脚本 | 用户确认后，可写入 Intervention |
| 反馈了方法效果 | 用户确认后，写入 Outcome |
| 纠正了信息 | 用户确认后，correct ChildProfile 或相关实体字段 |
| 要求删除或匿名化 | 使用 delete / anonymize；完成后 export 不应残留 direct identifier |
