#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from effectiveness_utils import (
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
    write_text,
)


def cosine_similarity(query: np.ndarray, bank: np.ndarray) -> np.ndarray:
    query = query.astype(np.float32)
    bank = bank.astype(np.float32)
    query = query / max(np.linalg.norm(query), 1e-8)
    bank = bank / np.maximum(np.linalg.norm(bank, axis=1, keepdims=True), 1e-8)
    return bank @ query


class ResNet50Encoder:
    def __init__(self):
        import torch
        from torchvision.models import ResNet50_Weights, resnet50

        weights = ResNet50_Weights.DEFAULT
        self._transform = weights.transforms()
        self._torch = torch
        self._model = resnet50(weights=weights)
        self._model.fc = torch.nn.Identity()
        self._model.eval().cpu()
        self.name = "torchvision_resnet50"

    def encode_images(self, images: list[Image.Image]) -> np.ndarray:
        batch = self._torch.stack([self._transform(image.convert("RGB")) for image in images], dim=0)
        with self._torch.inference_mode():
            feats = self._model(batch).detach().cpu().numpy().astype(np.float32)
        norms = np.linalg.norm(feats, axis=1, keepdims=True)
        norms = np.where(norms == 0.0, 1.0, norms)
        return feats / norms


def histogram_similarity(img_a: Image.Image, img_b: Image.Image, bins: int = 8) -> float:
    arr_a = np.asarray(img_a.convert("RGB").resize((224, 224)), dtype=np.float32)
    arr_b = np.asarray(img_b.convert("RGB").resize((224, 224)), dtype=np.float32)
    hist_a, _ = np.histogramdd(arr_a.reshape(-1, 3), bins=bins, range=((0, 255), (0, 255), (0, 255)))
    hist_b, _ = np.histogramdd(arr_b.reshape(-1, 3), bins=bins, range=((0, 255), (0, 255), (0, 255)))
    hist_a = hist_a.reshape(-1)
    hist_b = hist_b.reshape(-1)
    hist_a /= max(np.linalg.norm(hist_a), 1e-8)
    hist_b /= max(np.linalg.norm(hist_b), 1e-8)
    return float(np.dot(hist_a, hist_b))


def build_contact_sheet(reference: Image.Image, method_images: list[tuple[str, Image.Image, str]], out_path: Path) -> None:
    margin = 20
    panel_w = 320
    panel_h = 220
    header_h = 70
    width = margin + (panel_w + margin) * (1 + len(method_images))
    height = header_h + panel_h + 2 * margin
    canvas = Image.new("RGB", (width, height), color=(245, 245, 245))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()

    items = [("First Visit", reference, "reference")] + method_images
    for idx, (label, image, subtitle) in enumerate(items):
        x0 = margin + idx * (panel_w + margin)
        y0 = margin
        draw.text((x0, y0), label, fill=(0, 0, 0), font=font)
        draw.text((x0, y0 + 18), subtitle, fill=(70, 70, 70), font=font)
        panel = image.convert("RGB").copy()
        panel.thumbnail((panel_w, panel_h))
        px = x0
        py = header_h
        canvas.paste(panel, (px, py))
    ensure_parent(out_path)
    canvas.save(out_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first_visit_memory_bank", required=True)
    parser.add_argument("--selection_summary", required=True)
    parser.add_argument("--reference_memory_id", type=int, default=2)
    parser.add_argument("--candidate_start_fraction", type=float, default=0.35)
    parser.add_argument("--num_candidate_samples", type=int, default=6)
    parser.add_argument("--out_csv", required=True)
    parser.add_argument("--out_png", required=True)
    parser.add_argument("--out_html", required=True)
    parser.add_argument("--out_md", required=True)
    args = parser.parse_args()

    memory_bank = read_jsonl(args.first_visit_memory_bank)
    memory_by_id = {int(item["memory_id"]): item for item in memory_bank}
    reference_item = memory_by_id.get(args.reference_memory_id, memory_bank[0])
    reference_path = Path(reference_item["frame_path"])
    reference_image = Image.open(reference_path).convert("RGB")
    independent_encoder = ResNet50Encoder()
    reference_feature = independent_encoder.encode_images([reference_image])[0]

    summary_rows = list(csv.DictReader(Path(args.selection_summary).open("r", encoding="utf-8")))
    methods = [row for row in summary_rows if row["strategy"] in {"no_memory", "recent_only", "random_memory", "full_memory"}]

    result_rows: list[dict] = []
    contact_items: list[tuple[str, Image.Image, str]] = []
    for row in methods:
        method = row["strategy"]
        video_path = Path(row["selected_video"])
        info = read_video_info(video_path)
        start_index = int(round(max(0.0, min(0.95, args.candidate_start_fraction)) * (info["frame_count"] - 1)))
        candidate_indices = np.linspace(start_index, info["frame_count"] - 1, num=min(args.num_candidate_samples, info["frame_count"]))
        indices = sorted({int(round(value)) for value in candidate_indices})
        frames = sample_frames(video_path, indices)
        images = [Image.fromarray(frame).convert("RGB") for frame in frames]
        features = independent_encoder.encode_images(images)
        feature_scores = cosine_similarity(reference_feature, features)
        hist_scores = [histogram_similarity(reference_image, image) for image in images]
        combined_scores = [0.7 * float(fs) + 0.3 * float(hs) for fs, hs in zip(feature_scores, hist_scores)]
        best_idx = int(np.argmax(combined_scores))
        best_frame_index = indices[best_idx]
        best_image = images[best_idx]
        contact_items.append(
            (
                method.replace("_", " ").title(),
                best_image,
                f"seed={row['selected_seed']} feat={feature_scores[best_idx]:.3f} hist={hist_scores[best_idx]:.3f}",
            )
        )
        result_rows.append(
            {
                "method": method,
                "selected_seed": row["selected_seed"],
                "selected_video": row["selected_video"],
                "best_frame_index": best_frame_index,
                "independent_feature_encoder": independent_encoder.name,
                "independent_feature_cosine": f"{float(feature_scores[best_idx]):.6f}",
                "histogram_cosine": f"{float(hist_scores[best_idx]):.6f}",
                "combined_score": f"{float(combined_scores[best_idx]):.6f}",
                "reference_frame": path_for_report(reference_path),
                "selected_frame_note": f"best sampled frame under independent evaluation from frames >= {start_index}",
            }
        )

    write_csv(
        args.out_csv,
        [
            "method",
            "selected_seed",
            "selected_video",
            "best_frame_index",
            "independent_feature_encoder",
            "independent_feature_cosine",
            "histogram_cosine",
            "combined_score",
            "reference_frame",
            "selected_frame_note",
        ],
        result_rows,
    )
    build_contact_sheet(reference_image, contact_items, Path(args.out_png))

    reference64 = frame_to_base64(np.asarray(reference_image))
    method_cards = []
    for label, image, subtitle in contact_items:
        method_cards.append(
            "<div class='card'>"
            f"<img src='data:image/png;base64,{frame_to_base64(np.asarray(image))}' alt='{label}' />"
            f"<p><strong>{label}</strong><br/>{subtitle}</p>"
            "</div>"
        )
    html = make_html_page(
        "Memory Effectiveness Contact Sheet",
        (
            "<h1>Memory Effectiveness Contact Sheet</h1>"
            f"<div class='card' style='max-width:360px;'><img src='data:image/png;base64,{reference64}' alt='reference' />"
            "<p><strong>First-visit landmark reference</strong></p></div>"
            "<h2>Best sampled revisit-proxy frames</h2>"
            f"<div class='grid'>{''.join(method_cards)}</div>"
        ),
    )
    ensure_parent(args.out_html)
    Path(args.out_html).write_text(html, encoding="utf-8")

    manual_table = """| Method | Selected Seed | Landmark Identity | Color Consistency | Layout Consistency | Artifacts | Overall |
|---|---:|---:|---:|---:|---:|---:|
| No memory | 0 | TBD | TBD | TBD | TBD | TBD |
| Recent-only | TBD | TBD | TBD | TBD | TBD | TBD |
| Random memory | TBD | TBD | TBD | TBD | TBD | TBD |
| Full memory | TBD | TBD | TBD | TBD | TBD | TBD |
"""
    write_text(args.out_md, manual_table)
    print(f"WROTE {args.out_csv}")
    print(f"WROTE {args.out_png}")
    print(f"WROTE {args.out_html}")
    print(f"WROTE {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
