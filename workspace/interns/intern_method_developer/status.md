# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task006_eval_official_robomimic_square_bcrnn -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task006_eval_official_robomimic_square_bcrnn |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_method_developer/task006_eval_official_robomimic_square_bcrnn |
| Session | 9 |

## 最近进展
- 已解释 DP 配置中 `horizon=16` 的含义：它是 diffusion policy 一次去噪建模的动作序列长度，不是 rollout 最大步数；rollout 每次实际执行动作数由 `n_action_steps` 控制。
