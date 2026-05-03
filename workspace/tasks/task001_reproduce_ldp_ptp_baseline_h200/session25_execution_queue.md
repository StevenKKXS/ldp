# Session 25 Execution Queue

## Goal

Turn the simulation reproduction sheet into a staged execution queue that can be advanced automatically once the pending RoboMimic archive is fully downloaded and extracted.

## Trigger Rule

Start queued experiments only after all four public simulation datasets are confirmed ready:

- `robomimic_image`
- `pusht`
- `aloha_twomodes_single`
- `longhistsquare100`

For `robomimic_image`, "ready" means more than the preexisting `square/mh` subtree is present under shared storage, specifically:

- `datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- `datasets/robomimic/datasets/transport/mh/image_abs.hdf5`

## Queue Design

This queue is intentionally task-column aligned with the main result table.

Priority order:

1. fill one new task column with the core comparison first
2. add the matching short-hist anchor
3. move to the next task column

## Wave 0: Monitor And Gate

- `W0-1`: check download state every 10 minutes
- `W0-2`: stop after at most 12 checks if RoboMimic is still incomplete
- `W0-3`: if complete, sync the needed config files to the GPU machine and launch Wave 1

## Wave 1: Tool-Hang Core Pair

- `TH-1`: `Tool-Hang long-hist DP`
  - config family: `tool_hang`
  - effective meaning: `global_obs=16`, `past_action_pred=false`
  - purpose: fill the `Repro long-hist DP` cell for `Tool-Hang`

- `TH-2`: `Tool-Hang long-hist PTP`
  - config family: `tool_hang`
  - effective meaning: `global_obs=16`, `past_action_pred=true`
  - purpose: fill the `Repro long-hist PTP` cell for `Tool-Hang`

- `TH-3`: `Tool-Hang short-hist DP`
  - config family: `tool_hang`
  - effective meaning: `global_obs=2`, `past_action_pred=false`
  - purpose: fill the `Repro short-hist DP` cell for `Tool-Hang`

Wave 1 automatic launch policy:

- auto-launch `TH-1` and `TH-2`
- keep `TH-3` queued for the next free slot

## Wave 2: Transport Core Pair

- `TR-1`: `Transport long-hist DP`
  - `global_obs=16`, `past_action_pred=false`

- `TR-2`: `Transport long-hist PTP`
  - `global_obs=16`, `past_action_pred=true`

- `TR-3`: `Transport short-hist DP`
  - `global_obs=2`, `past_action_pred=false`

## Wave 3: Long Square

- `LS-1`: `Long Square long-hist DP`
- `LS-2`: `Long Square long-hist PTP`

These are high-priority because they align closely with the paper's long-horizon story, but they are not gated by RoboMimic and can be started independently once GPU capacity allows.

## Wave 4: ALOHA / Cube

- `AL-1`: `ALOHA long-hist DP`
- `AL-2`: `ALOHA long-hist PTP`

## Wave 5: Push-T Support

- `PT-1`: `Push-T short-hist DP`

Push-T is useful as a supporting column, but it is lower priority than `Tool-Hang`, `Transport`, and `Long Square` for the current table.

## Resource Policy

- current GPU observation:
  - GPU0 is mostly free
  - GPU1 still has surviving square baselines
- therefore the first automatic launch should target GPU0 only
- when Wave 1 starts, launch two jobs on GPU0:
  - `TH-1`: `Tool-Hang long-hist DP`
  - `TH-2`: `Tool-Hang long-hist PTP`

## Files Used By The Automation

- watchdog script:
  - `workspace/tasks/task001_reproduce_ldp_ptp_baseline_h200/session25_monitor_and_schedule.sh`
- watchdog log:
  - `/work-agents/intern_ldp_explorer/outputs/session25_monitor_schedule/session25_monitor_schedule.log`
- watchdog state dir:
  - `/work-agents/intern_ldp_explorer/outputs/session25_monitor_schedule/state`

