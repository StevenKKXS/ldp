# Translator / ACT / PTP Action Generation Dataflow Report

This report explains how the current Direction C code computes actions in the
Square action8 setting. It focuses on data flow, tensor shapes, module sizes,
and where the action tensor is produced.

## 0. Shared Notation And Square Defaults

```text
B  = batch size
T  = action / diffusion horizon
To = observation horizon
H  = translator obs history
P  = translator past action horizon
K  = future action horizon / action chunk length
Da = action_dim = 10
Do = robomimic obs feature dim = 137
D  = transformer hidden dim
```

For the Square image setting used here:

```text
raw obs keys:
  agentview_image             [B, To, 3, 84, 84]
  robot0_eye_in_hand_image    [B, To, 3, 84, 84]
  robot0_eef_pos              [B, To, 3]
  robot0_eef_quat             [B, To, 4]
  robot0_gripper_qpos         [B, To, 2]

action:
  Da = 10 = eef_pos(3) + rotation_6d(6) + gripper(1)

shared robomimic obs_encoder:
  normalized raw obs -> obs token [B * To, 137]
  reshaped as obs_tokens [B, To, 137]

shared obs_encoder params:
  22.394M
```

All trusted runs should use the main py39 environment:

```bash
VENV=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph
"$VENV/bin/python" diffusion_policy/scripts/check_main_runtime_env.py --require-cuda
```

## 1. Behavior Translator

### 1.1 Overview

Translator is an offline pretraining module. It directly predicts a sketchy
past/future action sequence from observation history. Its `context` is later
used by downstream probes or policy-conditioning experiments, but Stage 1
itself does not perform environment rollout.

```text
raw obs history
  [B, H=16, images + lowdim]
        |
        | normalize obs
        v
robomimic obs_encoder
        |
        v
obs_tokens
  [B, H=16, Do=137]
        |
        | Linear 137 -> D, add temporal pos
        v
z_input
  [B, 16, D]
        |
        | causal TransformerEncoder, 4 layers default
        v
z_obs
  [B, 16, D]
        |
        | learned action queries [P+K=24]
        v
action_query_decoder cross-attends to z_obs
        |
        v
h_action
  [B, 24, D]
        |
        | LayerNorm -> Linear D->D -> GELU -> Linear D->10
        v
pred_actions
  [B, 24, Da=10]
        |
        +-- pred_past   = pred_actions[:, :16]   [B, 16, 10]
        +-- pred_future = pred_actions[:, 16:]   [B,  8, 10]
```

### 1.2 Dataset Window

For the main translator setting:

```text
H = 16
P = 16
K = 8
anchor = max(P, H - 1) = 16
sequence_length = anchor + K = 24
```

The dataset samples one contiguous sequence of length 24. Within that sequence:

```text
obs indices:
  obs_start = anchor - H + 1 = 1
  obs_end   = anchor + 1     = 17
  obs_hist  = data[1:17]     [16 frames]

action indices:
  act_past   = action[0:16]   [16 actions]
  act_future = action[16:24]  [8 actions]
```

Conceptually, if `anchor` is the current time `t`:

```text
obs_hist   ~= o_{t-H+1 : t}
act_past   = a_{t-P : t-1}
act_future = a_{t : t+K-1}
```

### 1.3 Forward Computation

Input to `BehaviorTranslator.forward`:

```text
obs_tokens: [B, 16, 137]
```

The model computes:

```text
z = obs_projector(obs_tokens) + obs_pos_emb
  = Linear(137, D)([B,16,137]) + [1,16,D]
  = [B,16,D]

src_mask = causal upper-triangular mask if causal_obs_encoder=true

z_obs = TransformerEncoder(z, mask=src_mask)
      = [B,16,D]

queries = action_queries.expand(B, -1, -1)
        = [B,24,D]

h_action = TransformerDecoder(tgt=queries, memory=z_obs)
         = [B,24,D]

pred_actions = sketch_action_head(h_action)
             = [B,24,10]
```

The direct action-producing layer is:

```text
sketch_action_head:
  LayerNorm(D)
  Linear(D, D)
  GELU
  Linear(D, 10)
```

### 1.4 Stage 1 Loss

The workspace first normalizes actions unless `action_loss_space=raw`.

```text
act_past   -> normalizer["action"].normalize(...) -> [B,16,10]
act_future -> normalizer["action"].normalize(...) -> [B, 8,10]
```

Then:

```text
pred_past   = pred_actions[:, :P]  [B,16,10]
pred_future = pred_actions[:, P:]  [B, 8,10]

loss_past   = SmoothL1(pred_past,   act_past)
loss_future = SmoothL1(pred_future, act_future)

target_mode=past:
  loss_total = loss_past

target_mode=future:
  loss_total = loss_future

target_mode=past_future:
  loss_total = w_past * loss_past + w_future * loss_future
```

Important caveat:

```text
The Stage 1 action loss supervises sketch_action_head(pred_actions).
The downstream context vector is produced by context_projector and is not
directly supervised by a separate context loss.
```

### 1.5 Context Computation

The same forward pass also builds a pooled behavior context:

```text
h_future_pool = mean(h_action[:, P:, :], dim=1)  [B,D]
h_all_pool    = mean(h_action, dim=1)            [B,D]
z_last        = z_obs[:, -1, :]                  [B,D]

context_input = concat(h_future_pool, h_all_pool, z_last)
              = [B, 3D]

context = LayerNorm(3D) -> Linear(3D, 512)
        = [B,512]
```

This `context` is what Stage 2a and Stage 2b consume.

### 1.6 Translator Parameter Counts

Measured on the GPU-node py39 runtime with current Square configs:

```text
shared obs_encoder:
  22.394M params

default d256 translator:
  D=256, heads=4, encoder_layers=4, decoder_layers=2, ff=1024
  translator core: 5.776M
  full Stage 1 model with obs_encoder: 28.170M

ACT-size translator:
  D=512, heads=8, encoder_layers=4, decoder_layers=7, ff=3200
  translator core: 56.177M
  full Stage 1 model with obs_encoder: 78.571M
```

## 2. Official-ACT-Compatible CVAE Policy

### 2.1 Overview

This is the `OfficialActHybridImagePolicy` path. It is ACT-like because it uses:

```text
posterior action encoder -> latent z -> memory encoder -> action query decoder
```

The current Square official ACT config is short-history:

```text
To = 2
K  = 8
T  = horizon = 10
D  = hidden_dim = 512
qpos_dim = 9
latent_dim = 32
Da = 10
```

String diagram:

```text
raw obs [B,2,...]
        |
        | normalize obs
        v
robomimic obs_encoder
        |
        v
obs_tokens [B,2,137]

latest lowdim at obs step 1
        |
        v
qpos [B,9]

TRAIN ONLY:
  normalized target actions [B,8,10]
        |
        v
  posterior tokens:
    CLS [B,1,512]
    qpos token [B,1,512]
    action tokens [B,8,512]
        |
        v
  posterior_encoder [B,10,512]
        |
        v
  mu/logvar [B,32], sample z [B,32]

INFERENCE:
  z = zeros [B,32]

z + qpos + obs_tokens
        |
        v
memory tokens [B,4,512]
        |
        | memory_encoder, 4 layers
        v
memory [B,4,512]
        |
        | learned action queries [B,8,512]
        v
decoder, 7 layers
        |
        v
hidden [B,8,512]
        |
        +-- action_head Linear(512,10) -> normalized actions [B,8,10]
        +-- is_pad_head Linear(512,1)  -> pad logits [B,8]
```

### 2.2 Observation And Qpos Encoding

The policy encodes observations as:

```text
nobs = normalizer.normalize(obs_dict)
flat obs over first To=2 steps -> obs_encoder
obs_tokens = [B,2,137]

qpos = concat latest normalized lowdim keys at step To-1:
  robot0_eef_pos        [3]
  robot0_eef_quat       [4]
  robot0_gripper_qpos   [2]
qpos = [B,9]
```

### 2.3 Posterior Path During Training

Training target:

```text
nactions = normalizer["action"].normalize(batch["action"])  [B,10,10]
start = n_obs_steps - 1 = 1
end = start + n_action_steps = 9
target = nactions[:, 1:9]  [B,8,10]
```

Posterior:

```text
cls             = Embedding(1,512)               -> [B,1,512]
qpos_token      = Linear(9,512)(qpos)            -> [B,1,512]
action_tokens   = Linear(10,512)(target)         -> [B,8,512]
posterior_input = concat(cls, qpos_token, action_tokens)
                = [B,10,512]

posterior_encoder:
  TransformerEncoder, 4 layers, 8 heads, ff=3200

latent_info = Linear(512,64)(posterior_hidden[:,0])
mu, logvar  = split(latent_info) -> [B,32], [B,32]
z           = mu + exp(0.5*logvar) * noise -> [B,32]
```

### 2.4 Decoder Path During Training And Inference

```text
latent_token = Linear(32,512)(z)             -> [B,1,512]
qpos_token   = Linear(9,512)(qpos)           -> [B,1,512]
obs_hidden   = Linear(137,512)(obs_tokens)
             + obs_pos_emb                  -> [B,2,512]

special = concat(latent_token, qpos_token) + special_pos_emb
        = [B,2,512]

memory_input = concat(obs_hidden, special)
             = [B,4,512]

memory = memory_encoder(memory_input)
       = [B,4,512]

queries = query_embed.weight.expand(B, -1, -1)
        = [B,8,512]

hidden = decoder(tgt=queries, memory=memory)
       = [B,8,512]

naction_pred = action_head(hidden)
             = [B,8,10]
```

At inference, `actions=None`, so the posterior is not used:

```text
z = zeros([B,32])
```

The predicted normalized chunk is inserted into a full horizon tensor:

```text
naction_full = zeros [B,10,10]
naction_full[:, 1:9] = naction_pred
action_pred = normalizer["action"].unnormalize(naction_full)
action = action_pred[:, 1:9]  [B,8,10]
```

### 2.5 ACT Loss

```text
l1 = L1(naction_pred, target), masked by is_pad
kl = KL(q(z|qpos, action) || N(0,I))
loss = l1 + kl_weight * kl
kl_weight = 10.0
```

### 2.6 ACT Parameter Counts

Measured on the GPU-node py39 runtime:

```text
official ACT CVAE:
  obs_encoder params: 22.394M
  ACT core params:    72.513M
  full policy:        94.907M

core dimensions:
  hidden_dim=512
  posterior_encoder_layers=4
  memory_encoder_layers=4
  decoder_layers=7
  nheads=8
  dim_feedforward=3200
  latent_dim=32
  qpos_dim=9
```

### 2.7 Deterministic ACT-Style Baseline In This Repo

The repo also has `ActionChunkingTransformerHybridImagePolicy`, used by
`act_square_action8.yaml`. This is not the full CVAE ACT. It is a deterministic
action-chunking Transformer with ACT-size geometry:

```text
obs_tokens [B,16,137]
  -> Linear(137,512) + pos
  -> TransformerEncoder, 4 layers
  -> memory [B,16,512]
  -> action_queries [B,8,512]
  -> TransformerDecoder, 7 layers
  -> LayerNorm + Linear(512,10)
  -> normalized action chunk [B,8,10]
```

Parameter count:

```text
deterministic ACT-style core: 55.116M
full policy with obs_encoder: 77.510M
```

## 3. PTP / Diffusion Transformer Policy

### 3.1 Overview

The PTP / DP path uses `DiffusionTransformerHybridImagePolicy` plus
`TransformerForDiffusion`. It does not directly output actions in one forward
pass. Instead, the transformer predicts the diffusion target, usually epsilon
noise, and the scheduler iteratively denoises an action sequence.

Current corrected Stage2b Square action8 base:

```text
To = 16
T  = policy horizon = 8
K  = n_action_steps = 8
Da = 10
Do = 137
D  = 256 in default base, 512 in ACT-size base
T_cond = 1 time token + 16 obs tokens = 17
pred_action_steps_only = true
causal_cond_attn = false
```

String diagram:

```text
raw obs history [B,16,...]
        |
        | normalize obs
        v
robomimic obs_encoder
        |
        v
cond obs tokens [B,16,137]
        |
        | Linear 137 -> D
        v
cond obs embeddings [B,16,D]

diffusion timestep t
        |
        | sinusoidal time embedding
        v
time token [B,1,D]

condition tokens:
  concat(time token, cond obs embeddings)
        |
        v
cond [B,17,D]
        |
        | cond encoder
        |   n_cond_layers=0: token-wise MLP D->4D->D
        |   ACT-size: n_cond_layers=4 TransformerEncoder layers
        v
memory [B,17,D]

noisy action sample x_t [B,8,10]
        |
        | Linear 10 -> D, add pos
        v
action tokens [B,8,D]
        |
        | TransformerDecoder, cross-attend to memory
        v
hidden [B,8,D]
        |
        | LayerNorm + Linear D->10
        v
predicted epsilon / target [B,8,10]
        |
        | DDPM scheduler step repeated 100 times
        v
denoised normalized action chunk [B,8,10]
        |
        | unnormalize
        v
environment action chunk [B,8,10]
```

### 3.2 Training Target In Current Action8 Path

The dataset returns:

```text
batch["action"] [B,24,10]
```

For `pred_action_steps_only=true`, training selects:

```text
start = n_obs_steps - 1 = 15
end = start + n_action_steps = 23
trajectory = normalized_action[:, 15:23]
           = [B,8,10]
```

Then:

```text
noise      = randn_like(trajectory)
timesteps  = randint(0, 100, [B])
x_t        = scheduler.add_noise(trajectory, noise, timesteps)
pred       = model(x_t, timesteps, cond)
target     = noise  # because prediction_type=epsilon
loss       = MSE(pred, target)
```

The action-producing model forward predicts epsilon, not action. The final
action comes from the scheduler after iterative denoising.

### 3.3 Inference / Rollout Sampling

`predict_action` computes condition tokens from current obs history, then:

```text
trajectory = random Gaussian [B,8,10]

for each diffusion step t:
  trajectory[condition_mask] = condition_data[condition_mask]
  pred_epsilon = TransformerForDiffusion(trajectory, t, cond)
  trajectory = scheduler.step(pred_epsilon, t, trajectory).prev_sample

naction_pred = trajectory[..., :10]
action_pred = normalizer["action"].unnormalize(naction_pred)
action = action_pred  # because pred_action_steps_only=true
```

For non-action-only full-horizon mode, the code would instead sample
`[B,T,10]` and return:

```text
action = action_pred[:, To-1 : To-1+n_action_steps]
```

### 3.4 Full PTP-Style Past-Token Prediction Versus Current Action8 Base

The same policy class supports the PTP-style objective:

```text
past_action_pred=true
pred_action_steps_only=false
```

In that mode, the loss is not sliced down to only future actions; it can train
on a longer action sequence including past tokens. This is the "past-token
prediction" idea: the model learns past/future action dependency rather than
only predicting the immediate future chunk.

The corrected Stage2b action8 base used in current Direction C is a long-history
diffusion transformer baseline:

```text
cond obs history = 16
predicted action chunk = 8
pred_action_steps_only = true
```

So it is PTP/DP-architecture-compatible, but the checked action8 base is not the
full past+future PTP loss unless the config sets the full PTP mode above.

### 3.5 PTP / Diffusion Transformer Parameters

Measured on the GPU-node py39 runtime:

```text
d256 current Stage2b action8 base:
  D=256, heads=4, decoder_layers=8, cond_encoder_layers=0
  T=8, T_cond=17
  transformer core: 9.001M
  obs_encoder:       22.394M
  full policy:       31.395M

ACT-size diffusion transformer base:
  D=512, heads=8, decoder_layers=7, cond_encoder_layers=4
  T=8, T_cond=17
  transformer core: 42.133M
  obs_encoder:       22.394M
  full policy:       64.527M
```

Key module dimensions for d256 action8:

```text
input_emb:    Linear(10, 256)
cond_obs_emb: Linear(137, 256)
cond tokens:  [B,17,256]
action tokens:[B,8,256]
head:         LayerNorm(256) + Linear(256,10)
```

## 4. Side-By-Side Difference

```text
Translator:
  one forward pass
  obs history -> action-query decoder -> sketch actions
  action output is direct regression [B,24,10]
  used mainly for representation/context pretraining

Official ACT:
  one forward pass at inference
  obs + qpos + latent-zero -> memory -> action-query decoder
  action output is direct regression [B,8,10]
  training uses CVAE posterior and KL

PTP / Diffusion Transformer:
  iterative denoising
  obs history -> condition tokens
  noisy action sequence -> decoder predicts epsilon
  scheduler converts noise to action over 100 steps
  action output appears after denoising and unnormalization
```

## 5. Practical Interpretation

1. Translator and ACT both produce actions directly from decoder hidden states.
2. PTP produces a denoising prediction; the scheduler is part of action
   generation.
3. Translator Stage 1 has a supervised sketch-action head, but the pooled
   `context` used downstream is only indirectly shaped by that loss.
4. ACT has the largest core among current candidates because it includes both
   posterior and policy-side encoders/decoders.
5. Current d256 PTP core is much smaller than ACT; ACT-size PTP narrows the
   capacity gap but is still a diffusion policy, not a CVAE action decoder.
