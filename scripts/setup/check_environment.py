#!/usr/bin/env python3
"""Lightweight environment validator for matrix game memory tutorial."""

from __future__ import annotations

import os
import platform
import sys


def _check_import(name: str) -> bool:
    try:
        __import__(name)
        print(f"PASS import {name}")
        return True
    except Exception as err:
        print(f"FAIL import {name}: {err}")
        return False


def main() -> int:
    ok = True

    version = platform.python_version()
    print(f"Python version: {version}")
    if not version.startswith("3.10"):
        print("WARN Python version is recommended to be 3.10.x")

    for pkg in ["torch", "torchvision", "typing_extensions"]:
        if not _check_import(pkg):
            ok = False

    import torch

    print(f"torch CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"torch CUDA device count: {torch.cuda.device_count()}")

    print(f"Current working directory: {os.getcwd()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
