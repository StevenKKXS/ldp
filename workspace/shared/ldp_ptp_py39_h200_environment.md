# LDP PTP Python 3.9 Environment On H200

This note records a reusable PTP-style environment for `long-context-dp/ldp` on H200 GPU machines. It is intended for interns who need a closer upstream-version environment than the Python 3.12 / RoboMimic 0.3 compatibility stack.

## Mandatory Rule For PTP-Data Runs

For PTP reproduction, PTP encoder pretraining, downstream PTP/DP comparison on the PTP-preprocessed RoboMimic datasets, and rollout evaluation meant to compare with PTP claims, use a Python 3.9 environment with `robomimic==0.2.0`.

Do not use `gmp-py310` / `robomimic 0.4.0` for trusted PTP-data training or rollout unless the run is explicitly labeled as a version-ablation. Results produced under `robomimic 0.4.0` are version-confounded for this project.

Session 13 check on `2026-05-19T11:52:47Z`:

- Current FM GPU node `10.100.2.35:33805` does not have `/root/ptp_ldp_py39/bin/python`.
- The older recorded host `10.100.0.29:36645` refused SSH connection and should not be treated as available.
- No ready py39 / `robomimic==0.2.0` NFS environment was found under `/mnt/nfs/tingwen/ldp/envs`; before any new trusted run on the current GPU node, recreate or sync this environment from the CPU/common side and verify `robomimic.__version__ == "0.2.0"`.

Session 14 current NFS environment on `2026-05-19`:

- Env path: `/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020`
- Verified GPU node: `10.100.2.35:33805`
- Python: `3.9.23`
- RoboMimic: `0.2.0`
- RoboSuite: `1.2.0`, pinned `cheng-chi/robosuite@277ab9588ad7a4f4b55cf75508b44aa67ec171f0`
- Torch: `2.5.1`
- Gym: `0.21.0`
- MuJoCo runtime: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runtimes/mujoco210`

Activation on GPU nodes with `/mnt/nfs` and `/mnt/3fs2` mounted:

```bash
ENV=/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020
MUJOCO210=/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runtimes/mujoco210
source "$ENV/bin/activate"
export MUJOCO_PY_MUJOCO_PATH="$MUJOCO210"
export LD_LIBRARY_PATH="$MUJOCO210/bin:$ENV/lib:${LD_LIBRARY_PATH:-}"
export MUJOCO_GL=egl
export PYOPENGL_PLATFORM=egl
```

## Ready-To-Use Environment

Previously verified host:

- SSH target: `10.100.0.29`
- SSH port: `36645`
- venv path: `/root/ptp_ldp_py39`
- training checkout: `/mnt/3fs2/data/tingwen.du/workspace/ldp`
- training checkout branch: `intern_ldp_explorer/task001_ptp_py39_rerun`
- pushed training-code branch: `origin/intern_ldp_explorer/task001_ptp_py39_rerun`
- training-code commit: `529857fa8bab663510d88c5c7b72b973f4c37104`

Activation:

```bash
ssh -p 36645 root@10.100.0.29
cd /mnt/3fs2/data/tingwen.du/workspace/ldp
source /root/ptp_ldp_py39/bin/activate
export PYTHONPATH=/mnt/3fs2/data/tingwen.du/workspace/ldp:${PYTHONPATH:-}
```

The venv activation file also exports:

```bash
export MUJOCO_PY_MUJOCO_PATH=/root/.mujoco/mujoco210
export LD_LIBRARY_PATH=/root/.mujoco/mujoco210/bin:${LD_LIBRARY_PATH:-}
export MUJOCO_GL=${MUJOCO_GL:-egl}
```

## Core Versions

Verified package stack:

| Component | Version / Source |
|---|---|
| Python | `3.9.25` |
| Torch | `2.5.1` |
| TorchVision | `0.20.1` |
| CUDA used by torch | `12.4` stack |
| RoboMimic | `0.2.0` |
| RoboSuite | `cheng-chi/robosuite@277ab9588ad7a4f4b55cf75508b44aa67ec171f0`, source version `1.2.0` |
| MuJoCo binary for `mujoco-py` | `2.1.0` at `/root/.mujoco/mujoco210` |
| `mujoco-py` | `2.1.2.14` |
| `mujoco` | `2.3.7` |
| `dm-control` | `1.0.9` |
| `diffusers` | `0.11.1` |
| `huggingface-hub` | `0.10.1` |
| `gym` | `0.21.0` |
| `av` | `15.1.0` |
| `imagecodecs` | `2022.9.26` |

This is an H200-adapted PTP-style environment, not a byte-for-byte copy of upstream `conda_environment.yaml`:

- Torch is upgraded from the upstream-era `1.12.1/cu116` expectation to `2.5.1/cu124` for H200 compatibility.
- `av` is upgraded from `10.0.0` to `15.1.0` because Ubuntu 24.04 FFmpeg 6 headers do not build `av 10.0.0` cleanly.
- A lightweight local `pytorch3d` transforms/common stub is installed because the configured pip mirrors did not provide a usable `pytorch3d` wheel.

## Why This Environment Exists

The earlier H200 compatibility setup used:

- Python `3.12`
- RoboMimic `0.3.0`
- RoboSuite `1.4.1`
- MuJoCo `3.8.0`
- Diffusers `0.30.0`

That stack was useful operationally, but it is not the version family implied by the LDP / PTP repository pins. For reproducing Tool-Hang and Transport behavior, the version mismatch is a real confound. This Python 3.9 venv brings RoboMimic and RoboSuite closer to the repository-pinned environment while keeping Torch usable on H200.

## Recreate Procedure

Use the ready venv when possible. To recreate it on a similar H200 container:

1. Install system packages:

```bash
apt-get update
apt-get install -y \
  python3.9 python3.9-venv python3.9-dev python3.9-distutils \
  build-essential patchelf pkg-config \
  libosmesa6-dev libglfw3-dev libglew-dev libgl1-mesa-dev \
  libegl1-mesa-dev libgles2-mesa-dev \
  ffmpeg libavformat-dev libavcodec-dev libavdevice-dev \
  libavutil-dev libavfilter-dev libswscale-dev libswresample-dev
```

2. Create the venv:

```bash
python3.9 -m venv /root/ptp_ldp_py39
source /root/ptp_ldp_py39/bin/activate
python -m pip install pip==22.2.2 setuptools==65.5.0 wheel==0.38.4
```

3. Install MuJoCo 2.1.0:

```bash
mkdir -p /root/.mujoco
tar -xzf /root/mujoco210-linux-x86_64.tar.gz -C /root/.mujoco
```

Expected result:

```bash
/root/.mujoco/mujoco210
```

4. Add activation exports:

```bash
cat >> /root/ptp_ldp_py39/bin/activate <<'EOF'
export MUJOCO_PY_MUJOCO_PATH=/root/.mujoco/mujoco210
export LD_LIBRARY_PATH=/root/.mujoco/mujoco210/bin:${LD_LIBRARY_PATH:-}
export MUJOCO_GL=${MUJOCO_GL:-egl}
EOF
```

5. Install Python dependencies. The exact installed environment was built from the repository dependency pins plus H200 adaptations. Critical pins:

```bash
python -m pip install numpy==1.23.3 cython==0.29.32
python -m pip install torch==2.5.1 torchvision==0.20.1
python -m pip install \
  numba==0.56.4 scipy==1.9.1 opencv-python==4.6.0.66 \
  zarr==2.12.0 numcodecs==0.10.2 h5py==3.7.0 hydra-core==1.2.0 \
  einops==0.4.1 tqdm==4.64.1 dill==0.3.5.1 \
  scikit-video==1.1.11 scikit-image==0.19.3 gym==0.21.0 \
  pymunk==6.2.1 wandb==0.13.3 threadpoolctl==3.1.0 \
  shapely==1.8.4 imageio==2.22.0 imageio-ffmpeg==0.4.7 \
  termcolor==2.0.1 tensorboard==2.10.1 tensorboardx==2.5.1 \
  psutil==5.9.2 click==8.0.4 boto3==1.24.96 \
  accelerate==0.13.2 datasets==2.6.1 diffusers==0.11.1 \
  huggingface-hub==0.10.1 pygame==2.1.2 robomimic==0.2.0 \
  mujoco==2.3.7 mujoco-py==2.1.2.14 dm-control==1.0.9 \
  matplotlib==3.6.1 imagecodecs==2022.9.26 av==15.1.0
```

6. Install pinned RoboSuite source. PyPI `robosuite==1.2.0` is not sufficient for this project because it did not register `ToolHang` or `TwoArmTransport` in testing. Use the pinned `cheng-chi` source tarball:

```bash
python -m pip install --force-reinstall --no-deps \
  /root/robosuite-277ab9588ad7a4f4b55cf75508b44aa67ec171f0.tar.gz
```

7. Install the LDP repo editable:

```bash
cd /mnt/3fs2/data/tingwen.du/workspace/ldp
python -m pip install -e .
```

8. Ensure a `pytorch3d` transforms/common implementation is available. The verified venv copied the local lightweight stub from:

```bash
/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/pytorch3d_src
```

into:

```bash
/root/ptp_ldp_py39/lib/python3.9/site-packages/pytorch3d
```

## Smoke Tests

Run from the training checkout:

```bash
cd /mnt/3fs2/data/tingwen.du/workspace/ldp
source /root/ptp_ldp_py39/bin/activate
export PYTHONPATH=/mnt/3fs2/data/tingwen.du/workspace/ldp:${PYTHONPATH:-}
python - <<'PY'
import importlib.metadata as md
mods = [
    "diffusion_policy.env_runner.robomimic_image_runner",
    "diffusion_policy.env_runner.robomimic_longhist_image_runner",
    "diffusion_policy.dataset.robomimic_replay_image_dataset",
    "diffusion_policy.policy.diffusion_transformer_hybrid_image_policy",
]
for m in mods:
    mod = __import__(m, fromlist=["*"])
    print("IMPORT_OK", m, getattr(mod, "__file__", None))

import robosuite
from robosuite.environments.base import REGISTERED_ENVS
print("robosuite", robosuite.__version__)
print("ToolHang", "ToolHang" in REGISTERED_ENVS)
print("TwoArmTransport", "TwoArmTransport" in REGISTERED_ENVS)
for pkg in ["torch", "robomimic", "mujoco", "mujoco-py", "diffusers", "gym"]:
    print(pkg, md.version(pkg))
PY
```

Verified output includes:

```text
ToolHang True
TwoArmTransport True
torch 2.5.1
robomimic 0.2.0
mujoco 2.3.7
mujoco-py 2.1.2.14
diffusers 0.11.1
gym 0.21.0
```

Additional smoke already passed on `10.100.0.29:36645`:

- Square env reset
- Tool-Hang env reset
- Transport env reset
- `reset_to({"states": state})`
- `reset_to({"model": model_file, "states": state})`
- tiny mp4 write/read test at `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/debug/session107_ptp_py39_smoke_video.mp4`

## Known Caveats

- `pip check` reports RoboSuite metadata wants `free-mujoco-py` and `numba<=0.53.1`.
- `free-mujoco-py` was unavailable from configured mirrors, so this venv uses repository-pinned `mujoco-py==2.1.2.14` plus MuJoCo 2.1.0 binary.
- `numba==0.56.4` follows the repository conda environment and import / env smoke passed.
- GPU machines may not have GitHub network access. To publish a branch created on a GPU checkout, fetch it into the CPU work-agent repo over SSH and push from CPU.

## Related Branches

- Training-code branch with H200 runtime patches: `intern_ldp_explorer/task001_ptp_py39_rerun`
- Commit: `529857fa8bab663510d88c5c7b72b973f4c37104`
- Purpose: keep runtime patches off `main` while allowing `/root/ptp_ldp_py39` tests to use a named branch.

## Quick Recommendation

For reproduction experiments that need the PTP-style stack:

1. Use `/root/ptp_ldp_py39` only on a node where it has been verified with `robomimic==0.2.0`; the older `10.100.0.29:36645` record is stale as of Session 13.
2. Use the training checkout branch `intern_ldp_explorer/task001_ptp_py39_rerun`.
3. Record `git status`, venv package versions, and the output root before launch.
4. Treat results as H200-adapted PTP-style results, not exact upstream conda results, because Torch and `av` are adapted for the current container.
