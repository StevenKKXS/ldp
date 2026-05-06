# Task Knowledge

<!-- METADATA:SESSION=0 -->

## Working Rules
- Keep experiment artifacts under `/mnt/3fs2/data/tingwen.du`.
- Do not modify the original LDP checkout for experimental code; use an isolated copy or overlay in the task workdir.
- Prefer existing downloaded data under `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer`.
- Record exact commands and paths for every training or evaluation run.

## Findings
- Official SmolVLA uses images, state, optional language, continuous actions, and a flow-matching training objective. The isolated test mirrors those structural pieces with a compact 6.96M-parameter policy.
- Current explorer venv can run PyTorch/HDF5 training but does not include official `lerobot`, `transformers`, `robomimic`, or `robosuite`.
- The square HDF5 raw action is 7D, while current LDP square configs train with 10D `abs_action + rotation_6d`; the 10D representation performed better in the isolated SmolVLA-like test.
- Best 2-GPU short run: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task002_test_smolvla_square_ldp/runs/smolvla_like_square_ldp_abs10_ddp_800step_20260506_132912`, final `val_loss=0.2164`, `val_sample_action_mse=0.1947`.
- Existing explorer rollout reference for LDP policies: square DP `0/100`, square PTP `36/100` in `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/evals/session65_video_1778035802/`.
