# Figure polish report

This pass turns the AP0006 evidence into a PPT-ready figure set without running new model experiments.

## What was generated

- `figures/presentation/01_main_result_no_memory_vs_memory.png`
- `figures/presentation/02_candidate_gallery_memory_selection.png`
- `figures/presentation/03_memory_pipeline_write_read_use.png`
- `figures/presentation/04_memory_card.png`
- `figures/presentation/05_object_patch_memory_reader.png`
- `figures/presentation/06_correct_vs_wrong_memory_control.png`
- `figures/presentation/07_memory_strength_reranking_curve.png`
- `figures/presentation/08_completed_vs_planned_evidence.png`
- `figures/presentation/09_claims_and_limitations.png`

PDF copies were also exported next to the PNGs for easier slide import.

## Source material used

- Real demo frames from `media/demo/no_memory_seed1.mp4`
- Real demo frames from `media/demo/with_roadsign_memory_seed8.mp4`
- Approved crop asset from `figures/final/roadsign_memory_target.png`
- Existing candidate gallery poster from `figures/demo_v3/candidate_gallery_memory_selection_poster.png`
- Existing evaluation tables under `results/evaluation/`

## Design changes

- Rebuilt the main comparison as a balanced two-card layout with clear margins.
- Reduced the long titles and subtitles that were crowding the previous drafts.
- Converted the control and evidence slides into clean PPT dashboard cards.
- Added a memory card and pipeline slide that explicitly states write, read, use, storage cost, and limitation.
- Kept the message honest: external reranking only, not internal model modification.

## Audit

- `results/evaluation/figure_quality_audit.csv` records the exported figure set and file sizes.
- The script used to generate the pack is `scripts/make_presentation_figures.py`.

## Limitation

These are presentation assets for a case study. They improve clarity and evidence packaging, but they do not change the underlying Matrix-Game-2 model or add new human labels.
