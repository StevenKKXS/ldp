# History Log

<!-- METADATA:SESSION=0 -->

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
