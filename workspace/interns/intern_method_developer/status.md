# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task006_eval_official_robomimic_square_bcrnn -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task006_eval_official_robomimic_square_bcrnn |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_method_developer/task006_eval_official_robomimic_square_bcrnn |
| Session | 4 |

## 最近进展
- 已核对 SmolVLA checkpoint 保存逻辑和实际输出：命名 checkpoint 按 offline eval 频率保存，即 epoch 10-100 每 10 个 epoch 一次，之后每 100 个 epoch 一次到 1000；`latest.pt` 还会在每个 eval epoch 和每 25 个 epoch 的 checkpoint 触发点覆盖保存。
