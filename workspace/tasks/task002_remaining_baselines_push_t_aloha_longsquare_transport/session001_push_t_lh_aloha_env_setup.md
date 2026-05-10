# Session 001 - Push-T / LH-ALOHA PTP Environment Setup

## Servers

| Host | SSH | Hostname | GPU | Local Disk | Shared Disk |
|---|---:|---|---|---:|---:|
| `10.100.2.35` | `33486` | `lg-cmc-b7r201-e02u16-h200-000098` | `2 x NVIDIA H200`, `143771 MiB` each | `/` about `212T` free | `/mnt/3fs2` about `53T` free |
| `10.100.16.46` | `36566` | `lg-cmc-b7r202-h08u16-h200-000548` | `2 x NVIDIA H200`, `143771 MiB` each | `/` about `13T` free | `/mnt/3fs2` about `53T` free |

At setup completion both nodes showed idle GPUs: `1 MiB / 143771 MiB`, `0%` utilization on each card.

## Installed Environment

- Venv: `/root/ptp_ldp_py39`
- Repo: `/mnt/3fs2/data/tingwen.du/workspace/ldp`
- Branch: `intern_ldp_explorer/task001_ptp_py39_rerun`
- Commit: `529857fa8bab663510d88c5c7b72b973f4c37104`
- MuJoCo binary: `/root/.mujoco/mujoco210`
- Internal pip index: `http://10.100.197.13/simple/`

Critical runtime exports:

```bash
export MUJOCO_PY_MUJOCO_PATH=/root/.mujoco/mujoco210
export LD_LIBRARY_PATH=/root/.mujoco/mujoco210/bin:${LD_LIBRARY_PATH:-}
export MUJOCO_GL=egl
export PYTHONPATH=/mnt/3fs2/data/tingwen.du/workspace/ldp:${PYTHONPATH:-}
```

Critical package pins:

| Package | Version |
|---|---:|
| Python | `3.9.25` |
| torch | `2.5.1` |
| torchvision | `0.20.1` |
| robomimic | `0.2.0` |
| robosuite | `1.2.0` |
| mujoco-py | `2.1.2.14` |
| mujoco | `2.3.7` |
| dm-control | `1.0.9` |
| gym | `0.21.0` |
| diffusers | `0.11.1` |
| huggingface-hub | `0.10.1` |
| numpy | `1.23.3` |
| Cython | `0.29.32` |
| setuptools | `65.5.0` |
| wandb | `0.13.3` |
| pygame | `2.1.2` |
| pymunk | `6.2.1` |
| shapely | `1.8.4` |

## Setup Requirements

System packages used:

```bash
apt-get update
apt-get install -y \
  python3.9 python3.9-venv python3.9-dev python3.9-distutils \
  build-essential patchelf pkg-config cmake ninja-build ffmpeg \
  libosmesa6 libosmesa6-dev libglfw3 libglfw3-dev libglew-dev \
  libgl1 libgl1-mesa-dev libegl1 libegl1-mesa-dev \
  libxrender1 libsm6 libxext6 libx11-6
```

Important install details:

- Use internal pip mirror because external PyPI timed out from the GPU nodes.
- Install `robosuite==1.2.0` with `--no-deps`; its metadata asks for `mujoco-py==2.0.2.9`, which expects MuJoCo 2.0 and is wrong for this H200 PTP stack.
- Keep `mujoco-py==2.1.2.14`, `Cython==0.29.32`, and `numpy==1.23.3` together; Cython 3 breaks `mujoco-py` compilation.
- Keep `setuptools==65.5.0`; `wandb==0.13.3` imports `pkg_resources`, which is missing after the setuptools 82 upgrade path.
- Copy the pure-Python PyTorch3D stub from `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/pytorch3d_src` into `/root/ptp_ldp_py39/lib/python3.9/site-packages/pytorch3d`.
- After copying the stub, set `/root/ptp_ldp_py39/lib/python3.9/site-packages/pytorch3d/transforms/__init__.py` to:

```python
from .rotation_conversions import *
```

## Smoke Results

Both nodes passed the same smoke suite.

Shared checks:

- `torch.cuda.is_available()` returned `True`.
- `torch.cuda.device_count()` returned `2`.
- `import mujoco_py` passed.
- `import pytorch3d.transforms` passed with `matrix_to_quaternion` and `rotation_6d_to_matrix` available.
- `import diffusion_policy.env_runner.pusht_image_runner` passed.
- `import diffusion_policy.env_runner.aloha_image_runner` passed.

Push-T data check:

- Dataset: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/pusht/pusht_cchi_v7_replay.zarr`
- Keys: `action`, `img`, `keypoint`, `n_contacts`, `state`
- Shapes: `img=(25650,96,96,3)`, `action=(25650,2)`, `episode_ends=(206,)`
- Horizon-32 dataset sample: image `(32,3,96,96)`, agent position `(32,2)`, action `(32,2)`

LH-ALOHA data and env check:

- Dataset: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/aloha_twomodes_single/demos.hdf5`
- Demos: `50`
- First demo action shape: `(500,7)`
- Obs keys: `embedding`, `env_state`, `qpos`, `qvel`, `right_wrist`, `top`
- First demo embedding shape: `(500,135)`
- Env: `make_sim_env("sim_singlearm_pickandplace_twomodes_scripted")`
- Reset observation: `qpos=(7,)`, top camera `(84,84,3) uint8`

## Logs

- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session135_setup_ptp_py39_push_t_aloha_10.100.2.35.log`
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session135_setup_ptp_py39_push_t_aloha_10.100.16.46.log`
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session135_repair2_ptp_py39_push_t_aloha_10.100.2.35.log`
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session135_repair2_ptp_py39_push_t_aloha_10.100.16.46.log`
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session135_repair3_setuptools_smoke_10.100.2.35.log`
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session135_repair3_setuptools_smoke_10.100.16.46.log`
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session135_repair4_pytorch3d_task_smoke_10.100.2.35.log`
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session135_repair4_pytorch3d_task_smoke_10.100.16.46.log`

## Launch Skeleton

Use this before smoke, training, or rollout:

```bash
ssh -p <port> root@<host>
source /root/ptp_ldp_py39/bin/activate
export MUJOCO_PY_MUJOCO_PATH=/root/.mujoco/mujoco210
export LD_LIBRARY_PATH=/root/.mujoco/mujoco210/bin:${LD_LIBRARY_PATH:-}
export MUJOCO_GL=egl
export PYTHONPATH=/mnt/3fs2/data/tingwen.du/workspace/ldp:${PYTHONPATH:-}
cd /mnt/3fs2/data/tingwen.du/workspace/ldp
```

## Caveats

- This is an H200-adapted PTP-style stack, not an exact upstream conda replica; torch is newer for H200 compatibility.
- LH-ALOHA has a known task001 caveat: `aloha_twomodes_single/demos.hdf5` contains embeddings and passed structural smoke, but prior consistency checks found the released `aloha_encoder.ckpt` expected a 14D qpos setup while this dataset is 7D. Treat this as a training/evaluation design issue, not an environment-import issue.
- The PyTorch3D component is a local transforms-only stub sufficient for `RotationTransformer`; it is not a full PyTorch3D install.
