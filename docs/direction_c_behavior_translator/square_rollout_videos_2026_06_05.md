# Square Rollout Videos

Date: 2026-06-05

Purpose: generate short robomimic Square rollout videos for presentation from the corrected Stage2b Direction C runs.

## GPU / KeepGPU Change

Released KeepGPU on the py39-capable node:

```bash
10.100.2.39:23494
```

This node is now free after video generation; all 8 H200 GPUs were checked at about `1 MiB` and `0%` util.

The other KeepGPU node remains active:

```bash
10.100.4.23:21492
```

## Video Evaluator

Added:

```bash
eval_robomimic_rollout_videos.py
```

It loads the same workspace checkpoint format as `eval_flow_matching_rollout.py`, uses the EMA model by default, runs robomimic rollout, and writes:

- `eval_log.json`
- raw runner media under `media/`
- deterministic copies under `videos/rollout_<idx>_seed_<seed>_score_<0|1>.mp4`

The script omits the H264 `profile` option because PyAV `14.2.0` failed with both `profile=high` and `profile=baseline`; no profile succeeded in the smoke test.

## Output Root

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_rollout_videos_20260605
```

## Generated Sets

| Setting | Checkpoint | Videos | Scores on seeds `100000-100009` | Mean |
|---|---|---:|---|---:|
| Base, no context | `m1_base_no_context_action8_causalcond_off/checkpoints/epoch=0049-val_loss=0.048735.ckpt` | 10 | `[0,0,0,0,0,0,0,0,0,0]` | `0.0` |
| Random context, `add_last` | `m3_random_add_last_action8_causalcond_off/checkpoints/epoch=0024-val_loss=0.058755.ckpt` | 10 | `[0,0,1,0,0,0,0,0,1,0]` | `0.2` |
| Pretrained translator context, `add_last` | `m2_pretrained_past_add_last_action8_causalcond_off/checkpoints/epoch=0024-val_loss=0.050084.ckpt` | 10 | `[0,0,0,0,0,0,1,0,0,0]` | `0.1` |

Note: the prior 50-episode result table includes Base e24, but the corresponding e24 checkpoint file is not present in the current Ceph checkpoint directory. For video generation, Base e49 was used because it is an available checkpoint from the same corrected Stage2b rollout table.

## Video Directories

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_rollout_videos_20260605/base_e49_10vid/videos
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_rollout_videos_20260605/random_add_last_e24_10vid/videos
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_rollout_videos_20260605/pretrained_add_last_e24_10vid/videos
```

Each directory contains 10 files named by rollout index, test seed, and score.

## Verification

Checked with PyAV on the GPU node:

- each set contains 10 mp4 files;
- sampled videos decode successfully;
- sampled videos have 250 frames;
- files are non-empty.
