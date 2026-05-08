#!/usr/bin/env bash
set -euo pipefail

TASK_ROOT=/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn
PYTHON=${PYTHON:-/root/venv/bin/python}
TRAIN_MODULE="${TASK_ROOT}/scripts/train_eval_smolvla_square_scheduled.py"
ROLLOUT_SCRIPT="${TASK_ROOT}/scripts/rollout_smolvla_square_all_ckpts.py"
DEFAULT_RUN_BASE="${TASK_ROOT}/runs/smolvla_fourway_1000ep_20260508_130111"

RUN_BASE="${1:-${DEFAULT_RUN_BASE}}"
STAMP="${2:-$(date -u +%Y%m%d_%H%M%S)}"
LOG_ROOT="${TASK_ROOT}/logs/smolvla_fourway_rollout_after_train_${STAMP}"
ALL_OUT="${TASK_ROOT}/rollouts/smolvla_fourway_all_ckpts_20rollouts_${STAMP}"
BEST_LINK_BASE="${TASK_ROOT}/rollouts/smolvla_fourway_best_ckpt_links_${STAMP}"
BEST_OUT="${TASK_ROOT}/rollouts/smolvla_fourway_best_ckpts_50rollouts_${STAMP}"
REPORT="${TASK_ROOT}/reports/smolvla_fourway_rollout_after_train_${STAMP}.md"
LOCK_FILE="${TASK_ROOT}/logs/smolvla_fourway_rollout_after_train.lock"

EXPECTED_RUNS=${EXPECTED_RUNS:-4}
POLL_SEC=${POLL_SEC:-300}
ALL_NUM_ROLLOUTS=${ALL_NUM_ROLLOUTS:-20}
BEST_NUM_ROLLOUTS=${BEST_NUM_ROLLOUTS:-50}
NUM_WORKERS=${NUM_WORKERS:-4}
BEST_NUM_WORKERS=${BEST_NUM_WORKERS:-4}
START_SEED_ALL=${START_SEED_ALL:-10000}
START_SEED_BEST=${START_SEED_BEST:-20000}
MAX_STEPS=${MAX_STEPS:-400}
ACTION_HORIZON=${ACTION_HORIZON:-8}
SAMPLE_STEPS=${SAMPLE_STEPS:-10}
GPUS_CSV=${GPUS_CSV:-0,1,0,1}

mkdir -p "${LOG_ROOT}" "${TASK_ROOT}/reports" "${TASK_ROOT}/logs"
exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
  echo "Another SmolVLA post-train rollout monitor is already running: ${LOCK_FILE}"
  exit 0
fi

cat > "${LOG_ROOT}/run_info.env" <<EOF
RUN_BASE=${RUN_BASE}
ALL_OUT=${ALL_OUT}
BEST_LINK_BASE=${BEST_LINK_BASE}
BEST_OUT=${BEST_OUT}
REPORT=${REPORT}
EXPECTED_RUNS=${EXPECTED_RUNS}
POLL_SEC=${POLL_SEC}
ALL_NUM_ROLLOUTS=${ALL_NUM_ROLLOUTS}
BEST_NUM_ROLLOUTS=${BEST_NUM_ROLLOUTS}
NUM_WORKERS=${NUM_WORKERS}
BEST_NUM_WORKERS=${BEST_NUM_WORKERS}
START_SEED_ALL=${START_SEED_ALL}
START_SEED_BEST=${START_SEED_BEST}
MAX_STEPS=${MAX_STEPS}
ACTION_HORIZON=${ACTION_HORIZON}
SAMPLE_STEPS=${SAMPLE_STEPS}
GPUS_CSV=${GPUS_CSV}
EOF

count_epoch_1000() {
  find "${RUN_BASE}" -mindepth 2 -maxdepth 2 -name 'epoch_1000.pt' 2>/dev/null | wc -l
}

count_run_dirs() {
  find "${RUN_BASE}" -mindepth 1 -maxdepth 1 -type d -name 'smolvla_*' 2>/dev/null | wc -l
}

training_processes() {
  pgrep -af "train_eval_smolvla_square_scheduled.py.*${RUN_BASE}" || true
}

latest_progress() {
  for f in "${RUN_BASE}"/*/eval_metrics.jsonl; do
    [[ -f "${f}" ]] || continue
    echo "==== ${f}"
    tail -n 1 "${f}"
  done
}

echo "[monitor] $(date -u +%Y-%m-%dT%H:%M:%SZ) waiting for training completion" | tee -a "${LOG_ROOT}/monitor.log"
while true; do
  run_count=$(count_run_dirs)
  done_count=$(count_epoch_1000)
  alive=$(training_processes)
  {
    echo "[monitor] $(date -u +%Y-%m-%dT%H:%M:%SZ) run_dirs=${run_count} epoch_1000=${done_count}/${EXPECTED_RUNS}"
    if [[ -n "${alive}" ]]; then
      echo "${alive}"
    else
      echo "no training process matched ${RUN_BASE}"
    fi
    latest_progress
  } >> "${LOG_ROOT}/monitor.log"

  if [[ "${done_count}" -ge "${EXPECTED_RUNS}" && -z "${alive}" ]]; then
    break
  fi
  sleep "${POLL_SEC}"
done
echo "[monitor] $(date -u +%Y-%m-%dT%H:%M:%SZ) training complete; starting all-checkpoint rollout" | tee -a "${LOG_ROOT}/monitor.log"

run_rollout_workers() {
  local run_base="$1"
  local output_root="$2"
  local num_rollouts="$3"
  local start_seed="$4"
  local num_workers="$5"
  local log_prefix="$6"

  mkdir -p "${output_root}"
  IFS=',' read -r -a gpus <<< "${GPUS_CSV}"
  local pids=()
  local wid gpu
  for wid in $(seq 0 $((num_workers - 1))); do
    gpu="${gpus[$((wid % ${#gpus[@]}))]}"
    (
      export CUDA_VISIBLE_DEVICES="${gpu}"
      export CUDA_DEVICE_ORDER=PCI_BUS_ID
      export PYTHONUNBUFFERED=1
      export MUJOCO_GL=egl
      exec "${PYTHON}" "${ROLLOUT_SCRIPT}" \
        --run-base "${run_base}" \
        --train-module "${TRAIN_MODULE}" \
        --output-root "${output_root}" \
        --num-workers "${num_workers}" \
        --worker-id "${wid}" \
        --num-rollouts "${num_rollouts}" \
        --start-seed "${start_seed}" \
        --max-steps "${MAX_STEPS}" \
        --action-horizon "${ACTION_HORIZON}" \
        --sample-steps "${SAMPLE_STEPS}" \
        --device cuda:0 \
        --resume
    ) > "${LOG_ROOT}/${log_prefix}_worker_${wid}.log" 2>&1 &
    pids+=("$!")
    echo "[monitor] launched ${log_prefix} worker=${wid} gpu=${gpu} pid=${pids[-1]}" | tee -a "${LOG_ROOT}/monitor.log"
  done

  local status=0
  for pid in "${pids[@]}"; do
    if ! wait "${pid}"; then
      status=1
    fi
  done
  return "${status}"
}

run_rollout_workers "${RUN_BASE}" "${ALL_OUT}" "${ALL_NUM_ROLLOUTS}" "${START_SEED_ALL}" "${NUM_WORKERS}" "all_ckpts"
"${PYTHON}" "${ROLLOUT_SCRIPT}" \
  --mode summarize \
  --run-base "${RUN_BASE}" \
  --train-module "${TRAIN_MODULE}" \
  --output-root "${ALL_OUT}" \
  > "${LOG_ROOT}/all_ckpts_summarize.log" 2>&1

echo "[monitor] $(date -u +%Y-%m-%dT%H:%M:%SZ) selecting best checkpoint per run" | tee -a "${LOG_ROOT}/monitor.log"
"${PYTHON}" - "${RUN_BASE}" "${ALL_OUT}" "${BEST_LINK_BASE}" <<'PY'
import json
import os
import shutil
import sys
from pathlib import Path

run_base = Path(sys.argv[1])
all_out = Path(sys.argv[2])
best_link_base = Path(sys.argv[3])
payload = json.loads((all_out / "summary.json").read_text())

by_run = {}
for item in payload.get("summaries", []):
    by_run.setdefault(item["run_name"], []).append(item)

records = []
best_link_base.mkdir(parents=True, exist_ok=True)
for run_name, items in sorted(by_run.items()):
    best = max(
        items,
        key=lambda x: (
            float(x["success_rate"]),
            -float(x["mean_steps"]),
            int(x["epoch"]),
        ),
    )
    dst = best_link_base / run_name
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(run_base / run_name / "run_meta.json", dst / "run_meta.json")
    link = dst / f"epoch_{int(best['epoch']):04d}.pt"
    if link.exists() or link.is_symlink():
        link.unlink()
    os.symlink(best["checkpoint"], link)
    records.append(
        {
            "run_name": run_name,
            "selected_epoch": int(best["epoch"]),
            "all_rollout_successes": int(best["successes"]),
            "all_rollout_num_rollouts": int(best["num_rollouts"]),
            "all_rollout_success_rate": float(best["success_rate"]),
            "all_rollout_manifest": best["manifest"],
            "all_rollout_video_dir": best["video_dir"],
            "checkpoint": best["checkpoint"],
            "linked_checkpoint": str(link),
        }
    )

(best_link_base / "best_selection.json").write_text(json.dumps(records, indent=2) + "\n")
print(json.dumps({"event": "best_selection", "num_runs": len(records), "records": records}, indent=2))
PY

echo "[monitor] $(date -u +%Y-%m-%dT%H:%M:%SZ) starting best-50 rollout" | tee -a "${LOG_ROOT}/monitor.log"
run_rollout_workers "${BEST_LINK_BASE}" "${BEST_OUT}" "${BEST_NUM_ROLLOUTS}" "${START_SEED_BEST}" "${BEST_NUM_WORKERS}" "best50"
"${PYTHON}" "${ROLLOUT_SCRIPT}" \
  --mode summarize \
  --run-base "${BEST_LINK_BASE}" \
  --train-module "${TRAIN_MODULE}" \
  --output-root "${BEST_OUT}" \
  > "${LOG_ROOT}/best50_summarize.log" 2>&1

"${PYTHON}" - "${ALL_OUT}" "${BEST_OUT}" "${BEST_LINK_BASE}" "${REPORT}" <<'PY'
import json
import sys
from pathlib import Path

all_out = Path(sys.argv[1])
best_out = Path(sys.argv[2])
best_link_base = Path(sys.argv[3])
report = Path(sys.argv[4])

selection = json.loads((best_link_base / "best_selection.json").read_text())
best_payload = json.loads((best_out / "summary.json").read_text())
best50 = {item["run_name"]: item for item in best_payload.get("summaries", [])}

rows = []
for item in selection:
    run_name = item["run_name"]
    eval50 = best50.get(run_name, {})
    rows.append(
        {
            **item,
            "best50_successes": int(eval50.get("successes", 0)),
            "best50_num_rollouts": int(eval50.get("num_rollouts", 0)),
            "best50_success_rate": float(eval50.get("success_rate", 0.0)),
            "best50_mean_steps": float(eval50.get("mean_steps", 0.0)),
            "best50_manifest": eval50.get("manifest", ""),
            "best50_video_dir": eval50.get("video_dir", ""),
        }
    )

overall = max(rows, key=lambda x: (x["best50_success_rate"], -x["best50_mean_steps"])) if rows else None
report.parent.mkdir(parents=True, exist_ok=True)
with report.open("w", encoding="utf-8") as f:
    f.write("# SmolVLA Four-Way Rollout Report\n\n")
    f.write(f"- All-checkpoint rollout root: `{all_out}`\n")
    f.write(f"- Best-50 rollout root: `{best_out}`\n")
    f.write(f"- Best link base: `{best_link_base}`\n\n")
    if overall:
        f.write(
            f"- Overall best by 50-rollout success: `{overall['run_name']}` epoch "
            f"{overall['selected_epoch']} with {overall['best50_successes']}/"
            f"{overall['best50_num_rollouts']} = {overall['best50_success_rate']:.3f}\n\n"
        )
    f.write("| Run | Selected epoch | 20-rollout success | 50-rollout success | 50 mean steps | 50 videos |\n")
    f.write("| --- | ---: | ---: | ---: | ---: | --- |\n")
    for row in rows:
        f.write(
            f"| `{row['run_name']}` | {row['selected_epoch']} | "
            f"{row['all_rollout_successes']}/{row['all_rollout_num_rollouts']} = "
            f"{row['all_rollout_success_rate']:.3f} | "
            f"{row['best50_successes']}/{row['best50_num_rollouts']} = "
            f"{row['best50_success_rate']:.3f} | "
            f"{row['best50_mean_steps']:.2f} | `{row['best50_video_dir']}` |\n"
        )
    f.write("\n")
    f.write("## Manifests\n\n")
    for row in rows:
        f.write(f"- `{row['run_name']}` 20-rollout manifest: `{row['all_rollout_manifest']}`\n")
        f.write(f"- `{row['run_name']}` 50-rollout manifest: `{row['best50_manifest']}`\n")

print(json.dumps({"event": "report", "report": str(report), "rows": rows}, indent=2))
PY

echo "[monitor] $(date -u +%Y-%m-%dT%H:%M:%SZ) done report=${REPORT}" | tee -a "${LOG_ROOT}/monitor.log"
