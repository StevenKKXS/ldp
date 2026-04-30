# Task Knowledge

<!-- METADATA:SESSION=0 -->

## Working Rules
- Prefer upstream official assets first:
- official repo `https://github.com/long-context-dp/ldp`
- official website `https://long-context-dp.github.io/`
- official README-linked datasets / encoders
- Record exact Hydra configs, overrides, checkpoints, and evaluation commands.
- Distinguish clearly between:
- short-context baseline
- long-context baseline
- PTP / past-token prediction variants
- Reuse existing server runs only after checking `policy.past_action_pred`, config lineage, and task alignment.

## Findings
- Upstream public asset audit:
- GitHub Releases page exists but is empty.
- Official README provides dataset links and a Google Drive `obs_encoders.zip` for short-context encoders used in embedding caching.
- Existing remote data state on `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets`:
- Present: `robomimic/datasets/square/mh/image_abs.hdf5`
- Missing so far: `image_abs_past.hdf5`, `image_abs_emb.hdf5`, `image_abs_past_emb.hdf5`, `longhistsquare100/*`
- Paper protocol clarification from PMLR text:
- Default evaluation uses past 16 time steps as conditioning input.
- Baselines include:
- `no-history`: only current and previous single frame
- `no-PTP`: long-context conditioning without past-token prediction
- Current debug-server run classification:
- Output dir: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/outputs/full_train_3500ep_1777457545`
- Config lineage: `transformer_square`
- Effective setting: `policy.past_action_pred=true`, `task.name=square_image`
- Important caveat: config default is `global_obs=2`, so this run is PTP on standard square, not the paper-default long-context square setting.
- In-progress reproduction matrix on debug server:
- `baseline_square_3500ep_1777535019`: `square`, `global_obs=2`, `past_action_pred=false`
- `no_ptp_square_obs16_1777535301`: `square`, `global_obs=16`, `past_action_pred=false`
- `ptp_square_obs16_1777535313`: `square`, `global_obs=16`, `past_action_pred=true`
