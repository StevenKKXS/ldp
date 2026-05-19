#!/usr/bin/env bash
set -euo pipefail

LOG_BASE="${LOG_BASE:-/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/downstream_logs/20260519_session10}"
PID_FILE="${PID_FILE:-${LOG_BASE}/pids.tsv}"

if [[ ! -f "${PID_FILE}" ]]; then
  echo "Missing PID file: ${PID_FILE}" >&2
  exit 1
fi

printf "exp_id\tpid\tstate\tjson_lines\tlast_json\n"
tail -n +2 "${PID_FILE}" | while IFS=$'\t' read -r exp_id pid gpu log_path output_dir; do
  if kill -0 "${pid}" 2>/dev/null; then
    state="running"
  else
    state="exited"
  fi
  json_path="${output_dir}/logs.json.txt"
  if [[ -f "${json_path}" ]]; then
    json_lines="$(wc -l < "${json_path}")"
    last_json="$(tail -n 1 "${json_path}" | tr '\t' ' ' | cut -c 1-260)"
  else
    json_lines=0
    if [[ -f "${log_path}" ]]; then
      last_json="$(
        tail -c 3000 "${log_path}" \
          | tr '\r' '\n' \
          | grep -a -v '^$' \
          | tail -n 1 \
          | tr '\t' ' ' \
          | cut -c 1-220
      )"
    else
      last_json="log_missing"
    fi
  fi
  printf "%s\t%s\t%s\t%s\t%s\n" "${exp_id}" "${pid}" "${state}" "${json_lines}" "${last_json}"
done
