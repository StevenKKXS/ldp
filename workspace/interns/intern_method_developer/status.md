# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task006_eval_official_robomimic_square_bcrnn -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task006_eval_official_robomimic_square_bcrnn |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_method_developer/task006_eval_official_robomimic_square_bcrnn |
| Session | 8 |

## 最近进展
- 已暂停 DP no-hist 训练启动，先整理实验关键参数供确认：拟用 Square image absolute-action 数据、Diffusion Policy UNet image policy、`n_obs_steps=2`、`n_action_steps=1`、`horizon=16`、1000 epoch，按 10/100 epoch 节奏保存并 rollout。
