# Task Knowledge

<!-- METADATA:SESSION=0 -->

## Working Rules
- Own writable root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos`.
- Reuse task003 best checkpoint: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/runs/formal_ldp_abs10_1000epoch_eval100_20260506_135043/epoch_0300.pt`.
- Reuse task003 dataset copy: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`.
- Do not write into other intern-owned storage.

## Findings
- Video directory: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos/videos_epoch0300_20`.
- Manifest: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos/manifests/epoch0300_20_videos.jsonl`.
- Saved videos are side-by-side `agentview_image` and `robot0_eye_in_hand_image`, shape `84x168`, 20 fps, mp4/h264.
- Success videos are `seed_10001_success_176steps.mp4` and `seed_10007_success_189steps.mp4`.
- All 20 videos were generated; total size is about 6.8 MB.
- `imageio` decoded sample videos successfully.
