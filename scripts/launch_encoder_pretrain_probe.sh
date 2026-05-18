#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/mnt/nfs/tingwen/intern_method_developer/repos/ldp_encoder_probe}"
CONDA_SH="${CONDA_SH:-/mnt/nfs/tingwen/ldp/envs/gmp_released_ckpt/miniforge3/etc/profile.d/conda.sh}"
CONDA_ENV="${CONDA_ENV:-/mnt/nfs/tingwen/ldp/envs/gmp_released_ckpt/miniforge3/envs/gmp-py310}"
OUTPUT_BASE="${OUTPUT_BASE:-/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8}"
LOG_BASE="${LOG_BASE:-/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/logs/20260518_session8}"
SQUARE_DATA="${SQUARE_DATA:-/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5}"
TOOL_HANG_DATA="${TOOL_HANG_DATA:-/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5}"
SQUARE_ENCODER="${SQUARE_ENCODER:-/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/square_encoder.ckpt}"
TOOL_HANG_ENCODER="${TOOL_HANG_ENCODER:-/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/tool_hang_encoder.ckpt}"
START_DELAY_SECONDS="${START_DELAY_SECONDS:-20}"

mkdir -p "${OUTPUT_BASE}" "${LOG_BASE}"
source "${CONDA_SH}"
conda activate "${CONDA_ENV}"
cd "${REPO_DIR}"

PID_FILE="${LOG_BASE}/pids.tsv"
printf "exp_id\tpid\tgpu\tlog\toutput\n" > "${PID_FILE}"

launch_one() {
  local exp_id="$1"
  local gpu="$2"
  local config_name="$3"
  local dataset_path="$4"
  local encoder_path="$5"
  local seed="$6"
  shift 6
  local log_path="${LOG_BASE}/${exp_id}.log"
  local output_dir="${OUTPUT_BASE}/${exp_id}"

  mkdir -p "${output_dir}"
  echo "Launching ${exp_id} on GPU ${gpu}"
  nohup env CUDA_VISIBLE_DEVICES="${gpu}" WANDB_MODE=disabled PYTHONUNBUFFERED=1 \
    python train.py \
      --config-dir=experiment_configs/encoder_pretrain \
      --config-name="${config_name}" \
      hydra.run.dir="${output_dir}" \
      task.dataset.dataset_path="${dataset_path}" \
      task.dataset.use_cache=false \
      obs_encoder_dir="${encoder_path}" \
      training.device=cuda:0 \
      training.seed="${seed}" \
      task.dataset.seed="${seed}" \
      "$@" \
    > "${log_path}" 2>&1 &
  local pid="$!"
  printf "%s\t%s\t%s\t%s\t%s\n" "${exp_id}" "${pid}" "${gpu}" "${log_path}" "${output_dir}" >> "${PID_FILE}"
  sleep "${START_DELAY_SECONDS}"
}

launch_one "B_square_full_seed42" 0 "predictive_square" "${SQUARE_DATA}" "${SQUARE_ENCODER}" 42
launch_one "B_square_future_seed42" 1 "predictive_square" "${SQUARE_DATA}" "${SQUARE_ENCODER}" 42 pretrain.target_mode=future
launch_one "A_square_future_seed42" 2 "contrastive_square" "${SQUARE_DATA}" "${SQUARE_ENCODER}" 42
launch_one "A_square_future_seed43" 3 "contrastive_square" "${SQUARE_DATA}" "${SQUARE_ENCODER}" 43
launch_one "B_tool_hang_full_seed42" 4 "predictive_tool_hang" "${TOOL_HANG_DATA}" "${TOOL_HANG_ENCODER}" 42
launch_one "B_tool_hang_future_seed42" 5 "predictive_tool_hang" "${TOOL_HANG_DATA}" "${TOOL_HANG_ENCODER}" 42 pretrain.target_mode=future
launch_one "A_tool_hang_future_seed42" 6 "contrastive_tool_hang" "${TOOL_HANG_DATA}" "${TOOL_HANG_ENCODER}" 42
launch_one "A_tool_hang_future_seed43" 7 "contrastive_tool_hang" "${TOOL_HANG_DATA}" "${TOOL_HANG_ENCODER}" 43

echo "PID file: ${PID_FILE}"
