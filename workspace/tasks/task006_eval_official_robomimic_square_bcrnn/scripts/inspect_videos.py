#!/usr/bin/env python3
"""Inspect rollout videos with imageio and write a small JSON manifest."""

import argparse
import json
import os

import imageio.v2 as imageio


def inspect_video(path):
    reader = imageio.get_reader(path)
    meta = reader.get_meta_data()
    first_frame = reader.get_data(0)
    try:
        frames = reader.count_frames()
    except Exception as exc:
        frames = f"unavailable: {exc}"
    reader.close()
    return {
        "path": path,
        "size_bytes": os.path.getsize(path),
        "frames": frames,
        "first_frame_shape": list(first_frame.shape),
        "fps": meta.get("fps"),
        "duration": meta.get("duration"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("videos", nargs="+")
    args = parser.parse_args()

    manifest = [inspect_video(path) for path in args.videos]
    with open(args.output, "w", encoding="utf-8") as f:
        for item in manifest:
            f.write(json.dumps(item, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
