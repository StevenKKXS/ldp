#!/usr/bin/env bash
set -euo pipefail

# Launch the corrected Direction C Stage 2b Square action8 matrix.
#
# Required runtime assumptions:
# - Run from the ldp repo root on a clean GPU node.
# - Use the py39 / robomimic==0.2.0 environment.
# - Dataset and translator checkpoint paths in the configs are reachable.
#
# Optional environment variables:
#   PYTHON_BIN=/path/to/python
#   CONFIG_DIR=experiment_configs/square
#   RUN_ROOT=/path/to/output_root
#   DEVICES=0,1,2,3
#   DRY_RUN=1
#
# Extra CLI args are appended to every train.py invocation.

PYTHON_BIN="${PYTHON_BIN:-python}"
CONFIG_DIR="${CONFIG_DIR:-experiment_configs/square}"
RUN_ROOT="${RUN_ROOT:-/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage2b_square_causalcond_off_$(date -u +%Y%m%d_%H%M%S)}"
DEVICES="${DEVICES:-0,1,2,3}"
DRY_RUN="${DRY_RUN:-0}"

IFS=',' read -r -a GPU_LIST <<< "$DEVICES"
if [[ "${#GPU_LIST[@]}" -lt 4 ]]; then
  echo "Need at least 4 GPU ids in DEVICES, got: $DEVICES" >&2
  exit 2
fi

CONFIGS=(
  "transformer_square_action8_causalcond_off_base"
  "transformer_square_translator_context_action8_causalcond_off_add_last"
  "transformer_square_random_context_action8_causalcond_off_add_last"
  "transformer_square_translator_context_action8_causalcond_off_add_all"
)

NAMES=(
  "m1_base_no_context_action8_causalcond_off"
  "m2_pretrained_past_add_last_action8_causalcond_off"
  "m3_random_add_last_action8_causalcond_off"
  "m4_pretrained_past_add_all_action8_causalcond_off"
)

mkdir -p "$RUN_ROOT"
MANIFEST="$RUN_ROOT/launch_manifest.tsv"
printf "name\tgpu\tconfig\trun_dir\tpid\n" > "$MANIFEST"

for idx in "${!CONFIGS[@]}"; do
  gpu="${GPU_LIST[$idx]}"
  config="${CONFIGS[$idx]}"
  name="${NAMES[$idx]}"
  run_dir="$RUN_ROOT/$name"
  mkdir -p "$run_dir"

  cmd=(
    "$PYTHON_BIN" train.py
    --config-dir "$CONFIG_DIR"
    --config-name "$config"
    "training.device=cuda:0"
    "hydra.run.dir=$run_dir"
    "logging.name=$name"
    "exp_name=$name"
    "$@"
  )

  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run] CUDA_VISIBLE_DEVICES=%s' "$gpu"
    printf ' %q' "${cmd[@]}"
    printf '\n'
    printf "%s\t%s\t%s\t%s\t%s\n" "$name" "$gpu" "$config" "$run_dir" "DRY_RUN" >> "$MANIFEST"
  else
    (
      export CUDA_VISIBLE_DEVICES="$gpu"
      nohup "${cmd[@]}" > "$run_dir/train.log" 2>&1 &
      printf "%s\t%s\t%s\t%s\t%s\n" "$name" "$gpu" "$config" "$run_dir" "$!" >> "$MANIFEST"
    )
  fi
done

echo "Launch manifest: $MANIFEST"
