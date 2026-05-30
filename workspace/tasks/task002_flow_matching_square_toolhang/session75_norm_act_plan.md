# Session 75 Direction C Norm / ACT Plan

## Immediate environment

- GPU node: `10.100.0.20:26715`
- Hardware: `8 x NVIDIA H200`
- Storage: `/mnt/cephfs` and `/mnt/3fs1` are mounted.
- Runtime target: Python 3.9 with `robomimic==0.2.0`, matching the PTP reproduction environment.

## Motivation

The current translator losses are numerically small after action normalization. That makes the effective update size weak, especially for the translator hidden state that is later used as downstream context. The next round separates three questions:

1. Does a stronger normalized translator objective improve the learned history-to-action representation?
2. Is the weak result caused by our transformer being much smaller than ACT-scale action chunking models?
3. Does an ACT-style direct action chunking baseline beat or match the current DP/PTP-style baselines on the same Square action8 setting?

## Code changes

- Stage 1 translator training now supports:
  - `training.action_loss_reduction=mean | sum_action_dim`
  - `training.loss_scale`
- Translator-conditioned DP/PTP now supports:
  - `policy.translator_context_norm=true`
- Added a deterministic ACT-style baseline:
  - `diffusion_policy/policy/action_chunking_transformer_hybrid_image_policy.py`

## New configs

- `experiment_configs/square/behavior_translator_square_past_actsize_norm.yaml`
  - Translator hidden size 512, 8 heads, 4 encoder layers, 7 decoder layers, FFN 3200.
  - Uses `sum_action_dim` and `loss_scale=10`.
- `experiment_configs/square/act_square_action8.yaml`
  - ACT-style direct action chunking, deterministic v0 without CVAE latent path.
- `experiment_configs/square/transformer_square_action8_causalcond_off_base_actsize.yaml`
  - DP/PTP transformer scaled to ACT-size geometry.
- `experiment_configs/square/transformer_square_translator_context_action8_causalcond_off_add_last_actsize_norm.yaml`
  - ACT-size DP/PTP transformer plus pretrained translator context with LayerNorm.

## Execution order

1. Smoke test all new configs with `--cfg job` on the new node.
2. Run one short smoke train per config with `training.num_epochs=1` and limited train/val steps.
3. Start the 4 GPU-parallel Square runs:
   - ACT-style direct chunker.
   - ACT-size DP/PTP base.
   - ACT-size DP/PTP + normalized pretrained translator context.
   - Stage 1 ACT-size normalized past translator.
4. Monitor first 5 to 10 epochs. Stop any run whose validation loss diverges or whose throughput is clearly broken.
5. After epoch 25 or 50 checkpoints exist, run rollout eval for ACT-style, ACT-size base, and ACT-size translator-context models.

## Expected outcomes

- If ACT-style direct chunking is better than DP/PTP base early, the current bottleneck is likely action chunk architecture or diffusion sampling complexity rather than translator alone.
- If ACT-size base improves but ACT-style does not, parameter count and condition encoder capacity are the main suspects.
- If ACT-size normalized translator context beats ACT-size base, Direction C has a viable downstream signal.
- If normalized Stage 1 still only improves past loss but does not help downstream, the current translator target is likely learning proprio-to-action reconstruction rather than image-grounded behavior context.
