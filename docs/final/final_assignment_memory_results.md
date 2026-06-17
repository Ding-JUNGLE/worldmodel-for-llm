# Final Assignment Memory Results (Teammate Package)

## Diagnosis

- PASS_FINAL_ASSIGNMENT_RESULTS_READY

## Purpose

Package lightweight artifacts for teammates to write slides and reproduce the key conclusions without downloading checkpoints/videos.

## Reproducible source runs

- No-memory and baseline variants: `outputs/runs/20260617_007_gta_landmark_memory_v1`
- Manual landmark proxy: `outputs/runs/20260617_008_gta_manual_landmark_memory_v2`
- Approved road-sign variant: `outputs/runs/20260617_009_gta_roadsign_approved_memory_v3`

## Key result snapshot

- No-memory seed: **1**
- Approved road-sign memory seed: **8**
- Main comparison target: whether reranking with explicit road-sign memory can shift selected continuation away from seed1.

## Included lightweight outputs

- `final_memory_ablation_table.csv`
- `final_memory_ablation_table.md`
- `final_assignment_memory_results.md`
- `presentation_outline_for_teammates.md`
- `slide_content_draft.md`
- `speaker_notes_draft.md`
- `figures/memory_pipeline_diagram.md`
- `figures/no_memory_vs_memory_contact_sheet.png`
- `figures/final_ablation_summary.md`
- `figures/roadsign_memory_target.png`

## Quick methodology summary

1. Keep Matrix-Game-2 frozen.
2. Generate first-visit scene (seed0 style run in v1).
3. Build memory bank per strategy.
4. Render candidate videos for seeds 1..8.
5. Rerank candidates via external memory similarity.
6. Pick highest score candidate path per strategy.

## Data quality note

- `manual_landmark_memory_v2` is a provisional proxy and was not a fully finalized annotation.
- Final presentation should prioritize `approved_roadsign_memory` as the official completed variant.
