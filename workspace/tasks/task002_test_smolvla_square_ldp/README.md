## Task: Test SmolVLA Structure for LDP Square Training

<!-- METADATA:STATUS=Completed,ASSIGNEE=intern_method_developer -->

### Background
- The supervisor asked to test whether the SmolVLA model structure can be used for the `square` task under the current LDP codebase.
- All experiment files, cloned working copies, logs, outputs, and reports must stay under `/mnt/3fs2/data/tingwen.du`.
- Reuse existing assets under `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer` when available, especially downloaded square datasets and prior LDP artifacts.
- Use the provided 2-GPU machine at `10.100.16.46:16139` for GPU training tests when reachable.

### Goals
- Locate the active LDP code and relevant square datasets under `/mnt/3fs2/data/tingwen.du`.
- Create an isolated task work area that does not modify or pollute the original LDP checkout.
- Inspect the current LDP training stack and the SmolVLA structure to determine the smallest viable square-training integration.
- Run practical smoke or short training tests on the square task and record whether the model can start training, converge, and evaluate.
- Produce a written report with commands, paths, environment notes, metrics, and limitations.

### Acceptance Criteria
- The report states whether SmolVLA can be wired into current LDP square training.
- The report includes exact dataset/config/checkpoint/log paths under `/mnt/3fs2/data/tingwen.du`.
- The report includes observed training behavior and quantitative metrics available from the run.
- Any compatibility patches or wrappers are documented without changing the original LDP checkout.

### Report
- `/mnt/3fs2/data/tingwen.du/intern_method_developer/task002_test_smolvla_square_ldp/REPORT.md`
