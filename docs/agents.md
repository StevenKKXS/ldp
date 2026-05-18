# Agent 工作规范

## 1. 启动流程

agent 收到本项目任务后，必须先执行:

1. 阅读 `docs/main.md`。
2. 确认当前 active global plan。
3. 阅读 Direction A 和 Direction B 的 active plan。
4. 检查两个方向的 `status.md`、`experiments.md`、`obs_log.md`。
5. 在开始实验前提出对 plan 的异议、风险或实现建议。
6. 如果没有新的关键 idea 或阻塞问题，则按当前任务顺序执行。

## 2. 实验优先级

当前优先任务:

1. Square
2. ToolHang

如果上述任务中至少一个方向出现明确提升，再继续:

3. Push-T
4. Transport

## 3. 两个方向可以并行推进

Direction A 和 Direction B 都是可能方向，可以同时保存、同时 review、同时维护状态。

第一轮实验不要混合两个方向的 loss，否则无法判断单独贡献。组合版本 `L = L_contrast + lambda * L_pred` 只在两个方向分别完成单独验证后再讨论。

## 4. 必须记录的信息

每次实验后必须记录:

- task
- method / direction
- experiment id
- branch / commit
- dataset version
- checkpoint
- encoder 输入
- 是否 frozen
- 是否 finetune
- best score
- best epoch
- current epoch
- 是否完成
- 是否失败
- 关键 observation
- 下一步决策

## 5. 防幻觉规则

agent 不允许凭印象回答实验进度。

回答进度前必须检查:

- `docs/status.md`
- 对应方向的 `status.md`
- 对应方向的 `experiments.md`
- 对应方向的 `obs_log.md`

如果文档没有记录，必须回答:

```text
当前文档中没有记录该结果，不能确认。
```

不允许把计划中的实验说成已经完成。

不允许把未验证的假设说成结论。

不允许删除旧 plan。重大修改应创建新的 plan_update 文件，并在 `docs/main.md` 中切换 active plan。

## 6. Review 检查清单

执行前至少 review:

1. 两个方向是否都能挂到当前 PTP 代码中。
2. encoder 输出维度如何接入 diffusion condition。
3. 是否已有 PTP baseline checkpoint。
4. Square / ToolHang 的数据加载和 evaluation 是否正常。
5. 是否能复现实验表中的已有 PTP 分数。
6. 是否有必要先跑 same-architecture no-pretrain baseline。
7. Direction A 的 action distance 是否需要 normalization。
8. Direction B 的 action prediction decoder 是否过强。
9. frozen / finetune 是否都能在代码中明确控制。
10. 每个实验是否有独立 experiment id 和日志路径。

如果 agent 对 plan 有异议，应先写入对应方向的 `obs_log.md` 或 `status.md`，并在执行前反馈。
