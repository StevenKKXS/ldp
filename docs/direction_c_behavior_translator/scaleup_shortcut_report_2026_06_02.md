# Direction C Translator Scale-up 与 Shortcut 诊断报告

日期：2026-06-02

这份报告整理 Direction C 当前关于 behavior translator 的主要结论：translator 结构是什么，scale up 后发生了什么，ACT / ACT-style 尝试是否带来提升，以及为什么当前证据更支持“proprio / lowdim shortcut”，而不是学到了有效的 image-grounded behavior representation。

## 1. 当前结论

当前 v0 translator 路线应视为一次 **negative exploration**：它可以学到 obs history 到 action 的映射，尤其是 past action，但这个映射很大概率主要由 lowdim/proprio 信息完成，image 信息在当前目标下没有被充分利用。

更精确地说，不是“translator 什么都没学到”，而是：

```text
obs history -> past-action reconstruction
    这个监督目标太容易被 proprio / robot state 解释
    因此 hidden state 没有被迫学习 image-grounded task progress
    冻结后注入 DP/PTP 的 context 也没有优于 base 或 random context
```

所以当前不能 claim：

```text
translator 学到了有用的 history-aware image representation
```

更合理的阶段性结论是：

```text
v0 translator objective 暴露了一个 shortcut：
past-action translation 基本可以被 lowdim/proprio 解决，
因此没有自然转化成更好的 DP/PTP condition。
```

## 2. 原始假设与判据

最初想验证的是：

```text
obs history -> translator -> behavior-aware hidden state
behavior-aware hidden state + DP/PTP -> better future action generation
```

关键 go/no-go 判据是：

```text
DP/PTP + pretrained translator context
    > DP/PTP + random translator context
    >= DP/PTP base
```

目前最可靠的 rollout 结果没有满足这个判据。

## 3. Translator 结构

Stage 1 translator 输入 Robomimic 的 observation window，并预测 sketch actions。

```text
Robomimic obs window
  image:
    agentview_image
    robot0_eye_in_hand_image
  lowdim / proprio:
    robot0_eef_pos
    robot0_eef_quat
    robot0_gripper_qpos
        |
        v
shared Robomimic obs encoder per timestep
        |
        v
obs tokens [B, H, 137]     # Square 当前 encoded obs dim
        |
        v
ObsProjector: 137 -> d_model
        |
        v
CausalObsEncoder
        |
        v
z_obs [B, H, d_model]
        |
        v
learned action queries cross-attend to z_obs
        |
        v
h_action [B, P + K, d_model]
        |
        +--> SketchActionHead -> pred actions [B, P + K, Da]
        |
        +--> Context pooling/projector -> downstream behavior context
```

Square action8 下常用维度：

```text
H = 16 observation steps
P = 16 past action steps
K = 8 或 16，取决于 config
Da = 10 action dims
```

关键实现注意点：

- Stage 1 loss 直接监督的是 `SketchActionHead` 输出的 action。
- downstream 用的 pooled/projected context 不是被 rollout success 直接监督出来的。
- 如果 past action 能靠 proprio 解释，hidden state 就没有强压力去编码 image 中的 object state、contact state、task phase。

## 4. Scale-up 尝试与结果

我们测试了一个问题：是不是原始 translator 太小，所以才没有学出有用表示？

在 py39 / robomimic 0.2.0 GPU 环境下测得的参数量：

| 模型 | core params | 含 obs encoder full params |
|---|---:|---:|
| shared Robomimic obs encoder | - | 22.394M |
| d256 translator | 5.776M | 28.170M |
| ACT-size translator | 56.177M | 78.571M |
| deterministic ACT-style baseline | 55.116M | 77.510M |
| official-ACT-compatible CVAE adapter | 72.513M | 94.907M |

Stage 1 translator offline metrics：

| Run | Epochs | Best epoch | Best val total | Best val past L1 | Best val future L1 | 解读 |
|---|---:|---:|---:|---:|---:|---|
| d256 full, normalized, obs lr 1e-4 | 178 | 110 | 0.000485 | 0.01172 | 0.06096 | 原始稳定 past run |
| d256 full, normalized, obs lr 5e-5 | 178 | 129 | 0.000524 | 0.01261 | 0.06708 | 接近但略差 |
| ACT-size normalized | 507 | 430 | 0.002727 | 0.00917 | 0.08539 | past L1 更好，future L1 更差 |
| ACT-size raw-action-loss | 50 | 37 | 0.004895 | 0.00857 | 0.05367 | raw-space past L1 更好，但尚未验证 downstream |

注意：

- ACT-size normalized 的 `loss_total` 和 d256 不直接可比，因为 loss reduction 和 loss scale 改过；更适合看 L1。
- ACT-size 确实把 past L1 从约 `0.0117` 降到 `0.00917`，说明更大模型能更好拟合 past-action reconstruction。
- 但 normalized ACT-size 的 future L1 变差，downstream context 也没有显示出收益。

阶段性判断：

```text
scale up 帮助模型拟合最容易的监督目标，
但没有证明 hidden state 对下游控制有用。
```

## 5. Downstream Context 结果

当前最重要的 downstream 证据来自 corrected Square Stage2b rollout：

| Method | Checkpoint | Rollout SR |
|---|---:|---:|
| base, no translator context | e24 EMA | 22/50 = 44% |
| random translator context | e24 EMA | 21/50 = 42% |
| random translator context | e49 EMA | 26/50 = 52% |
| pretrained translator add_last | e24 EMA | 15/50 = 30% |
| pretrained translator add_all | e24 EMA | 18/50 = 36% |

这组结果没有通过 go/no-go：

```text
pretrained context 本应优于 random context
但实际 pretrained context < random context，也低于 base。
```

ACT-size downstream offline validation 也没有扭转这个判断：

| Run | Epochs | Best val loss | Best epoch | Rollout SR |
|---|---:|---:|---:|---|
| ACT-size base no context | 400 | 0.02965 | 43 | 未跑出/未解析 |
| ACT-size pretrained past add_last | 400 | 0.03138 | 41 | 未跑出/未解析 |

offline loss 层面，ACT-size base 仍略优于 pretrained-context add_last。

## 6. ACT 相关尝试

ACT 相关有两条线。

### 6.1 Deterministic ACT-style baseline

这不是 official ACT，只是使用 ACT-like transformer 几何结构，没有 CVAE posterior / action-history latent path。

```text
obs tokens + action queries
    -> transformer decoder
    -> action chunk
```

结果：

| Run | Epochs | Best val loss | 解读 |
|---|---:|---:|---|
| deterministic ACT-style Square action8 | 400 | 0.32680 | offline 明显差于 diffusion/ACT-size base |

结论：简单 deterministic ACT-style 替换没有提供有竞争力的参考。

### 6.2 Official-ACT-compatible CVAE adapter

这条线把 official ACT 思路适配到 Robomimic Square：

```text
training:
  qpos + action chunk -> CVAE posterior z
  images + qpos + z -> transformer decoder -> action chunk

inference:
  z = zero latent
  images + qpos + z -> action chunk
```

结果：

| Run | Budget | Val loss | Rollout SR |
|---|---:|---:|---:|
| official-ACT-compatible Square action8 | 25 epochs | 0.04674 | 1/20 = 5% |

结论：

- 这个 official-ACT-compatible adapter 当前只是 smoke-tested weak baseline。
- 它没有证明 official ACT 在 Robomimic 上不行，因为训练预算和适配仍然有限。
- 但它也没有支持“借 ACT 结构即可让 translator 路线变好”。

## 7. Shortcut 证据

核心问题是：

```text
translator 是否真的用到了 image？
还是主要从 proprio/lowdim 推出了 past action？
```

目前有两个互补证据。

### 7.1 checkpoint perturbation

对训练好的 translator 做 modality perturbation。

d256 quick checkpoint：

| Condition | val total | past L1 | 解读 |
|---|---:|---:|---|
| baseline | 0.000800 | 0.01737 | 正常 |
| image zero | 0.002051 | 0.03078 | 变差，但不灾难 |
| image shuffle | 0.002043 | 0.01957 | 接近 baseline |
| proprio zero | 0.233882 | 0.56714 | 灾难性变差 |
| proprio shuffle | 0.006923 | 0.03096 | 明显变差 |

ACT-size micro check：

| Condition | val total | past L1 | 解读 |
|---|---:|---:|---|
| baseline | 0.002205 | 0.01598 | 正常 |
| image zero | 0.006270 | 0.02231 | 小到中等变差 |
| image shuffle | 0.002401 | 0.01659 | 几乎不变 |
| proprio zero | 2.446047 | 0.52645 | 灾难性变差 |
| proprio shuffle | 0.002468 | 0.01734 | micro batch 下几乎不变 |

最可靠的是 zeroing 结果：

```text
zero proprio 会摧毁预测；
zero/shuffle image 没有同量级破坏。
```

shuffle 的证据要更谨慎，因为 micro batch 内 shuffle 可能不足以构造真正跨 episode 的强扰动。

### 7.2 lowdim-only vs image-only retrain

这个证据更干净，因为它是从头训练不同输入合同的模型。

同样是 ACT-size normalized past setup，20 epoch budget：

| Input | Best epoch | Best val total | Best past L1 | Best future L1 | 解读 |
|---|---:|---:|---:|---:|---|
| full input, ACT-size reference at e20 | 20 | 0.00638 | 0.01211 | 0.07398 | image + lowdim |
| lowdim-only | 20 | 0.00533 | 0.01264 | 0.06974 | 接近 full |
| image-only | 18 | 0.01141 | 0.02054 | 0.07031 | past prediction 明显更差 |

这条证据最直接：

```text
lowdim-only ~= full input
image-only << full input
```

因此当前 past-action objective 没有迫使模型依赖 image。

## 8. 为什么这解释了 downstream 失败

原始希望是 past/future action reconstruction 能学到 history-aware behavior state。但当前证据更像是：

```text
当前 proprio / lowdim state
  -> 推断近期 robot motion / gripper trend
  -> 重构 past action
```

这可以降低 Stage 1 validation loss，但不一定学习：

- image 中 object pose；
- contact state；
- task phase；
- 当前观测相似但历史不同的 visual ambiguity；
- 不是 proprio 已经显式包含的 future intent。

因此 downstream 注入的 context 可能只是 base policy 已经有的 lowdim 条件的冗余版本，或者只是一个没有稳定语义的额外 token/projection。这样 random context 反而可以接近甚至超过 pretrained context，因为它可能只是改变了优化路径或正则化，而 pretrained 内容本身没有提供可靠语义。

## 9. 当前运行任务

已检查 `10.100.2.39:23494`：

```text
8 x H200
GPU util: 0%
GPU memory: 每卡约 1 MB
没有 train / rollout / eval python 进程
```

因此这次没有需要停止的无结论长跑任务。

## 10. 建议的下一步

我建议把当前 pooled-context translator v0 作为 negative result 收尾，不再对同一个 shortcut-prone objective 做更长训练。

如果继续探索 translator 思路，应该先改 supervision / input design，而不是单纯 scale up：

1. Stage 1 加 modality dropout：
   - 随机 drop lowdim/proprio；
   - 随机 drop image 做对照；
   - 检查 image reliance 是否上升。

2. 修改 auxiliary target：
   - 不再以 pure past-action reconstruction 为主；
   - 如果能取到 object/contact state，加入 future object/contact prediction；
   - 在 proprio dropout 下预测 future action，让模型必须看 image。

3. 显式评估 image dependence：
   - offline eval 或 rollout 中分别做 image zero/shuffle、proprio zero/shuffle；
   - 同时报告 validation loss 和 rollout SR。

4. representation 变好后再改 downstream injection：
   - pooled context vs action-token context；
   - projection addition vs encoder replacement；
   - 同参数量下必须满足 pretrained > random。

如果 12-14h 内需要补一个 confirmatory 实验，最合适的是：

```text
在 best ACT-size checkpoint 上做更大 batch 的 modality perturbation eval：
  baseline
  image zero
  image shuffle across episodes
  proprio zero
  proprio shuffle across episodes
这个不需要训练。
```

这次没有启动该实验，因为 lowdim-only / image-only retrain 已经给出当前报告需要的更干净证据。

## 11. 最终判断

当前 translator 方向已经产出了有价值的信息，即使没有带来 policy 提升：

```text
1. 主要瓶颈不是模型太小。
2. ACT-style 结构本身不是直接解法。
3. 当前 Stage 1 objective 有明显 shortcut。
4. proprio/lowdim 足以解释大部分 past-action prediction。
5. image-grounded behavior context 需要被目标函数或输入扰动强制学出来。
```

因此建议当前阶段的汇报口径是：

```text
我们验证了 v0 history-to-action translator 的一个失败模式：
past-action translation 很容易走 proprio shortcut，
这使得 scale-up 和 ACT-like architecture 都没有转化为更好的 downstream SR。
下一版如果继续探索，需要先解决 image-grounded supervision，而不是继续扩大同一目标。
```
