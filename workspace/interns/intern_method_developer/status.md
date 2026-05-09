# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task006_eval_official_robomimic_square_bcrnn -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task006_eval_official_robomimic_square_bcrnn |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_method_developer/task006_eval_official_robomimic_square_bcrnn |
| Session | 30 |

## 最近进展
- 当前可访问四个 GPU 入口：`10.100.16.46:16139`、`10.100.16.46:23989`、`10.100.2.35:26482`、`10.100.2.35:17821`，每个入口各可见 2 张 NVIDIA H200。
- `16139` 旧环境 DP no-hist 四路仍在训练：UNet official-PH epoch 762 best `0.68`，DiT official-PH epoch 812 best `0.60`，UNet LDP-MH epoch 282 best `0.06`，DiT LDP-MH epoch 296 best `0.04`。
- `23989` 旧环境 SmolVLA 四路训练已完成 epoch 1000；原 post-train monitor 在 2026-05-08 17:58 UTC 未生成报告，Session 30 已用 stamp `20260509_old_smolvla_resume` 重新启动 all-checkpoint rollout。
- Session 21 已新增 `current_work_handoff.md`，记录当前全部实验、路径、数据版本、脚本入口，以及迁移到 H200 py39 + robomimic 0.2.0 环境后的复测步骤。
- Session 22 已在 `origin/main` 找到 py39 H200 环境文档：`workspace/shared/ldp_ptp_py39_h200_environment.md`，提交 `968f3ca`。
- Session 23 于 2026-05-08 14:40 UTC 检查：DP 四路仍在跑，official-PH 最好 rollout 为 UNet epoch 90 `0.68`、DiT epoch 70 `0.60`；SmolVLA 四路仍在训练，official-PH 到约 epoch 850/875，PTP/LDP-MH 到约 epoch 330，`epoch_1000.pt` 仍为 `0/4`。
- Session 24 分析 DP 比 SmolVLA 慢的主因：DP 将 50-rollout、50-video、`num_inference_steps=100`、`n_action_steps=1` 的闭环评估嵌入训练，且 batch size 64 导致每 epoch optimizer steps 约为 SmolVLA 的两倍；SmolVLA 当前只做离线 eval。
- Session 25 估算 DP 运行时长与 20-rollout 提速：当前四路已跑约 `5.6h`；20 rollout 主要提升前 100 epoch 的 eval-every-10 阶段，official-PH 约提速 `40-45%`，LDP-MH 约提速 `20-30%`，100 epoch 后因 eval 每 100 epoch 一次整体收益约 `2-6%`。
- Session 26 估算 DP 完成时间：official-PH 两路预计 2026-05-09 05:40-06:20 UTC 完成；总完成时间由 LDP-MH 决定，预计 2026-05-10 夜间到 2026-05-11 上午 UTC，保守按当前均速可到 2026-05-11 13:00 UTC 左右。
- Session 27 估算 SmolVLA 剩余时间：official-PH 两路已完成 epoch 1000，PTP/LDP-MH 两路约 epoch 421；训练预计 2026-05-08 18:00 UTC 左右完成，自动 rollout/report 预计再需约 `50-60min`。
- Session 28 汇总当前 rollout 成功率：DP official-PH 最好为 UNet `0.68`、DiT `0.60`，DP LDP-MH 仍低于 `0.06`；当前四路 SmolVLA 尚无 rollout，既有 SmolVLA 50-rollout 最好为 big384 LDP-MH `0.26`，BC-RNN issue157 最好 `0.80`。
- Session 29 查验新 GPU 入口 `10.100.2.35:26482` 和 `10.100.2.35:17821`：两边各 2 张空闲 H200，UUID 不同；当前仅有 Python 3.12.3，未发现 `/root/ptp_ldp_py39` 或 MuJoCo 2.1.0。
- Session 30 已在 `10.100.2.35:26482` 和 `10.100.2.35:17821` 配好 py39 + robomimic 0.2.0 + robosuite 1.2.0 环境，完成数据/env/video、SmolVLA 1-epoch、DP UNet/DiT train+rollout smoke test，并挂起 py39 对比实验。
- 新 py39 对比实验：`26482` 跑 DP no-hist UNet/DiT × PTP-LDP-MH/official-PH v1.4.1，前 100 epoch 每 20 epoch rollout；`17821` 跑 SmolVLA small/big384 × 两套数据，monitor 将训练后做全 checkpoint 20-rollout 和 best 50-rollout。
- 2026-05-09 进度：py39 SmolVLA 已完成并生成报告，最好为 big384 PTP/LDP-MH epoch 400，`16/50 = 0.32`；py39 DP 四路仍在训练，当前 best 为 UNet LDP-MH `0.36`、DiT official-PH `0.48`、DiT LDP-MH `0.10`、UNet official-PH `0.10`。
- Session 30 已新增 `ROLLOUT_BEST_SUMMARY_20260509.md`，按运行版本、模型设定、数据版本汇总当前最好的 closed-loop rollout；旧环境四路 SmolVLA 补跑仍标记为 pending。
- Session 30 已新增 `DP_ROLLOUT_EVAL_CURVES_20260509.md`，展开旧环境 DP official-PH 的 scheduled rollout 曲线：UNet 最好 epoch 90 `34/50 = 0.68`，DiT 最好 epoch 70 `30/50 = 0.60`。
