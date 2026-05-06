# Task Knowledge

<!-- METADATA:SESSION=0 -->

## Working Rules
- Own writable root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval`.
- Do not write into `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer` or other intern-owned storage.
- Use resumable checkpoints because formal 1000-epoch training may exceed one interactive session.
- Record exact train/eval commands and server state.

## Findings
- Formal run directory: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/runs/formal_ldp_abs10_1000epoch_eval100_20260506_135043`.
- Dataset copy: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`.
- Formal model uses `ldp_abs10` actions, two image views, 9D state, chunk size 16, DDP world size 2, batch size 128 per rank, 6.96M parameters.
- Epoch 100 offline square action eval: `val_loss=0.20909729599952698`, `val_sample_action_mse=0.13123467564582825`, train loss `0.09809166193008423`.
- Available Python environments on the GPU host do not contain `robomimic`, `robosuite`, `mujoco`, `mujoco_py`, or `lerobot`; remote pip probes against PyPI timed out. Full simulator rollout eval is blocked unless an environment with these dependencies becomes available.
- Completed final epoch 1000. Total runtime was `7774.679127454758` seconds for `294000` global steps.
- Full eval table is in `REPORT.md` and `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/runs/formal_ldp_abs10_1000epoch_eval100_20260506_135043/eval_metrics.jsonl`.
- Best sampled action MSE checkpoint is `epoch_0300.pt` with `val_sample_action_mse=0.13077014684677124`.
- Final checkpoint is `epoch_1000.pt` with `val_loss=0.3399428427219391` and `val_sample_action_mse=0.13218089938163757`.
