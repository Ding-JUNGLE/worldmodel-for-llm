# Final Assignment Memory Results V2 Expanded

## Executive summary

External object-level memory changes the final selected continuation of a frozen Matrix-Game-2 world model in the current GTA road-sign case study.

## Base model and task

- Base model: Matrix-Game-2
- Status: frozen, no training, no internal architecture edits
- Task: generate GTA-style candidate continuations and select the final candidate with external memory guidance

## Stage A/B/C alignment

### Stage A — Memory module analysis

- Memory module is external and sits at inference time.
- Covered lifecycle: write → store → read → update (static within a run) → use.
- Memory components are documented with fields and code locations in `docs/final/memory_card_and_cost_analysis.md`.

### Stage B — Memory visualization

- Pipeline diagram and visual assets are captured in:
  - `figures/final/memory_pipeline_diagram.md`
  - `figures/final/roadsign_memory_target.png`
  - `figures/demo_v2/demo_v2_contact_sheet.png`
- Candidate evidence and selection comparison is available in:
  - `figures/final/no_memory_vs_memory_contact_sheet.png`
  - `media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4`

### Stage C — New memory strategy design

- Strategy stack moves from weak controls to object-level control:
  - `no_memory`
  - `uniform_memory`
  - `recent_only`
  - `random_memory`
  - `wrong_scene_memory`
  - `auto_landmark_memory`
  - `manual_landmark_memory_v2`
- `approved_roadsign_memory`
- `approved_roadsign_memory` is the final object-level strategy.

### Alignment check against AP0006 deliverable requirement

| Requirement | Evidence in this package |
|---|---|
| Stage A: memory analysis | `docs/final/memory_card_and_cost_analysis.md` + write/read/update/use lifecycle in this file |
| Stage B: visualization | pipeline diagram, target card, and side-by-side demo files |
| Stage C: strategy design progression | strategy path in this file and `results/final/expanded_memory_strategy_scores.csv` |

## Memory module design

The memory module is external to Matrix-Game-2 and consists of:

- Writer
- Encoder
- Retriever
- Reranker

## Memory card and unit table

| Memory type | Memory unit | Write | Read | Update | Use | Stored fields | Code locations |
|---|---|---|---|---|---|---|---|
| Full context bank | First-visit keyframe cards (`memory/uniform/..._memory_bank.jsonl`) | Extract keyframes from first-visit video, encode to features, write JSONL rows | Retrieve top-k by cosine similarity | Static within run | Generic rerank control baseline | `memory_id`, `frame_index`, `frame_path`, `feature_path`, `feature_dim`, `encoder`, quality/meta | `scripts/external_memory/extract_keyframes.py`, `scripts/external_memory/build_memory_bank.py`, `scripts/external_memory/retrieve_memory.py`, `scripts/external_memory/rerank_candidates.py`, `scripts/external_memory/external_memory_effectiveness_v1/run_memory_ablation.py` |
| Landmark bank | Auto-cropped landmark frames (`memory/landmark/..._memory_bank.jsonl`) | Build landmark crops from first-visit frames and encode | Retrieve landmark candidate matches then rerank | Static within run | Generic object-level strategy | `memory_id`, `frame_index`, `frame_path`, `feature_path`, `feature_dim`, `encoder`, `landmark_tag` | `scripts/external_memory/build_landmark_memory.py`, `scripts/external_memory/external_memory_effectiveness_v1/run_memory_ablation.py`, `scripts/external_memory/retrieve_memory.py` |
| Approved roadsign bank | Human-approved road-sign crops (`manual_memory/roadsign_memory_bank.jsonl`) | Write approved crops + feature vectors from approved annotation | Retrieve only approved sign memory during candidate scoring | Static within run | Strong object-level strategy | `memory_id`, `frame_index`, `frame_path`, `feature_path`, `feature_dim`, `encoder`, annotation provenance | N/A in this package; generated in run snapshot `20260617_009_gta_roadsign_approved_memory_v3` and referenced by `docs/final/TEAMMATE_FILE_DATA_GUIDE.md` |

## Memory data structure

- first-visit keyframes
- landmark crops
- approved road-sign crops
- bbox metadata and source references (in annotation paths)
- feature vectors
- JSONL memory bank entries

## Memory lifecycle

- Write:
  - first-visit keyframes are extracted
  - memory banks are created for uniform, landmark, wrong-scene and approved variants
- Store:
  - memory entries (JSONL) + feature files
  - crop/frame references
- Read:
  - during candidate reranking for every strategy
- Update:
  - static within the current run; no online memory insertion during reranking
- Use:
  - select final output candidate after model generates seed pool

## Cost analysis (current evidence package)

### Storage

- Uniform bank + frames/features: **~2.8 MB** (`memory/uniform` in `20260617_007_gta_landmark_memory_v1`).
- Landmark bank + frames/features: **~1.3 MB** (`memory/landmark`).
- Wrong-scene bank + frames/features: **~2.5 MB** (`memory/wrong_scene`).
- Approved roadsign bank + features: **~116 KB** (`manual_memory` in `20260617_009...`).
- Candidate outputs under seed1..8: **~39 MB** (`candidates` directory).
- Rerank artifacts (top-k/selected CSV + selected video + HTML): single-digit MB.

### Runtime

- Candidate inference runtime from existing stderr logs is dominated by model generation:
  - ~20 s per 16-step candidate generation in observed reference logs.
  - 8 seeds were generated (seed1..8), so candidate generation is on the order of a few minutes.
- Memory write/read/retrieval/rerank steps are fast relative to generation and are implemented with CPU numpy/PIL operations plus lightweight torch/vision ops.

### GPU / compute

- External memory code itself is not the large compute bottleneck; Matrix-Game-2 generation is.
- The package uses GPU-accelerated generation in the upstream model path.
- Exact model GPU type/memory usage is not stored in these package-level files, so this is reported as a constrained operational estimate.

## Experimental protocol

- fixed approved road-sign memory target
- candidate pool reported in full
- anti-cherry-picking controls and auditability applied
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

## Manual visual review guide

Manual review is intentionally separated from proxy-only automated metrics.

- Fillable template: `results/evaluation/manual_review_table_template.csv`
- The template includes:
  - road-sign presence
  - position consistency
  - appearance consistency
  - scene quality
  - artifact level
  - overall preference
  - reviewer notes
- Review instructions:
  - mark each relevant candidate row as `template_only` to `filled` over time
  - keep notes conservative and scene-frame-specific
  - do not infer statistical claims from manual template rows

Current fill workflow:

- Start with `TBD` values and `review_type=template_only`.
- Use `0/1/2` scores per item.
- Set `review_type` to `reviewed` after all three frame stages are complete.

Suggested conservative interpretation:

- If no reviewed rows exist, keep reporting this as a case-study + proxy-control package.

## Failure / weak-evidence explanation

- Main claim is from **one approved-road-sign case**, not a broad benchmark.
- Random-memory control has **10 trials** only.
- Candidate pool is **seed1..8**, not seed1..16.
- Manual review in this package is currently a guide template; it is not a completed human-evaluation dataset yet.
- Therefore current claim wording must stay case-study and control-aware.

### Failure-case wording to use in slides

> Approved road-sign memory improves candidate selection in this one-case package, but it is not yet a broad memory benchmark.

> Controls are present (random/wrong-scene/recent-only), yet manual review is not yet complete and candidate diversity is limited (seed1..8).

## Results table

See `final_memory_ablation_table.csv` and `expanded_memory_strategy_scores.csv`.

## Random-memory control

Existing 10 random-memory trials select only seed1 and seed7.
Seed8 is never selected by the random-memory control.

## Manual visual review

- Contact sheet and placeholder review workflow are available.
- The package includes a review template and contact-sheet references for manual validation.

## Automatic proxy metrics

The package reports approved-road-sign candidate scores, crop similarities, and margin between selected candidate and next-best candidate.
These are proxy metrics only.

## Demo video

Primary demo: `demo_v2_no_memory_vs_memory_annotated.mp4`

## What we can claim

- External memory changes final candidate selection in this case study.
- Approved object-level memory is more specific than the existing random-memory control for the current candidate pool.
- The package satisfies the AP0006 requirement to analyze and visualize a memory module in a world-model pipeline.

## What we cannot claim

- We do not prove universal spatial-consistency improvement.
- We do not show internal Matrix-Game-2 memory.
- We do not claim statistical significance from the current limited random-control sample.

## Why this satisfies AP0006

- Memory is analyzed with explicit write/read/update/use steps.
- Memory is visualized with multiple artifacts and tables.
- Strategy design evolves toward object-level external control (approved roadsign memory).
