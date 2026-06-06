# Square Rollout Stability Eval - 2026-06-06

## Setup

- Node: `10.100.2.39:23494`
- Runtime: `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph`
- Output root: `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_rollout_stability_nenv8_max8_20260605`
- Evaluator: `eval_flow_matching_rollout.py`
- Launcher: `tools/direction_c_launch_square_rollout_stability_nenv8_max8.sh`
- Eval protocol: 3 seed ranges per setting, 100 rollout episodes per seed range, `n_envs=8`, EMA policy.
- Seed ranges: `100000`, `200000`, `300000`

## Results

| Setting | Seed 100000 | Seed 200000 | Seed 300000 | Pooled SR |
| --- | ---: | ---: | ---: | ---: |
| `base_e49` | 49/100 | 56/100 | 61/100 | 166/300 = 55.33% |
| `random_add_last_e24` | 53/100 | 60/100 | 51/100 | 164/300 = 54.67% |
| `pretrained_add_last_e24` | 44/100 | 50/100 | 41/100 | 135/300 = 45.00% |

Aggregate error estimates from `summary.json`:

| Setting | Mean of 3x100 | SD across seed ranges | SEM across seed ranges | Binomial SE over 300 |
| --- | ---: | ---: | ---: | ---: |
| `base_e49` | 0.5533 | 0.0603 | 0.0348 | 0.0287 |
| `random_add_last_e24` | 0.5467 | 0.0473 | 0.0273 | 0.0287 |
| `pretrained_add_last_e24` | 0.4500 | 0.0458 | 0.0265 | 0.0287 |

## Readout

The larger rollout sample resolves the 10-video instability: `base_e49` and `random_add_last_e24` are both around 55% SR over 300 episodes, while `pretrained_add_last_e24` is lower at 45% SR.

This does not support the current pretrained translator `add_last` injection path. The control with random frozen context is not worse than base, and the pretrained context is worse than both base and random under this protocol.

All 9 eval logs completed. The launcher exited and `10.100.2.39:23494` GPUs are idle.
