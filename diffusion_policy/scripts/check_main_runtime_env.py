#!/usr/bin/env python
"""Preflight check for the main PTP / RoboMimic runtime."""

import argparse
import importlib
import sys


EXPECTED_PYTHON = (3, 9)
EXPECTED_ROBOMIMIC = "0.2.0"


def fail(message):
    print(f"[FAIL] {message}")
    return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-cuda",
        action="store_true",
        help="Fail if torch imports but CUDA is unavailable.",
    )
    args = parser.parse_args()

    print(f"python_executable={sys.executable}")
    print(f"python_version={sys.version.replace(chr(10), ' ')}")

    if sys.version_info[:2] != EXPECTED_PYTHON:
        return fail(
            f"expected Python {EXPECTED_PYTHON[0]}.{EXPECTED_PYTHON[1]}, "
            f"got {sys.version_info.major}.{sys.version_info.minor}"
        )

    try:
        robomimic = importlib.import_module("robomimic")
    except Exception as exc:
        return fail(f"robomimic import failed: {exc!r}")

    print(f"robomimic_version={getattr(robomimic, '__version__', 'UNKNOWN')}")
    print(f"robomimic_file={getattr(robomimic, '__file__', 'UNKNOWN')}")
    if getattr(robomimic, "__version__", None) != EXPECTED_ROBOMIMIC:
        return fail(
            f"expected robomimic {EXPECTED_ROBOMIMIC}, "
            f"got {getattr(robomimic, '__version__', None)}"
        )

    try:
        torch = importlib.import_module("torch")
    except Exception as exc:
        return fail(f"torch import failed: {exc!r}")

    cuda_available = torch.cuda.is_available()
    print(f"torch_version={torch.__version__}")
    print(f"cuda_available={cuda_available}")
    if args.require_cuda and not cuda_available:
        return fail("CUDA is required but torch.cuda.is_available() is False")

    print("[OK] main runtime environment matches the py39 / robomimic 0.2.0 requirement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
