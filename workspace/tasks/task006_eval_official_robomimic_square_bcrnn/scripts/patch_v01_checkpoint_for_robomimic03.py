#!/usr/bin/env python3
"""Patch robomimic-v0.1 checkpoint config so robomimic 0.3 can load it.

The official checkpoint weights are left unchanged. This only recursively fills
fields that exist in robomimic 0.3's default BC config but are absent from the
older checkpoint config.
"""

import argparse
import copy
import json

import torch
from robomimic.config import config_factory


def fill_missing(dst, defaults):
    for key, value in defaults.items():
        if key not in dst:
            dst[key] = copy.deepcopy(value)
        elif isinstance(dst[key], dict) and isinstance(value, dict):
            fill_missing(dst[key], value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()

    ckpt = torch.load(args.input, map_location="cpu")
    original_config = json.loads(ckpt["config"])
    default_config = json.loads(str(config_factory(ckpt.get("algo_name", "bc"))))

    patched_config = copy.deepcopy(original_config)
    before = json.dumps(patched_config, sort_keys=True)
    fill_missing(patched_config, default_config)
    after = json.dumps(patched_config, sort_keys=True)

    ckpt["config"] = json.dumps(patched_config, indent=4)
    torch.save(ckpt, args.output)

    summary = {
        "input": args.input,
        "output": args.output,
        "config_changed": before != after,
        "top_level_keys": sorted(patched_config.keys()),
        "algo_keys": sorted(patched_config["algo"].keys()),
        "train_keys": sorted(patched_config["train"].keys()),
    }
    with open(args.summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
