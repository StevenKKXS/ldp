## Task: Save SmolVLA Square Rollout Videos

<!-- METADATA:STATUS=InProgress,ASSIGNEE=intern_method_developer -->

### Background
- The square rollout success-rate test in task004 produced jsonl metrics but no saved videos.
- The supervisor requested saved videos for manual inspection.

### Goals
- Reuse the task004 GPU simulator environment and task003 best checkpoint.
- Save rollout videos under the intern-owned task005 path.
- Include both successful and failed rollout examples when available.

### Acceptance Criteria
- Videos are saved under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task005_smolvla_square_rollout_videos`.
- A manifest records video paths, seeds, success flags, and rollout settings.
- Task status and knowledge are updated in the branch.
