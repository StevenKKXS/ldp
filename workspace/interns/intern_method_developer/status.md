# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task006_eval_official_robomimic_square_bcrnn -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task006_eval_official_robomimic_square_bcrnn |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_method_developer/task006_eval_official_robomimic_square_bcrnn |
| Session | 16 |

## 最近进展
- 已确认新 GPU 入口 `10.100.16.46:23989` 上 SmolVLA 四路训练按每卡两个任务运行：GPU0 运行 PTP small + official v1.4.1 big384，GPU1 运行 PTP big384 + official v1.4.1 small。
- 2026-05-08 13:19 UTC 检查时四个主 PID 均存活，GPU dmon 采样显示两张 H200 的 SM util 基本在 89%-99%。
- 当前进度：official-PH v1.4.1 两个任务已经越过 epoch 100，PTP/LDP-MH 两个任务在 epoch 57 附近继续推进。
