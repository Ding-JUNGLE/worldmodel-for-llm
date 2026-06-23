# World Model External Memory Project

Final package for AP0006 Final Project: **Memory Modules in World Models**.

We use Matrix-Game-2 as a frozen world model and add an external inference-time memory module that stores first-visit visual evidence and reranks candidate continuations.

## CVPR-style Final Paper Draft

A CVPR 2026-format paper skeleton is under:

`paper/cvpr2026_ap0006_memory_modules/`

Gate 1 only verifies the template and compilation. The final content will be added in later gates.

## Ready for PPT

### 1. One-sentence project claim

```text
We use Matrix-Game-2 as a frozen world model and add an external inference-time memory module. The memory stores first-visit visual evidence and reranks candidate continuations. In the GTA road-sign case study, no-memory selects seed1, while approved road-sign memory selects seed8.
```

Chinese:

```text
我们把 Matrix-Game-2 作为 frozen world model，不训练、不改内部结构；在推理阶段外接 memory module，存 first-visit 的关键帧和人工确认的路牌 crop，并用它 rerank 后续 candidate videos。最终 no-memory 选择 seed1，而 approved road-sign memory 选择 seed8。
```

### 2. PPT slide structure

| Slide | Title | Core message | Main file |
|---|---|---|---|
| 1 | Motivation | World models suffer from spatial forgetting | `docs/story/experiment_story_and_direction.md` |
| 2 | Base Model | Matrix-Game-2 is frozen | `docs/final/final_assignment_memory_results_v2_expanded.md` |
| 3 | Memory Location | Memory is external, not inside Matrix-Game-2 | `docs/02_MEMORY_MODULE_LOCATION.md` |
| 4 | Memory Lifecycle | write / read / update / use | `docs/final/memory_card_and_cost_analysis.md` |
| 5 | Memory Data | keyframes, crops, bbox, feature vectors | `figures/final/roadsign_memory_target.png` |
| 6 | Experiment Design | baseline + controls + final method | `results/final/expanded_memory_strategy_scores.csv` |
| 7 | Demo | no-memory seed1 vs approved memory seed8 | `figures/presentation/01_main_result_no_memory_vs_memory.png` |
| 8 | Results | memory changes selected candidate | `results/final/all_candidate_scores_by_strategy.csv` |
| 9 | Evidence Strength | case-study + controls | `docs/story/evidence_ladder_v2.md` |
| 10 | Limitations | not internal memory, not universal proof | `docs/story/limitations_and_next_experiments.md` |
| 11 | Future Work | more seeds, more objects, 3D memory | `docs/story/limitations_and_next_experiments.md` |
| 12 | Conclusion | external object memory can guide frozen world models | README safe claim |

### 3. Demo narration

Use this when playing:

```text
This demo shows the same frozen Matrix-Game-2 generation setup. The left side is the no-memory baseline selected candidate, seed1. The right side is the candidate selected by approved road-sign memory, seed8. The base model is unchanged. The memory module stores first-visit road-sign evidence and reranks candidate videos after generation.
```

Chinese:

```text
这个 demo 展示同一个 frozen Matrix-Game-2 生成流程下，外部 memory controller 如何改变最终候选选择。左边是 no-memory baseline，对应 seed1。右边是 approved road-sign memory 选择的结果，对应 seed8。Memory 不改变模型参数，只是在候选生成后根据 first-visit road-sign memory 进行 reranking。
```

### 4. Results to emphasize

Main completed result:

```text
no_memory -> seed1
approved_roadsign_memory -> seed8
```

Control evidence:

```text
uniform_memory
recent_only
random_memory
wrong_scene_memory
auto_landmark_memory
manual_landmark_memory_v2
approved_roadsign_memory
```

Main table:

```text
results/final/expanded_memory_strategy_scores.csv
```

Backup candidate-level table:

```text
results/final/all_candidate_scores_by_strategy.csv
```

Current evidence tier:

```text
MINIMUM_PASS / case-study + controls evidence
```

Do not present this as a large-scale benchmark.

### 5. Teacher / TA Q&A

#### Q: Is Matrix-Game-2 trained or modified?

```text
No. Matrix-Game-2 is frozen. We do not modify its DiT, attention layers, checkpoints, or training code.
```

#### Q: Where is the memory added?

```text
The memory is added outside Matrix-Game-2, at the inference-time candidate-selection layer.
```

#### Q: Why does it count as memory?

```text
It stores historical visual evidence, reads it later, and uses it to change final candidate selection.
```

#### Q: What is stored?

```text
first-visit keyframes, landmark crops, approved road-sign crops, bbox metadata, feature vectors, and JSONL memory entries.
```

#### Q: What is the main result?

```text
No-memory baseline selects seed1. Approved road-sign memory selects seed8.
```

#### Q: Did we solve spatial forgetting?

```text
No. We provide case-study evidence that external object-level memory can influence candidate selection. We do not claim spatial forgetting is universally solved.
```

#### Q: How do you avoid cherry-picking?

```text
We include strategy-level results, candidate-level scores, random-memory controls, wrong-scene control, recent-only control, proxy metrics, and a manual review template.
```

### 6. Safe claims

Can say:

```text
External object-level memory can change final candidate selection in a frozen world model.
```

Can say:

```text
The method is an external memory controller, not internal model modification.
```

Cannot say:

```text
Matrix-Game-2 internally learned long-term memory.
We solved spatial forgetting.
This is statistically significant large-scale proof.
Manual review is completed if only the template exists.
```

### 7. Current limitations

```text
Candidate pool is seed1..8.
Random-memory trials are existing 10 trials.
Manual review is a fillable template unless reviewers actually fill it.
Memory is external reranking only.
```

### 8. Future upgrades

```text
seed1..16 / seed1..32 candidate pool
30 / 50 random-memory trials
multi-object memory targets
filled human visual review
cost analysis table
3D memory using depth / point cloud / Gaussian scaffold
internal memory conditioning in future work
```

一句话中文主线：
我们冻结 Matrix-Game-2，不训练、不改模型内部结构；在推理阶段外接 memory module，保存 first-visit 的 keyframes / road-sign crops，并在后续多个 candidate videos 中根据 memory similarity 进行 reranking。最终 no-memory 选择 seed1，approved road-sign memory 选择 seed8。

## Presentation-ready figure pack

Use these polished PNGs for the final PPT / README story. They are the recommended presentation assets for AP0006:

- `figures/presentation/01_main_result_no_memory_vs_memory.png` Main no-memory vs memory comparison
- `figures/presentation/02_candidate_gallery_memory_selection.png` Candidate gallery summary
- `figures/presentation/03_memory_pipeline_write_read_use.png` Write / read / use pipeline
- `figures/presentation/04_memory_card.png` Memory card and cost summary
- `figures/presentation/05_object_patch_memory_reader.png` Object-patch memory reader
- `figures/presentation/06_correct_vs_wrong_memory_control.png` Control cases and distractors
- `figures/presentation/07_memory_strength_reranking_curve.png` Memory strength curve
- `figures/presentation/08_completed_vs_planned_evidence.png` Completed vs planned evidence
- `figures/presentation/09_claims_and_limitations.png` Claims and limitations

The older video `figures/presentation/01_main_result_no_memory_vs_memory.png` is historical reference only. Use the static figure above for slides.

## True World-Model Generated Demos

Use these as actual generated-video evidence:

| Demo | File | Meaning |
|---|---|---|
| Main clean generated comparison | `figures/presentation/01_main_result_no_memory_vs_memory.png` | no-memory seed1 vs approved memory seed8 from true Matrix-Game-2 generated sources |
| Generated candidate pool gallery (optional) | `media/generated_demos_checked/02_generated_candidate_pool_gallery.mp4` | optional moving gallery assembled from true generated seed clips |

Additional true generated backup clips kept in the repo:

- `media/generated_demos_checked/03_backup_generated_sample_a.mp4` - single no-memory seed1 generated clip.
- `media/generated_demos_checked/04_backup_generated_sample_b.mp4` - single approved-memory seed8 generated clip.

## Visualization / Analysis Demos

These explain the memory method but are not raw world-model rollouts:

| File | Purpose |
|---|---|
| `media/demo_v3/demo_v3_object_patch_memory_story.mp4` | memory write/read/use explanation |
| `media/demo_v3/candidate_gallery_memory_selection.mp4` | historical candidate-pool visualization |
| `media/demo_v3/memory_strength_slider_demo.mp4` | external-memory score visualization |
| `media/demo_v3/correct_vs_wrong_memory_battle.mp4` | control visualization |
| `media/demo_v3/object_patch_heatmap_demo.mp4` | patch-matching visualization |

### Candidate gallery figure

Use:

`figures/demo_v3/candidate_gallery_memory_selection_poster.png`

This is the recommended presentation asset for explaining the candidate pool and memory-guided selection.

The older MP4 remains a historical visualization file, but the static figure is clearer and better for PPT / report use.

## Deprecated

Do not use for presentation:

`media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4`

Reason:

`persistent overlay bug blocks the right-side panel.`

## V2 demo playback / overlay note

The old file:

`media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4`

is kept as a historical artifact and may include a persistent right-side overlay.

For generated-demo presentation, use:

`figures/presentation/01_main_result_no_memory_vs_memory.png`

This clean version keeps both panels visible and removes the overlay artifact.

The memory target / road-sign crop is shown separately as:

`figures/demo_v2_memory_target_separate.png`

The overlay in the old file is a post-processing visualization artifact, not model output.

1. Watch demo:

`figures/presentation/01_main_result_no_memory_vs_memory.png`

2. Read this README first.

3. Read file guide for detailed file meanings:

`docs/final/TEAMMATE_FILE_DATA_GUIDE.md`

4. Main report:

`docs/final/final_assignment_memory_results_v2_expanded.md`

5. Assignment mapping:

`docs/final/assignment_requirement_mapping_v2.md`

6. Main result table:

`results/final/expanded_memory_strategy_scores.csv`

7. Candidate-level backup table:

`results/final/all_candidate_scores_by_strategy.csv`

## V3 Stronger Evidence

New V3 evidence extends the AP0006 package beyond the original side-by-side demo:

- Demo V3: `media/demo_v3/demo_v3_object_patch_memory_story.mp4`
- Object-patch reranker: `scripts/external_memory/object_patch_memory_reranker.py`
- Object-patch result table: `results/final/object_patch_rerank_seed1_8.csv`
- Demo V3 contact sheets:
  - `figures/demo_v3/demo_v3_object_patch_contact_sheet.png`
  - `figures/demo_v3/object_patch_rerank_contact_sheet.png`
- Memory size curve:
  - `results/evaluation/memory_size_curve.csv`
  - `figures/final/memory_size_curve.md`
- Road-sign robustness:
  - `results/evaluation/roadsign_memory_robustness.csv`
  - `figures/final/roadsign_memory_robustness_summary.md`
- Distractor controls:
  - `results/evaluation/distractor_memory_controls.csv`
  - `results/evaluation/distractor_memory_controls.md`
- Cost analysis:
  - `results/evaluation/memory_cost_analysis.csv`
  - `docs/final/memory_card_and_cost_analysis.md`
- Manual review packet:
  - `results/evaluation/manual_review_table_to_fill_v3.csv`
  - `docs/evaluation/manual_review_instructions_v3.md`
  - `figures/demo_v3/manual_review_contact_sheet_v3.png`

Important V3 readout:

- `object_patch_rerank_seed1_8` still selects `seed8`.
- `1 crop` falls back to `seed1`, while `2+ crops` switch to `seed8`.
- leave-one-out and small bbox jitter keep `seed8` in this case study.
- distractor patch controls also selected `seed8`, so specificity is still limited.

This remains **external reranking** and still **case-study evidence**, not internal memory injection or benchmark-level proof.

## Fun Demo V3 Pack

This package also adds presentation-facing demos that are visually clearer but still tied to memory-module analysis.

Preferred candidate-gallery presentation asset:

```text
figures/demo_v3/candidate_gallery_memory_selection_poster.png
```

### Demo V3 files

```text
media/demo_v3/memory_strength_slider_demo.mp4
media/demo_v3/correct_vs_wrong_memory_battle.mp4
media/demo_v3/object_patch_heatmap_demo.mp4
```

Historical candidate-gallery MP4 kept for reference only:

```text
media/demo_v3/candidate_gallery_memory_selection.mp4
```

### What each demo proves

| Demo | Purpose |
|---|---|
| Candidate Gallery Figure | shows candidate-pool comparison with a cleaner PPT-ready layout and clearer selection story |
| Memory Strength Slider | visualizes external memory influence as a reranking weight |
| Correct vs Wrong Memory Battle | tests whether relevant memory matters more than distractor memory |
| Object-Patch Heatmap | visualizes how object-level memory is read from candidate frames |

### Important limitation

These demos are external reranking / visualization demos. They do not mean Matrix-Game-2 internally learned memory.

## What this project is

- Base model: `Matrix-Game-2` (external memory is an add-on)
- Project goal: design and evaluate external memory for long-horizon continuity in a frozen world model
- Core idea: maintain a **candidate pool**, then use external memory retrieval/reranking to select a final continuation

### What the project is not doing

- No model re-training
- No internal architecture change
- No new checkpoints
- No new videos generated in this package

## How this matches AP0006 requirements

### Requirement A: Memory Module Analysis

We analyze:

- what memory stores
- where memory is stored
- when memory is written
- when memory is read
- how memory is used
- how memory affects generation output

### Requirement B: Memory Visualization

We provide:

- demo video
- memory pipeline diagram
- road-sign memory target image
- demo contact sheets
- ablation/result tables

### Requirement C: New Memory Strategy Design

Strategy progression:

```text
full-frame keyframe memory
        ↓
landmark memory
        ↓
human-approved road-sign memory
```

### Evaluation evidence included

- no-memory baseline
- uniform memory
- recent-only control
- random-memory control
- wrong-scene control
- auto-landmark memory
- approved road-sign memory
- candidate-level score table
- automatic proxy metrics
- manual review template

Honest limitation: this is a case-study and control-based package, not a universal benchmark proof.

## Memory Card

| Item | Our design |
|---|---|
| Base model | Matrix-Game-2 |
| Model status | Frozen |
| Training used | No |
| Internal architecture modified | No |
| Memory type | External image / feature retrieval memory |
| Memory unit | first-visit keyframes, landmark crops, approved road-sign crops |
| Write time | after first_visit generation |
| Read time | during candidate reranking |
| Update policy | static within current run |
| Use | rerank multiple candidate videos |
| Output effect | changes selected candidate |
| Main baseline | no_memory -> seed1 |
| Main memory result | approved_roadsign_memory -> seed8 |

This memory is **not** internal neural memory tokens. It is an external controller that stores visual evidence and uses it to select the most memory-consistent candidate.

## Where the memory is added

We do not modify:

- Matrix-Game-2 DiT / transformer
- attention layers
- model checkpoints
- training code
- core `inference.py` generation logic

Instead, memory is added outside the frozen world model, at the inference-time candidate-selection layer.

```text
Matrix-Game-2 frozen world model
        ↓
generate first_visit video
        ↓
external Memory Writer stores keyframes / road-sign crops
        ↓
Matrix-Game-2 generates multiple candidate continuations
        ↓
external Memory Retriever reads historical memory
        ↓
external Memory Reranker scores candidates
        ↓
selected candidate becomes final output
```

## Data tables and figures: what they mean

- `results/final/expanded_memory_strategy_scores.csv`: strategy-level success score summary for no-memory and all memory controls/methods
- `results/final/all_candidate_scores_by_strategy.csv`: candidate-level outcomes for each strategy (seed1~seed8)
- `results/evaluation/random_memory_trials.csv`: existing random-memory baseline control (10 trials)
- `results/evaluation/automatic_proxy_metrics.csv`: proxy quality metrics for the same candidates
- `results/evaluation/manual_review_table_template.csv`: review form for human visual validation (template until filled)
- `figures/presentation/01_main_result_no_memory_vs_memory.png`: core demo clip used in slides (seed1 vs approved-memory seed8)
- `figures/demo_v2/demo_v2_contact_sheet.png`: candidate contact sheet
- `figures/demo_v2/manual_review_contact_sheet.png`: manual-review visual context
- `figures/final/roadsign_memory_target.png`: road-sign target image used for object-level memory
- `docs/final/memory_card_and_cost_analysis.md`: memory card + storage/runtime/GPU cost + limitations/future upgrade
- `figures/final/memory_pipeline_diagram.md`: memory pipeline schematic
- `results/final/expanded_memory_strategy_scores.csv` / `results/final/all_candidate_scores_by_strategy.csv` support anti-cherry-picking claims

## Completed evidence

### Main demo

`figures/presentation/01_main_result_no_memory_vs_memory.png`

Shows:

- no-memory baseline: seed1
- approved road-sign memory: seed8

### Main result table

`results/final/expanded_memory_strategy_scores.csv`

Strategies:

- no_memory
- uniform_memory
- recent_only
- random_memory
- wrong_scene_memory
- auto_landmark_memory
- manual_landmark_memory_v2
- approved_roadsign_memory

### Candidate-level backup table

`results/final/all_candidate_scores_by_strategy.csv`

Seed-level detail across candidate1~candidate8 for each strategy.

### Control data

- `results/evaluation/random_memory_trials.csv`
- `results/evaluation/automatic_proxy_metrics.csv`
- `results/evaluation/manual_review_table_template.csv`

Important limitation:

```text
Candidate pool is seed1..8.
Random-memory trials are existing 10 trials.
Manual review file is a template unless reviewers have already filled it.
```

## Presentation logic

Recommended 10-12 slide structure:

| Slide | Core question | Suggested material |
|---|---|---|
| 1 | What problem are we solving? | spatial forgetting / object persistence |
| 2 | What is the base world model? | Matrix-Game-2 frozen |
| 3 | What memory do we add? | external memory card |
| 4 | Where is memory inserted? | inference-time candidate-selection layer |
| 5 | What does memory store? | keyframes / road-sign crops / features |
| 6 | What is the new strategy? | full-frame -> landmark -> approved road-sign |
| 7 | What is the experiment design? | baseline + controls + final method |
| 8 | What does the demo show? | no-memory seed1 vs memory seed8 |
| 9 | What do the results show? | strategy table + candidate table |
| 10 | Why is this not cherry-picking? | controls and candidate-level scores |
| 11 | What are the limitations? | case study, seed1..8, external reranking |
| 12 | What is the conclusion? | external object-level memory changes selected output |

## AP0006 evidence upgrade pack (PPT-ready)

### Memory Card figure/table

| Memory type | Memory unit | Write | Read | Update | Use | Stored fields | Code locations |
|---|---|---|---|---|---|---|---|
| Full context bank | First-visit keyframe cards | Extract first-visit keyframes and persist with feature vectors | Retrieve top-k cards for rerank scoring | Static within a run | Generic reranking baseline | `memory_id`, `frame_index`, `frame_path`, `feature_path`, `feature_dim`, `encoder`, `quality` | `scripts/external_memory/extract_keyframes.py`, `scripts/external_memory/build_memory_bank.py`, `scripts/external_memory/retrieve_memory.py`, `scripts/external_memory/rerank_candidates.py` |
| Landmark memory | Cropped landmark cards (auto-detected) | Build landmark crops and persist metadata/features | Retrieve landmark matches for rerank | Static within a run | Intermediate object-level strategy | `memory_id`, `frame_index`, `frame_path`, `feature_path`, `feature_dim`, `encoder`, `landmark_tag` | `scripts/external_memory/build_landmark_memory.py`, `scripts/external_memory/rerank_candidates.py`, `scripts/external_memory/retrieve_memory.py` |
| Approved road-sign bank | Human-approved road-sign crops | Write approved crops only and persist features | Read approved crop set during scoring | Static within a run | Final strategy (`approved_roadsign_memory`) | `memory_id`, `frame_index`, `frame_path`, `feature_path`, `feature_dim`, `encoder`, `annotation_provenance` | `manual_memory/roadsign_memory_bank.jsonl` (run reference), `docs/final/TEAMMATE_FILE_DATA_GUIDE.md` |

### Stage A/B/C alignment

| Stage | Requirement | Package evidence |
|---|---|---|
| Stage A | Memory module analysis | `docs/final/memory_card_and_cost_analysis.md`, `docs/story/evidence_ladder_v2.md`, this document |
| Stage B | Memory visualization | `figures/final/memory_pipeline_diagram.md`, `figures/demo_v2/demo_v2_contact_sheet.png`, `figures/final/no_memory_vs_memory_contact_sheet.png`, `media/demo_v3/demo_v3_object_patch_memory_story.mp4`, `media/demo_v3/object_patch_heatmap_demo.mp4` |
| Stage C | New memory strategy design | `docs/final/final_assignment_memory_results_v2_expanded.md`, `results/final/expanded_memory_strategy_scores.csv`, `results/final/all_candidate_scores_by_strategy.csv` |

### Cost analysis

- Storage: ~2.8 MB (uniform), ~1.3 MB (landmark), ~116 KB (approved roadsign), ~39 MB (seed1..8 candidates)
- Runtime: candidate inference dominates; external memory read/rerank is lightweight and post-inference
- GPU: heavy compute remains in Matrix-Game-2; memory code is inference-time auxiliary and lightweight

### Manual review guide (fillable)

`results/evaluation/manual_review_table_template.csv` is intentionally a fillable guide.

Recommended steps:

1. Keep `TBD` rows as `template_only` before review.
2. Replace `TBD` with `0/1/2` numeric judgments and add concise notes.
3. Update row status to `reviewed` only after three-stage frame labels (`early`, `middle`, `late`) are filled.

### Failure / weak-evidence explanation

- This is one GTA road-sign case only.
- Candidate pool is only seeds `1..8`.
- Existing random-memory control count is `10`.
- Manual review remains template-driven until reviewed rows exist.

The strongest safe wording is: **case-study + control-backed claim of external rerank influence**, not universal memory solving.

## Teacher / TA Q&A

### Q1: What is the base world model?

We use Matrix-Game-2 as a frozen interactive world model. We do not train it and do not modify its internal architecture.

### Q2: Where is memory added?

Memory is added outside Matrix-Game-2 at the inference-time candidate-selection layer.

### Q3: Why does this count as memory?

It stores historical visual evidence, reads it later, and uses it to change final candidate selection.

### Q4: What is stored?

first-visit keyframes, landmark crops, approved road-sign crops, bbox metadata, feature vectors, JSONL memory entries.

### Q5: What is the main result?

No-memory baseline selects seed1. Approved road-sign memory selects seed8.

### Q6: How do we avoid cherry-picking?

We report strategy-level results, candidate-level scores, random-memory controls, wrong-scene control, recent-only control, and proxy metrics.

### Q7: Did we solve spatial forgetting?

No. We show case-study evidence that external object-level memory can influence candidate selection. We do not claim spatial forgetting is universally solved.

### Q8: Why GTA road-sign?

GTA scenes contain persistent landmarks such as road signs, buildings, lanes, and turns. A road sign is a clear object-persistence target.

### Q9: Why no training?

The project studies memory module design and analysis. We test whether external memory can influence generation result without retraining or changing the world model.

### Q10: What are next experiments?

More seeds, more objects, more random trials, filled human evaluation, 3D memory, dynamic memory update, and future internal conditioning.

## Additional Experiments We Can Add

These are recommended extensions if time allows. Do not report them as completed unless data exists.

### Experiment 1: Larger candidate pool

Current:

`seed1..8`

Next:

`seed1..16` or `seed1..32`

Purpose:

Reduce the chance that one result is due to a small candidate pool.

Expected output files:

`results/final/all_candidate_scores_seed1_16.csv`
`results/final/expanded_memory_strategy_scores_seed1_16.csv`

### Experiment 2: More random-memory trials

Current:

`10 existing random-memory trials`

Next:

`30` or `50` random-memory trials

Purpose:

Strengthen random-memory control.

Expected output:

`results/evaluation/random_memory_trials_30.csv`
`results/evaluation/random_memory_distribution_30.md`

### Experiment 3: Multi-object memory targets

Current:

`approved right-side road-sign memory`

Next:

traffic sign / car / lane marking / building corner / road turn

Purpose:

Show strategy generalizes beyond one road sign.

Expected output:

`results/final/multi_object_memory_targets.csv`
`figures/demo_v2/multi_object_memory_contact_sheet.png`

### Experiment 4: Filled human visual review

Current:

`manual_review_table_template.csv`

Next:

filled labels on road-sign presence / consistency

Purpose:

Complement proxy metrics with human visual judgment.

Expected output:

`results/evaluation/manual_review_filled.csv`
`results/evaluation/manual_review_summary.md`

### Experiment 5: Failure-case analysis

Purpose:

Show honest scientific analysis.

Examples:

- generic full-frame memory can be too broad
- random memory can sometimes select high-scoring candidates
- wrong-scene memory should not be trusted

Expected output:

`docs/story/failure_case_analysis.md`
`figures/final/failure_case_contact_sheet.png`

### Experiment 6: Cost analysis

Measure:

- memory bank size
- number of candidates
- rerank runtime
- storage cost
- GPU memory impact

Expected output:

`results/evaluation/memory_cost_analysis.csv`
`docs/final/memory_card_and_cost_analysis.md`

### Experiment 7: Future internal memory

Not for this project, but for future work:

- retrieved memory as conditioning
- memory tokens
- 3D memory from depth / point cloud
- Gaussian scaffold memory

## Completed vs Planned

| Item | Status | Notes |
|---|---|---|
| Matrix-Game-2 frozen base model | Completed | no training |
| External memory writer / retriever / reranker | Completed | inference-time only |
| No-memory vs approved memory demo | Completed | seed1 vs seed8 |
| Strategy-level ablation | Completed | see expanded_memory_strategy_scores.csv |
| Candidate-level table | Completed | seed1..8 |
| Random-memory control | Limited completed | 10 existing trials |
| Wrong-scene control | Completed if present in table | negative control |
| Recent-only control | Completed if present in table | short-term memory control |
| Automatic proxy metrics | Completed | proxy only |
| Manual review | Template only unless filled | do not claim completed human study |
| seed1..16 / seed1..32 | Planned | not completed unless generated |
| multi-object memory | Planned | not completed unless generated |
| 3D memory / internal conditioning | Future work | not completed |

## Final Safe Claim

English:

We use Matrix-Game-2 as a frozen world model and add an external inference-time memory module.
The memory stores first-visit keyframes and approved road-sign crops, retrieves them later, and reranks candidate continuations.
In our GTA road-sign case study, no-memory selects seed1, while approved road-sign memory selects seed8.
This shows that external object-level memory can change final candidate selection in a frozen world model.

中文:

我们把 Matrix-Game-2 作为 frozen world model，不训练、不改内部结构。
我们在推理阶段外接 memory module，存 first-visit 的关键帧和人工确认的路牌 crop。
后续生成多个候选视频后，memory module 根据历史路牌记忆对候选进行 reranking。
在 GTA road-sign case 中，no-memory 选择 seed1，而 approved road-sign memory 选择 seed8。
这说明 external object-level memory 可以改变 frozen world model 的最终候选选择。

## Claims to Avoid

Do not claim:

- Matrix-Game-2 internally learned long-term memory.
- spatial forgetting is solved.
- this is statistically significant, large-scale, benchmark-level proof.
- the model itself “remembers” the road sign.
- manual review is completed if only the template exists.

## What to open first (for teammates)

Always open this file in order:

1. `README.md` (you are here)
2. `docs/final/TEAMMATE_FILE_DATA_GUIDE.md`
3. `docs/final/final_assignment_memory_results_v2_expanded.md`

## Reproduction pointer

A lightweight reproduction helper is available in this repo when environment is prepared:

```bash
bash scripts/run/reproduce_gta_roadsign_memory.sh \
  --matrix-game2-root /path/to/Matrix-Game-2 \
  --output-root /path/to/repro_outputs \
  --mode smoke
```

This package does not include full outputs or checkpoints; it is a documentation/evidence package for AP0006.

## What is not included

- Model checkpoints
- Full-resolution generated videos
- Full raw output folders
- Private credentials
- Training artifacts

Only compressed demos and evidence tables are included.
