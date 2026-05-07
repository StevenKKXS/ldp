# History Log

<!-- METADATA:SESSION=0 -->

## Session 0
- Created task to save manual-check rollout videos for the compact SmolVLA-style square checkpoint.
- Implemented `rollout_smolvla_square_with_video.py` to save side-by-side `agentview` and wrist-camera mp4 videos.
- Ran a 2-episode smoke video check and confirmed mp4 generation.
- Ran the full 20-seed video rollout for seeds `10000-10019`.
- Saved 20 mp4 videos and manifest under the intern-owned task005 path.
- Verified sample mp4 files with `imageio`; frames decode as `uint8` shape `[84, 168, 3]`.
