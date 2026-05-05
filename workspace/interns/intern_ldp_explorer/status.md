# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 59 |
| Recent Progress | Checked the additional GPU container at `10.100.0.29:36645`; it has 4 x H200 GPUs, `/mnt/3fs2` mounted, and no pre-existing training jobs. Ran `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/setup_gpu_machine.sh` because `/root/venv` was missing, then patched the local venv/shared pytorch3d stub with `common/workaround.py` so `pytorch3d.transforms` and `RotationTransformer` import successfully. Launched Wave B seed-42 runs on this host: Transport DP PID `27557` GPU0, Transport PTP PID `27559` GPU1, LongSquare DP PID `27562` GPU2, LongSquare PTP PID `27565` GPU3. All use `global_obs=16`, `global_horizon=32`, `global_action=8`, `num_epochs=500`, `batch_size=64`, cached embeddings, explicit `policy.past_steps_reg=-1`, and training rollout `n_test=40`, `n_envs=4`. Health check at `2026-05-05 11:52 UTC` showed all four parent PIDs alive and in `Training epoch 0`. |
