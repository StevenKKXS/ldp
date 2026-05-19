# 全局实验状态

Last updated: 2026-05-19

## 当前 Active Plan

- Global: `docs/plans/plan_init_2026-05-18.md`
- Execution: `docs/plans/encoder_probe_execution_2026-05-18.md`
- Direction A: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Direction B: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`

## 总体状态表

| Direction | Status | Current Task | Current Experiment | Latest Result | Next Step |
|---|---|---|---|---|---|
| A: Future-Action Contrastive | Downstream probes running | Square / ToolHang | `20260519_session10`, `20260519_session10_extra` | Early train/val diffusion losses are close to original encoder baselines; no rollout score yet | Let running exact-PTP probes continue and compare completed loss curves before any rollout request |
| B: Action-Sequence Predictive | Downstream probes running | Square / ToolHang | `20260519_session10`, `20260519_session10_extra` | Early Square finetuned rows are below original at epoch 17, but there is no rollout score yet | Let running exact-PTP probes continue and compare full vs future-only frozen/finetune curves |

## 当前实验顺序

1. Direction A: Square downstream exact-PTP frozen/finetune probe
2. Direction A: ToolHang downstream exact-PTP frozen/finetune probe
3. Direction B: Square downstream exact-PTP full/future frozen/finetune probe
4. Direction B: ToolHang downstream exact-PTP full/future frozen/finetune probe
5. 如果任一方向有效，再扩展 Push-T
6. 如果任一方向有效，再扩展 Transport

## 最新关键结论

- Direction A 已保存详细 plan 并完成初步 review。
- Direction A review 已根据用户澄清更新: first pass 优先保持 PTP policy 结构不变，只做 encoder pretraining。
- Direction A soft contrastive smoke 已在 Square 和 ToolHang raw image 数据上跑通；一次早期 smoke 暴露 `0 * -inf` NaN，commit `7dcc632` 通过 diagonal `log_p` masking 修复。
- Direction A 四个 long-run pretraining probes 已完成 10 epochs: Square seed42/43 final train loss `3.3737`/`3.3742`, ToolHang seed42/43 final train loss `2.6360`/`2.6395`.
- Direction B 已保存详细 plan 并完成初步 review。
- Direction B review 建议 first pass 保持 PTP policy 结构不变，只做 predictive encoder pretraining。
- Direction B predictive smoke 已在 Square 和 ToolHang raw image 数据上跑通，能写出只含 `obs_encoder.*` 权重的兼容 checkpoint。
- Direction B 四个 long-run pretraining probes 已完成 10 epochs: Square full/future final train loss `0.0167`/`0.0164`, ToolHang full/future final train loss `0.0243`/`0.0252`.
- 不允许把任何方向视为已验证有效。
- Session 10 downstream exact-PTP smoke passed for `B_square_full_seed42` frozen encoder: train loss `1.0785`, val loss `1.2045`, train action MSE `0.7062`.
- Session 10 main downstream matrix is running at `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10`.
- Session 10 extra downstream matrix is running at `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10_extra`.
- Latest main Square poll, epoch 17-18: original val `0.0965`, `B_full_frozen` `0.0933`, `B_full_finetune` `0.0865`, `A_future_finetune` `0.0866`.
- Latest main ToolHang poll, epoch 6: original val `0.1568`, `B_full_frozen` `0.1585`, `B_full_finetune` `0.1566`, `A_future_finetune` `0.1572`.
- Latest extra Square poll, epoch 7-8: `A_future_frozen` val `0.1001`, `B_future_frozen` `0.1012`, `B_future_finetune` `0.1144`, `A_future_seed43_finetune` `0.1126`.
- Latest extra ToolHang poll, epoch 1-2: `A_future_frozen` val `0.2679`, `B_future_frozen` `0.2668`, `B_future_finetune` `0.2624`, `A_future_seed43_finetune` `0.3481`.
- Current evidence is downstream train/val diffusion loss only; there is no rollout success-rate score.
- GPU node `10.100.2.4:35140` is running 16 downstream PTP training processes across 8 H200 GPUs. Raw-image PTP remains CPU/data-pipeline limited, so instantaneous SM utilization is low even while processes are active.
- New GPU `10.100.2.4:35140` has 8x H200 available for exploration.
- Initial environment check found `gmp-py310` with RoboMimic `0.4.0`; documented py39/RoboMimic `0.2.0` venv was not present on the node. Any smoke in 0.4.0 is an implementation feasibility observation, not final release-like evidence.
- Cached PTP embedding datasets bypass `obs_encoder`; encoder-pretraining downstream tests must either disable cached embeddings or regenerate embeddings.
- Session 8 long-run logs: `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/logs/20260518_session8/pids.tsv`.
- Session 8 long-run outputs and encoder checkpoints: `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8`.
