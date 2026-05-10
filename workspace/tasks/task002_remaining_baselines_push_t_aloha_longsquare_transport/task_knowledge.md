# task002_remaining_baselines_push_t_aloha_longsquare_transport - Task Knowledge

<!-- METADATA:SESSION=1 -->

> Rule: each item is one sentence in the format `N. Category: content`.
>
> Categories include: user requirement, technical fact, file change, research conclusion.

---

## Knowledge Entries

1. User requirement: The second task should run the remaining baselines and improve them into usable baselines where possible.
2. User requirement: The initial focus tasks are Push-T, LH-ALOHA, Long Square, and Transport.
3. Technical fact: Task 001 evidence suggests the Robomimic tasks should start from the PTP-compatible Python 3.9 environment rather than the modern Python 3.12 stack.
4. Technical fact: Task 001 evidence suggests `global_action=8` is the first priority for rapid iteration, while `global_action=1` is diagnostic only unless specifically needed.
5. Technical fact: Push-T and LH-ALOHA have a configured PTP-style venv at `/root/ptp_ldp_py39` on `10.100.2.35:33486` and `10.100.16.46:36566`.
6. Technical fact: Both new servers have `2 x NVIDIA H200` and passed CUDA visibility checks with `torch.cuda.device_count()==2`.
7. Technical fact: The environment uses Python `3.9.25`, torch `2.5.1`, robomimic `0.2.0`, robosuite `1.2.0`, `mujoco-py==2.1.2.14`, `mujoco==2.3.7`, `dm-control==1.0.9`, and `gym==0.21.0`.
8. Technical fact: The environment requires `MUJOCO_PY_MUJOCO_PATH=/root/.mujoco/mujoco210`, `LD_LIBRARY_PATH=/root/.mujoco/mujoco210/bin:$LD_LIBRARY_PATH`, `MUJOCO_GL=egl`, and `PYTHONPATH=/mnt/3fs2/data/tingwen.du/workspace/ldp:$PYTHONPATH`.
9. Technical fact: `robosuite==1.2.0` must be installed with `--no-deps` in this stack, otherwise pip tries to install `mujoco-py==2.0.2.9`.
10. Technical fact: `mujoco-py==2.1.2.14` requires the Cython `0.29.32` path here; Cython 3 failed to compile `mujoco_py/cymj.pyx`.
11. Technical fact: `wandb==0.13.3` requires `pkg_resources`, so `setuptools==65.5.0` is pinned.
12. Technical fact: `AlohaImageRunner` requires a local `pytorch3d.transforms` stub copied from `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/pytorch3d_src`.
13. Technical fact: Push-T smoke passed using `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/pusht/pusht_cchi_v7_replay.zarr`, with `img=(25650,96,96,3)`, `action=(25650,2)`, and horizon-32 samples.
14. Technical fact: LH-ALOHA smoke passed using `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/aloha_twomodes_single/demos.hdf5`, with `50` demos, actions `(500,7)`, embeddings `(500,135)`, and a successful reset of `sim_singlearm_pickandplace_twomodes_scripted`.
15. File change: Detailed reusable setup requirements were recorded in `workspace/tasks/task002_remaining_baselines_push_t_aloha_longsquare_transport/session001_push_t_lh_aloha_env_setup.md`.

---
