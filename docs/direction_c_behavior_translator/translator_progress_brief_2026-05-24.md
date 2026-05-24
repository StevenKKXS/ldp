# Behavior Translator 方向汇报简版

Date: 2026-05-24

## 目标

Direction C 的核心问题不是让 translator 直接成为最终 policy，而是验证：

```text
obs history -> action sketch
```

这个预训练任务学到的 hidden state，是否能作为更好的 behavior-aware condition，帮助下游 DP/PTP 生成更精细的 future action chunk。

最小判据是：

```text
PTP/DP + pretrained frozen translator context
>
PTP/DP + same-architecture frozen random translator context
```

如果这个成立，说明提升不是单纯来自多加参数，而是 translator 的 history-action 对齐表征有价值。

## 已实现内容

已完成一套 Square 上的最小闭环实现：

- Stage 1: raw image/proprio history 经过 robomimic obs encoder 和 `BehaviorTranslator`，预测历史动作、未来动作或两者。
- Stage 2a: freeze translator context，训练一个简单 MLP future-action head，做 offline representation probe。
- Stage 2b: 将 translator context 接入 transformer DP/PTP policy，作为额外 condition 做下游 policy 训练与 rollout。

主要代码入口：

- `diffusion_policy/dataset/behavior_translation_dataset.py`
- `diffusion_policy/model/behavior_translator.py`
- `diffusion_policy/workspace/train_behavior_translator_workspace.py`
- `diffusion_policy/workspace/train_translator_head_workspace.py`
- `diffusion_policy/policy/translator_conditioned_transformer_hybrid_image_policy.py`

环境要求仍按 PTP 复现实验标准：

```text
Python 3.9
robomimic==0.2.0
raw image_abs.hdf5
```

## 数据与任务设置

当前主设置：

```text
H = 16 obs history
P = 16 past action horizon
K = 8 future action horizon
```

以时间 anchor 为中心，模型看到 `o[t-15:t]`，目标动作窗口为：

```text
past:        a[t-16:t-1]
future:      a[t:t+7]
past_future: a[t-16:t+7]
```

输入是 raw obs，不是预编码 embedding；encoder 本身参与训练，这符合我们想验证“训练 history-aware encoder/context”的目标。

## Stage 1 结果

Stage 1 训练了三个目标：`past`、`future`、`past_future`。

| Objective | 现象 | 代表性结果 |
|---|---|---|
| `past` | 最稳定，验证 loss 持续较低，是当前最可靠的 translator 预训练目标 | formal best 约 `0.000455 @ e113`；tuned best 约 `0.000434 @ e118` |
| `future` | train loss 下降，但 val 很早达到最优后变差，说明未来动作从 observation history 直接预测更强多模态 | early best 约 `0.008961 @ e4` |
| `past_future` | 目标最接近原始设想，但 future 部分噪声较大；调低 future 权重后有改善 | `w_future=0.5` best 约 `0.006501 @ e4` |

阶段性判断：`past` 目标更像稳定的行为历史表征学习；`future` 和 `past_future` 更容易出现 offline overfit 或多模态不确定性。

## Stage 2a 结果

Stage 2a 是 offline probe，不产生 rollout success rate。它只回答：

```text
frozen translator context 是否比 frozen random context 更容易预测 future action
```

主要结果：

| Context | Frozen | Offline val loss | Future L1 | 结论 |
|---|---:|---:|---:|---|
| random translator | yes | `0.011571` | `0.06736` | random baseline |
| pretrained `past` e50 | yes | `0.007839` | `0.04917` | 明显优于 random |
| pretrained `past` best/latest | yes | 约 `0.00796` 到 `0.00803` | - | 信号稳定 |
| pretrained `past` finetune | no | 约 `0.00806` | - | 没有明显优于 frozen |
| pretrained `past_future` | yes | 约 `0.0106` 到 `0.0136` | - | 当前弱于 `past` |

阶段性判断：Stage 2a 支持 `past` translator context 确实学到可用表征；这一步的 go/no-go 是正向的。

## Stage 2b 现状

已实现 downstream 接入：

```text
base transformer policy condition
+ projected translator context
```

旧 rollout 曾出现混合结果：

| Setting | 旧结果摘要 |
|---|---|
| pretrained `past` + `add_all` | e49 `2/10`，e99 `4/10` |
| random + `add_all` | e49 `5/10`，e99 `3/10` |
| pretrained `past` + `add_last` | e49 `4/10` |
| random + `add_last` | e49 `0/10` |

但这些旧 Stage 2b rollout 不能作为稳定结论，因为后来发现 action8 transformer mask 有关键问题。

## 关键修正

旧 action8 设置为：

```text
horizon=8
n_obs_steps=16
causal_attn=true
n_cond_layers=0
```

在这个组合下，action token 只能看到 obs condition token `0..7`，看不到 obs token `8..15`。也就是说，最新/current obs 和 `add_last` 注入的 translator context 实际上被 mask 掉了。

已经修复：

- `TransformerForDiffusion` 增加 `causal_cond_attn` 参数。
- corrected long-history action8 设置使用 `policy.causal_cond_attn=false`。
- 已准备四个 corrected config：
  - base no-context
  - pretrained `past` + `add_last`
  - random + `add_last`
  - pretrained `past` + `add_all`

因此当前最诚实的结论是：offline representation 已经有正信号；rollout 提升还需要用 corrected mask 重跑确认。

## 系统与资源经验

训练瓶颈主要在 raw image dataloader，而不是 H200 compute。已有测试里更快的 raw-image Stage 1 配置大约是：

```text
batch_size=128
num_workers=64
约 149 samples/sec
约 8.86 min/epoch
```

但 batch size 改变了 optimizer step 数，不能直接和 batch 32 的 epoch 对齐；比较训练效果时应按 update steps 或固定 wall-clock budget 评估。

当前存储状态曾出现 NFS/page I/O wait，两个 H200 节点上有 stale Python 进程卡在 `wait_on_page_bit_common`。代码和小文件已经通过 GitHub branch 和 Ceph 小文件归档保住；大 checkpoint/rollout artifact 仍依赖 NFS/3FS 恢复情况。

## 当前结论

1. `past` translator 是目前最有希望的 Direction C 变体。
2. Stage 2a 已证明 pretrained `past` context 比同结构 random context 更有 offline future-action 信息。
3. `future` 和 `past_future` 暂时不如 `past` 稳定，原因可能是未来动作多模态、loss 权重不平衡，以及 pooled context 未必保留足够 action-side token 信息。
4. Stage 2b 的旧 rollout 结果不能作为最终 evidence，因为 action8 condition mask 让最新 obs/context 不可见。
5. 下一轮真正关键实验是 corrected Stage 2b rollout：base、random context、pretrained `past` add-last、pretrained `past` add-all，在同一 mask 修正和同一 rollout protocol 下比较。

## 建议推进

优先级最高的是在干净 GPU/存储上跑 corrected Stage 2b 四组：

```text
M1: base no-context, causal_cond_attn=false
M2: pretrained past + add_last, causal_cond_attn=false
M3: random + add_last, causal_cond_attn=false
M4: pretrained past + add_all, causal_cond_attn=false
```

如果 M2 > M3 且 M2 >= M1，Direction C 的核心假设成立。之后再扩展到 ToolHang、更多 seeds、token context、projector-only finetune，以及 `past_future` 的更细权重调参。
