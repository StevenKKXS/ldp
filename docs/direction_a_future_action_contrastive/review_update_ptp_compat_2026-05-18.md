# Direction A Review Update: PTP-Compatible First Pass

Date: 2026-05-18

## Why This Update Exists

The user clarified that the first Direction A experiments should reproduce the proven PTP structure as much as possible, because PTP has already been shown useful in the referenced GitHub / robomimic 0.2.0 environment.

This changes the implementation priority from "add a new condition feature `z_t` to PTP" toward "use future-action contrastive learning as a pretraining objective for the encoder that PTP already uses."

## Clarification: What I Meant By Action Window

In the previous review, "action window" meant the action segment used as the label for contrastive similarity:

```text
A_i+ = action chunk used to decide whether sample i and sample j are behaviorally similar
```

It does **not** mean changing PTP's prediction horizon, rollout horizon, or action execution logic.

For Direction A, this window is only the teacher signal for the contrastive loss:

```text
d_future(i, j) = distance(A_i+, A_j+)
q_ij = softmax(-d_future(i, j) / sigma)
```

The policy itself should keep the PTP configuration unless we explicitly run an ablation.

## Updated Recommendation

First-pass Direction A should preserve the PTP policy architecture.

Do **not** add a new policy-side `concat(original_condition, z_t)` path in the first implementation.

Instead:

1. Keep the same PTP config, horizon, `n_obs_steps`, action slicing, transformer, and evaluation setup.
2. Train the existing PTP observation encoder with an auxiliary future-action contrastive pretraining objective.
3. Use any temporal aggregator / projection head only during pretraining.
4. Discard the contrastive projection head for policy training.
5. Load the pretrained encoder into the existing PTP policy through the already available `obs_encoder_dir` path.
6. Test both `obs_encoder_freeze=true` and `obs_encoder_freeze=false`.

This path best isolates the question:

```text
Does future-action contrastive pretraining improve the encoder used by otherwise unchanged PTP?
```

## Updated Interpretation Of The Action Similarity Target

To avoid accidental mismatch with PTP:

- Use the same dataset action tensor, normalizer, action representation, and episode slicing as the PTP training config.
- Do not introduce a separate data horizon solely for contrastive learning in the first pass.
- Record the exact action segment used for `A_i+`.

Recommended default:

```text
A_i+ = the downstream future/executed action segment from the same PTP sample
```

In current policy code, environment-executed actions are sliced as:

```text
start = n_obs_steps - 1
end = start + n_action_steps
action[:, start:end]
```

This is a useful default for behavior similarity because it reflects the future behavior the policy is evaluated on.

However, if the exact PTP baseline uses a different validated action-token convention for its past-token-prediction objective, follow the PTP convention and log it. Do not silently change horizons or indexing.

## Updated Baseline Matrix

Because the first-pass implementation should keep the PTP architecture unchanged, `B2` needs to be defined carefully.

### Required

```text
B1. Exact PTP baseline in the proven environment/config.
O1. Exact PTP + contrastive-pretrained encoder, frozen.
O2. Exact PTP + contrastive-pretrained encoder, finetuned.
```

### Control If Needed

```text
B2. Exact PTP + same encoder loading/freeze protocol, but without future-action contrastive pretraining.
```

If no policy-side architecture is added and no non-contrastive encoder checkpoint exists, `B2` may collapse into `B1` for the finetune setting. In that case, do not invent a misleading B2. Record that the first comparison is pretraining-vs-no-pretraining under the exact PTP architecture.

If we later add a temporal aggregator or condition fusion module to the policy, then `B2` becomes mandatory again and must match O1/O2 architecture exactly.

## What Changes From The Previous Review

The earlier review treated condition fusion as a core open implementation issue. After the user's clarification, this is demoted:

- Condition concat is **not** part of the first-pass implementation.
- Feature-dim concat or extra condition-token fusion can be considered only after exact-PTP encoder pretraining is tested.
- The first-pass implementation should use existing PTP encoder loading and freezing hooks.

Still valid from the previous review:

- Action segment alignment must be explicitly recorded.
- The contrastive loss should mask diagonal self-pairs.
- Action distance should use normalized action chunks.
- `sigma` should be derived from the action-distance distribution or carefully swept.
- Hard negatives should wait until soft contrastive pretraining is understood.
- Offline representation checks should precede full policy training.

## Revised First-Pass Workflow

1. Reproduce exact PTP baseline config and score on the intended robomimic 0.2.0-compatible environment.
2. Build a pretraining workspace around the same PTP obs encoder.
3. Add temporary temporal pooling / projection only for contrastive pretraining.
4. Save an encoder checkpoint compatible with existing `obs_encoder_dir` loading.
5. Run one-batch policy load smoke:

   ```text
   pretrained encoder checkpoint -> existing PTP config -> forward/backward
   ```

6. Run Square:

   ```text
   B1, O1, O2
   ```

7. Run ToolHang with the same protocol.

## Current Decision

Direction A remains a strong candidate, but the first version should be "PTP-compatible encoder pretraining", not "PTP plus new condition module."

No experiment has run yet. No effectiveness conclusion exists.
