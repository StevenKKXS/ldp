# PTP / LDP Square 提分建议

日期：2026-05-11 UTC

目标：在现有 PTP / LDP-MH Square 设置上，把闭环 rollout 成功率调到当前结果之上。当前最有价值的起点不是 SmolVLA，而是 py39 / robomimic 0.2 / robosuite 1.2 环境下的 DP no-hist UNet：best epoch 900 为 `25/50 = 0.50`。

## 先定基线

| 设定 | 当前结果 | 判断 |
| --- | ---: | --- |
| py39 + PTP/LDP-MH + DP UNet no-hist | best `0.50`, final `0.42` | 当前最值得继续调的主线 |
| py39 + PTP/LDP-MH + DP DiT no-hist | best `0.24`, final `0.20` | 可做结构对照，不是主攻线 |
| current-stack + PTP/LDP-MH + DP UNet | best `0.10` | 更像版本错配负例 |
| SmolVLA PTP/LDP-MH | best `0.32` | 当前 recipe 不建议作为短期提分主线 |

## 工程优先级

1. 先把评估协议固定住。

   用固定 eval seed 集合做 quick eval，再用独立 seed 集合做确认。`50` rollouts 的统计噪声不小，`0.50` 的二项分布 95% 误差大约是正负 `0.14`，所以小于 `0.10` 的提升不应只凭一组 50-rollout 下结论。建议保留 50-rollout 作为训练中筛选，最终候选用 100 或 200 rollout 确认。

2. 主攻 DP UNet，不要先换大模型。

   我们已经看到 UNet 在 py39 + PTP/LDP-MH 上能到 `0.50`，而 DiT 和 SmolVLA 都低。短期想赢 baseline，最稳的是围绕 UNet 做小网格，而不是投入新架构。

3. 做小网格而不是大海捞针。

   建议第一批只改这些参数：

   | 参数 | 当前 | 建议候选 | 动机 |
   | --- | ---: | --- | --- |
   | `n_action_steps` | 1 | 2, 4 | 每步重规划容易抖，Square contact 阶段可能需要更平滑动作 |
   | `n_obs_steps` | 2 | 4, 8 | 给策略更多短历史，弥补 no-hist 对接触阶段状态不可观测的问题 |
   | `horizon` | 16 | 16, 32 | horizon 32 可能改善插入阶段的动作一致性 |
   | `num_inference_steps` | 100 | 50, 100 | 50 可提速；若不掉分，可扩大搜索 |
   | batch size | 64 | 128 | H200 内存足够，减少梯度噪声 |
   | eval checkpoint | every 100 | 700 后每 50 | py39 UNet best 在 epoch 900，后段需要更细选择 |

4. 不要用 final epoch 报结果。

   DP official-PH 和 PTP/LDP-MH 都出现 final 低于 best 的情况。工程上应默认用 closed-loop rollout 选 checkpoint。报告中要写 best checkpoint 和 final checkpoint 两个数。

5. 数据和 runtime 要成套。

   PTP/LDP-MH 在 py39 / robosuite 1.2 上显著好于 current-stack；official-PH v1.4.1 则在 current-stack 上更好。这说明不要混用“数据来自一个视觉/物理版本，rollout 用另一个版本”的设置。若要改进 PTP idea，最应该保证训练 HDF5、env metadata、camera、action conversion、robosuite 版本一致。

6. 针对 Square 的阶段不平衡做 loss。

   Square 的成功主要卡在接触和插入阶段，但普通 BC / DP loss 大部分被 reaching 和靠近阶段占掉。建议从 demo 轨迹中按 gripper-open/close、object height、eef-object distance、reward/success signal 粗分阶段，对接触和插入阶段做采样加权或 loss 加权。这个比换模型更可能带来稳定提升。

7. 做 rollout 视频失败分类。

   先抽 py39 UNet best checkpoint 的失败视频，按失败模式分三类：没抓住、抓住但对不准、对准但插不下。不同失败模式对应不同改法：

   | 失败模式 | 优先改法 |
   | --- | --- |
   | 没抓住 | 增强 gripper / eef proprio 历史，检查 action scaling 和 gripper threshold |
   | 抓住但对不准 | 增加 obs history，horizon 32，phase-balanced loss |
   | 对准但插不下 | 增加 action smoothing，尝试 `n_action_steps=2/4`，插入阶段 loss 加权 |

8. 复用 specialist 的强信号。

   image BC-RNN 能到 `0.80`，说明 observation 足够。PTP 若想超过当前 DP，可以引入 recurrent specialist 的归纳偏置：例如在 DP 的 image encoder 后加轻量 GRU/temporal transformer，或者用 BC-RNN 作为 teacher 做 action distillation / phase classifier。这个是方法改进，不是第一批调参。

## 建议的第一轮实验矩阵

固定数据和环境：py39 / robomimic 0.2 / robosuite 1.2 + PTP/LDP-MH image_abs。

固定模型：DP UNet。

| Run | 改动 | 预期 |
| --- | --- | --- |
| A | baseline repeat，seed x3 | 确认 `0.50` 是否稳定 |
| B | `n_action_steps=2` | 降低一步一规划的抖动 |
| C | `n_action_steps=4` | 更平滑，但可能牺牲纠错 |
| D | `n_obs_steps=4` | 补短历史 |
| E | `n_obs_steps=4, n_action_steps=2` | 最可能的低风险组合 |
| F | `horizon=32, n_obs_steps=4, n_action_steps=2` | 测长 horizon 是否帮助插入 |
| G | E + batch size 128 | 测稳定性和优化噪声 |

每个 run 先用 50 rollout 筛，超过 baseline 的候选再做 100/200 rollout。第一轮目标不是证明所有因素，而是找到能稳定超过 `0.50` 的组合。

## 最高概率提分路径

我会按这个顺序推进：

1. `py39 + PTP/LDP-MH + DP UNet` 固定住，重复 3 个 seed。
2. 搜 `n_action_steps=2/4` 和 `n_obs_steps=4`。
3. 对 best checkpoint 做失败视频分类。
4. 根据失败类型加 phase-balanced sampling / loss。
5. 再考虑 recurrent DP 或 BC-RNN teacher。

短期目标可以定为从 `0.50` 提到 `0.60+`。如果第一轮小网格拿不到 `0.60`，我会优先做数据阶段加权和 runtime/data provenance 检查，而不是继续加模型容量。
