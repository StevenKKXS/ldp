#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/mnt/nfs/tingwen/intern_method_developer/repos/ldp_encoder_probe}"
CONDA_SH="${CONDA_SH:-/mnt/nfs/tingwen/ldp/envs/gmp_released_ckpt/miniforge3/etc/profile.d/conda.sh}"
CONDA_ENV="${CONDA_ENV:-/mnt/nfs/tingwen/ldp/envs/gmp_released_ckpt/miniforge3/envs/gmp-py310}"
OUTPUT_BASE="${OUTPUT_BASE:-/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10}"
LOG_BASE="${LOG_BASE:-/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/downstream_logs/20260519_session10}"
SQUARE_DATA="${SQUARE_DATA:-/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5}"
TOOL_HANG_DATA="${TOOL_HANG_DATA:-/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5}"
ORIG_SQUARE_ENCODER="${ORIG_SQUARE_ENCODER:-/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/square_encoder.ckpt}"
ORIG_TOOL_HANG_ENCODER="${ORIG_TOOL_HANG_ENCODER:-/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/tool_hang_encoder.ckpt}"
PRETRAIN_BASE="${PRETRAIN_BASE:-/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8}"
SQUARE_EPOCHS="${SQUARE_EPOCHS:-50}"
TOOL_EPOCHS="${TOOL_EPOCHS:-50}"
SQUARE_MAX_TRAIN_STEPS="${SQUARE_MAX_TRAIN_STEPS:-200}"
SQUARE_MAX_VAL_STEPS="${SQUARE_MAX_VAL_STEPS:-20}"
TOOL_MAX_TRAIN_STEPS="${TOOL_MAX_TRAIN_STEPS:-100}"
TOOL_MAX_VAL_STEPS="${TOOL_MAX_VAL_STEPS:-10}"
START_DELAY_SECONDS="${START_DELAY_SECONDS:-20}"

mkdir -p "${OUTPUT_BASE}" "${LOG_BASE}"
source "${CONDA_SH}"
conda activate "${CONDA_ENV}"
cd "${REPO_DIR}"

PID_FILE="${LOG_BASE}/pids.tsv"
printf "exp_id\tpid\tgpu\tlog\toutput\n" > "${PID_FILE}"

launch_square() {
  local exp_id="$1"
  local gpu="$2"
  local encoder_path="$3"
  local freeze="$4"
  local log_path="${LOG_BASE}/${exp_id}.log"
  local output_dir="${OUTPUT_BASE}/${exp_id}"
  mkdir -p "${output_dir}"
  echo "Launching ${exp_id} on GPU ${gpu}"
  nohup env CUDA_VISIBLE_DEVICES="${gpu}" WANDB_MODE=disabled PYTHONUNBUFFERED=1 \
    python train.py \
      --config-dir=experiment_configs/square \
      --config-name=transformer_square \
      hydra.run.dir="${output_dir}" \
      task.dataset.dataset_path="${SQUARE_DATA}" \
      task.dataset.use_cache=false \
      '~task.dataset.shape_meta.obs.embedding' \
      policy.use_embed_if_present=false \
      task.dataset.use_embed_if_present=false \
      obs_encoder_dir="${encoder_path}" \
      obs_encoder_freeze="${freeze}" \
      training.device=cuda:0 \
      training.num_epochs="${SQUARE_EPOCHS}" \
      training.max_train_steps="${SQUARE_MAX_TRAIN_STEPS}" \
      training.max_val_steps="${SQUARE_MAX_VAL_STEPS}" \
      training.rollout_every=999999 \
      training.sample_every=5 \
      training.checkpoint_every=10 \
      checkpoint.topk.k=0 \
      logging.mode=disabled \
      dataloader.num_workers=4 \
      val_dataloader.num_workers=2 \
      > "${log_path}" 2>&1 &
  local pid="$!"
  printf "%s\t%s\t%s\t%s\t%s\n" "${exp_id}" "${pid}" "${gpu}" "${log_path}" "${output_dir}" >> "${PID_FILE}"
  sleep "${START_DELAY_SECONDS}"
}

launch_tool_hang() {
  local exp_id="$1"
  local gpu="$2"
  local encoder_path="$3"
  local freeze="$4"
  local log_path="${LOG_BASE}/${exp_id}.log"
  local output_dir="${OUTPUT_BASE}/${exp_id}"
  mkdir -p "${output_dir}"
  echo "Launching ${exp_id} on GPU ${gpu}"
  nohup env CUDA_VISIBLE_DEVICES="${gpu}" WANDB_MODE=disabled PYTHONUNBUFFERED=1 \
    python train.py \
      --config-dir=experiment_configs/tool \
      --config-name=transformer_tool_hang \
      hydra.run.dir="${output_dir}" \
      task.dataset.dataset_path="${TOOL_HANG_DATA}" \
      task.dataset.use_cache=false \
      obs_encoder_dir="${encoder_path}" \
      obs_encoder_freeze="${freeze}" \
      training.device=cuda:0 \
      training.num_epochs="${TOOL_EPOCHS}" \
      training.max_train_steps="${TOOL_MAX_TRAIN_STEPS}" \
      training.max_val_steps="${TOOL_MAX_VAL_STEPS}" \
      training.rollout_every=999999 \
      training.sample_every=5 \
      training.checkpoint_every=10 \
      checkpoint.topk.k=0 \
      logging.mode=disabled \
      dataloader.num_workers=4 \
      val_dataloader.num_workers=2 \
      > "${log_path}" 2>&1 &
  local pid="$!"
  printf "%s\t%s\t%s\t%s\t%s\n" "${exp_id}" "${pid}" "${gpu}" "${log_path}" "${output_dir}" >> "${PID_FILE}"
  sleep "${START_DELAY_SECONDS}"
}

launch_square "square_original_finetune" 0 "${ORIG_SQUARE_ENCODER}" false
launch_square "square_B_full_frozen" 1 "${PRETRAIN_BASE}/B_square_full_seed42/checkpoints/latest.ckpt" true
launch_square "square_B_full_finetune" 2 "${PRETRAIN_BASE}/B_square_full_seed42/checkpoints/latest.ckpt" false
launch_square "square_A_future_finetune" 3 "${PRETRAIN_BASE}/A_square_future_seed42/checkpoints/latest.ckpt" false
launch_tool_hang "tool_hang_original_finetune" 4 "${ORIG_TOOL_HANG_ENCODER}" false
launch_tool_hang "tool_hang_B_full_frozen" 5 "${PRETRAIN_BASE}/B_tool_hang_full_seed42/checkpoints/latest.ckpt" true
launch_tool_hang "tool_hang_B_full_finetune" 6 "${PRETRAIN_BASE}/B_tool_hang_full_seed42/checkpoints/latest.ckpt" false
launch_tool_hang "tool_hang_A_future_finetune" 7 "${PRETRAIN_BASE}/A_tool_hang_future_seed42/checkpoints/latest.ckpt" false

echo "PID file: ${PID_FILE}"
