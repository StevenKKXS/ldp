## Task: Formal SmolVLA Square Training and Evaluation

<!-- METADATA:STATUS=InProgress,ASSIGNEE=intern_method_developer -->

### Background
- The supervisor requested formal SmolVLA-style training on the LDP square task.
- Target schedule should reference LDP: 1000 epochs, evaluation every 100 epochs.
- Work must be autonomous unless server resources are unavailable or a hard blocker is reached.
- Do not write into other interns' storage. Use `/mnt/3fs2/data/tingwen.du/intern_method_developer` and accessible overlay/read-only assets only.

### Goals
- Implement a resumable formal training pipeline for the SmolVLA-style square policy.
- Train for 1000 epochs with checkpointing and evaluation every 100 epochs.
- Implement evaluation that reports square performance; if full Robosuite rollout cannot be made reliable, report the exact blocker and provide offline evaluation metrics at every scheduled interval.
- Save all code, logs, checkpoints, and reports under the intern-owned task directory.

### Acceptance Criteria
- A report under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/` summarizes commands, artifacts, metrics, and limitations.
- Training/eval artifacts are reproducible and isolated from the original LDP checkout.
- Task status and knowledge are updated in this branch.
