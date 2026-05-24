# Direction C Session 49 Mask Analysis Report

## Question

The previous Direction C pipeline had a positive offline representation signal, but downstream rollout evidence was mixed:

| stage | setting | result |
| --- | --- | --- |
| Stage 2a | pretrained frozen `past` context | better offline future-action loss than frozen random context |
| Stage 2b add-all e24 | pretrained vs random | `0/10` vs `2/10` |
| Stage 2b add-all e49 | pretrained vs random | `2/10` vs `5/10` |
| Stage 2b add-all e99 | pretrained vs random | `4/10` vs `3/10` |
| Stage 2b nonzero-projector e99 | pretrained | `4/10` |
| Stage 2b add-last e49 | pretrained vs random | `4/10` vs `0/10` |

The key question is why the offline translator context did not reliably help after injection into the diffusion transformer.

## Diagnosis

The action8 downstream config uses:

```yaml
policy.horizon: 8
policy.n_obs_steps: 16
policy.causal_attn: true
policy.n_cond_layers: 0
```

`TransformerForDiffusion` builds a causal `memory_mask` with:

```python
mask = t >= (s - 1)
```

where `t` is the action-token index and `s` is the condition-token index after the time token. With `horizon=8` and `n_obs_steps=16`, action tokens `0..7` can attend only obs condition tokens `0..7`. Obs tokens `8..15`, including the newest/current observation token, are invisible to the action decoder.

This matters for the translator experiments:

- `context_injection=add_last` modifies obs condition token `15`, which is fully masked out in the old action8 config.
- `context_injection=add_all` modifies visible tokens `0..7`, but those are the older half of the history window rather than the newest observation context.
- The apparent `add_last` rollout improvement is therefore not reliable evidence that the behavior context reached the policy; it is more likely run variance or indirect training nondeterminism.

## Code Change

Added a backward-compatible transformer option:

```python
causal_cond_attn: bool = True
```

Default behavior is unchanged. Setting `policy.causal_cond_attn=false` keeps the action self-attention setting but disables the causal memory mask from action tokens to observation condition tokens. This is appropriate for long observation history conditioning because all observation tokens are already known at action-generation time.

Touched files:

- `diffusion_policy/model/diffusion/transformer_for_diffusion.py`
- `diffusion_policy/policy/diffusion_transformer_hybrid_image_policy.py`
- `experiment_configs/square/transformer_square_translator_context_action8.yaml`

## Experiment A: Perturbation Visibility

Setup:

- Synthetic `TransformerForDiffusion`
- `horizon=8`
- `n_obs_steps=16`
- `cond_dim=64`
- `n_layer=2`
- `n_head=4`
- `n_emb=64`
- `n_cond_layers=0`
- dropout disabled
- 12 random seeds

For each obs token, add the same small perturbation and measure RMS output change.

Result:

| setting | nonzero sensitivity obs tokens | `add_last` RMS | `add_visible_last` RMS | `add_all` RMS |
| --- | --- | ---: | ---: | ---: |
| `causal_cond_attn=true` | `0..7` | `0.00000000` | `0.00000352` | `0.00007238` |
| `causal_cond_attn=false` | `0..15` | `0.00000546` | `0.00000548` | `0.00008744` |

Interpretation:

- Old behavior makes the true last obs token exactly invisible.
- Disabling causal condition attention makes every history token visible.
- `add_all` is still a much larger global perturbation than a single-token injection, so it should be treated as a strong intervention rather than a clean context token.

## Experiment B: Gradient Visibility

Setup matches Experiment A. Backpropagate a simple output loss and measure gradient norm with respect to each condition token.

Result:

| setting | condition tokens with nonzero gradient |
| --- | --- |
| `causal_cond_attn=true` | `0..7` |
| `causal_cond_attn=false` | `0..15` |

Gradient norms for old behavior are exactly zero for obs tokens `8..15`; after the change, all 16 obs tokens have nonzero gradients.

## Next Formal Experiment Design

Do not continue the old Stage2b jobs. They trained under a condition mask that hid the newest half of the observation window from the action decoder.

Once a clean GPU/storage resource is available, run the corrected Square action8 matrix:

| ID | policy | context | injection | `causal_cond_attn` | purpose |
| --- | --- | --- | --- | --- | --- |
| M1 | base DP/PTP transformer | none | none | `false` | corrected no-context baseline |
| M2 | translator-conditioned | pretrained `past` | `add_last` | `false` | main corrected Direction C test |
| M3 | translator-conditioned | random | `add_last` | `false` | same-architecture random control |
| M4 | translator-conditioned | pretrained `past` | `add_all` | `false` | test whether global injection remains harmful |

Prepared config entry points:

| ID | config |
| --- | --- |
| M1 | `experiment_configs/square/transformer_square_action8_causalcond_off_base.yaml` |
| M2 | `experiment_configs/square/transformer_square_translator_context_action8_causalcond_off_add_last.yaml` |
| M3 | `experiment_configs/square/transformer_square_random_context_action8_causalcond_off_add_last.yaml` |
| M4 | `experiment_configs/square/transformer_square_translator_context_action8_causalcond_off_add_all.yaml` |

Use the same py39 / `robomimic==0.2.0` environment. Evaluate at least e24/e49/e99 or equivalent fixed step budgets, and use more than 10 rollout seeds before treating small differences as signal.

## Current Result Status

This session produced an implementation-level experiment, not a new Robomimic rollout. A meaningful rollout is blocked until the stale NFS/page-I/O-wait jobs are killed or clean storage/GPU resources are provided. The code path for the corrected experiment is implemented and py_compile passed.

Session 50 cleanup attempt:

- Tried `SIGTERM` then `SIGKILL` on stale parent PIDs `1086376`, `4026333`, `26885`, `4026336`, `4086173`, `2080560`, `2080562`, and `2080564`.
- The same PIDs remained in `D/Dl` with `wchan=wait_on_page_bit_common`.
- GPU memory remained occupied by those Python compute apps.

Conclusion: these jobs are in uninterruptible kernel I/O wait. The existing nodes require platform-level restart/release or storage recovery before they are clean training resources.
