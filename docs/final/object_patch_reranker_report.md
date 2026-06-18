# Object-Patch Memory Reranker Report

## Diagnosis

`PASS_OBJECT_PATCH_RERANKER_READY`

## Why this improves memory

The earlier approved-memory package already showed that human-approved road-sign memory can change candidate selection.

This V3 reranker is a stricter external-memory read/use module:

- it samples candidate frames
- it splits frames into grid patches
- it encodes candidate patches
- it compares patch features against approved road-sign crop memory
- it scores each candidate by top-k patch similarity over time

This is still fully external to Matrix-Game-2.

## Result

Object-patch reranking on the `seed1..8` candidate pool selects `seed8`.

Top-5 candidates:

| Rank | Seed | Score |
|---|---:|---:|
| 1 | 8 | 0.740770 |
| 2 | 1 | 0.727386 |
| 3 | 3 | 0.719987 |
| 4 | 5 | 0.717236 |
| 5 | 4 | 0.716683 |

Primary output table:

- `results/final/object_patch_rerank_seed1_8.csv`

Primary visual:

- `figures/demo_v3/object_patch_rerank_contact_sheet.png`

## Interpretation

- Memory is written as approved road-sign crops and feature references.
- Memory is read only during candidate reranking.
- The selected output still changes away from the no-memory baseline (`seed1` -> `seed8`).

## Important limitation

The V3 distractor controls show that this patch matcher is not yet perfectly object-specific:

- `random_crop_memory` also selects `seed8`
- `same_frame_non_roadsign_crop` also selects `seed8`

So the strongest honest claim is:

`object_patch_reranker` is operational and aligns with approved-memory selection, but its specificity is still limited and should not be overclaimed as a solved object-memory mechanism.
