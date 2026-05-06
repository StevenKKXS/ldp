# History Log

<!-- METADATA:SESSION=0 -->

## Session 0
- Created task for testing SmolVLA structure on LDP square training.
- Scope includes isolated workdir setup, asset discovery under `/mnt/3fs2/data/tingwen.du`, remote GPU execution, and final report.

## Session 1
- Located LDP checkout at `/mnt/3fs2/data/tingwen.du/workspace/ldp` and square data under `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer`.
- Wrote an isolated SmolVLA-like flow-matching training script under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task002_test_smolvla_square_ldp/scripts/`.
- Ran 2-GPU smoke tests and 800-step short training runs on H200 node `10.100.16.46:16139`.
- Best matched run used LDP-style `abs_action + rotation_6d` 10D actions and reached final train loss `0.2213`, validation flow loss `0.2164`, and 10-step sampled action MSE `0.1947`.
- Wrote final report to `/mnt/3fs2/data/tingwen.du/intern_method_developer/task002_test_smolvla_square_ldp/REPORT.md`.
