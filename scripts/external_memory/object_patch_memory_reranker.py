#!/usr/bin/env python3
"""Object-level patch reranker for external memory candidates.

This script is a pure external-memory reranker. It does not modify
Matrix-Game-2 internals.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

from memory_utils import (
    create_encoder,
    ensure_parent,
    normalize_features,
    path_for_report,
    read_jsonl,
    read_video_info,
    sample_frames,
    uniform_indices,
    write_csv,
)


@dataclass
class MemoryItem:
    memory_id: int
    crop_path: Path
    feature: np.ndarray
    source: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Object-patch memory reranker")
    parser.add_argument("--memory_crops_dir", required=True)
    parser.add_argument("--candidates_dir", required=True)
    parser.add_argument("--out_csv", required=True)
    parser.add_argument("--out_json", required=True)
    parser.add_argument("--out_contact_sheet", required=True)
    parser.add_argument("--encoder", default="auto", choices=["auto", "dinov2", "clip", "torchvision", "rgb"])
    parser.add_argument("--num_frames", type=int, default=8)
    parser.add_argument("--patch_grid", type=int, default=4)
    parser.add_argument("--top_k", type=int, default=3)
    parser.add_argument("--out_html", default="", help="Optional simple text html path")
    return parser.parse_args()


def _parse_seed(path: Path) -> int:
    match = re.search(r"seed(\d+)", path.stem.replace("-", "_"))
    return int(match.group(1)) if match else -1


def _resolve_path(base_dir: Path, value: str) -> Path | None:
    raw = Path(value)
    if raw.exists():
        return raw
    if raw.is_absolute():
        return None

    candidate_roots = [base_dir, base_dir.parent]
    candidate_roots.extend(base_dir.parents)
    for root in candidate_roots:
        candidate = root / raw
        if candidate.exists():
            return candidate

    basename = raw.name
    for root in candidate_roots:
        for hit in root.rglob(basename):
            return hit
    return None


def _read_memory_records(memory_root: Path) -> list[dict]:
    for p in sorted(memory_root.rglob("*.jsonl")):
        try:
            items = read_jsonl(p)
        except Exception:
            continue
        if items and any("crop_path" in item for item in items):
            return items
    return []


def _collect_memory_records(memory_root: Path) -> list[dict]:
    records = _read_memory_records(memory_root)
    if records:
        return records
    paths = sorted(
        p
        for p in memory_root.rglob("*")
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )
    return [{"memory_id": idx, "crop_path": str(path)} for idx, path in enumerate(paths)]


def _load_memory_items(memory_root: Path, encoder) -> tuple[list[MemoryItem], str]:
    records = _collect_memory_records(memory_root)
    if not records:
        raise RuntimeError("FAIL_OBJECT_PATCH_MEMORY: no memory crops found")

    requested_encoder = None
    for item in records:
        raw_encoder = str(item.get("encoder", "")).strip().lower()
        if raw_encoder:
            requested_encoder = raw_encoder
            break

    if requested_encoder in {"torchvision_resnet18", "torchvision"}:
        requested_encoder = "torchvision"
    elif requested_encoder:
        requested_encoder = requested_encoder.replace("_local", "")

    memory_items: list[MemoryItem] = []
    missing_feature_items: list[MemoryItem] = []
    for idx, raw in enumerate(records):
        memory_id = int(raw.get("memory_id", idx))
        crop_path = _resolve_path(memory_root, str(raw.get("crop_path", raw.get("frame_path", ""))))
        if crop_path is None or not crop_path.exists():
            raise RuntimeError(f"FAIL_OBJECT_PATCH_MEMORY: missing crop {raw.get('crop_path')}")

        feature = None
        feature_path = raw.get("feature_path")
        if feature_path:
            resolved = _resolve_path(memory_root, str(feature_path))
            if resolved and resolved.exists():
                feature = np.load(resolved).astype(np.float32)
        memory_items.append(
            MemoryItem(
                memory_id=memory_id,
                crop_path=crop_path,
                feature=feature,
                source=str(raw.get("tag", raw.get("source", "unknown"))),
            )
        )

    missing_feature_items = [item for item in memory_items if item.feature is None]
    if missing_feature_items:
        encoded = encoder.encode_images([Image.open(item.crop_path).convert("RGB") for item in missing_feature_items])
        for item, vec in zip(missing_feature_items, encoded):
            item.feature = vec.astype(np.float32)

    if any(item.feature is None for item in memory_items):
        raise RuntimeError("FAIL_OBJECT_PATCH_MEMORY: failed to build all memory features")

    if requested_encoder is None:
        requested_encoder = encoder.spec.name
    return memory_items, requested_encoder


def _frame_patches(frame: np.ndarray, grid: int) -> list[tuple[int, tuple[int, int, int, int], np.ndarray]]:
    h, w = frame.shape[:2]
    cell_h = max(1, h // grid)
    cell_w = max(1, w // grid)
    patches: list[tuple[int, tuple[int, int, int, int], np.ndarray]] = []
    patch_idx = 0
    for r in range(grid):
        y0 = r * cell_h
        y1 = h if r == grid - 1 else (r + 1) * cell_h
        for c in range(grid):
            x0 = c * cell_w
            x1 = w if c == grid - 1 else (c + 1) * cell_w
            patch = frame[y0:y1, x0:x1]
            if patch.size == 0:
                continue
            patches.append((patch_idx, (x0, y0, x1, y1), patch))
            patch_idx += 1
    return patches


def _patch_similarity_matrix(patch_features: np.ndarray, memory_features: np.ndarray) -> np.ndarray:
    p = normalize_features(np.asarray(patch_features, dtype=np.float32))
    m = normalize_features(np.asarray(memory_features, dtype=np.float32))
    return p @ m.T


def run_object_patch_rerank(
    memory_items: list[MemoryItem],
    candidates_dir: Path,
    num_frames: int,
    patch_grid: int,
    top_k: int,
    encoder,
) -> tuple[list[dict], int, str, str]:
    if patch_grid < 1:
        raise ValueError("patch_grid must be >= 1")
    if top_k < 1:
        raise ValueError("top_k must be >= 1")

    memory_features = np.stack([item.feature for item in memory_items], axis=0)
    candidate_paths = sorted(
        p
        for p in candidates_dir.glob("candidate_seed*.mp4")
        if not p.stem.endswith("_icon") and "preview" not in p.name
    )
    if not candidate_paths:
        raise RuntimeError("FAIL_OBJECT_PATCH_MEMORY: no candidate_seed*.mp4 found")

    preview_root = ensure_parent(Path("/tmp")) / "object_patch_memory_rerank"
    preview_root.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for candidate_path in candidate_paths:
        seed = _parse_seed(candidate_path)
        info = read_video_info(candidate_path)
        if info["frame_count"] <= 0:
            continue

        sample_indices = uniform_indices(info["frame_count"], max(1, min(num_frames, info["frame_count"])) )
        sampled_frames = sample_frames(candidate_path, sample_indices)

        frame_scores: list[float] = []
        best_frame_index = -1
        best_patch_index = -1
        best_patch_path = ""
        best_frame_path = ""
        best_score = -1.0

        for local_frame_idx, (frame_index, frame_rgb) in enumerate(zip(sample_indices, sampled_frames)):
            patches = _frame_patches(np.asarray(frame_rgb), patch_grid)
            if not patches:
                continue
            patch_images = [Image.fromarray(item[2]).convert("RGB") for item in patches]
            patch_features = encoder.encode_images(patch_images)
            sims = _patch_similarity_matrix(patch_features, memory_features)
            per_patch_max = np.max(sims, axis=1)
            frame_top_k = np.sort(per_patch_max)[-min(top_k, len(per_patch_max)) :]
            frame_score = float(np.mean(frame_top_k))
            frame_scores.append(frame_score)

            flat_best = int(np.argmax(sims))
            local_patch_idx, _ = divmod(flat_best, sims.shape[1])
            local_best = float(sims.flat[flat_best])
            if local_best > best_score:
                best_score = local_best
                best_frame_index = frame_index
                best_patch_index = local_frame_idx * len(patches) + local_patch_idx
                patch_img = Image.fromarray(patches[local_patch_idx][2])
                best_patch_path = str(preview_root / f"seed{seed}_best_patch.png")
                patch_img.save(best_patch_path)
                best_frame_path = str(preview_root / f"seed{seed}_frame{frame_index}.png")
                Image.fromarray(frame_rgb).save(best_frame_path)

        if not frame_scores:
            continue

        object_memory_score = float(np.mean(frame_scores))
        max_patch_similarity = float(max(frame_scores))
        threshold = 0.7 * max_patch_similarity if max_patch_similarity > 0 else 0.0
        temporal_coverage_count = sum(1 for v in frame_scores if v >= threshold)

        rows.append(
            {
                "candidate_seed": str(seed),
                "candidate_path": path_for_report(candidate_path),
                "object_memory_score": f"{object_memory_score:.6f}",
                "best_frame_index": str(best_frame_index),
                "best_patch_index": str(best_patch_index),
                "score_margin": "",
                "rank": "",
                "selected": "0",
                "best_patch_path": best_patch_path,
                "notes": "object_patch_reranker_v1",
                "max_patch_similarity": f"{max_patch_similarity:.6f}",
                "temporal_coverage_count": str(temporal_coverage_count),
                "best_frame_path": best_frame_path,
            }
        )

    if not rows:
        raise RuntimeError("FAIL_OBJECT_PATCH_MEMORY: scored zero candidates")

    ranked = sorted(rows, key=lambda x: float(x["object_memory_score"]), reverse=True)
    for rank, row in enumerate(ranked, start=1):
        row["rank"] = str(rank)
        row["selected"] = "1" if rank == 1 else "0"

    margin = 0.0
    if len(ranked) > 1:
        margin = float(ranked[0]["object_memory_score"]) - float(ranked[1]["object_memory_score"])
    ranked[0]["score_margin"] = f"{margin:.6f}"

    return ranked, int(ranked[0]["candidate_seed"]), ranked[0]["object_memory_score"], f"{margin:.6f}"


def _build_contact_sheet(rows: list[dict], out_path: Path) -> None:
    if not rows:
        ensure_parent(out_path)
        Image.new("RGB", (900, 220), color=(245, 245, 245)).save(out_path)
        return

    columns = min(4, len(rows))
    cell_w, cell_h = 220, 220
    rows_num = int(np.ceil(len(rows) / columns))
    canvas = Image.new("RGB", (columns * cell_w, rows_num * cell_h + 40), color=(250, 250, 250))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, columns * cell_w, 30), fill=(45, 45, 45))
    draw.text((10, 8), "Object Patch Memory Reranker", fill=(255, 255, 255))

    for idx, row in enumerate(rows):
        col = idx % columns
        r = idx // columns
        x = col * cell_w + 8
        y = r * cell_h + 38

        frame_path = row.get("best_frame_path", "")
        if frame_path and Path(frame_path).exists():
            frame_img = Image.open(frame_path).convert("RGB")
        else:
            frame_img = Image.new("RGB", (180, 100), color=(238, 238, 238))
        frame_img = ImageOps.contain(frame_img, (180, 100))
        canvas.paste(frame_img, (x, y))

        patch_path = row.get("best_patch_path", "")
        if patch_path and Path(patch_path).exists():
            patch_img = Image.open(patch_path).convert("RGB")
        else:
            patch_img = Image.new("RGB", (90, 60), color=(220, 220, 220))
        patch_img = ImageOps.contain(patch_img, (90, 50))
        canvas.paste(patch_img, (x + 120, y + 108))

        text = (
            f"seed={row['candidate_seed']} score={row['object_memory_score']}\n"
            f"frame={row['best_frame_index']} patch={row['best_patch_index']} rank={row['rank']}\n"
            f"selected={row['selected']}"
        )
        draw.text((x, y + 102), text, fill=(20, 20, 20))

    ensure_parent(out_path)
    canvas.save(out_path)


def main() -> int:
    args = parse_args()
    memory_root = Path(args.memory_crops_dir).expanduser().resolve()
    candidates_dir = Path(args.candidates_dir).expanduser().resolve()

    if args.patch_grid < 1 or args.num_frames < 1 or args.top_k < 1:
        raise ValueError("patch_grid, num_frames, top_k must be >= 1")

    # Build encoder from explicit request and then memory metadata can keep same encoder.
    encoder = create_encoder(args.encoder)
    memory_items, memory_encoder = _load_memory_items(memory_root, encoder)

    ranked_rows, selected_seed, selected_score, score_margin = run_object_patch_rerank(
        memory_items=memory_items,
        candidates_dir=candidates_dir,
        num_frames=args.num_frames,
        patch_grid=args.patch_grid,
        top_k=args.top_k,
        encoder=encoder,
    )

    write_csv(
        args.out_csv,
        [
            "candidate_seed",
            "candidate_path",
            "object_memory_score",
            "best_frame_index",
            "best_patch_index",
            "score_margin",
            "rank",
            "selected",
            "best_patch_path",
            "best_frame_path",
            "notes",
            "max_patch_similarity",
            "temporal_coverage_count",
        ],
        ranked_rows,
    )

    ensure_parent(args.out_json)
    Path(args.out_json).write_text(
        json.dumps(
            {
                "encoder": memory_encoder,
                "memory_crops_dir": str(memory_root),
                "candidates_dir": str(candidates_dir),
                "num_frames": args.num_frames,
                "patch_grid": args.patch_grid,
                "top_k": args.top_k,
                "memory_entries": len(memory_items),
                "selected_seed": selected_seed,
                "selected_score": selected_score,
                "score_margin": score_margin,
                "rows": ranked_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    _build_contact_sheet(ranked_rows, Path(args.out_contact_sheet))

    if args.out_html:
        ensure_parent(args.out_html)
        lines = []
        for row in ranked_rows:
            lines.append(
                f"seed={row['candidate_seed']} score={row['object_memory_score']} "
                f"rank={row['rank']} selected={row['selected']}"
            )
        Path(args.out_html).write_text("\n".join(lines), encoding="utf-8")

    print(f"ENCODER={encoder.spec.name}")
    print(f"SELECTED_SEED={selected_seed}")
    print(f"SELECTED_SCORE={selected_score}")
    print(f"WROTE {args.out_csv}")
    print(f"WROTE {args.out_json}")
    print(f"WROTE {args.out_contact_sheet}")
    if args.out_html:
        print(f"WROTE {args.out_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
