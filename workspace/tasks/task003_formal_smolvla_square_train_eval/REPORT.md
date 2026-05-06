# Formal SmolVLA-style Square Training Report

## 结论

- 已完成 2 卡 H200 正式训练：1000 epoch，每 100 epoch 做一次离线 square action eval。
- 最优 sampled action MSE 出现在 epoch 300：`0.13077014684677124`，对应 checkpoint 为 `epoch_0300.pt`。
- 最终 epoch 1000 的 sampled action MSE 为 `0.13218089938163757`，不是本次离线指标下的最优点。
- train loss 从 epoch 100 的 `0.09809166193008423` 降到 epoch 1000 的 `0.07334687560796738`；val flow loss 从 `0.20909729599952698` 上升到 `0.3399428427219391`，说明继续训练会压低训练误差，但验证 flow loss 有过拟合趋势。
- simulator rollout success rate 没有产出：当前可用 Python 环境缺少 `robomimic`、`robosuite`、`mujoco`、`mujoco_py`、`lerobot`，远端 pip/PyPI 探测超时。本报告的性能结论是离线 action eval，不是 Robosuite success-rate。

## 运行与隔离

- Task root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval`
- Run dir: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/runs/formal_ldp_abs10_1000epoch_eval100_20260506_135043`
- Dataset copy: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`
- Script: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/scripts/train_eval_smolvla_square_formal.py`
- 所有输出、checkpoint、日志和报告均写在本人 task root 下；没有写入 `intern_ldp_explorer` 或其他 intern 目录。

## 模型与训练设置

- 模型：compact SmolVLA-like flow policy
- 输入：2 个 image view、9D robot state、learned language/task token
- 输出：`ldp_abs10` action chunk，chunk size 16
- action expert：Transformer decoder，embedding dim 256，6 layers，8 heads
- 参数量：6,959,178
- DDP world size：2
- Batch size：128 per rank
- Train sequences：75,457
- Val sequences：5,274
- Optimizer：AdamW，lr `1e-4`，weight decay `1e-4`
- AMP：bf16 autocast
- 总步数：294,000 global steps
- 总耗时：7,774.679 秒，约 129.58 分钟

## Eval 指标

`val_loss` 是 normalized action chunk 上的 flow-matching velocity MSE。`val_sample_action_mse` 是 10-step reverse-flow 采样出的 normalized action chunk MSE。

| Epoch | Train loss | Val flow loss | Sampled action MSE |
|---:|---:|---:|---:|
| 100 | 0.098091662 | 0.209097296 | 0.131234676 |
| 200 | 0.086906515 | 0.252506375 | 0.134672940 |
| 300 | 0.082552940 | 0.272654414 | 0.130770147 |
| 400 | 0.079913929 | 0.283117294 | 0.132187814 |
| 500 | 0.078301638 | 0.302946478 | 0.134787828 |
| 600 | 0.076880455 | 0.317568988 | 0.132793903 |
| 700 | 0.075147212 | 0.315889567 | 0.130900383 |
| 800 | 0.074293688 | 0.328449816 | 0.132800817 |
| 900 | 0.073381528 | 0.327847749 | 0.131422669 |
| 1000 | 0.073346876 | 0.339942843 | 0.132180899 |

## 判断

这个 SmolVLA-style 结构可以在当前 LDP square HDF5 上稳定训练，1000 epoch 没有数值崩溃，也能生成有效 action chunk。按离线 sampled action MSE 选择，`epoch_0300.pt` 是本次最优；如果必须使用最后训练结果，`epoch_1000.pt` 的 MSE 只比 best 高约 `0.00141`，但验证 flow loss 明显更差。

没有给出 Robosuite square success rate 的原因不是训练失败，而是环境依赖不可用；当前结论应解读为 offline square action prediction performance。
