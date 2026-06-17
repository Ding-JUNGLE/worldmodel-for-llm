#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Sequence

import numpy as np
from PIL import Image

from effectiveness_utils import (
    create_encoder,
    ensure_dir,
    ensure_parent,
    path_for_report,
    read_frame_at,
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
    return int(stem.split("seed")[-1].split("_")[0])


def cosine_similarity(query: np.ndarray, bank: np.ndarray) -> np.ndarray:
    query = query.astype(np.float32)
    bank = bank.astype(np.float32)
    query = query / max(np.linalg.norm(query), 1e-8)
    bank = bank / np.maximum(np.linalg.norm(bank, axis=1, keepdims=True), 1e-8)
    return bank @ query


def build_strategy_rows(
    strategy: str,
    candidate_paths: Sequence[Path],
    memory_items: list[dict],
    encoder_name: str,
    top_k: int,
    sampled_frames: int,
    out_topk_csv: Path,
    out_rerank_csv: Path,
    out_selected: Path,
    notes: str,
) -> tuple[dict, list[dict]]:
    encoder = create_encoder(encoder_name)
    memory_features = np.stack([np.load(item["feature_path"]).astype(np.float32) for item in memory_items], axis=0)

    topk_rows: list[dict] = []
    rerank_rows: list[dict] = []
    best_row: dict | None = None

    for candidate_path in candidate_paths:
        seed = parse_seed(candidate_path)
        info = read_video_info(candidate_path)
        query_frame = read_frame_at(candidate_path, info["frame_count"] - 1)
        query_feature = encoder.encode_images([Image.fromarray(query_frame).convert("RGB")])[0]
        sims = cosine_similarity(query_feature, memory_features)
        ranked_indices = list(np.argsort(-sims))[: min(top_k, len(memory_items))]
        retrieved_items = [memory_items[idx] for idx in ranked_indices]
        retrieved_features = np.stack([memory_features[idx] for idx in ranked_indices], axis=0)

        for rank, idx in enumerate(ranked_indices, start=1):
            item = memory_items[idx]
            topk_rows.append(
                {
                    "strategy": strategy,
                    "candidate_seed": seed,
                    "rank": rank,
                    "memory_id": item["memory_id"],
                    "frame_index": item["frame_index"],
                    "similarity_score": f"{float(sims[idx]):.6f}",
                    "frame_path": item["frame_path"],
                    "feature_path": item["feature_path"],
                }
            )

        sample_indices = uniform_indices(info["frame_count"], min(sampled_frames, info["frame_count"]))
        sampled = sample_frames(candidate_path, sample_indices)
        sampled_features = encoder.encode_images([Image.fromarray(frame).convert("RGB") for frame in sampled])
        frame_scores = []
        for feature in sampled_features:
            frame_scores.append(float(np.max(cosine_similarity(feature, retrieved_features))))
        memory_score = float(np.mean(frame_scores))
        row = {
            "candidate_path": path_for_report(candidate_path),
            "seed": seed,
            "num_sampled_frames": len(sampled),
            "memory_score": f"{memory_score:.6f}",
            "selected": "0",
        }
        rerank_rows.append(row)
        if best_row is None or float(row["memory_score"]) > float(best_row["memory_score"]):
            best_row = row

    assert best_row is not None
    for row in rerank_rows:
        row["selected"] = "1" if row["candidate_path"] == best_row["candidate_path"] else "0"

    ensure_parent(out_topk_csv)
    ensure_parent(out_rerank_csv)
    ensure_parent(out_selected)
    write_csv(
        out_topk_csv,
        ["strategy", "candidate_seed", "rank", "memory_id", "frame_index", "similarity_score", "frame_path", "feature_path"],
        topk_rows,
    )
    write_csv(out_rerank_csv, ["candidate_path", "seed", "num_sampled_frames", "memory_score", "selected"], rerank_rows)
    shutil.copy2(Path(best_row["candidate_path"]), out_selected)

    summary = {
        "strategy": strategy,
        "selected_seed": int(best_row["seed"]),
        "selected_video": best_row["candidate_path"],
        "memory_score": best_row["memory_score"],
        "notes": notes,
    }
    return summary, rerank_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory_bank", required=True)
    parser.add_argument("--candidates_dir", required=True)
    parser.add_argument("--strategies_dir", required=True)
    parser.add_argument("--rerank_dir", required=True)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--sampled_frames", type=int, default=6)
    parser.add_argument("--random_seed", type=int, default=123)
    args = parser.parse_args()

    memory_bank = read_jsonl(args.memory_bank)
    if len(memory_bank) < 3:
        raise SystemExit("FAIL_MEMORY_ABLATION: insufficient first-visit memory")
    encoder_name = memory_bank[0]["encoder"]

    candidates_dir = Path(args.candidates_dir)
    candidate_paths = sorted(
        path for path in candidates_dir.glob("candidate_seed*.mp4") if not path.stem.endswith("_icon")
    )
    if len(candidate_paths) < 2:
        raise SystemExit("FAIL_CANDIDATE_GENERATION: fewer than 2 candidate videos")

    strategies_dir = ensure_dir(args.strategies_dir)
    rerank_dir = ensure_dir(args.rerank_dir)
    rng = np.random.default_rng(args.random_seed)

    full_memory = list(memory_bank)
    recent_only = list(memory_bank[-min(3, len(memory_bank)):])
    random_count = min(3, len(memory_bank))
    random_indices = sorted(rng.choice(len(memory_bank), size=random_count, replace=False).tolist())
    random_memory = [memory_bank[idx] for idx in random_indices]

    selection_rows = [
        {
            "strategy": "no_memory",
            "selected_seed": parse_seed(candidate_paths[0]),
            "selected_video": path_for_report(candidate_paths[0]),
            "memory_score": "",
            "notes": "Default seed0 baseline under weak revisit proxy.",
        }
    ]

    configs = [
        ("full_memory", full_memory, "All first-visit landmark keyframes."),
        ("recent_only", recent_only, "Last first-visit keyframes only; proxy for recency-biased memory."),
        ("random_memory", random_memory, f"Random memory ids: {','.join(str(item['memory_id']) for item in random_memory)}."),
    ]
    for strategy, items, notes in configs:
        summary, _ = build_strategy_rows(
            strategy=strategy,
            candidate_paths=candidate_paths,
            memory_items=items,
            encoder_name=encoder_name,
            top_k=args.top_k,
            sampled_frames=args.sampled_frames,
            out_topk_csv=strategies_dir / f"{strategy}_topk.csv",
            out_rerank_csv=rerank_dir / f"rerank_scores_{strategy}.csv",
            out_selected=rerank_dir / f"selected_{strategy}.mp4",
            notes=notes,
        )
        selection_rows.append(summary)

    write_csv(
        rerank_dir / "selection_summary.csv",
        ["strategy", "selected_seed", "selected_video", "memory_score", "notes"],
        selection_rows,
    )
    print(f"WROTE {rerank_dir / 'selection_summary.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
