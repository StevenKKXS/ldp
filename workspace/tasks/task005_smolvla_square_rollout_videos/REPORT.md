# SmolVLA Square Rollout Videos

## 结果

- 已保存 20 条 Robosuite square rollout 视频，seed 为 `10000-10019`。
- 每个视频为左右拼接画面：左侧 `agentview_image`，右侧 `robot0_eye_in_hand_image`。
- 分辨率：`84x168`，20 fps，mp4/h264。
- 成功视频 2 条：
  - `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos/videos_epoch0300_20/seed_10001_success_176steps.mp4`
  - `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos/videos_epoch0300_20/seed_10007_success_189steps.mp4`
- 失败视频 18 条，均在同一目录下。

## 路径

- Video dir: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos/videos_epoch0300_20`
- Manifest: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos/manifests/epoch0300_20_videos.jsonl`
- Log: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos/logs/video_epoch0300_20.log`
- Script: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos/scripts/rollout_smolvla_square_with_video.py`

## 运行设置

- Checkpoint: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/runs/formal_ldp_abs10_1000epoch_eval100_20260506_135043/epoch_0300.pt`
- Dataset: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`
- Max steps: 400
- Action horizon: 8
- Flow sample steps: 10
- Seeds: `10000-10019`

Summary from manifest:

```json
{"num_rollouts": 20, "successes": 2, "success_rate": 0.1, "mean_steps": 378.25}
```

## 校验

用 `imageio` 读取了样例视频首帧，返回 `uint8` frame，shape 为 `[84, 168, 3]`。视频文件可正常解码。
