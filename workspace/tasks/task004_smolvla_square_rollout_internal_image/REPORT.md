# SmolVLA-style Square Rollout Report

## 结论

- 已按主管要求复制并使用 `intern_ldp_explorer/setup_gpu_machine.sh`，在 GPU 机上通过内部 pip 镜像完成 simulator 环境配置。
- 依赖验证通过：`torch 2.5.1+cu124`、`mujoco 3.8.0`、`robosuite 1.4.1`、`robomimic 0.3.0`，CUDA 可见 2 张 GPU。
- 使用 task003 离线 eval 最优 checkpoint `epoch_0300.pt` 做 Robosuite square rollout。
- 正式 rollout：20 条 test seeds `10000-10019`，每条最多 400 step，成功 `2/20`，成功率 `10%`。
- demonstration absolute-action replay sanity check：states-only replay 前 5 条 demo 成功 `5/5`，说明当前 absolute-action env 配置可用。

## 路径

- Task root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task004_smolvla_square_rollout_internal_image`
- Copied setup script: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task004_smolvla_square_rollout_internal_image/scripts/setup_gpu_machine.sh`
- Rollout script: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task004_smolvla_square_rollout_internal_image/scripts/rollout_smolvla_square.py`
- Checkpoint: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/runs/formal_ldp_abs10_1000epoch_eval100_20260506_135043/epoch_0300.pt`
- Dataset: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`
- Formal result jsonl: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task004_smolvla_square_rollout_internal_image/rollouts/epoch0300_20rollouts.jsonl`

## Rollout 方法

- Policy: task003 compact SmolVLA-style flow policy
- Checkpoint selection: offline sampled action MSE best, epoch 300
- Action representation: model predicts normalized `ldp_abs10 = [pos, rot6d, gripper]`
- Env control: Robosuite `NutAssemblySquare` with `controller_configs.control_delta=False`
- Conversion: denormalize 10D action, convert rot6d back to axis-angle rotvec, execute 7D absolute action
- Closed-loop mode: receding horizon, execute 8 actions from each 16-action predicted chunk
- Flow sampling steps: 10
- Max episode steps: 400
- Seeds: `10000-10019`

## Rollout 结果

| Seed | Success | Steps | Max reward |
|---:|:---:|---:|---:|
| 10000 | false | 400 | 0.0 |
| 10001 | true | 176 | 1.0 |
| 10002 | false | 400 | 0.0 |
| 10003 | false | 400 | 0.0 |
| 10004 | false | 400 | 0.0 |
| 10005 | false | 400 | 0.0 |
| 10006 | false | 400 | 0.0 |
| 10007 | true | 189 | 1.0 |
| 10008 | false | 400 | 0.0 |
| 10009 | false | 400 | 0.0 |
| 10010 | false | 400 | 0.0 |
| 10011 | false | 400 | 0.0 |
| 10012 | false | 400 | 0.0 |
| 10013 | false | 400 | 0.0 |
| 10014 | false | 400 | 0.0 |
| 10015 | false | 400 | 0.0 |
| 10016 | false | 400 | 0.0 |
| 10017 | false | 400 | 0.0 |
| 10018 | false | 400 | 0.0 |
| 10019 | false | 400 | 0.0 |

Summary: `2/20 = 10%` success rate, mean steps `378.25`.

## 判断

补上 simulator 后，之前的 offline best checkpoint 在 Robosuite square 上能成功，但成功率较低：`10%` on 20 seeded rollouts. 这和离线 MSE 指标的判断一致：结构可训练、能产生有效动作，但 compact SmolVLA-style policy 还不足以达到强 square policy 的闭环成功率。
