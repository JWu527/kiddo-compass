# Kiddo Compass Public Beta Kanban

本看板把 deep research 报告中的优化建议收敛到当前 OpenClaw skill 仓库范围。当前目标是内部测试可控和 public-beta candidate，不是直接公开发布，也不是做 App、小程序、付费系统或真实埋点。

## 公测门槛

- 发布包由 `skill-package-manifest.txt` 白名单生成，不包含真实儿童、家庭、学校、电话、地址或实践日志。
- 常规回答先安全分诊，再做年龄-场景-照护者路由。
- 没有画像时也能先给临时建议，不强制五轮建档。
- 高频场景至少有安全边界、年龄提醒、话术和失败后的下一步。
- 中文和英文走同一安全与路由逻辑。
- 发布前通过 YAML、链接、隐私、白名单包和 P0 回归检查。

## 看板

状态口径：

- `Done (skill beta)`：当前 OpenClaw skill 公测版范围内已经可用。
- `Partial`：已有第一版产出，但距离 deep research 报告的完整验收标准仍有差距。
- `Deferred`：依赖 App / 小程序 / 账号 / 存储 / 支付 / 专家资源，当前 skill 版本不实现。

| 阶段 | 状态 | ID | 卡片 | 当前产出 |
| --- | --- | --- | --- | --- |
| P0 发布安全闸门 | Done (internal beta gate) | H-01 | 去种子化复核 | `.gitignore` / `.clawhubignore` 保护运行期文件；`skill-package-manifest.txt` 白名单打包；`scripts/release_guardrails.py` 做隐私与红线扫描 |
| P0 发布安全闸门 | Partial | H-07 | 安全分诊前置 | `references/safety-triage.md`，并接入 `SKILL.md` 主流程；仍缺地区资源位和安全规则运营更新机制 |
| P0 发布安全闸门 | Done (skill beta) | H-03 | 渐进式建档 | `SKILL.md` 改为先答后补档，完整五轮建档变为可选路径；补档后需让用户确认事实 |
| P1 内容稳定层 | Done (skill beta) | H-05 | 证据矩阵 | `references/evidence-matrix.md` 覆盖 30 个高频主题；长文笔记更深的来源标签留作后续增强 |
| P1 内容稳定层 | Partial | H-06 | 年龄-场景-照护者路由 | `references/routing-guide.md` 已定义三维路由；仍需更多路由样例和回归验证 |
| P1 内容稳定层 | Partial | M-01 | 场景模板标准化 | `references/scenario-template.md` 扩展为 20 个公测场景卡；仍需深写内容包、来源标签和变体测试 |
| P2 质量与回归 | Done (skill beta gate) | H-09 | 轻量评测集 | `references/evaluation-set.jsonl` + `scripts/run_regression.py` + `scripts/beta_kpi_gate.py` 覆盖 P0/P1 回归数据、模式/语言覆盖和静态 KPI gate；真实埋点、仪表盘和周报延期到平台层 |
| P2 质量与回归 | Done (skill beta) | - | 发布检查清单 | `PUBLISHING.md` 补充公测版检查命令 |
| P3 体验增强 | Done (text beta) | M-02 | 低认知负荷输出 | `references/dialogue-modes.md` 和 `references/accessibility-i18n.md` 明确 easy-read / TTS、中文、英文和双语模板；UI 可访问性和可用性测试延期 |
| P3 体验增强 | Partial | M-03 | 家庭协同卡片 | `references/scenario-template.md` 增加家庭规则卡和祖辈沟通卡；共享权限和 co-parent 视图延期 |
| Parking Lot | Deferred | H-02 / H-04 / H-08 | 同意 UI、结构化状态服务、平台存储抽象 | 等进入 App / 小程序阶段再设计 |
| Parking Lot | Deferred | M-04 / M-05 / L-01 | 目标驱动学习、商业化、专家网络、社区 | 不进入当前 skill 公测范围 |

## 后续版本建议

- `0.4.x`：把 20 个公测场景卡补上更细的证据标签、年龄差异和更多失败后路径。
- `0.5.x`：把 JSONL 回归接入语义评分 harness。
- `1.0.0`：冻结公测版触发、分诊、路由、评测规则，发布稳定版。

完整覆盖度见 `PUBLIC_BETA_COVERAGE.md`。
