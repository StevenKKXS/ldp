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
#   DATASET_PATH=/path/to/square/mh/image_abs.hdf5
#   TRANSLATOR_CKPT=/path/to/stage1/past/best.ckpt
#   DEVICES=0,1,2,3
#   DRY_RUN=1
#   ALLOW_MISSING_TRANSLATOR_CKPT=0
#
# Extra CLI args are appended to every train.py invocation.

PYTHON_BIN="${PYTHON_BIN:-python}"
CONFIG_DIR="${CONFIG_DIR:-experiment_configs/square}"
RUN_ROOT="${RUN_ROOT:-/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_square_causalcond_off_$(date -u +%Y%m%d_%H%M%S)}"
DATASET_PATH="${DATASET_PATH:-/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/datasets/robomimic/datasets/square/mh/image_abs.hdf5}"
TRANSLATOR_CKPT="${TRANSLATOR_CKPT:-}"
DEVICES="${DEVICES:-0,1,2,3}"
DRY_RUN="${DRY_RUN:-0}"
ALLOW_MISSING_TRANSLATOR_CKPT="${ALLOW_MISSING_TRANSLATOR_CKPT:-0}"

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

NEEDS_CKPT=(
  "0"
  "1"
  "0"
  "1"
)

mkdir -p "$RUN_ROOT"
MANIFEST="$RUN_ROOT/launch_manifest.tsv"
printf "name\tgpu\tconfig\trun_dir\tpid\n" > "$MANIFEST"

launch_idx=0
for idx in "${!CONFIGS[@]}"; do
  config="${CONFIGS[$idx]}"
  name="${NAMES[$idx]}"
  needs_ckpt="${NEEDS_CKPT[$idx]}"

  if [[ "$needs_ckpt" == "1" && -z "$TRANSLATOR_CKPT" && "$ALLOW_MISSING_TRANSLATOR_CKPT" != "1" ]]; then
    echo "Skipping $name because TRANSLATOR_CKPT is not set." >&2
    continue
  fi
  if [[ "$needs_ckpt" == "1" && -n "$TRANSLATOR_CKPT" && ! -f "$TRANSLATOR_CKPT" && "$DRY_RUN" != "1" ]]; then
    echo "Missing TRANSLATOR_CKPT for $name: $TRANSLATOR_CKPT" >&2
    exit 3
  fi

  gpu="${GPU_LIST[$launch_idx]}"
  launch_idx=$((launch_idx + 1))
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
    "task.dataset_path=$DATASET_PATH"
    "$@"
  )

  if [[ "$needs_ckpt" == "1" && -n "$TRANSLATOR_CKPT" ]]; then
    cmd+=("policy.translator_checkpoint=$TRANSLATOR_CKPT")
  fi

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
