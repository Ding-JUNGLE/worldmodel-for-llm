#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
DAY1_DIR = THIS_DIR.parent / "external_memory_day1"
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
if str(DAY1_DIR) not in sys.path:
    sys.path.insert(0, str(DAY1_DIR))

from memory_utils import (  # noqa: E402
    BaseEncoder,
    create_encoder,
    ensure_dir,
    ensure_parent,
    frame_to_base64,
    image_to_base64,
    make_html_page,
    normalize_features,
    path_for_report,
    read_frame_at,
    read_jsonl,
    read_video_info,
    sample_frames,
    save_frame,
    save_json,
    triplet_indices,
    uniform_indices,
    write_csv,
    write_jsonl,
)


def write_text(path: str | Path, text: str) -> None:
    ensure_parent(path)
    Path(path).write_text(text, encoding="utf-8")
