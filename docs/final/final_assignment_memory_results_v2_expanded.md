# Final Assignment Memory Results V2 Expanded

## Executive summary

External object-level memory changes the final selected continuation of a frozen Matrix-Game-2 world model in the current GTA road-sign case study.

## Base model and task

- Base model: Matrix-Game-2
- Status: frozen, no training, no internal architecture edits
- Task: generate GTA-style candidate continuations and select the final candidate with external memory guidance

## Memory module design

The memory module is external to Matrix-Game-2 and consists of a writer, encoder, retriever, and reranker.

## Memory data structure

- first-visit keyframes
- landmark crops
- approved road-sign crops
- bbox metadata
- feature vectors
- JSONL memory bank entries

## Memory lifecycle

- Write: after first_visit generation
- Store: keyframes, crops, features, metadata
- Read: during candidate reranking
- Update: static within the current run
- Use: choose the final candidate from the generated pool

## Experimental protocol

- fixed approved road-sign memory target
- candidate pool reported in full
- demo pair selected under a written anti-cherry-picking protocol
- controls reported alongside the main memory condition

## Candidate pool

- available and audited: seed1..seed8
- missing for this package: seed9..seed16
- evidence tier: `MINIMUM_PASS`

## Memory strategies

- no_memory
- uniform_memory
- recent_only
- random_memory
- wrong_scene_memory
- auto_landmark_memory
- manual_landmark_memory_v2
- approved_roadsign_memory

## Results table

See `final_memory_ablation_table.csv` and `expanded_memory_strategy_scores.csv`.

## Random-memory control

Existing 10 random-memory trials select only seed1 and seed7. Seed8 is never selected by the random-memory control.

## Manual visual review

The package includes a contact sheet and a blank review template marked `template_only`.

## Automatic proxy metrics

The package reports approved-road-sign candidate scores, crop similarities, and the margin between the selected candidate and the next-best candidate. These are proxy metrics only.

## Demo video

Primary demo: `demo_v2_no_memory_vs_memory_annotated.mp4`

## What we can claim

- External memory changes final candidate selection in this case study.
- Approved object-level memory is more specific than the existing random-memory control for the current candidate pool.
- The project satisfies the AP0006 requirement to analyze and visualize a memory module in a world-model pipeline.

## What we cannot claim

- We do not prove universal spatial-consistency improvement.
- We do not show internal Matrix-Game-2 memory.
- We do not claim statistical significance from the current limited random-control sample.

## Why this satisfies AP0006

The package analyzes what memory stores, when it is written/read, how it changes output selection, and how the memory strategy evolves from generic keyframes to an approved object-level target.
