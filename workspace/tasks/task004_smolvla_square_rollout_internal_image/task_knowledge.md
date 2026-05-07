# Task Knowledge

<!-- METADATA:SESSION=0 -->

## Working Rules
- Own writable root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task004_smolvla_square_rollout_internal_image`.
- Reference setup script path: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/setup_gpu_machine.sh`.
- Do not modify or write into `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer` or other intern-owned storage.
- Best checkpoint from formal training: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/runs/formal_ldp_abs10_1000epoch_eval100_20260506_135043/epoch_0300.pt`.

## Findings
- Copied setup script path: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task004_smolvla_square_rollout_internal_image/scripts/setup_gpu_machine.sh`.
- Setup succeeded in `/root/venv`: `torch 2.5.1+cu124`, `mujoco 3.8.0`, `robosuite 1.4.1`, `robomimic 0.3.0`, `gym 0.25.2`, `pytorch3d.transforms` stub.
- Robosuite square rollout requires `controller_configs.control_delta=False` because `image_abs.hdf5` stores absolute actions.
- Best checkpoint rollout command wrote `/mnt/3fs2/data/tingwen.du/intern_method_developer/task004_smolvla_square_rollout_internal_image/rollouts/epoch0300_20rollouts.jsonl`.
- Formal rollout success rate: `2/20 = 10%`, successes on seeds `10001` and `10007`.
- States-only demo replay succeeded `5/5`, confirming the absolute-action env configuration. Replay with stored XML `model_file` failed due old XML / robosuite 1.4 geom-name mismatch (`robot0_g0_vis` missing), but formal random-seed rollout does not use demo XML reset.
