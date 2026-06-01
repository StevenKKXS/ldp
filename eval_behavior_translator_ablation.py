#!/usr/bin/env python3
"""Evaluate BehaviorTranslator checkpoints under observation modality ablations."""

import argparse
import csv
import json
import pathlib

import dill
import hydra
import torch
from omegaconf import OmegaConf
from torch.utils.data import DataLoader

from diffusion_policy.workspace.train_behavior_translator_workspace import (
    TrainBehaviorTranslatorWorkspace,
)


OmegaConf.register_new_resolver("eval", eval, replace=True)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--dataset-path", default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--num-workers", type=int, default=None)
    parser.add_argument("--max-val-batches", type=int, default=50)
    parser.add_argument(
        "--variants",
        nargs="+",
        default=[
            "baseline",
            "image_zero",
            "image_shuffle",
            "proprio_zero",
            "proprio_shuffle",
        ],
    )
    return parser.parse_args()


def obs_keys(cfg):
    rgb_keys = []
    lowdim_keys = []
    for key, attr in cfg.shape_meta.obs.items():
        if attr.get("type", "low_dim") == "rgb":
            rgb_keys.append(key)
        else:
            lowdim_keys.append(key)
    return rgb_keys, lowdim_keys


def corrupt_obs(obs, variant, rgb_keys, lowdim_keys):
    if variant == "baseline":
        return obs

    result = {k: v.clone() for k, v in obs.items()}
    if variant.startswith("image_"):
        keys = rgb_keys
    elif variant.startswith("proprio_"):
        keys = lowdim_keys
    else:
        raise ValueError(f"Unsupported variant: {variant}")

    if variant.endswith("_zero"):
        for key in keys:
            if key in result:
                result[key].zero_()
    elif variant.endswith("_shuffle"):
        for key in keys:
            if key in result:
                # Deterministic batch-level shuffle preserving marginal values.
                result[key] = torch.roll(result[key], shifts=1, dims=0)
    else:
        raise ValueError(f"Unsupported variant: {variant}")
    return result


def main():
    args = parse_args()
    checkpoint = pathlib.Path(args.checkpoint)
    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = torch.load(checkpoint.open("rb"), pickle_module=dill, map_location="cpu")
    cfg = payload["cfg"]
    if args.dataset_path:
        cfg.task.dataset.base_dataset.dataset_path = args.dataset_path
    if args.batch_size is not None:
        cfg.val_dataloader.batch_size = int(args.batch_size)
    if args.num_workers is not None:
        cfg.val_dataloader.num_workers = int(args.num_workers)
    cfg.val_dataloader.shuffle = False
    cfg.training.device = args.device

    workspace = TrainBehaviorTranslatorWorkspace(cfg, output_dir=str(output_dir))
    workspace.load_payload(payload, exclude_keys=("optimizer",), include_keys=tuple())

    dataset = hydra.utils.instantiate(cfg.task.dataset)
    val_dataset = dataset.get_validation_dataset()
    val_dataloader = DataLoader(val_dataset, **cfg.val_dataloader)
    normalizer = dataset.get_normalizer()

    device = torch.device(args.device)
    workspace.obs_encoder.to(device).eval()
    workspace.model.to(device).eval()
    normalizer.to(device)

    rgb_keys, lowdim_keys = obs_keys(cfg)
    rows = []
    with torch.no_grad():
        for variant in args.variants:
            metrics_list = []
            for batch_idx, batch in enumerate(val_dataloader):
                batch = dict(batch)
                batch["obs"] = corrupt_obs(batch["obs"], variant, rgb_keys, lowdim_keys)
                _, metrics = workspace._compute_batch(batch, normalizer, device)
                metrics_list.append(metrics)
                if args.max_val_batches is not None and batch_idx >= args.max_val_batches - 1:
                    break
            row = {"variant": variant}
            row.update(workspace._mean_metrics(metrics_list))
            rows.append(row)
            print(json.dumps(row, sort_keys=True))

    json_path = output_dir / "ablation_metrics.json"
    csv_path = output_dir / "ablation_metrics.csv"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
