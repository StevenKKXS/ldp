# KeepGPU Reservation

Date: 2026-06-05

Purpose: keep two 8xH200 GPU nodes active with about half VRAM per GPU and full reported GPU utility.

## Runtime

Dedicated KeepGPU venv:

```bash
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/keepgpu_py312
```

Installed package versions:

- Python `3.12.3`
- KeepGPU `0.5.1`
- torch `2.5.1+cu124`

Reason for using this venv: KeepGPU `0.5.1` uses Python 3.10+ syntax and cannot run in the main Direction C py39 experiment venv. The first py312 install resolved torch `2.12.0+cu130`, which was incompatible with the current CUDA 12.8 driver. The final venv pins torch `2.5.1+cu124`.

## Active Jobs

| Node | SSH | Hostname | KeepGPU PID | Job ID | GPUs | VRAM setting | Interval | Busy threshold |
|---|---:|---|---:|---|---|---|---:|---:|
| `10.100.2.39` | `23494` | `lg-cmc-b7r201-e03u26-h200-000102` | `501645` | `direction_c_keepgpu_10_100_2_39_20260605` | `0,1,2,3,4,5,6,7` | `70GiB` | `0` | `100` |
| `10.100.4.23` | `21492` | `lg-cmc-b7r201-g03u26-h200-000150` | `3501701` | `direction_c_keepgpu_10_100_4_23_20260605` | `0,1,2,3,4,5,6,7` | `70GiB` | `0` | `100` |

Observed after startup:

- Each H200 reports total memory about `143771 MiB`.
- Each GPU reports used memory about `72302 MiB`.
- Each GPU reports utilization `100%`.

## Status Commands

```bash
KEEPVENV=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/keepgpu_py312

ssh -p 23494 root@10.100.2.39 \
  "$KEEPVENV/bin/keep-gpu status && nvidia-smi --query-gpu=index,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits"

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 21492 root@10.100.4.23 \
  "$KEEPVENV/bin/keep-gpu status && nvidia-smi --query-gpu=index,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits"
```

## Stop Commands

Stop the sessions and daemon on `10.100.2.39`:

```bash
KEEPVENV=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/keepgpu_py312
ssh -p 23494 root@10.100.2.39 \
  "$KEEPVENV/bin/keep-gpu stop --job-id direction_c_keepgpu_10_100_2_39_20260605 && $KEEPVENV/bin/keep-gpu service-stop"
```

Stop the sessions and daemon on `10.100.4.23`:

```bash
KEEPVENV=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/keepgpu_py312
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 21492 root@10.100.4.23 \
  "$KEEPVENV/bin/keep-gpu stop --job-id direction_c_keepgpu_10_100_4_23_20260605 && $KEEPVENV/bin/keep-gpu service-stop"
```
