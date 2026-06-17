#!/usr/bin/env python3
"""Validate Matrix-Game-2 checkpoint layout locally."""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_FILES = [
    "Wan2.1_VAE.pth",
    "models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth",
    "xlm-roberta-large/tokenizer.json",
    "base_distilled_model/base_distill.safetensors",
    "gta_distilled_model/gta_keyboard2dim.safetensors",
    "templerun_distilled_model/templerun_7dim_onlykey.safetensors",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix_game2_root", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.matrix_game2_root)
    ok = True

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            print(f"MISSING: {path}")
            ok = False
            continue
        size = path.stat().st_size
        if size < 1024:
            print(f"TOO_SMALL: {path} ({size} bytes)")
            ok = False
        else:
            print(f"OK: {path} ({size} bytes)")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
