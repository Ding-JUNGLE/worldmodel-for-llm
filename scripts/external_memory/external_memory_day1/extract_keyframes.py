#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from memory_utils import ensure_dir, read_video_info, sample_frames, save_frame, triplet_indices, uniform_indices


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--mode", choices=["uniform", "triplet"], default="uniform")
    parser.add_argument("--num_keyframes", type=int, default=8)
    args = parser.parse_args()

    info = read_video_info(args.video)
    frame_count = info["frame_count"]
    if args.mode == "triplet":
        indices = triplet_indices(frame_count)
    else:
        indices = uniform_indices(frame_count, args.num_keyframes)

    frames = sample_frames(args.video, indices)
    out_dir = ensure_dir(args.out_dir)
    manifest_path = out_dir / "manifest.csv"
    with manifest_path.open("w", encoding="utf-8") as manifest:
        manifest.write("memory_id,frame_index,frame_path\n")
        for idx, (frame_index, frame) in enumerate(zip(indices, frames)):
            out_path = out_dir / f"keyframe_{idx:06d}.png"
            save_frame(frame, out_path)
            manifest.write(f"{idx},{frame_index},{out_path}\n")
            print(f"[KEYFRAME] {frame_index} -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
