# DP Rollout Eval Curves

Date: 2026-05-09 UTC

This file expands the scheduled rollout evaluation curve for the DP no-history Square experiments. Each scheduled eval runs 50 closed-loop rollouts with videos. The score below is the mean of `test/sim_max_reward_*`, equivalent to successes / 50 for Square.

## Current-Stack Official-PH v1.4.1

Runtime: py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8.

| Eval epoch | UNet successes / 50 | UNet success rate | DiT successes / 50 | DiT success rate |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 14/50 | 0.28 | 0/50 | 0.00 |
| 20 | 19/50 | 0.38 | 3/50 | 0.06 |
| 30 | 29/50 | 0.58 | 7/50 | 0.14 |
| 40 | 24/50 | 0.48 | 18/50 | 0.36 |
| 50 | 31/50 | 0.62 | 25/50 | 0.50 |
| 60 | 27/50 | 0.54 | 28/50 | 0.56 |
| 70 | 33/50 | 0.66 | 30/50 | 0.60 |
| 80 | 30/50 | 0.60 | 23/50 | 0.46 |
| 90 | 34/50 | 0.68 | 27/50 | 0.54 |
| 100 | 31/50 | 0.62 | 29/50 | 0.58 |
| 200 | 25/50 | 0.50 | 28/50 | 0.56 |
| 300 | 28/50 | 0.56 | 25/50 | 0.50 |
| 400 | 27/50 | 0.54 | 20/50 | 0.40 |
| 500 | 26/50 | 0.52 | 25/50 | 0.50 |
| 600 | 23/50 | 0.46 | 14/50 | 0.28 |
| 700 | 26/50 | 0.52 | 19/50 | 0.38 |
| 800 | - | - | 21/50 | 0.42 |

Best observed official-PH results:

| Model | Best eval epoch | Best rollout |
| --- | ---: | ---: |
| DP no-hist UNet | 90 | 34/50 = 0.68 |
| DP no-hist DiT | 70 | 30/50 = 0.60 |

## Current-Stack PTP / LDP-MH

Runtime: py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8.

| Eval epoch | UNet successes / 50 | UNet success rate | DiT successes / 50 | DiT success rate |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 2/50 | 0.04 | 0/50 | 0.00 |
| 20 | 0/50 | 0.00 | 2/50 | 0.04 |
| 30 | 0/50 | 0.00 | 0/50 | 0.00 |
| 40 | 0/50 | 0.00 | 2/50 | 0.04 |
| 50 | 1/50 | 0.02 | 0/50 | 0.00 |
| 60 | 3/50 | 0.06 | 0/50 | 0.00 |
| 70 | 0/50 | 0.00 | 2/50 | 0.04 |
| 80 | 0/50 | 0.00 | 0/50 | 0.00 |
| 90 | 3/50 | 0.06 | 1/50 | 0.02 |
| 100 | 1/50 | 0.02 | 0/50 | 0.00 |
| 200 | 3/50 | 0.06 | 2/50 | 0.04 |

Best observed PTP / LDP-MH results:

| Model | Best eval epoch | Best rollout |
| --- | ---: | ---: |
| DP no-hist UNet | 60 / 90 / 200 | 3/50 = 0.06 |
| DP no-hist DiT | 20 / 40 / 70 / 200 | 2/50 = 0.04 |

## Py39 Comparison Snapshot

Runtime: py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1. These runs are still training, and the schedule uses every 20 epochs through epoch 100, then every 100 epochs.

| Data version | Model | Best eval epoch | Best rollout |
| --- | --- | ---: | ---: |
| Official-PH image_abs v1.4.1 | DP no-hist UNet | 200 | 5/50 = 0.10 |
| Official-PH image_abs v1.4.1 | DP no-hist DiT | 60 | 24/50 = 0.48 |
| PTP / LDP-MH image_abs | DP no-hist UNet | 80 / 100 | 18/50 = 0.36 |
| PTP / LDP-MH image_abs | DP no-hist DiT | 40 / 80 | 5/50 = 0.10 |

## Notes

- The strong `0.68` / `0.60` values are from current-stack official-PH v1.4.1 DP, not from the py39 robomimic 0.2 comparison.
- Official-PH learns quickly in the first 70-90 epochs, then fluctuates downward. This is why selecting by rollout checkpoint matters.
- PTP / LDP-MH remains much lower on the current stack under the same no-history DP setting.
