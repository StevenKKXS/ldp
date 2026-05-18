# 全局实验状态

Last updated: 2026-05-18

## 当前 Active Plan

- Global: `docs/plans/plan_init_2026-05-18.md`
- Execution: `docs/plans/encoder_probe_execution_2026-05-18.md`
- Direction A: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Direction B: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`

## 总体状态表

| Direction | Status | Current Task | Current Experiment | Latest Result | Next Step |
|---|---|---|---|---|---|
| A: Future-Action Contrastive | Smoke passed; pretraining probes running | Square / ToolHang | `A_square_future_seed42`, `A_square_future_seed43`, `A_tool_hang_future_seed42`, `A_tool_hang_future_seed43` | Soft contrastive pretraining runs without NaN after diagonal `log_p` masking fix | Monitor pretraining losses and produce encoder checkpoints for downstream PTP frozen/finetune tests |
| B: Action-Sequence Predictive | Smoke passed; pretraining probes running | Square / ToolHang | `B_square_full_seed42`, `B_square_future_seed42`, `B_tool_hang_full_seed42`, `B_tool_hang_future_seed42` | Huber predictive pretraining runs on raw image Square and ToolHang | Monitor full vs future-only predictive loss and produce encoder checkpoints for downstream PTP frozen/finetune tests |

## 当前实验顺序

1. Direction A: Square pretraining probe
2. Direction A: ToolHang pretraining probe
3. Direction B: Square pretraining probe
4. Direction B: ToolHang pretraining probe
5. 如果任一方向有效，再扩展 Push-T
6. 如果任一方向有效，再扩展 Transport

## 最新关键结论

- Direction A 已保存详细 plan 并完成初步 review。
- Direction A review 已根据用户澄清更新: first pass 优先保持 PTP policy 结构不变，只做 encoder pretraining。
- Direction A soft contrastive smoke 已在 Square 和 ToolHang raw image 数据上跑通；一次早期 smoke 暴露 `0 * -inf` NaN，commit `7dcc632` 通过 diagonal `log_p` masking 修复。
- Direction B 已保存详细 plan 并完成初步 review。
- Direction B review 建议 first pass 保持 PTP policy 结构不变，只做 predictive encoder pretraining。
- Direction B predictive smoke 已在 Square 和 ToolHang raw image 数据上跑通，能写出只含 `obs_encoder.*` 权重的兼容 checkpoint。
- 不允许把任何方向视为已验证有效。
- 当前结果只是 encoder pretraining implementation feasibility；没有 downstream PTP policy score。
- Direction A / B 的下一步是使用这些 encoder checkpoint 做 exact-PTP policy frozen/finetune ablation。
- New GPU `10.100.2.4:35140` has 8x H200 available for exploration.
- Initial environment check found `gmp-py310` with RoboMimic `0.4.0`; documented py39/RoboMimic `0.2.0` venv was not present on the node. Any smoke in 0.4.0 is an implementation feasibility observation, not final release-like evidence.
- Cached PTP embedding datasets bypass `obs_encoder`; encoder-pretraining downstream tests must either disable cached embeddings or regenerate embeddings.
- Session 8 long-run logs: `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/logs/20260518_session8/pids.tsv`.
- Session 8 long-run outputs and encoder checkpoints: `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8`.
