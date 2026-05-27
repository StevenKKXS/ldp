# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 73 |
| Recent Progress | Rechecked archived LDP/Square rollout records to separate the config ceiling from the actually useful training budgets. The repo Square configs still set `num_epochs=3500`, `batch_size=64`, and rollout/checkpoint cadence every `100` epochs, but archived reproducible Square rollout records do not show that we used the full 3500. The clearest old Square PTP record selected `epoch=0099-test_mean_score=0.475.ckpt` and evaluated to `0.36` over 100 seeds; old Square DP selected `epoch=0499-test_mean_score=0.025.ckpt` and evaluated to `0.0` over 100 seeds. The earlier FM Square run showed useful rollout signal by roughly e457-e459 under py39 / `robomimic==0.2.0` (`h10 7/10`, `action8 4/10`), with no recorded improvement after it later reached e786-e788. Practical budget target for current Square Stage2b should therefore be staged checkpoints at e50/e100/e200 and a 400-500 epoch cap for DP/FM-style comparisons, not 3500 by default. |
