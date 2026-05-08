# Session 110 Experiment Report: PTP vs DP 4x2x2 Batch

## Scope

This report summarizes the stopped `session89_4x2x2_2000ep` simulation batch. The batch was designed as a practical diffusion-only subset of the PTP Fig. 9-style reproduction:

- 4 tasks: Square, Tool-Hang, Transport, LongSquare
- 2 methods: DP / no-PTP and PTP
- 2 action horizons: `global_action=8` and `global_action=1`
- 1 seed: `training.seed=42`

The metric reported here is training-time rollout `test/mean_score` from each run's `logs.json.txt`, using `task.env_runner.n_test=100`. These are not 3-seed final evaluation results.

## Artifacts

- Output base: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/outputs/session89_4x2x2_2000ep_1778075154/`
- Launch script: `/work-agents/intern_ldp_explorer/ldp/workspace/tasks/task001_reproduce_ldp_ptp_baseline_h200/session89_launch_4x2x2_2000ep.sh`
- PTP-priority script: `/work-agents/intern_ldp_explorer/ldp/workspace/tasks/task001_reproduce_ldp_ptp_baseline_h200/session93_ptp_priority.sh`
- DP resume script: `/work-agents/intern_ldp_explorer/ldp/workspace/tasks/task001_reproduce_ldp_ptp_baseline_h200/session97_resume_dp_2gpu_36645.sh`

## Environment Used For This Batch

The active training batch used `/root/venv`, not the newly configured `/root/ptp_ldp_py39` isolation environment.

Observed active-stack summary from project history:

- Python: `3.12`
- Torch: `2.5.1`
- RoboMimic: `0.3.0`
- RoboSuite: `1.4.1`
- MuJoCo: `3.8.0`

This is an H200 compatibility environment, not the upstream PTP pinned stack. A separate PTP-compatible Python 3.9 venv was configured and smoke-tested in Session 107 at `/root/ptp_ldp_py39`, but it was not used for the runs summarized in this report.

## Common Training Recipe

Common overrides observed in run commands:

| Field | Value |
|---|---|
| `global_obs` | `16` |
| `global_horizon` | `32` |
| `global_action` | `8` or `1` |
| `training.seed` | `42` |
| `training.num_epochs` | `2000` |
| `training.gradient_accumulate_every` | `1` |
| `dataloader.batch_size` | `64` |
| `val_dataloader.batch_size` | `64` |
| `dataloader.num_workers` | `4` |
| `val_dataloader.num_workers` | `4` |
| `training.rollout_every` | `100` |
| `training.checkpoint_every` | `100` |
| `training.val_every` | `1` |
| `training.sample_every` | `5` |
| `task.env_runner.n_envs` | `4` |
| `task.env_runner.n_test` | `100` |
| `task.env_runner.n_test_vis` | `4` |
| `task.env_runner.n_train_vis` | `2` |
| `policy.use_embed_if_present` | `true` |
| `task.dataset.use_cache` | `false` |

Method switches:

| Method | `policy.past_action_pred` | `policy.past_steps_reg` |
|---|---:|---:|
| DP / no-PTP | `false` | `-1` |
| PTP | `true` | `-1` |

## Task-Specific Data And Encoder Settings

| Task | Config | Train dataset | Env / rollout dataset | Encoder checkpoint |
|---|---|---|---|---|
| Square | `experiment_configs/square/transformer_square_emb` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image_abs_emb.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image_abs.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/obs_encoders/obs_encoders/square_encoder.ckpt` |
| Tool-Hang | `experiment_configs/tool/transformer_tool_hang_emb` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/tool_hang/ph/image_abs_emb_compact.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/obs_encoders/obs_encoders/tool_hang_encoder.ckpt` |
| Transport | `experiment_configs/transport/transformer_transport_emb` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/transport/mh/image_abs_emb_compact.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/transport/mh/image_abs.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/obs_encoders/obs_encoders/transport_encoder.ckpt` |
| LongSquare | `experiment_configs/longhist/transformer_longhist_emb` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/longhistsquare100/image.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/longhistsquare100/image.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/obs_encoders/obs_encoders/longhist_encoder.ckpt` |

## Final Snapshot Results

The final snapshot was taken immediately before stopping active processes in Session 110.

| Task | Method | Action horizon | Current epoch | Latest eval epoch | Latest success | Best success | Best epoch |
|---|---|---:|---:|---:|---:|---:|---:|
| Square | DP | 1 | 899 | 799 | 0.00 | 0.02 | 699 |
| Square | DP | 8 | 2778 | 2699 | 0.02 | 0.08 | 1299 |
| Square | PTP | 1 | 1099 | 999 | 0.27 | 0.28 | 599 |
| Square | PTP | 8 | 1999 | 1999 | 0.38 | 0.45 | 599 |
| Tool-Hang | DP | 1 | 799 | 699 | 0.00 | 0.00 | 99 |
| Tool-Hang | DP | 8 | 2599 | 2499 | 0.00 | 0.00 | 99 |
| Tool-Hang | PTP | 1 | 699 | 599 | 0.00 | 0.00 | 99 |
| Tool-Hang | PTP | 8 | 1999 | 1899 | 0.00 | 0.00 | 99 |
| Transport | DP | 1 | 399 | 299 | 0.00 | 0.00 | 99 |
| Transport | DP | 8 | 966 | 899 | 0.00 | 0.00 | 99 |
| Transport | PTP | 1 | 399 | 299 | 0.00 | 0.00 | 99 |
| Transport | PTP | 8 | 851 | 799 | 0.00 | 0.01 | 599 |
| LongSquare | DP | 1 | 1458 | 1399 | 0.00 | 0.00 | 99 |
| LongSquare | DP | 8 | 1999 | 1999 | 0.00 | 0.00 | 99 |
| LongSquare | PTP | 1 | 1371 | 1299 | 0.00 | 0.00 | 99 |
| LongSquare | PTP | 8 | 1999 | 1999 | 0.00 | 0.00 | 99 |

## Aggregated Readout

Best success by task / method / action-horizon family:

| Family | Square | Tool-Hang | Transport | LongSquare | Mean |
|---|---:|---:|---:|---:|---:|
| DP, action horizon 1 | 0.02 | 0.00 | 0.00 | 0.00 | 0.005 |
| DP, action horizon 8 | 0.08 | 0.00 | 0.00 | 0.00 | 0.020 |
| PTP, action horizon 1 | 0.28 | 0.00 | 0.00 | 0.00 | 0.070 |
| PTP, action horizon 8 | 0.45 | 0.00 | 0.01 | 0.00 | 0.115 |

Main observations:

- Square is the only task with meaningful success in this batch.
- PTP clearly outperforms DP on Square under both action horizons.
- For Square, action horizon 8 is better than action horizon 1 for PTP: best `0.45` vs `0.28`.
- Tool-Hang remains `0.00` across DP / PTP and action horizon 1 / 8.
- Transport remains effectively zero; only PTP action horizon 8 reached one nonzero point, best `0.01`.
- LongSquare remains `0.00` across all variants.

## Caveats For Reporting

- This is a single-seed batch, seed `42`.
- The metric is training-time rollout, not a standalone final evaluation with 3 seeds.
- Some resumed DP logs exceeded the nominal `2000ep` run label because resume logic continued from existing log/checkpoint state.
- This batch used the H200 compatibility environment (`robomimic 0.3.0`, `robosuite 1.4.1`, `mujoco 3.8.0`), which is a known confound versus the upstream PTP pinned environment.
- The all-zero Tool-Hang / Transport results should not be interpreted as a clean negative result for PTP until the upstream-version environment is used for a controlled replay or retraining check.

## Stop Confirmation

In Session 110, active training processes matching `session89_4x2x2_2000ep_1778075154` were terminated on both endpoints:

- `10.100.0.29:30103`
- `10.100.0.29:36645`

Post-stop verification showed all 8 visible H200 GPUs at about `1 MiB` used memory and `0%` utilization, with no remaining matching `train.py` process.
