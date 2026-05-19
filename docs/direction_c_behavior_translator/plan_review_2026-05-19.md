# Direction C: Behavior Translator Context Pretraining

## 0. Review Summary

The proposed direction is feasible, but the first version should be narrower than the draft.

Core hypothesis:

```text
A history-to-action translator may be too coarse as a final policy, but its hidden state may provide behavior-aware context that improves downstream DP/PTP.
```

The key go/no-go remains:

```text
frozen pretrained translator context > frozen random translator context
```

I recommend validating this with offline translation and a frozen-head probe before touching DP/PTP. If the probe has no signal, DP/PTP integration is not worth the extra implementation and GPU cost.

## 1. Required Feasibility Corrections

### Correction 1: Do not assume dataloader returns camera embeddings

Current PTP dataloader normally returns raw image/proprio tensors:

```text
obs["agentview_image"] or task camera images
obs["robot0_eye_in_hand_image"] / sideview image
obs["robot0_eef_pos"]
obs["robot0_eef_quat"]
obs["robot0_gripper_qpos"]
```

The existing policy encodes them inside `DiffusionTransformerHybridImagePolicy` with `self.obs_encoder(...)`.

Therefore v0 should use:

```text
raw obs history -> existing robomimic obs_encoder -> obs feature tokens -> BehaviorTranslator
```

Precomputed `embedding` datasets can be an optional speed path only after verifying shape and semantics. They should not be the default because the normal PTP path is raw image/proprio.

### Correction 2: Keep action normalization identical to PTP

The translator target must use the same action normalizer as PTP:

```text
abs_action position dims: range-normalized to [-1, 1]
other action dims: identity
dual arm: same rule per arm
```

The trainer should call `dataset.get_normalizer()` and use `normalizer["action"]`.

### Correction 3: Decouple Stage 1/2a from DP/PTP

Stage 1 and Stage 2a can be implemented with no environment rollout and no diffusion policy edits. This is the right first milestone because it tests the representation claim directly and is much cheaper than training PTP variants.

### Correction 4: Window construction is easy for fixed windows

For `subsample_frames=1`, using:

```text
n_obs_steps = H
horizon = H + K
pad_before = H - 1
pad_after = K
```

lets the sample be centered at current frame `t = H - 1`:

```text
obs_hist   = o[t-H+1 : t]
act_past   = a[t-P : t-1]
act_future = a[t : t+K-1]
```

For v0 set `P = H` and include the current action in the future chunk. If later we need `P != H`, implement explicit index slicing in the dataset wrapper.

## 2. Revised V0 Scope

V0 deliverables:

```text
1. BehaviorTranslationDataset wrapper over RobomimicReplayImageDataset
2. ObsFeatureAdapter that reuses the existing robomimic obs_encoder
3. BehaviorTranslator model
4. Stage 1 trainer
5. Stage 2a frozen-head probe
6. CSV/JSON logs and result tables
```

V0 does not implement:

```text
DP/PTP injection
action encoder
VQ/action tokenizer
latent diffusion or flow matching
future obs prediction
EMA teacher
contrastive loss
```

## 3. Data Interface

The dataset should return raw obs and action windows, not pre-flattened camera embeddings:

```python
{
    "obs_hist": {
        "agentview_image": Tensor[H, C, H_img, W_img],  # task dependent
        "robot0_eye_in_hand_image": Tensor[H, C, H_img, W_img],
        "sideview_image": Tensor[H, C, H_img, W_img],  # ToolHang
        "robot0_eef_pos": Tensor[H, 3],
        "robot0_eef_quat": Tensor[H, 4],
        "robot0_gripper_qpos": Tensor[H, 2],
    },
    "act_past": Tensor[P, Da],
    "act_future": Tensor[K, Da],
}
```

The trainer then runs:

```text
obs_hist raw dict
    -> normalizer.normalize(obs_hist)
    -> existing obs_encoder over B*H
    -> obs_tokens [B, H, Dobs]
    -> BehaviorTranslator
```

This avoids committing to a cached embedding format and stays closest to the PTP path.

## 4. BehaviorTranslator V0

Input:

```text
obs_tokens: [B, H, Dobs]
```

Model:

```text
ObsProjector(Dobs -> D)
causal TransformerEncoder
learned action queries [P+K, D]
TransformerDecoder cross-attending to obs tokens
SketchActionHead(D -> Da)
ContextProjector
```

Outputs:

```python
{
    "pred_actions": [B, P + K, Da],
    "context": [B, context_dim],
    "context_tokens": [B, P + K, D],
    "z_obs": [B, H, D],
}
```

Default dimensions:

```yaml
d_model: 256
n_encoder_layers: 4
n_decoder_layers: 2
n_heads: 4
ff_dim: 1024
dropout: 0.1
context_dim: 512
```

V0 cross-attention mask:

```text
Round 1: no cross-attn mask, all action queries attend full history
Round 1b: causal_past_full_future mask as ablation
```

Reason: the mask is useful, but it is not necessary for the first shape-correct and loss-correct implementation.

## 5. Stage 1 Offline Translation

Loss:

```text
SmoothL1(pred_past, act_past) * w_past
+ SmoothL1(pred_future, act_future) * w_future
```

Defaults:

```yaml
obs_horizon: 16
past_action_horizon: 16
future_action_horizon: 8
w_past: 1.0
w_future: 1.0
batch_size: 64
lr: 1.0e-4
epochs_smoke: 1
epochs_probe: 20
```

I changed the initial future horizon from 16 to 8 for the first GPU pass because current PTP/ToolHang configs use action chunk 8 and this lowers the cost of validating the idea. If offline curves look healthy, run K=16.

Metrics:

```text
train/loss_total
train/loss_past
train/loss_future
val/loss_total
val/loss_past
val/loss_future
val/future_l1
val/future_mse
val/per_horizon_l1_00 ... val/per_horizon_l1_K
val/gripper_acc
```

## 6. Stage 1 Round 1 Experiments

Run only Square first, then ToolHang if Square smoke and metrics are stable.

| ID | Task | Setting | Purpose |
|---|---|---|---|
| C1-T1 | Square | single-frame -> future | weakest baseline |
| C1-T2 | Square | history -> future | tests history value |
| C1-T3 | Square | history -> past+future | main translator |
| C1-T4 | Square | shuffled history -> past+future | tests temporal order |
| C1-T5 | ToolHang | history -> future | second task sanity |
| C1-T6 | ToolHang | history -> past+future | second task main |

Implementation simplification:

```text
single-frame: keep only obs_hist[:, -1:] and adapt model H=1
history future: set w_past=0 and skip past output loss
shuffled history: permute obs history order before obs_encoder
```

## 7. Stage 2a Frozen-Head Probe

Before DP/PTP integration, train a simple future action head:

```text
translator.get_context(obs_tokens) -> MLP -> future actions [K, Da]
```

Comparisons:

| ID | Task | Context | Frozen | Purpose |
|---|---|---|---:|---|
| C2-H1 | Square | random translator | yes | structure/parameter control |
| C2-H2 | Square | pretrained translator | yes | main representation test |
| C2-H3 | Square | pretrained translator | no | finetune sanity |
| C2-H4 | ToolHang | random translator | yes | second task control |
| C2-H5 | ToolHang | pretrained translator | yes | second task representation test |

Go/no-go:

```text
C2-H2 > C2-H1 is required before DP/PTP integration.
C2-H5 > C2-H4 is desirable before spending ToolHang rollout budget.
```

## 8. DP/PTP Integration Is Round 3

Do not implement this until Stage 2a has a positive signal.

Preferred injection after signal:

```text
original PTP condition tokens + projected behavior token
```

Not replacement. Replacement risks losing the proven PTP condition path.

Round 3 comparisons:

| ID | Task | Method | Translator | Frozen |
|---|---|---|---|---:|
| C3-D1 | Square | PTP baseline | none | - |
| C3-D2 | Square | PTP + random behavior token | random | yes |
| C3-D3 | Square | PTP + pretrained behavior token | pretrained | yes |
| C3-D4 | Square | PTP + pretrained behavior token | pretrained | projector-only |
| C3-D5 | ToolHang | PTP baseline | none | - |
| C3-D6 | ToolHang | PTP + random behavior token | random | yes |
| C3-D7 | ToolHang | PTP + pretrained behavior token | pretrained | yes |

## 9. Implementation Order

1. Create `diffusion_policy/dataset/behavior_translation_dataset.py`.
2. Create `diffusion_policy/model/behavior_translator.py`.
3. Create `train_behavior_translator.py` for Stage 1.
4. Create `train_translator_head.py` for Stage 2a.
5. Add Square configs under `experiment_configs/square/behavior_translator_*.yaml`.
6. Run CPU/py_compile and Hydra config parse.
7. Run GPU smoke with py39 / `robomimic==0.2.0`.
8. Run Square C1-T1 to C1-T4.
9. If Square shows signal, run ToolHang C1-T5/C1-T6.
10. Run Stage 2a frozen-head probe.

## 10. Environment Requirements

All PTP-data experiments must use:

```text
Python 3.9
robomimic==0.2.0
```

Current verified NFS env:

```text
/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020
```

Before any run, record:

```text
sys.executable
robomimic.__version__
robomimic.__file__
torch.__version__
```

GPU nodes should not perform external network operations. Prepare packages on CPU/common storage.

## 11. Initial File Targets

Likely code paths:

```text
diffusion_policy/dataset/behavior_translation_dataset.py
diffusion_policy/model/behavior_translator.py
diffusion_policy/workspace/train_behavior_translator_workspace.py
diffusion_policy/workspace/train_translator_head_workspace.py
experiment_configs/square/behavior_translator_square_t1.yaml
experiment_configs/square/behavior_translator_square_t2.yaml
experiment_configs/square/behavior_translator_square_t3.yaml
experiment_configs/square/behavior_translator_square_t4.yaml
```

I prefer workspace-style training over standalone scripts because this repo already uses Hydra workspace patterns, checkpoint helpers, JSON logger, and dataset instantiation that can be reused.

## 12. My Next Implementation Step

Start with code structure only:

```text
BehaviorTranslationDataset + BehaviorTranslator + one Square T3 config
```

Then verify:

```text
python -m py_compile new files
Hydra --cfg job parses
dataset[0] has expected shapes
one batch forward/backward runs on CPU or one GPU
```

Only after this shape smoke passes should we launch real Stage 1 runs.
