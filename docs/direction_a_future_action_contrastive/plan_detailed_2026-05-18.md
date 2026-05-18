# Direction A: Future-Action / Behavior Contrastive History Encoder

## 0. 文档目的

本文档用于指导 agent 并行推进一个可能用于超越 PTP 的 encoder 改进方向: Future-Action / Behavior Contrastive History Encoder。

该方向目前属于候选方案，不要求一次性做成最终方法。目标是先通过小规模实验判断其是否有效。如果实验有效，再逐步扩大任务和 ablation。

本方向允许保存和维护历史实验信息。每次实验、讨论或 debug 后，agent 需要把关键 observation 记录到 `obs_log.md` 中，形成持续更新的文档库。

## 1. 核心想法

PTP 主要通过 Past-Token Prediction 强化 diffusion policy head 对长历史动作依赖的建模。但原始视觉/历史 encoder 的 representation 可能仍然没有被显式组织成对控制最有用的结构。

本方向尝试在 diffusion policy 之前，额外训练一个 action-aware history encoder。

核心原则:

```text
embedding 的相似性不应该只由图像外观决定，而应该由未来专家动作行为决定。
```

如果两个历史状态对应的未来专家动作相似，则它们的 embedding 应该接近；如果两个历史状态虽然当前图像相似，但未来动作不同，则它们的 embedding 应该被拉远。

目标是让 encoder 学到更接近 POMDP belief 的历史表征。

## 2. 主要假设

### Hypothesis A1: 未来动作相似性可以作为历史状态表征的监督信号

在 POMDP / 长历史任务中，当前单帧图像可能不足以决定下一步动作。专家未来动作轨迹可以被视为当前 latent state / belief 的行为投影。因此，可以用未来动作轨迹相似性来组织 history embedding 空间。

### Hypothesis A2: PTP 的 policy head 强化不足以完全解决 encoder 端历史表征问题

PTP 已经改善 diffusion policy 对过去 token 的利用，但可能主要发生在 policy head / action sequence modeling 层。需要验证额外预训练 history encoder 是否能进一步提升 PTP。

### Hypothesis A3: diffusion loss 反传到上游 encoder 的监督可能不稳定或不匹配

如果出现:

```text
contrastive encoder frozen > contrastive encoder finetuned
```

则可能说明 diffusion loss 微调破坏 action-aware representation。

如果出现:

```text
contrastive encoder finetuned > frozen
```

则说明 contrastive pretraining 提供了更好的 initialization。

两种结果都必须记录。

## 3. 输入与模型形式

### 3.1 推荐输入

优先使用:

```text
x_t = {o_{t-H:t}, a_{t-H:t-1}}
```

即多帧观测 + 历史动作。

如果多帧图像实现成本较高，可以先使用降级版本:

```text
x_t = {o_t, a_{t-H:t-1}}
```

或者:

```text
x_t = {o_{t-H:t}}
```

日志中必须明确记录采用了哪种输入形式。

### 3.2 Encoder 输出

```text
z_t = Enc(x_t)
```

其中 `z_t` 是 history embedding，用于后续接入 PTP / diffusion policy。

### 3.3 建议实现策略

第一版不要大改视觉 backbone。

推荐:

```text
原始 visual encoder / PTP visual features
        +
轻量 temporal transformer / MLP aggregator
        +
projection head for contrastive loss
```

这样降低工程风险，也方便判断提升是否来自 contrastive objective。

## 4. Contrastive 目标设计

### 4.1 未来动作窗口

对每个样本 `i`，定义未来动作窗口:

```text
A_i^+ = a_{t:t+K}
```

其中 `K` 应与 PTP / DP action horizon 保持一致或接近。

### 4.2 动作距离

```text
d_future(i, j) = ||A_i^+ - A_j^+||
```

建议动作先 normalize，再计算距离。

可选距离:

```text
L2 distance
Huber distance
cosine distance after flattening action chunk
weighted distance by timestep
```

第一版建议使用 normalized action chunk 的 L2 distance。

## 5. 推荐 Loss: Soft Future-Action Contrastive Loss

第一版不使用硬阈值正负样本，因为 threshold 难调。

### 5.1 Action similarity distribution

```text
q_ij = softmax(-d_future(i, j) / sigma)
```

### 5.2 Embedding similarity distribution

```text
p_ij = softmax(sim(z_i, z_j) / tau)
```

### 5.3 Loss

```text
L_contrast = CE(q_i, p_i)
```

直觉:

```text
未来动作越相似，embedding 越应该相似；
未来动作越不同，embedding 越应该分开。
```

## 6. Hard Negative 版本

如果 soft contrastive 第一版有效或接近有效，下一步加入 hard negative。

Hard negative 定义:

```text
visual_sim(o_i, o_j) high
but d_future(i, j) high
```

这类样本最贴近 partial observability / long-history disambiguation。

### 6.1 Hard negative 采样方式

先用简单方式:

1. 用当前帧 visual feature 计算视觉相似度。
2. 对每个 anchor 找 top-k visually similar samples。
3. 从这些样本中选择 future action distance 较大的作为 hard negatives。
4. 在 contrastive denominator 中提高 hard negative 权重。

### 6.2 Hard negative loss 加权

候选:

```text
L = L_soft + lambda_hn * L_hard_negative
```

或者在 softmax denominator 中对 hard negatives 加权。

第一版建议先做 sampling，不引入复杂 loss。

## 7. 接入 PTP / Diffusion Policy

### 7.1 推荐接入方式

第一版建议 concat，不直接替换原始 condition:

```text
condition = concat(original_PTP_condition, z_t)
```

这样风险较小，也不会因为替换掉原始信息导致性能明显下降。

### 7.2 可选接入方式

后续如果 concat 有效，可以测试:

```text
condition = z_t
```

或者:

```text
condition = gated_fusion(original_condition, z_t)
```

第一轮不做复杂 fusion。

## 8. 实验任务顺序

### Phase 1: 优先任务

先测试:

```text
Square
ToolHang
```

选择原因:

```text
Square: 已有 PTP 和 DP 差异明显，适合观察方法是否能进一步提升；
ToolHang: 阶段性和历史依赖更强，适合验证 history encoder 是否有价值。
```

### Phase 2: 扩展任务

如果 Phase 1 中至少一个任务有明显提升，继续测试:

```text
Push-T
Transport
```

Push-T 用于测试方法是否对简单/低维任务仍然稳定；Transport 用于测试更复杂任务上的扩展性。

## 9. 第一轮实验矩阵

### 9.1 Baselines

```text
B1. PTP baseline
B2. PTP + same encoder architecture, no contrastive pretraining
```

B2 用于排除提升只是因为参数量变大。

### 9.2 Ours

```text
O1. PTP + future-action contrastive encoder, frozen
O2. PTP + future-action contrastive encoder, finetuned
O3. PTP + future-action contrastive encoder + hard negative, frozen
```

如果时间有限，先做:

```text
B1, B2, O1, O2
```

再补 O3。

## 10. 关键判断标准

### 10.1 预训练是否有效

```text
O1 > B2
```

说明 future-action contrastive pretraining 本身有效。

### 10.2 是否只是参数量提升

```text
B2 ~= B1 或 B2 < O1
```

说明提升不是单纯来自更大的 encoder。

### 10.3 diffusion finetune 是否破坏 encoder

```text
O1 > O2
```

可能说明 frozen action-aware representation 更稳定，diffusion loss 对上游 encoder 的反传存在不匹配。

```text
O2 > O1
```

说明 contrastive pretraining 可作为好 initialization，end-to-end finetune 仍有收益。

### 10.4 hard negative 是否解决 POMDP disambiguation

```text
O3 > O1
```

说明视觉相似但未来动作不同的 hard negatives 对任务有帮助。

## 11. 需要记录的实验信息

每次实验必须记录:

```text
任务名
数据集版本
代码 commit / branch
PTP baseline checkpoint
encoder 输入形式
history length H
action horizon K
batch size
contrastive temperature tau
action similarity sigma
是否使用 hard negative
hard negative top-k
是否 frozen encoder
是否 finetune encoder
best score
best epoch
current epoch
训练是否稳定
失败现象
初步判断
```

## 12. 需要特别观察的现象

重点记录:

1. encoder 预训练 loss 是否稳定下降。
2. embedding 是否 collapse。
3. frozen 是否优于 finetune。
4. Square / ToolHang 中是否有明显提升。
5. hard negative 是否带来收益。
6. 是否出现训练更慢但最终更高。
7. 是否只在某些任务有效。
8. 是否对 Push-T 这种简单任务无收益甚至负收益。
9. 是否和 PTP 的 past-token prediction 存在冲突。
10. 是否提升历史依赖强的任务但不提升普通任务。

## 13. Observation Log

Observation 记录在 `docs/direction_a_future_action_contrastive/obs_log.md`。

## 14. Current Status

```text
Status: Candidate direction, not yet validated.
Priority: High.
First tasks: Square, ToolHang.
Expansion tasks: Push-T, Transport.
Main risk: Contrastive objective may not transfer to diffusion policy performance.
Main expected value: Better history/belief representation under partial observability.
```
