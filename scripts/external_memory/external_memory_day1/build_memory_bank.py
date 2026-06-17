#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from PIL import Image

from memory_utils import create_encoder, ensure_dir, ensure_parent, path_for_report, write_jsonl


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyframes_dir", required=True)
    parser.add_argument("--features_dir", required=True)
    parser.add_argument("--out_jsonl", required=True)
    parser.add_argument("--encoder", default="auto")
    args = parser.parse_args()

    keyframes_dir = Path(args.keyframes_dir)
    frame_paths = sorted(keyframes_dir.glob("keyframe_*.png"))
    if len(frame_paths) < 3:
        raise SystemExit("FAIL_MEMORY_BANK: fewer than 3 keyframes found")
    manifest_path = keyframes_dir / "manifest.csv"
    frame_index_by_name: dict[str, int] = {}
    if manifest_path.exists():
        with manifest_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                frame_index_by_name[Path(row["frame_path"]).name] = int(row["frame_index"])

    encoder = create_encoder(args.encoder)
    features_dir = ensure_dir(args.features_dir)
    images = [Image.open(path).convert("RGB") for path in frame_paths]
    features = encoder.encode_images(images)
    source_video = "baseline_seed42.mp4"

    items: list[dict] = []
    for memory_id, (frame_path, feature) in enumerate(zip(frame_paths, features)):
        feature_path = features_dir / f"{frame_path.stem}.npy"
        ensure_parent(feature_path)
        np.save(feature_path, feature.astype(np.float32))
        frame_index = frame_index_by_name.get(frame_path.name, memory_id)
        items.append(
            {
                "memory_id": memory_id,
                "source_video": source_video,
                "frame_index": frame_index,
                "frame_path": path_for_report(frame_path),
                "feature_path": path_for_report(feature_path),
                "feature_dim": int(feature.shape[0]),
                "encoder": encoder.spec.name,
                "pseudo_pose": [0.0, 0.0, 0.0],
                "action_tag": "baseline_unknown",
                "quality_score": 1.0,
            }
        )
    write_jsonl(args.out_jsonl, items)
    print(f"ENCODER={encoder.spec.name}")
    print(f"MEMORY_ITEMS={len(items)}")
    print(f"WROTE {args.out_jsonl}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
