# Direction C GPU Environment Migration Summary

Date: 2026-06-05

Scope: summarize the two currently reachable GPU nodes and the shared Ceph runtime used by Direction C / BehaviorTranslator experiments, so the work can be moved to a new GPU node and the current nodes can be released.

## Current GPU Nodes

| Node | SSH | Hostname | GPU | Current state | Mounts checked |
|---|---:|---|---|---|---|
| `10.100.0.20` | `26715` | `lg-cmc-b7r201-a08u06-h200-000019` | `8 x NVIDIA H200` | idle, all GPUs about `1 MiB`, `0%` util, no compute apps | `/mnt/cephfs`, `/mnt/3fs1` |
| `10.100.2.39` | `23494` | `lg-cmc-b7r201-e03u26-h200-000102` | `8 x NVIDIA H200` | idle, all GPUs about `1 MiB`, `0%` util, no compute apps | `/mnt/cephfs`, `/mnt/3fs1` |

Snapshot time: 2026-06-05 04:03 UTC.

Both nodes are clean from our Direction C processes after stopping the ACT-size Stage1 translator on `10.100.0.20:26715` in Session 95.

## Shared Runtime

Main venv:

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph
```

Verified package versions on both current GPU nodes:

| Package | Version |
|---|---|
| Python | `3.9.25` |
| torch | `2.5.1+cu124` |
| torch CUDA | `12.4` |
| robomimic | `0.2.0` |
| robosuite | `1.2.0` |
| hydra-core | `1.2.0` |
| diffusers | `0.11.1` |
| numpy | `1.23.5` |
| h5py | `3.7.0` |
| av | `14.2.0` |

This is the main environment for all trusted PTP-data Direction C runs. Do not use the local system Python 3.12 shell or any py310 / robomimic 0.4 environment for these runs unless explicitly labeling it as a version ablation.

Preflight command on a new GPU node:

```bash
REPO=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/repos/ldp
VENV=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph
cd "$REPO"
"$VENV/bin/python" diffusion_policy/scripts/check_main_runtime_env.py --require-cuda
```

Expected: Python 3.9, `robomimic==0.2.0`, CUDA available.

## Node-Level Requirements

The Ceph venv uses the node-level Python 3.9 binary. A fresh Ubuntu 24.04 GPU node may need these packages before the venv works:

```bash
apt-get install -y \
  python3.9 python3.9-venv python3.9-dev python3.9-distutils \
  build-essential patchelf pkg-config \
  libosmesa6-dev libglfw3-dev libglew-dev \
  libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev \
  ffmpeg libavformat-dev libavcodec-dev libavdevice-dev \
  libavutil-dev libavfilter-dev libswscale-dev libswresample-dev
```

GPU-node pip config currently points at the internal mirror:

```text
index-url = http://10.100.197.13/simple/
trusted-host = 10.100.197.13
timeout = 120
no-cache-dir = true
```

For explicit installs, prefer:

```bash
"$VENV/bin/pip" install <package> \
  --index-url http://10.100.197.13/simple/ \
  --trusted-host 10.100.197.13
```

## Code Source

Authoritative git worktree:

```bash
/work-agents/intern_ldp_explorer/ldp
branch: intern_ldp_explorer/task002_flow_matching_square_toolhang
```

Ceph execution copy:

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/repos/ldp
```

Important caveat: the Ceph execution copy currently has no `.git` directory. It is usable for running experiments, but it is not the authoritative source for branch, commit, or history. For a new GPU migration, refresh or sync this copy from the authoritative local branch before launching new experiments.

## Data

Confirmed Square dataset on Ceph:

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/datasets/robomimic/datasets/square/mh/image_abs.hdf5
```

Size checked on both nodes: about `6.5G`.

Current caveat: ToolHang was not confirmed under the Ceph Direction C dataset root during this migration check. ToolHang experiments need the dataset restored or copied before launch.

## Main Output Roots

Direction C root:

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator
```

Important output roots to preserve:

```bash
# ACT-size Stage1 translator, stopped near the end of the 1000-epoch run.
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/behavior_translator_square_past_actsize_norm_20260530_061543

# Official-ACT-compatible Square smoke baseline.
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/official_act_square_action8/20260601_1208_official_act_square_action8_fixed_rollout25

# Modality-ablation diagnostics for proprio/image shortcut.
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage1_square_modality_ablation_20260601

# Corrected non-ACT-size Stage2b rollout evaluation.
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_rollout_eval_newnode_20260527

# ACT-size downstream offline-validation runs.
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_actsize
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_actsize_norm_current
```

## Key Configs

Stage1 ACT-size normalized past translator:

```bash
experiment_configs/square/behavior_translator_square_past_actsize_norm.yaml
```

Key settings:

- `d_model=512`
- `n_encoder_layers=4`
- `n_decoder_layers=7`
- `n_heads=8`
- `ff_dim=3200`
- `context_dim=512`
- `batch_size=64`
- `num_workers=16`
- `obs_encoder_lr=5e-5`
- `translator_lr=5e-5`
- `action_loss_reduction=sum_action_dim`
- `loss_scale=10.0`
- `checkpoint_every=50`

Official-ACT-compatible Square action8:

```bash
experiment_configs/square/official_act_square_action8.yaml
```

Key settings:

- `global_obs=2`
- `global_action=8`
- `hidden_dim=512`
- `enc_layers=4`
- `dec_layers=7`
- `nheads=8`
- `dim_feedforward=3200`
- `latent_dim=32`
- `kl_weight=10.0`
- `lr=1e-5`
- `batch_size=32`
- `num_workers=16`
- `num_epochs=100`
- `rollout_every=25`

ACT-size downstream base:

```bash
experiment_configs/square/transformer_square_action8_causalcond_off_base_actsize.yaml
```

Key settings:

- `n_emb=512`
- `n_head=8`
- `n_layer=7`
- `n_cond_layers=4`
- `lr=5e-5`
- output root: `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_actsize`

ACT-size downstream translator context:

```bash
experiment_configs/square/transformer_square_translator_context_action8_causalcond_off_add_last_actsize_norm.yaml
```

Key settings:

- same ACT-size downstream transformer geometry as base
- frozen translator checkpoint:

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage1_square_past_ceph_20260526_032417_safe_workers/stage1_past_bs128_obs1e4_tr1e4/checkpoints/best.ckpt
```

- `translator_context_norm=true`
- `context_injection=add_last`
- `context_projector_zero_init=true`
- `lr=5e-5`

## Rollout / Eval Environment Notes

For reward-only robomimic rollout checks on current Ceph py39 nodes, the known working exports are:

```bash
export MUJOCO_GL=osmesa
export PYOPENGL_PLATFORM=osmesa
export MUJOCO_PY_FORCE_CPU=1
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
export PYTHONPATH=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/repos/ldp:$PYTHONPATH
```

Use score-only rollout/eval when possible:

```bash
diffusion_policy/scripts/eval_flow_matching_rollout.py
```

Avoid video path as the default smoke test, because previous `gather_rollouts.py` video encoding hit PyAV h264 profile issues with `av==14.2.0`.

## Migration Checklist

1. Confirm the new node has `/mnt/cephfs` mounted.
2. Confirm `/usr/bin/python3.9` exists on the new node. Install node-level packages if it does not.
3. Confirm the main venv runs:

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph/bin/python --version
```

4. Refresh the Ceph execution repo from the authoritative local git branch if code changes are needed.
5. Run the runtime preflight:

```bash
REPO=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/repos/ldp
VENV=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph
cd "$REPO"
"$VENV/bin/python" diffusion_policy/scripts/check_main_runtime_env.py --require-cuda
```

6. Check Square dataset exists before launch:

```bash
ls -lh /mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/datasets/robomimic/datasets/square/mh/image_abs.hdf5
```

7. Parse the intended Hydra config before a long run:

```bash
"$VENV/bin/python" train.py \
  --config-dir=experiment_configs/square \
  --config-name=behavior_translator_square_past_actsize_norm \
  --cfg job
```

8. After migration, the two current nodes can be released if no new process has been started.
