#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator}
REPO=${REPO:-$ROOT/repos/ldp}
VENV=${VENV:-$ROOT/envs/ptp_ldp_py39_ceph}
DATA=${DATA:-$ROOT/datasets/robomimic/datasets/square/mh/image_abs.hdf5}
OUTROOT=${OUTROOT:-$ROOT/outputs/stage2b_square_rollout_stability_nenv8_max4_20260605}
export OUTROOT

N_TEST=${N_TEST:-100}
N_ENVS=${N_ENVS:-8}
MAX_STEPS=${MAX_STEPS:-500}

BASE_CKPT=${BASE_CKPT:-$ROOT/outputs/stage2b_square_causalcond_off_20260526_032417_safe_workers/m1_base_no_context_action8_causalcond_off/checkpoints/epoch=0049-val_loss=0.048735.ckpt}
RANDOM_CKPT=${RANDOM_CKPT:-$ROOT/outputs/stage2b_square_causalcond_off_20260526_032417_safe_workers/m3_random_add_last_action8_causalcond_off/checkpoints/epoch=0024-val_loss=0.058755.ckpt}
ADD_LAST_CKPT=${ADD_LAST_CKPT:-$ROOT/outputs/stage2b_square_causalcond_off_pretrained_cephpast_20260526_144615/m2_pretrained_past_add_last_action8_causalcond_off/checkpoints/epoch=0024-val_loss=0.050084.ckpt}

mkdir -p "$OUTROOT/logs"
cd "$REPO"

export MUJOCO_GL=${MUJOCO_GL:-osmesa}
export PYOPENGL_PLATFORM=${PYOPENGL_PLATFORM:-osmesa}
export MUJOCO_PY_FORCE_CPU=${MUJOCO_PY_FORCE_CPU:-1}
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}
export PYTHONPATH=$REPO:${PYTHONPATH:-}

run_one() {
  local name=$1
  local gpu=$2
  local ckpt=$3
  local seed=$4
  local out=$OUTROOT/$name

  rm -rf "$out"
  echo "START $(date -Is) name=$name gpu=$gpu seed=$seed n_envs=$N_ENVS n_test=$N_TEST"
  CUDA_VISIBLE_DEVICES=$gpu "$VENV/bin/python" eval_flow_matching_rollout.py \
    --checkpoint "$ckpt" \
    --output-dir "$out" \
    --n-test "$N_TEST" \
    --n-envs "$N_ENVS" \
    --test-start-seed "$seed" \
    --max-steps "$MAX_STEPS" \
    --dataset-path "$DATA" \
    --device cuda:0 \
    > "$OUTROOT/logs/$name.log" 2>&1
  local code=$?
  echo "DONE $(date -Is) name=$name code=$code"
  return $code
}

wait_wave() {
  local status=0
  local pid
  for pid in "$@"; do
    wait "$pid" || status=1
  done
  return "$status"
}

status=0

run_one base_e49_seed100000 0 "$BASE_CKPT" 100000 & p1=$!
run_one base_e49_seed200000 1 "$BASE_CKPT" 200000 & p2=$!
run_one base_e49_seed300000 2 "$BASE_CKPT" 300000 & p3=$!
run_one random_add_last_e24_seed100000 3 "$RANDOM_CKPT" 100000 & p4=$!
wait_wave "$p1" "$p2" "$p3" "$p4" || status=1

run_one random_add_last_e24_seed200000 0 "$RANDOM_CKPT" 200000 & p1=$!
run_one random_add_last_e24_seed300000 1 "$RANDOM_CKPT" 300000 & p2=$!
run_one pretrained_add_last_e24_seed100000 2 "$ADD_LAST_CKPT" 100000 & p3=$!
run_one pretrained_add_last_e24_seed200000 3 "$ADD_LAST_CKPT" 200000 & p4=$!
wait_wave "$p1" "$p2" "$p3" "$p4" || status=1

run_one pretrained_add_last_e24_seed300000 0 "$ADD_LAST_CKPT" 300000 || status=1

"$VENV/bin/python" - <<'PY'
import json
import math
import os
import pathlib
import statistics

root = pathlib.Path(os.environ["OUTROOT"])
settings = {
    "base_e49": [
        "base_e49_seed100000",
        "base_e49_seed200000",
        "base_e49_seed300000",
    ],
    "random_add_last_e24": [
        "random_add_last_e24_seed100000",
        "random_add_last_e24_seed200000",
        "random_add_last_e24_seed300000",
    ],
    "pretrained_add_last_e24": [
        "pretrained_add_last_e24_seed100000",
        "pretrained_add_last_e24_seed200000",
        "pretrained_add_last_e24_seed300000",
    ],
}

summary = {}
for setting, names in settings.items():
    means = []
    all_scores = []
    summary[setting] = {"runs": []}
    for name in names:
        path = root / name / "eval_log.json"
        if not path.exists():
            summary[setting]["runs"].append({"name": name, "missing": True})
            continue
        data = json.load(open(path))
        scores = [float(x) for x in data["scores"]]
        mean = sum(scores) / len(scores)
        means.append(mean)
        all_scores.extend(scores)
        summary[setting]["runs"].append(
            {
                "name": name,
                "test_start_seed": data.get("test_start_seed"),
                "n": len(scores),
                "mean": mean,
                "successes": int(sum(scores)),
            }
        )

    if means:
        mean_of_means = sum(means) / len(means)
        sd = statistics.stdev(means) if len(means) > 1 else 0.0
        sem = sd / math.sqrt(len(means)) if len(means) > 1 else 0.0
        pooled = sum(all_scores) / len(all_scores) if all_scores else None
        binom_se = (
            math.sqrt(pooled * (1.0 - pooled) / len(all_scores))
            if pooled is not None and all_scores
            else None
        )
        summary[setting].update(
            {
                "mean_of_3x100": mean_of_means,
                "sd_across_seed_ranges": sd,
                "sem_across_seed_ranges": sem,
                "pooled_mean_300": pooled,
                "pooled_binomial_se": binom_se,
                "total_successes": int(sum(all_scores)),
                "total_n": len(all_scores),
            }
        )

summary_path = root / "summary.json"
json.dump(summary, open(summary_path, "w"), indent=2)
print(json.dumps(summary, indent=2))
PY

exit "$status"
