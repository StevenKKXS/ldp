# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 51 |
| Recent Progress | Unified main experiment `_emb` configs to `global_obs=16` by changing Square and Transport from `2` to `16`; Tool-Hang and LongSquare were already `16`. Verified all four main configs now report `global_obs: 16`. Checkpoint behavior remains config-driven: Square/Transport save and rollout every `100` epochs; Tool-Hang/LongSquare save and rollout every `50` epochs. Checkpoints are written under each Hydra output directory's `checkpoints/` folder as `latest.ckpt` plus top-k `epoch=....ckpt` files keyed by `test_mean_score`. |
