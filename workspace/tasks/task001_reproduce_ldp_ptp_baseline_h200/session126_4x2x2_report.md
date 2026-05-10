# Session 126 4x2x2 Experiment Report

<!-- METADATA:SESSION=126 -->

## Scope

This report summarizes the current 4x2x2 reproduction batch for the diffusion-only subset of PTP Figure 9:

- Tasks: Square, Tool-Hang, Transport, Long Square.
- Methods: DP / no-PTP and PTP.
- Action horizons: `global_action=1` and `global_action=8`.
- Seed: `42`.
- Evaluation metric: `test/mean_score` from rollout, configured with `n_test=100` where rollout completed.

## Why We Re-Ran The Older PTP Environment

Before the current `/root/ptp_ldp_py39` run, we tested the same four-task diffusion subset on the modern H200 setup created from `setup_gpu_machine.sh`:

- Environment: `/root/venv`, Python `3.12.3`, torch `2.5.1`, robomimic `0.3.0`, robosuite `1.4.1`, MuJoCo `3.8.0`, diffusers `0.30.0`, gym `0.25.2`.
- This stack was operationally convenient for the H200 container, but it did not match the LDP / Diffusion Policy pinned provenance: robomimic `0.2.0`, pinned `cheng-chi/robosuite@277ab9588...` with source version `1.2.0`, MuJoCo `2.3.7`, and `mujoco-py 2.1.2.14`.
- The trigger for the current py39 rerun was that the modern-stack experiments stayed near zero, and the public robomimic version discussion made Tool-Hang success rates plausibly version-sensitive.

### Evidence Chain

| Step | Hypothesis | Test | Evidence | Decision |
|---|---|---|---|---|
| 1. Direct 4x2 modern-stack reproduction | The Fig. 9 diffusion subset should work with `global_action=8` on the modern H200 stack. | 4 tasks x DP/PTP, `global_obs=16`, `global_horizon=32`, `global_action=8`, 500 epochs, selected-checkpoint eval with `n_test=100`, `n_samples=1`. | Only Square PTP had nonzero final eval: `0.36`. DP/no-PTP was `0.00` on all four tasks; Tool-Hang, Transport, and Long Square PTP were also `0.00`. | The implementation path was not completely broken because Square PTP worked, but the result was far below the paper and failed on the other three tasks. |
| 2. Action-horizon ablation on modern stack | Low score might be caused by using chunk size 8 when the task needs action horizon 1. | 4 tasks x DP/PTP x `global_action in {1,8}`, 2000 epoch target, training-time rollout with `n_test=100`. | Square improved only modestly: PTP a8 best `0.45`, PTP a1 best `0.28`. Tool-Hang and Long Square stayed `0.00` for all cells. Transport only reached `0.01` for PTP a8. | Action horizon alone did not explain the failures. This moved the investigation toward environment / data-generation version mismatch. |
| 3. Version-sensitivity check | robomimic / robosuite version mismatch may affect success rates. | Compare active stack against repository pins and robomimic issue guidance; then build `/root/ptp_ldp_py39` with robomimic `0.2.0` and robosuite source version `1.2.0`. | Upstream pins and robomimic issue notes point to older offline-study-era robosuite lineage. Current py39 run already recovers high PTP on Square and Tool-Hang. | Continue current py39 4x2x2 as the main isolation run; treat old modern-stack results as evidence that the stack mismatch is a real confound. |

### Prior Modern-Stack 4x2 Result

Source: `fig9_diffusion_subset_*` training outputs and Session 63 / 65 selected-checkpoint evals.

| Task | DP selected ckpt | DP eval | PTP selected ckpt | PTP eval | Interpretation |
|---|---|---:|---|---:|---|
| Square | `epoch=0499-test_mean_score=0.025.ckpt` | `0.00` | `epoch=0099-test_mean_score=0.475.ckpt` | `0.36` | Only meaningful nonzero result. |
| Tool-Hang | `epoch=0499-test_mean_score=0.000.ckpt` | `0.00` | `epoch=0499-test_mean_score=0.000.ckpt` | `0.00` | Both methods failed. |
| Transport | `epoch=0499-test_mean_score=0.000.ckpt` | `0.00` | `epoch=0499-test_mean_score=0.000.ckpt` | `0.00` | Both methods failed. |
| Long Square | `epoch=0499-test_mean_score=0.000.ckpt` | `0.00` | `epoch=0499-test_mean_score=0.000.ckpt` | `0.00` | Both methods failed. |

### Prior Modern-Stack 4x2x2 Action-Horizon Result

Source: `session89_4x2x2_2000ep_1778075154` checkpoint filename scores, single-seed training-time rollout with `n_test=100`.

| Task | DP a1 best | DP a8 best | PTP a1 best | PTP a8 best | Interpretation |
|---|---:|---:|---:|---:|---|
| Square | `0.02` | `0.08` | `0.28` | `0.45` | Horizon 8 was better, but still well below paper. |
| Tool-Hang | `0.00` | `0.00` | `0.00` | `0.00` | Horizon change did not help. |
| Transport | `0.00` | `0.00` | `0.00` | `0.01` | Only a negligible nonzero point. |
| Long Square | `0.00` | `0.00` | `0.00` | `0.00` | Horizon change did not help. |

The key logic is that the first failure was not enough to blame versioning, because action chunking was still a plausible parameter mismatch. After the `a1/a8` ablation remained near zero, the environment mismatch became the cleaner explanation to isolate.

## Current Run

| Item | Value |
|---|---|
| Stamp | `20260509_014611` |
| Output root | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/outputs/session120_ptp_py39_ht_4x2x2_2000ep_20260509_014611` |
| Log root | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session120_ptp_py39_ht_4x2x2_2000ep_20260509_014611` |
| Launch script | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/scripts/session120_launch_ptp_py39_high_throughput_4x2x2_2000ep.sh` |
| GPU snapshot branch | `intern_ldp_explorer/task001_ptp_py39_rerun` |
| GPU snapshot HEAD | `529857fa8bab663510d88c5c7b72b973f4c37104` |
| GPU code patch in snapshot | Gym 0.21-compatible `concatenate` wrapper in `async_vector_env.py` and `sync_vector_env.py` |
| Current artifacts | `52` checkpoints, `586` mp4 files, output root about `36G` |

## Environment Snapshot

| Component | Version / Path |
|---|---|
| Python | `/root/ptp_ldp_py39/bin/python`, Python `3.9.25` |
| torch / torchvision | `2.5.1` / `0.20.1` |
| robomimic | `0.2.0` |
| robosuite | `1.2.0` |
| gym | `0.21.0` |
| mujoco / mujoco-py | `2.3.7` / `2.1.2.14` |
| dm-control | `1.0.9` |
| diffusers | `0.11.1` |
| huggingface-hub | `0.10.1` |

## Shared Training Settings

| Setting | Value |
|---|---|
| `global_obs` | `16` |
| `global_horizon` | `32` |
| `global_action` | `1` or `8` |
| Epoch target | `2000` |
| Batch size | `64` |
| Gradient accumulation | `1` |
| Rollout interval | `100` epochs |
| Checkpoint interval | `100` epochs |
| Validation interval | `1` epoch |
| EMA | Enabled by base config |
| Visual encoder | Official released encoder checkpoint, frozen |
| Cached embedding | Enabled via `policy.use_embed_if_present=true` and `task.dataset.use_embed_if_present=true` |
| DP / no-PTP | `policy.past_action_pred=false`, `policy.past_steps_reg=-1` |
| PTP | `policy.past_action_pred=true`, `policy.past_steps_reg=-1` |
| Rollout | `task.env_runner.n_test=100`, `n_test_vis=4`, `n_train_vis=2`, `n_envs=4` |

## Dataset Paths

| Task | Training dataset | Rollout dataset | Encoder |
|---|---|---|---|
| Square | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image_abs_emb.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image_abs.hdf5` | `square_encoder.ckpt` |
| Tool-Hang | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/tool_hang/ph/image_abs_emb_compact.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5` | `tool_hang_encoder.ckpt` |
| Transport | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/transport/mh/image_abs_emb_compact.hdf5` | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/transport/mh/image_abs.hdf5` | `transport_encoder.ckpt` |
| Long Square | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/longhistsquare100/image.hdf5` | same file | `longhist_encoder.ckpt` |

## Current Best Scores

These are not final 2000-epoch numbers. They are the best rollout scores present in shared logs and checkpoints as of Session 126.

| Task | Action | DP best | DP epoch | PTP best | PTP epoch | Gap |
|---|---:|---:|---:|---:|---:|---:|
| Square | 1 | `0.02` | `99` | `0.76` | `99` | `+0.74` |
| Square | 8 | `0.02` | `299` | `0.85` | `99` | `+0.83` |
| Tool-Hang | 1 | `0.00` | `99` | `0.86` | `99` | `+0.86` |
| Tool-Hang | 8 | `0.00` | `99/199` | `0.85` | `199/399` | `+0.85` |
| Transport | 1 | no completed score | n/a | `0.01` | `99` | n/a |
| Transport | 8 | `0.00` | `99` | `0.30` | `99` | `+0.30` |
| Long Square | 1 | `0.00` | `99/199` | `0.17` | `199` | `+0.17` |
| Long Square | 8 | `0.00` | `99/199/299/399` | `0.24` | `599` | `+0.24` |

## Rollout History

| Task | Method | Action | Score history |
|---|---|---:|---|
| Square | DP | 1 | `e99=0.02` |
| Square | DP | 8 | `e99=0.00`, `e199=0.01`, `e299=0.02` |
| Square | PTP | 1 | `e99=0.76`, `e199=0.74` |
| Square | PTP | 8 | `e99=0.85`, `e199=0.79`, `e299=0.72`, `e399=0.78`, `e499=0.80` |
| Tool-Hang | DP | 1 | `e99=0.00` |
| Tool-Hang | DP | 8 | `e99=0.00`, `e199=0.00` |
| Tool-Hang | PTP | 1 | `e99=0.86` |
| Tool-Hang | PTP | 8 | `e99=0.84`, `e199=0.85`, `e299=0.82`, `e399=0.85` |
| Transport | DP | 1 | no completed score |
| Transport | DP | 8 | `e99=0.00` |
| Transport | PTP | 1 | `e99=0.01` |
| Transport | PTP | 8 | `e99=0.30` |
| Long Square | DP | 1 | `e99=0.00`, `e199=0.00` |
| Long Square | DP | 8 | `e99=0.00`, `e199=0.00`, `e299=0.00`, `e399=0.00` |
| Long Square | PTP | 1 | `e99=0.13`, `e199=0.17` |
| Long Square | PTP | 8 | `e99=0.17`, `e199=0.17`, `e299=0.21`, `e399=0.11`, `e499=0.09`, `e599=0.24`, `e699=0.19` |

## Progress And Failure Notes

| Run | Last logged epoch | Last scored epoch | Notes |
|---|---:|---:|---|
| `longsquare_dp_a1` | `294` | `199` | No explicit traceback in sampled log, did not reach 2000 |
| `longsquare_dp_a8` | `499` | `399` | No explicit traceback in sampled log, did not reach 2000 |
| `longsquare_ptp_a1` | `299` | `199` | Failed during rollout with `ValueError: Internal algorithm failed to converge` |
| `longsquare_ptp_a8` | `799` | `699` | No explicit traceback in sampled log, did not reach 2000 |
| `square_dp_a1` | `199` | `99` | No explicit traceback in sampled log, did not reach 2000 |
| `square_dp_a8` | `399` | `299` | No explicit traceback in sampled log, did not reach 2000 |
| `square_ptp_a1` | `299` | `199` | No explicit traceback in sampled log, did not reach 2000 |
| `square_ptp_a8` | `599` | `499` | No explicit traceback in sampled log, did not reach 2000 |
| `toolhang_dp_a1` | `199` | `99` | No explicit traceback in sampled log, did not reach 2000 |
| `toolhang_dp_a8` | `299` | `199` | Failed during rollout with MuJoCo QACC instability |
| `toolhang_ptp_a1` | `199` | `99` | No explicit traceback in sampled log, did not reach 2000 |
| `toolhang_ptp_a8` | `498` | `399` | No explicit traceback in sampled log, did not reach 2000 |
| `transport_dp_a1` | `99` | n/a | No completed score in parsed JSON |
| `transport_dp_a8` | `135` | `99` | No explicit traceback in sampled log, did not reach 2000 |
| `transport_ptp_a1` | `130` | `99` | No explicit traceback in sampled log, did not reach 2000 |
| `transport_ptp_a8` | `199` | `99` | No explicit traceback in sampled log, did not reach 2000 |

## Paper Comparison For A8

| Task | Paper no-PTP | Repro DP a8 best | Paper PTP | Repro PTP a8 best |
|---|---:|---:|---:|---:|
| Square | `0.17 ± 0.01` | `0.02` | `0.89 ± 0.01` | `0.85` |
| Tool-Hang | `0.00 ± 0.00` | `0.00` | `0.75 ± 0.10` | `0.85` |
| Transport | `0.00 ± 0.00` | `0.00` | `0.67 ± 0.08` | `0.30` |
| Long Square | `0.03 ± 0.02` | `0.00` | `0.93 ± 0.02` | `0.24` |

## Conclusions For Reporting

1. The strongest validated signal is that PTP is working on short Robomimic tasks: Square and Tool-Hang reach `0.85` and `0.85/0.86` success early, while DP / no-PTP remains near zero in the same batch.
2. The current reproduction is not a finished 2000-epoch result. Most lanes stopped before the epoch target, and two lanes hit rollout-time simulator failures. The table should be presented as intermediate best-observed scores, not final paper-grade scores.
3. The recommended-version environment resolved the earlier all-zero Tool-Hang issue: PTP Tool-Hang is now high-scoring. That points to the previous zero-success behavior being driven by environment / action / rollout compatibility issues rather than the PTP objective itself.
4. Transport and Long Square remain below paper PTP levels. Transport PTP a8 reached `0.30` at epoch `99`, but only one completed score is available. Long Square PTP a8 reached `0.24` at epoch `599`, still far below the paper's long-horizon result and likely needs a clean uninterrupted continuation plus simulator stability checks.
5. Action horizon ablation is currently inconclusive outside Square and Tool-Hang. For Square, a8 is better than a1 at best score (`0.85` vs `0.76`). For Tool-Hang, a1 and a8 are both high (`0.86` vs `0.85`). For Transport and Long Square, the current evidence favors a8, but the jobs did not complete enough rollouts to make this robust.
6. The immediate technical risks are rollout interruption, MuJoCo instability during some evaluations, and single-seed reporting. Before presenting as final reproduction, run uninterrupted completion or resume from the best checkpoints, then evaluate selected checkpoints with fixed `n_test=100`, mp4 saved, and at least three seeds.
