# 全局实验状态

Last updated: 2026-05-20

## 当前 Active Plan

- Global: `docs/plans/plan_init_2026-05-18.md`
- Direction A: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Direction B: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`
- Direction C: `docs/direction_c_behavior_translator/plan_review_2026-05-19.md`

Owner note: `intern_ldp_explorer` is responsible for Direction C. Direction A/B are owned by another intern.

## 总体状态表

| Direction | Status | Current Task | Current Experiment | Latest Result | Next Step |
|---|---|---|---|---|---|
| A: Future-Action Contrastive | Reviewed, owned by another intern | Square / ToolHang | N/A | N/A | Not in intern_ldp_explorer execution queue |
| B: Action-Sequence Predictive | Reviewed, owned by another intern | Square / ToolHang | N/A | N/A | Not in intern_ldp_explorer execution queue |
| C: Behavior Translator Context | Active for intern_ldp_explorer, Stage 1 running | Square first | Three Square translator objectives: `past`, `future`, `past_future` | Runs reached epoch 43/44; `past` is the most stable validation objective so far. GPU3 CPU-pressure benchmark shows DataLoader IPC/shared-memory bottleneck before full CPU saturation. | Reach epoch 50, then compare best/epoch-50 checkpoints in Stage 2a frozen-head probe |

## 当前实验顺序 for intern_ldp_explorer

1. Direction C: Square dataset/model/config smoke
2. Direction C: Square offline translator Stage 1
3. Direction C: Square frozen-head probe Stage 2a
4. Direction C: ToolHang offline translator Stage 1
5. Direction C: ToolHang frozen-head probe Stage 2a
6. Direction C: DP/PTP integration only if Stage 2a passes the pretrained-vs-random gate

## 最新关键结论

- PTP 数据相关训练、encoder pretraining 对比、rollout 复现必须使用 Python 3.9 + `robomimic==0.2.0`；`gmp-py310` / `robomimic 0.4.0` 结果不可作为可信 PTP-data 复现证据。
- 当前 FM GPU 节点 `10.100.2.35:33805` 尚未发现可用 `/root/ptp_ldp_py39`；继续可信实验前需要从 CPU/公共侧重建或同步并验证 py39 / `robomimic==0.2.0` 环境。
- Direction C Stage 1 Square experiments are running on `10.100.2.35:25076` under Python 3.9 + `robomimic==0.2.0`.
- Direction A 已保存详细 plan 并完成初步 review，但没有实验结果；由另一个 intern 负责。
- Direction A review 已根据用户澄清更新: first pass 优先保持 PTP policy 结构不变，只做 encoder pretraining。
- Direction B 已保存详细 plan 并完成初步 review，但没有实验结果；由另一个 intern 负责。
- Direction B review 建议 first pass 保持 PTP policy 结构不变，只做 predictive encoder pretraining。
- Direction C implemented the offline translator path: raw obs history -> existing robomimic obs_encoder -> BehaviorTranslator -> past/future action sketch.
- Direction C Stage 1 active run root is `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage1_square_20260519_143020`.
- Direction C GPU3 CPU-pressure benchmark root is `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/benchmarks/stage1_square_past_cpu_extreme_20260520_020004_v2`; best valid same-batch setting was `batch=32,num_workers=64`, and fastest valid raw setting was `batch=64,num_workers=96`.
- `intern_ldp_explorer` 当前主线是 Direction C，不主动推进 Direction A/B。
- 不允许把任何方向视为已验证有效。
- Direction A 需要先讨论 exact PTP baseline、contrastive action segment、encoder checkpoint format、frozen/finetune protocol、以及 B2 是否与 B1 区分。
- Direction B 需要先讨论 exact PTP baseline、predictive action target、decoder capacity、encoder checkpoint format、frozen/finetune protocol、以及 B2 是否与 B1 区分。
