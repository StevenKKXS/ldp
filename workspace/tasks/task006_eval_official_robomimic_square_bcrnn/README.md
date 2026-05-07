## Task: Evaluate Official robomimic BC-RNN Square Checkpoint

<!-- METADATA:STATUS=InProgress,ASSIGNEE=intern_method_developer -->

### Background
- The user asked whether the official robomimic model-zoo Square(PH) low-dimensional BC-RNN checkpoint can reproduce the reported approximate 84% success rate without training.
- The official model-zoo page states that robomimic-v0.1 pretrained models require robomimic v0.1 and the robosuite `offline_study` branch, so version compatibility must be reported explicitly.
- The user requested saved rollout videos for inspection.

### Goals
- Download the official Square(PH) low-dimensional BC-RNN checkpoint into the intern_method_developer-owned task directory.
- Run evaluation only, with no training, using the official 50-rollout, horizon-400 setup.
- Save rollout videos under the task directory for user inspection.
- Compare the measured success rate against the official approximate 84% claim and document environment caveats.

### Acceptance Criteria
- Report includes exact checkpoint URL / local path, environment versions, rollout command, success count, success rate, and comparison to the 84% model-zoo number.
- Rollout videos and logs are saved under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn`.
- Any incompatibility with current GPU environment is diagnosed with logs and a concrete next action.
