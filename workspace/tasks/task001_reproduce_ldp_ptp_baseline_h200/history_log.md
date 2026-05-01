# History Log

<!-- METADATA:SESSION=3 -->

## Session 0
- Created task for reproducing LDP baseline and PTP on H200.
- Scope includes upstream asset audit, current debug-server run classification, baseline/PTP reproduction, and comparative report.
- Accepted by `intern_ldp_explorer` on branch `intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200`.
- GitHub CLI is unavailable in the current environment; status file stores the prefilled PR creation URL.
- Confirmed upstream `long-context-dp/ldp` has no GitHub Releases; official public assets currently identified are README-linked datasets and `obs_encoders.zip`.
- Classified existing debug-server run `full_train_3500ep_1777457545` as `square` + `PTP` (`policy.past_action_pred=true`) but with `global_obs=2`, so it is not the paper's default long-context (`16-step`) setting.
- Launched `baseline_square_3500ep_1777535019`: `square`, `global_obs=2`, `policy.past_action_pred=false` on GPU1. This is useful as a no-history baseline candidate.
- Launched `no_ptp_square_obs16_1777535301`: `square`, `global_obs=16`, `policy.past_action_pred=false` on GPU1. This is the closest in-progress run to the paper's `no-PTP` diffusion baseline.
- Launched `ptp_square_obs16_1777535313`: `square`, `global_obs=16`, `policy.past_action_pred=true` on GPU0. This is the closest in-progress run to the paper's main PTP setting on the public RoboMimic square dataset.
- Downloaded official upstream `obs_encoders.zip` locally, copied it to `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/obs_encoders.zip`, and verified the archive contains `square_encoder.ckpt`, `longhist_encoder.ckpt`, `transport_encoder.ckpt`, `tool_hang_encoder.ckpt`, `aloha_encoder.ckpt`, and related encoder checkpoints.
- Verified that `baseline_square_3500ep_1777535019` has entered epoch 1, while both `no_ptp_square_obs16_1777535301` and `ptp_square_obs16_1777535313` have entered `Training epoch 0`.

## Session 1
- Re-checked debug server status on `2026-05-01 03:02 UTC`.
- Confirmed four active runs still occupy both H200 GPUs:
- legacy short-context PTP: `full_train_3500ep_1777457545`
- short-context no-history candidate: `baseline_square_3500ep_1777535019`
- long-context no-PTP: `no_ptp_square_obs16_1777535301`
- long-context PTP: `ptp_square_obs16_1777535313`
- Structured metric snapshot:
- `full_train_3500ep_1777457545`: epoch 825 train, epoch 824 val, latest val loss `0.0913`, recent checkpoint lineage degrades to `test_mean_score=0.000` by epochs 499/599/699/799.
- `baseline_square_3500ep_1777535019`: epoch 386 train, epoch 385 val, latest val loss `0.0930`, existing checkpoints include `epoch=0099 score=0.025`, `epoch=0199 score=0.000`, `epoch=0299 score=0.100` (best so far).
- `no_ptp_square_obs16_1777535301`: epoch 69 train, epoch 68 val, latest val loss `0.0549`, no checkpoint yet.
- `ptp_square_obs16_1777535313`: epoch 69 train, epoch 68 val, latest val loss `0.0387`, no checkpoint yet.
- Current strongest immediate signal is that `global_obs=16` PTP already has materially lower validation loss than `global_obs=16` no-PTP at the same epoch (`0.0387` vs `0.0549`).
- Confirmed official encoder archive is present on shared storage at `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/obs_encoders.zip`.

## Session 2
- Re-checked official parameter references in the upstream repo and local extracted paper text.
- Clarified that the repo provides concrete runnable hyperparameters for PTP through experiment configs:
- short-history square: `global_obs=2`, `global_action=1`, `global_horizon=32`, `batch_size=64`, `learning_rate=1e-4`, `past_action_pred=true`, `past_steps_reg=-1`, `num_epochs=3500`, `checkpoint_every=100`, `rollout_every=100`.
- long-history square: `global_obs=16`, `global_action=1`, `global_horizon=32`, `batch_size=64`, `learning_rate=1e-4`, `past_action_pred=true`, `past_steps_reg=-1`, `num_epochs=3500`, `checkpoint_every=10`, `rollout_every=50`.
- Confirmed the base workspace config is different (`num_epochs=3050`, `checkpoint_every=50`, `rollout_every=50`) but task-specific experiment configs override it.
- Clarified that the paper text itself gives protocol-level references rather than a full hyperparameter table in the sections inspected:
- default history-conditioned evaluation uses past 16 time steps
- all policies use diffusion policies with context length 16 and chunk size 8
- caching ablation evaluates checkpoints saved every 50 epochs for two days
- Clarified to user-facing report that the previously mentioned `100` was not a hand-picked total training length; it was derived from the official `transformer_square.yaml` values `checkpoint_every=100` and `rollout_every=100` while total training length remained `num_epochs=3500`.

## Session 3
- Sampled live GPU utilization on the debug server at `2026-05-01 03:26:21 UTC`.
- `nvidia-smi` snapshot:
- GPU0: `0%` utilization, `27874 MiB / 143771 MiB` allocated, `33 C`
- GPU1: `15%` utilization, `27876 MiB / 143771 MiB` allocated, `38 C`
- Active compute processes still match the expected 4-run packing:
- GPU0: PID `1653544` and PID `3623114`
- GPU1: PID `3608565` and PID `3622380`
- Interpretation: the box is under-utilized at this sample point even though four training processes are resident; the workload is currently not saturating either H200.
