# Kiddo Compass Public Beta Kanban

本看板把 deep research 报告中的优化建议收敛到当前 OpenClaw skill 仓库范围。目标不是做 App、小程序、付费系统或真实埋点，而是把 skill 推到可公开复用的公测版。

## 公测门槛

- 发布包不包含真实儿童、家庭、学校、电话、地址或实践日志。
- 常规回答先安全分诊，再做年龄-场景-照护者路由。
- 没有画像时也能先给临时建议，不强制五轮建档。
- 高频场景至少有安全边界、年龄提醒、话术和失败后的下一步。
- 中文和英文走同一安全与路由逻辑。
- 发布前通过 YAML、链接、隐私和轻量评测集检查。

## 看板

| 阶段 | 状态 | ID | 卡片 | 当前产出 |
| --- | --- | --- | --- | --- |
| P0 发布安全闸门 | Done | H-01 | 去种子化复核 | `.gitignore` / `.clawhubignore` 保护运行期文件；示例模板改为隐私友好字段 |
| P0 发布安全闸门 | Done | H-07 | 安全分诊前置 | `references/safety-triage.md`，并接入 `SKILL.md` 主流程 |
| P0 发布安全闸门 | Done | H-03 | 渐进式建档 | `SKILL.md` 改为先答后补档，完整五轮建档变为可选路径 |
| P1 内容稳定层 | Done | H-05 | 证据矩阵 | `references/evidence-matrix.md` 覆盖睡眠、喂养、如厕、攻击、分离 |
| P1 内容稳定层 | Done | H-06 | 年龄-场景-照护者路由 | `references/routing-guide.md` |
| P1 内容稳定层 | Done | M-01 | 场景模板标准化 | `references/scenario-template.md`，含 8 个高频场景骨架 |
| P2 质量与回归 | Done | H-09 | 轻量评测集 | `references/evaluation-set.md`，含中英文路由和安全场景 |
| P2 质量与回归 | Done | - | 发布检查清单 | `PUBLISHING.md` 补充公测版检查命令 |
| P3 体验增强 | Done | M-02 | 低认知负荷输出 | `SKILL.md` 增加超短 / 标准 / 深度模式 |
| P3 体验增强 | Done | M-03 | 家庭协同卡片 | `references/scenario-template.md` 增加家庭规则卡和祖辈沟通卡骨架 |
| Parking Lot | Deferred | H-02 / H-04 / H-08 | 同意 UI、结构化状态服务、平台存储抽象 | 等进入 App / 小程序阶段再设计 |
| Parking Lot | Deferred | M-05 / L-01 | 商业化、专家网络、社区 | 不进入当前 skill 公测范围 |

## 后续版本建议

- `0.4.x`：把 8 个场景骨架扩写成完整可用卡片。
- `0.5.x`：把证据矩阵扩展到屏幕、兄弟姐妹、公共场所、家务拖延。
- `1.0.0`：冻结公测版触发、分诊、路由、评测规则，发布稳定版。
