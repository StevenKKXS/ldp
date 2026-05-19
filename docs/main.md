# PTP Encoder 改进实验入口

## 当前采用的总计划

- Active global plan: `docs/plans/plan_init_2026-05-18.md`
- Current owner focus for `intern_ldp_explorer`: Direction C only. Direction A/B are owned by another intern.

## 当前候选方向

### Direction A: Future-Action / Behavior Contrastive History Encoder

- Active plan: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_a_future_action_contrastive/review_2026-05-18.md`
- Latest review update: `docs/direction_a_future_action_contrastive/review_update_ptp_compat_2026-05-18.md`
- Status file: `docs/direction_a_future_action_contrastive/status.md`
- Experiment file: `docs/direction_a_future_action_contrastive/experiments.md`
- Observation log: `docs/direction_a_future_action_contrastive/obs_log.md`
- 当前阶段: 已 review；not owned by `intern_ldp_explorer`

### Direction B: Action-Sequence Predictive Encoder Pretraining

- Active plan: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_b_action_sequence_predictive/review_2026-05-18.md`
- Status file: `docs/direction_b_action_sequence_predictive/status.md`
- Experiment file: `docs/direction_b_action_sequence_predictive/experiments.md`
- Observation log: `docs/direction_b_action_sequence_predictive/obs_log.md`
- 当前阶段: 已 review；not owned by `intern_ldp_explorer`

### Direction C: Behavior Translator Context Pretraining

- Active plan: `docs/direction_c_behavior_translator/plan_review_2026-05-19.md`
- Status file: `docs/direction_c_behavior_translator/status.md`
- Experiment file: `docs/direction_c_behavior_translator/experiments.md`
- Observation log: `docs/direction_c_behavior_translator/obs_log.md`
- 当前阶段: `intern_ldp_explorer` 主负责，先做 offline translator 与 frozen-head probe，不接 DP/PTP

## 文件说明

- `main.md`: 总入口，记录当前采用的 plan 和文档索引。
- `agents.md`: agent 工作规则，尤其是 review、状态更新和防幻觉规则。
- `status.md`: 全局状态概览。
- `plans/`: 总计划历史。
- `direction_a_*/`: Direction A 的方案、实验和 observation。
- `direction_b_*/`: Direction B 的方案、实验和 observation。
- `direction_c_*/`: Direction C 的方案、实验和 observation。

## 当前任务顺序 for intern_ldp_explorer

1. Direction C: implement dataset/model/config smoke path.
2. Direction C: run Square offline translator Stage 1.
3. Direction C: run Square frozen-head probe Stage 2a.
4. Direction C: add ToolHang only after Square shape/loss path is stable.
5. Direction C: consider DP/PTP integration only after pretrained frozen context beats random frozen context.
6. 每次实验后更新 Direction C 的 `obs_log.md`、`experiments.md` 和 `status.md`。

## 当前约束

- PTP 数据相关实验硬约束：必须使用 Python 3.9 + `robomimic==0.2.0`。`gmp-py310` / `robomimic 0.4.0` 的结果只能当作版本消融，不能作为可信 PTP claim 复现结果。
- 新实验启动前必须记录 `sys.executable`、`robomimic.__version__`、`robomimic.__file__`，并确认版本为 `0.2.0`。
- 当前只有启动规则和方向草案，没有实验结果。
- 不允许声称 Direction A 或 Direction B 已经有效。
- GPU 资源在用户明确分配前不申请、不使用。
- Direction A/B 由另一个 intern 负责；`intern_ldp_explorer` 不把 A/B 放入自己的执行队列。
