#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from memory_utils import ensure_dir, read_frame_at, read_video_info, save_frame, save_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--out_json", required=True)
    parser.add_argument("--out_dir", required=True)
    args = parser.parse_args()

    try:
        info = read_video_info(args.video)
        if info["frame_count"] <= 0:
            raise RuntimeError("Video reports zero frames.")
    except Exception as exc:
        print(f"FAIL_BASELINE_VIDEO_READ: {exc}", file=sys.stderr)
        return 1

    out_dir = ensure_dir(args.out_dir)
    preview_indices = {
        "first": 0,
        "middle": info["frame_count"] // 2,
        "last": info["frame_count"] - 1,
    }
    preview_paths: dict[str, str] = {}
    for name, index in preview_indices.items():
        frame = read_frame_at(args.video, index)
        out_path = out_dir / f"{name}.png"
        save_frame(frame, out_path)
        preview_paths[name] = str(out_path)

    payload = dict(info)
    payload["preview_frames"] = preview_paths
    save_json(args.out_json, payload)
    print(f"WROTE {args.out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
