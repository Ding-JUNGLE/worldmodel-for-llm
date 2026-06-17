#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

from memory_utils import (
    cosine_similarity,
    create_encoder,
    ensure_parent,
    frame_to_base64,
    make_html_page,
    path_for_report,
    read_jsonl,
    read_video_info,
    sample_frames,
    uniform_indices,
    write_csv,
)


def parse_seed(path: Path) -> int:
    stem = path.stem
    if "seed" not in stem:
        return -1
    return int(stem.split("seed")[-1])


def load_retrieved_memory(memory_bank: list[dict], retrieved_csv: str | Path) -> list[dict]:
    by_id = {int(item["memory_id"]): item for item in memory_bank}
    rows: list[dict] = []
    with Path(retrieved_csv).open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            memory_id = int(row["memory_id"])
            merged = dict(by_id[memory_id])
            merged["similarity_score"] = float(row["similarity_score"])
            rows.append(merged)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates_dir", required=True)
    parser.add_argument("--memory_bank", required=True)
    parser.add_argument("--retrieved_csv", required=True)
    parser.add_argument("--out_csv", required=True)
    parser.add_argument("--out_selected", required=True)
    parser.add_argument("--out_html", required=True)
    args = parser.parse_args()

    memory_bank = read_jsonl(args.memory_bank)
    if not memory_bank:
        raise SystemExit("FAIL_RERANKING: empty memory bank")
    retrieved_memory = load_retrieved_memory(memory_bank, args.retrieved_csv)
    if not retrieved_memory:
        raise SystemExit("FAIL_RERANKING: empty retrieved memory set")

    encoder = create_encoder(memory_bank[0]["encoder"])
    retrieved_features = np.stack([np.load(item["feature_path"]).astype(np.float32) for item in retrieved_memory], axis=0)

    candidates_dir = Path(args.candidates_dir)
    candidate_paths = sorted(
        path for path in candidates_dir.glob("candidate_seed*.mp4") if not path.stem.endswith("_icon")
    )
    if len(candidate_paths) < 2:
        raise SystemExit("FAIL_RERANKING: fewer than 2 candidate videos")

    rows: list[dict] = []
    candidate_cards: list[str] = []
    best_row: dict | None = None
    for candidate_path in candidate_paths:
        seed = parse_seed(candidate_path)
        info = read_video_info(candidate_path)
        indices = uniform_indices(info["frame_count"], min(6, max(5, info["frame_count"])))
        frames = sample_frames(candidate_path, indices)
        images = [Image.fromarray(frame).convert("RGB") for frame in frames]
        features = encoder.encode_images(images)
        per_frame_scores = []
        for feature in features:
            sims = cosine_similarity(feature, retrieved_features)
            per_frame_scores.append(float(np.max(sims)))
        memory_score = float(np.mean(per_frame_scores))
        row = {
            "candidate_path": path_for_report(candidate_path),
            "seed": seed,
            "num_sampled_frames": len(frames),
            "memory_score": f"{memory_score:.6f}",
            "selected": "0",
        }
        rows.append(row)
        preview_html = "".join(
            f"<img src='data:image/png;base64,{frame_to_base64(frame, max_size=(220, 220))}' alt='seed_{seed}_frame' />"
            for frame in frames[:4]
        )
        candidate_cards.append(
            "<div class='card'>"
            f"<h3>seed {seed}</h3><p><strong>score</strong>: {memory_score:.6f}</p>"
            f"<div class='grid'>{preview_html}</div>"
            "</div>"
        )
        if best_row is None or float(row["memory_score"]) > float(best_row["memory_score"]):
            best_row = row

    assert best_row is not None
    for row in rows:
        row["selected"] = "1" if row["candidate_path"] == best_row["candidate_path"] else "0"

    selected_src = Path(best_row["candidate_path"])
    ensure_parent(args.out_selected)
    shutil.copy2(selected_src, args.out_selected)
    write_csv(args.out_csv, ["candidate_path", "seed", "num_sampled_frames", "memory_score", "selected"], rows)

    default_seed = min(parse_seed(path) for path in candidate_paths)
    selected_seed = int(best_row["seed"])
    ablation_rows = [
        {
            "method": "no_memory",
            "selected_seed": default_seed,
            "score": next(row["memory_score"] for row in rows if int(row["seed"]) == default_seed),
            "selected_video": next(row["candidate_path"] for row in rows if int(row["seed"]) == default_seed),
            "notes": "Default first candidate.",
        },
        {
            "method": "full_memory",
            "selected_seed": selected_seed,
            "score": best_row["memory_score"],
            "selected_video": best_row["candidate_path"],
            "notes": f"MEMORY_AFFECTS_OUTPUT={'true' if selected_seed != default_seed else 'false'}",
        },
    ]
    ablation_path = Path(args.out_csv).with_name("ablation_summary.csv")
    write_csv(ablation_path, ["method", "selected_seed", "score", "selected_video", "notes"], ablation_rows)

    memory_cards = []
    for item in retrieved_memory:
        img64 = frame_to_base64(np.array(Image.open(item["frame_path"]).convert("RGB")))
        memory_cards.append(
            "<div class='card'>"
            f"<img src='data:image/png;base64,{img64}' alt='memory_{item['memory_id']}' />"
            f"<p><strong>memory_id</strong>: {item['memory_id']}<br/>"
            f"<strong>frame_index</strong>: {item['frame_index']}<br/>"
            f"<strong>retrieval score</strong>: {item['similarity_score']:.6f}</p>"
            "</div>"
        )
    body = (
        "<h1>Memory-based Candidate Reranking</h1>"
        "<h2>Retrieved memory frames</h2>"
        f"<div class='grid'>{''.join(memory_cards)}</div>"
        "<h2>Candidates</h2>"
        f"<div class='grid'>{''.join(candidate_cards)}</div>"
        f"<p><strong>Selected candidate</strong>: <code>{best_row['candidate_path']}</code></p>"
        f"<p><strong>MEMORY_AFFECTS_OUTPUT</strong>: {'true' if selected_seed != default_seed else 'false'}</p>"
    )
    html = make_html_page("Memory-based Candidate Reranking", body)
    ensure_parent(args.out_html)
    Path(args.out_html).write_text(html, encoding="utf-8")
    print(f"WROTE {args.out_csv}")
    print(f"WROTE {args.out_html}")
    print(f"WROTE {args.out_selected}")
    print(f"WROTE {ablation_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
