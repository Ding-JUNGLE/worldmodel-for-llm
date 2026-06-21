# Candidate Gallery Static Figure Report

## Why the redesign was needed

The earlier candidate-gallery visualization was useful for internal checking, but it looked crowded and debug-like in final presentation contexts. Text, borders, and image panels competed for attention, so the selection story was harder to read quickly in README, report, and PPT slides.

## Source used

- Primary source clips: `candidate_seed1.mp4` through `candidate_seed8.mp4`
- Source location: `/mnt/data1/dgw/external_repos/Matrix-Game/Matrix-Game-2/outputs/runs/20260617_007_gta_landmark_memory_v1/candidates/`
- Figure generator: `scripts/make_candidate_gallery_static_figure.py`
- Representative frame time: approximately `8.0s` from each candidate clip

## What the figure is meant to show

The figure visualizes a single candidate pool produced by frozen Matrix-Game-2 and highlights how external memory changes which candidate is chosen:

- no-memory selection -> `Seed 1`
- approved road-sign memory selection -> `Seed 8`

It is a candidate-level comparison and explanation figure, not a new rollout.

## Why the static figure is preferred over the old mp4

- It gives cleaner text hierarchy and more balanced spacing.
- It makes the candidate pool readable in one glance.
- It is easier to place in slides, README, and written reports.
- It avoids the crowded, debug-style look of the older visualization-first layout.

## Output files

- `figures/demo_v3/candidate_gallery_memory_selection_poster.png`
- `figures/demo_v3/candidate_gallery_memory_selection_slide_16x9.png`
- `figures/demo_v3/candidate_gallery_memory_selection_thumbnail.png`
- `figures/demo_v3/candidate_gallery_memory_selection_poster.pdf`

## Safe claim

External memory can change final candidate selection in a frozen world model, and the figure makes that candidate-pool comparison easier to explain.

## Limitation

This is a visualization / analysis figure assembled from representative candidate frames. It is not itself a raw world-model generated rollout, and it should not be presented as one.
