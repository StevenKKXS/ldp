# To Be Improved

This document tracks problems and improvement directions for Direction C / behavior translator / long-context policy experiments.

Last updated: 2026-06-06

## 1. Current Translator Injection Does Not Improve Diffusion Policy

### Confirmed Observation

The current behavior translator path does not improve downstream Square rollout success rate when injected into the diffusion / transformer policy as the current pooled projection context.

Most recent 300-episode Square stability eval:

| Setting | Episodes | Success Rate |
| --- | ---: | ---: |
| `base_e49` | 300 | `166/300 = 55.33%` |
| `random_add_last_e24` | 300 | `164/300 = 54.67%` |
| `pretrained_add_last_e24` | 300 | `135/300 = 45.00%` |

Earlier 50-episode corrected Stage2b eval also pointed in the same direction:

| Setting | Episodes | Success Rate |
| --- | ---: | ---: |
| base e24 EMA | 50 | `22/50 = 44%` |
| random context e24 EMA | 50 | `21/50 = 42%` |
| random context e49 EMA | 50 | `26/50 = 52%` |
| pretrained add_last e24 EMA | 50 | `15/50 = 30%` |
| pretrained add_all e24 EMA | 50 | `18/50 = 36%` |

### Likely Sub-Problems

- The Stage1 translator objective supervises sketch action prediction, but the pooled `context_projector` used by downstream `get_context()` is not directly supervised by a downstream-aligned representation loss.
- The strongest Stage1 signal is `past` action reconstruction, but this can be solved largely through lowdim/proprio state trajectories instead of image/object understanding.
- The current `add_last` / `add_all` projection injection may be the wrong interface for diffusion conditioning. It may perturb the base condition rather than provide useful behavior context.
- Offline reconstruction loss is not a reliable selector for rollout success. Some checkpoints with better validation loss still produce worse SR.
- Random frozen context is not worse than base in the current protocol, so parameter count / regularization / injection noise can confound interpretation.

### Improvement Ideas

- Stop treating current pooled/projection `add_last` as the main positive path.
- Test translator hidden states through a more faithful interface:
  - encoder replacement;
  - token-level context injection;
  - cross-attention over `h_action` / `z_obs` tokens;
  - direct downstream supervision on the exported context.
- Keep random same-architecture controls in every downstream experiment.
- Add source-free modality diagnostics as standard checks:
  - full input;
  - lowdim-only;
  - image-only;
  - image masked / shuffled;
  - proprio masked / shuffled.
- If translator pretraining continues, prefer objectives that force image/object grounding rather than only reconstructing past action from proprio history.

## 2. Long-Context Training Cost Is Too High

### Confirmed Observation

Long-context policy training is much slower than short-context DP-style runs. The cost increases in both PTP-like code and our current long-context translator / diffusion experiments, especially without cached visual features.

### Likely Sub-Problems

- Raw image observations are encoded repeatedly for many history frames.
- Long observation windows multiply encoder cost before the diffusion / transformer head even runs.
- Larger temporal windows increase memory pressure and reduce batch size.
- The current training loop often uses conservative batch size / worker settings because image loading, Robomimic env, and Ceph/NFS/3FS availability have varied across nodes.
- Rollout itself is CPU/MuJoCo-heavy; too many vector envs can overload CPU, while too few underuse H200 GPUs.

### Improvement Ideas

- Separate "research signal" experiments from "fully trainable encoder" experiments:
  - use cached visual embeddings for fast ablations when the encoder is frozen;
  - use raw images only for the final end-to-end confirmation.
- Benchmark and record speed in a standard table:
  - samples/epoch;
  - steps/epoch;
  - seconds/epoch;
  - GPU util;
  - CPU idle/load;
  - dataloader worker count;
  - batch size.
- Test cheaper long-context formats:
  - current image frames plus lowdim history;
  - sparse/keyframe image history;
  - pooled temporal image features;
  - sliding cache for repeated image embeddings.
- Keep rollout concurrency adaptive:
  - `n_envs=8` per eval worked on `10.100.2.39`;
  - 8 concurrent evals gave a 64-env cap and acceptable CPU pressure on a 192-core node;
  - avoid 8 concurrent evals with `n_envs=20`, which creates about 160 active envs.
- For training, retest batch size / learning rate jointly instead of only changing one:
  - larger batch may improve throughput;
  - LR should be scaled or swept after batch-size changes.

## 3. Codebase Choice Is Still Open

### Question

We need decide whether future long-context / translator work should continue in the current PTP/LDP-derived codebase, move to Gated Memory Policy, or move toward a latent-planner / LDP-style codebase.

### Option A: Continue In Current PTP/LDP-Derived Codebase

Pros:

- Already integrated with our Square Robomimic py39 / `robomimic==0.2.0` environment.
- Existing rollout evaluator, configs, checkpoints, and reports are reproducible here.
- Best for comparing against our current PTP/DP reproduction records.

Cons:

- Long-context raw-image training is slow.
- The current code has accumulated many experiment-specific patches.
- Some features needed for fast research loops, especially cached visual features and clean token-level condition injection, are not yet first-class.

Best use:

- Continue here for controlled comparisons that must match current PTP/DP reproduction settings.

### Option B: Explore Gated Memory Policy Codebase

Pros:

- It is directly relevant to long-context memory and may contain cleaner memory-policy interfaces.
- It may offer a better reference implementation for long-context conditioning than our current pooled translator context.

Cons:

- Environment and Robomimic version alignment must be checked carefully before trusting comparisons.
- Released checkpoints/configs may not map cleanly to our current py39 / `robomimic==0.2.0` evaluation stack.
- Porting our translator idea there may add a new source of implementation variance.

Best use:

- Use as a reference / sanity-check codebase, especially for memory injection interfaces and released-checkpoint evaluation, before migrating the main experiment.

### Option C: Move Toward Latent Planner / LDP-Style Codebase

Pros:

- A latent planner may be a better conceptual fit if the goal is high-level behavior context rather than directly injecting a pooled translator vector into diffusion.
- Could separate long-horizon intent from short-horizon action generation more cleanly.

Cons:

- This changes the research question more substantially.
- Comparisons against PTP/DP become less direct unless we keep a strict bridge protocol.
- Requires more setup before getting a fair SR metric.

Best use:

- Consider after we define the exact interface between long-context history, latent intent, and short-horizon action generation.

## 4. Proposed Decision Criteria

Before choosing the next major implementation path, require each candidate to answer:

1. Does it preserve a fair Square/ToolHang rollout comparison under py39 + `robomimic==0.2.0`?
2. Can it run a useful ablation within one GPU allocation, not only a multi-day end-to-end train?
3. Does it avoid the current proprio shortcut, or at least expose it through clean diagnostics?
4. Does it provide a better interface than pooled `add_last` context?
5. Can we keep random same-architecture controls cheap enough to run every time?

## 5. Current Working Recommendation

The current evidence supports this working direction:

- Treat the v0 pooled/projection translator context as a negative result.
- Keep the current codebase for fair reproduction-controlled comparisons.
- Use Gated Memory Policy as a reference for memory/injection interface design, not as an immediate full migration.
- Prototype the next translator variant as encoder replacement or token-level context injection, with modality diagnostics and random controls built in from the start.
- In parallel, build speed benchmarks and cached-feature ablations so long-context experiments can iterate faster before full raw-image confirmation.
