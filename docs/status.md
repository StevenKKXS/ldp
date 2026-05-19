# 全局实验状态

Last updated: 2026-05-19

## 当前 Active Plan

- Global: `docs/plans/plan_init_2026-05-18.md`
- Direction A: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Direction B: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`

## 总体状态表

| Direction | Status | Current Task | Current Experiment | Latest Result | Next Step |
|---|---|---|---|---|---|
| A: Future-Action Contrastive | Reviewed, PTP-compatible plan preferred | Square / ToolHang | N/A | N/A | Finalize exact PTP baseline, contrastive action segment, encoder checkpoint protocol, and frozen/finetune settings |
| B: Action-Sequence Predictive | Reviewed, PTP-compatible plan preferred | Square / ToolHang | N/A | N/A | Finalize action target sequence, decoder capacity, checkpoint protocol, and frozen/finetune settings |

## 当前实验顺序

1. Direction A: Square
2. Direction A: ToolHang
3. Direction B: Square
4. Direction B: ToolHang
5. 如果任一方向有效，再扩展 Push-T
6. 如果任一方向有效，再扩展 Transport

## 最新关键结论

- PTP 数据相关训练、encoder pretraining 对比、rollout 复现必须使用 Python 3.9 + `robomimic==0.2.0`；`gmp-py310` / `robomimic 0.4.0` 结果不可作为可信 PTP-data 复现证据。
- 当前 FM GPU 节点 `10.100.2.35:33805` 尚未发现可用 `/root/ptp_ldp_py39`；继续可信实验前需要从 CPU/公共侧重建或同步并验证 py39 / `robomimic==0.2.0` 环境。
- 尚未开始实验。
- Direction A 已保存详细 plan 并完成初步 review，但没有实验结果。
- Direction A review 已根据用户澄清更新: first pass 优先保持 PTP policy 结构不变，只做 encoder pretraining。
- Direction B 已保存详细 plan 并完成初步 review，但没有实验结果。
- Direction B review 建议 first pass 保持 PTP policy 结构不变，只做 predictive encoder pretraining。
- 不允许把任何方向视为已验证有效。
- Direction A 需要先讨论 exact PTP baseline、contrastive action segment、encoder checkpoint format、frozen/finetune protocol、以及 B2 是否与 B1 区分。
- Direction B 需要先讨论 exact PTP baseline、predictive action target、decoder capacity、encoder checkpoint format、frozen/finetune protocol、以及 B2 是否与 B1 区分。
