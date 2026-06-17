#!/usr/bin/env python3
"""Simple contact sheet checker used in the tutorial."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contact_sheet", required=True)
    args = parser.parse_args()

    p = Path(args.contact_sheet)
    if p.exists():
        print(f"Found: {p}")
    else:
        print(f"Missing: {p}")


if __name__ == "__main__":
    main()
