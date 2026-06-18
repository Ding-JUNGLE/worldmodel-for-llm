# Manual Review Instructions V3

## Goal

This file explains how to fill `results/evaluation/manual_review_table_to_fill_v3.csv` without inventing labels.

## Reviewer rules

- Do not fill rows unless a human reviewer actually inspects the frames.
- Do not copy scores from proxy metrics.
- Do not infer object presence from the reranker score alone.
- Keep `review_type=template_only` until a human has reviewed the row.

## Files to open

- `figures/demo_v3/manual_review_contact_sheet_v3.png`
- `media/demo_v3/demo_v3_object_patch_memory_story.mp4`
- candidate videos under `media/demo_v2/` if frame-level checking is needed

## Suggested scoring

Use `0/1/2` for each visual judgment:

- `0`: absent / inconsistent / poor
- `1`: ambiguous / partial
- `2`: present / consistent / good

## Required fields

Review at least:

- `road_sign_present`
- `road_sign_position_consistent`
- `road_sign_appearance_consistent`
- `scene_quality`
- `artifact_level`
- `overall_preference`
- `reviewer_notes`

## When a row becomes filled

Set:

- `review_type=reviewed`
- `review_status=filled`
- `reviewer_id=<human reviewer name or id>`
- `reviewed_at=<date>`

only after the reviewer has completed the row honestly.
