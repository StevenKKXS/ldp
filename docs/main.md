# PTP Encoder 改进实验入口

## 当前采用的总计划

- Active global plan: `docs/plans/plan_init_2026-05-18.md`

## 当前候选方向

### Direction A: Future-Action / Behavior Contrastive History Encoder

- Active plan: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_a_future_action_contrastive/review_2026-05-18.md`
- Latest review update: `docs/direction_a_future_action_contrastive/review_update_ptp_compat_2026-05-18.md`
- Status file: `docs/direction_a_future_action_contrastive/status.md`
- Experiment file: `docs/direction_a_future_action_contrastive/experiments.md`
- Observation log: `docs/direction_a_future_action_contrastive/obs_log.md`
- 当前阶段: 已 review，优先定型 PTP-compatible encoder pretraining

### Direction B: Action-Sequence Predictive Encoder Pretraining

- Active plan: `docs/direction_b_action_sequence_predictive/plan_init_2026-05-18.md`
- Status file: `docs/direction_b_action_sequence_predictive/status.md`
- Experiment file: `docs/direction_b_action_sequence_predictive/experiments.md`
- Observation log: `docs/direction_b_action_sequence_predictive/obs_log.md`
- 当前阶段: 等待详细 plan review

## 文件说明

- `main.md`: 总入口，记录当前采用的 plan 和文档索引。
- `agents.md`: agent 工作规则，尤其是 review、状态更新和防幻觉规则。
- `status.md`: 全局状态概览。
- `plans/`: 总计划历史。
- `direction_a_*/`: Direction A 的方案、实验和 observation。
- `direction_b_*/`: Direction B 的方案、实验和 observation。

## 当前任务顺序

1. 保存并 review Direction A / Direction B 初始 plan。
2. agent 对两个方向提出异议或补充建议。
3. 如果没有新的关键 idea，先在 Square 和 ToolHang 上验证。
4. 如果 Square / ToolHang 至少一个任务出现稳定提升，再扩展 Push-T 和 Transport。
5. 每次实验后更新对应方向的 `obs_log.md`、`experiments.md` 和 `status.md`。

## 当前约束

- 当前只有启动规则和方向草案，没有实验结果。
- 不允许声称 Direction A 或 Direction B 已经有效。
- GPU 资源在用户明确分配前不申请、不使用。
- Direction A 已保存详细 plan 和 review；仍未进入实现或实验。
