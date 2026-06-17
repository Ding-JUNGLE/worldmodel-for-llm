#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from memory_utils import (
    cosine_similarity,
    create_encoder,
    ensure_parent,
    image_to_base64,
    make_html_page,
    path_for_report,
    read_jsonl,
    write_csv,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query_frame", required=True)
    parser.add_argument("--memory_bank", required=True)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--out_csv", required=True)
    parser.add_argument("--out_html", required=True)
    args = parser.parse_args()

    memory_items = read_jsonl(args.memory_bank)
    if len(memory_items) < 1:
        raise SystemExit("FAIL_RETRIEVAL: empty memory bank")

    encoder_name = memory_items[0]["encoder"]
    encoder = create_encoder(encoder_name)
    query_feature = encoder.encode_images([Image.open(args.query_frame).convert("RGB")])[0]

    features = []
    for item in memory_items:
        feature = np.load(item["feature_path"]).astype(np.float32)
        features.append(feature)
    bank = np.stack(features, axis=0)
    scores = cosine_similarity(query_feature, bank)

    ranked = sorted(
        zip(memory_items, scores.tolist()),
        key=lambda pair: pair[1],
        reverse=True,
    )[: args.top_k]
    rows: list[dict] = []
    cards: list[str] = []
    for rank, (item, score) in enumerate(ranked, start=1):
        row = {
            "rank": rank,
            "memory_id": item["memory_id"],
            "frame_index": item["frame_index"],
            "similarity_score": f"{score:.6f}",
            "frame_path": item["frame_path"],
            "feature_path": item["feature_path"],
            "encoder": item["encoder"],
        }
        rows.append(row)
        img64 = image_to_base64(item["frame_path"])
        cards.append(
            "<div class='card'>"
            f"<img src='data:image/png;base64,{img64}' alt='memory_{item['memory_id']}' />"
            f"<p><strong>rank</strong>: {rank}<br/><strong>memory_id</strong>: {item['memory_id']}<br/>"
            f"<strong>frame_index</strong>: {item['frame_index']}<br/><strong>similarity</strong>: {score:.6f}</p>"
            "</div>"
        )

    write_csv(
        args.out_csv,
        ["rank", "memory_id", "frame_index", "similarity_score", "frame_path", "feature_path", "encoder"],
        rows,
    )

    query64 = image_to_base64(args.query_frame)
    body = (
        "<h1>External Memory Retrieval</h1>"
        f"<p><strong>query_frame</strong>: <code>{path_for_report(args.query_frame)}</code></p>"
        f"<div class='card' style='max-width:360px;'><img src='data:image/png;base64,{query64}' alt='query' />"
        "<p><strong>Query frame</strong></p></div>"
        "<h2>Top-k retrieved memory frames</h2>"
        f"<div class='grid'>{''.join(cards)}</div>"
    )
    html = make_html_page("External Memory Retrieval", body)
    ensure_parent(args.out_html)
    Path(args.out_html).write_text(html, encoding="utf-8")
    print(f"WROTE {args.out_csv}")
    print(f"WROTE {args.out_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
