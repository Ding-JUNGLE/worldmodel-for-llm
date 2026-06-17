# Teammate File Data Guide

## Purpose

This document explains what each important file in the final GitHub package is for, what data it contains, and how teammates should use it for the AP0006 final report and presentation.

Use branch:

```text
final-assignment-demo-v2-expanded-evidence-20260617
```

Current evidence tier:

```text
MINIMUM_PASS
```

This means the package is sufficient for the course presentation and report, but it is still a case-study style result rather than a large benchmark.

---

## One-minute reading order

If you only have a few minutes, read or watch these first:

1. `media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4`
2. `docs/final/assignment_requirement_mapping_v2.md`
3. `docs/final/final_assignment_memory_results_v2_expanded.md`
4. `docs/story/evidence_ladder_v2.md`
5. `results/final/expanded_memory_strategy_scores.csv`
6. `figures/demo_v2/demo_v2_contact_sheet.png`

---

## Core claim

The base model is Matrix-Game-2, used as a frozen world model.

We do not train Matrix-Game-2 and do not modify its internal architecture.

The memory module is external. It stores first-visit keyframes and approved road-sign crops, retrieves this visual memory later, and reranks generated candidate continuations.

Main comparison:

```text
No memory: seed1
Approved road-sign memory: seed8
```

Main honest claim:

```text
External object-level memory can change the final selected candidate of a frozen world model.
```

Do not overclaim:

```text
We do not claim Matrix-Game-2 internally learned long-term memory.
We do not claim spatial forgetting is universally solved.
```

---

# 1. Top-level navigation files

## `README.md`

Purpose:

- Landing page for the whole repository.
- Tells readers which branch to use.
- Points to the strongest demo video and main evidence files.

Data/content inside:

- Branch name.
- Recommended demo video path.
- Main evidence documents.
- Expanded results table paths.
- Main claim and limitation.

How teammates should use it:

- Use this as the first public-facing explanation.
- Copy the main claim into Slide 1 or Slide 2.

---

## `START_HERE.md`

Purpose:

- Quick path for teammates preparing the final PPT.

Data/content inside:

- First video to watch.
- First documents to read.
- Result tables to use.
- Figures to use.

How teammates should use it:

- Follow it before reading the rest of the repository.
- Use it to avoid opening outdated docs first.

---

## `upload_demo_v2_expanded_evidence_report.md`

Purpose:

- Records what was uploaded in the final expanded evidence package.

Data/content inside:

- Diagnosis label.
- Evidence tier.
- Branch and commit information.
- Candidate pool status.
- Random trial count.
- Uploaded video/table/figure/doc summary.
- Safety scan summary.

How teammates should use it:

- Use it to understand the status of the final package.
- Do not use it as a scientific result section; use it as provenance / repository audit.

---

# 2. Demo videos

## `media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4`

Purpose:

- Main presentation demo.
- This is the best video to show in class or in PPT.

Data/content inside:

- No-memory baseline candidate.
- Approved road-sign memory selected candidate.
- Labels showing that Matrix-Game-2 is frozen and memory is external reranking.

How teammates should use it:

- Put this in the main demo slide.
- Explain: left/baseline is no-memory; right/memory is approved road-sign memory.

Message to say:

```text
The world model generates candidate videos. The external memory module selects the candidate that is more consistent with remembered road-sign evidence.
```

---

## `media/demo_v2/demo_v2_no_memory_seed1.mp4`

Purpose:

- Individual baseline video.

Data/content inside:

- Candidate selected by the no-memory baseline.
- This is the baseline side of the comparison.

How teammates should use it:

- Use only if the side-by-side video is not enough.
- Do not claim this is the only possible no-memory output; it is the selected baseline candidate in this experiment package.

---

## `media/demo_v2/demo_v2_with_memory_seed8_or_best.mp4`

Purpose:

- Individual with-memory video.

Data/content inside:

- Candidate selected by approved road-sign memory.
- In the current package, this corresponds to seed8 / best memory-selected candidate.

How teammates should use it:

- Use next to the baseline video if making a custom PPT animation.

---

## `media/demo_v2/README.md`

Purpose:

- Explains what the demo videos mean.

Data/content inside:

- Recommended video.
- Meaning of no-memory and with-memory videos.
- Reminder that videos are compressed for GitHub.

How teammates should use it:

- Read before putting videos into PPT.

---

# 3. Final assignment documents

## `docs/final/assignment_requirement_mapping_v2.md`

Purpose:

- Directly maps the project to the AP0006 final project requirements.

Data/content inside:

- Project topic: Memory Modules in World Models.
- Base model: Matrix-Game-2.
- Definition of memory in this project.
- Requirement A: memory module analysis.
- Requirement B: memory visualization.
- Requirement C: new memory strategy design.
- Evaluation and honest claim.

How teammates should use it:

- Use this to write the report introduction and assignment alignment section.
- Use it to answer: “Are we actually following the assignment?”

---

## `docs/final/final_assignment_memory_results_v2_expanded.md`

Purpose:

- Main written result document for the final project.

Data/content inside:

- Executive summary.
- Base model and task.
- Memory design.
- Memory lifecycle.
- Experimental protocol.
- Candidate pool.
- Memory strategies.
- Result tables.
- Random-memory control.
- Manual visual review.
- Proxy metrics.
- Demo video.
- Claims and limitations.

How teammates should use it:

- Treat this as the main source for final report writing.
- Convert its sections into PPT slides.

---

## `docs/final/demo_v2_report.md`

Purpose:

- Explains what demo v2 shows and how it was chosen.

Data/content inside:

- Demo diagnosis.
- Which videos were used.
- Why the demo is memory-related.
- Why this is not internal memory injection.
- Notes about candidate pool and selected output.

How teammates should use it:

- Use for the demo slide speaker notes.
- Use if asked why this video proves memory affects output.

---

## `docs/final/TEAMMATE_FILE_DATA_GUIDE.md`

Purpose:

- This file. It explains every important file and dataset in the GitHub package.

How teammates should use it:

- Keep it open while preparing slides.
- Use it to decide which data table or figure belongs to each slide.

---

# 4. Story documents

## `docs/story/experiment_story_and_direction.md`

Purpose:

- Explains the research story.

Data/content inside:

- Why spatial forgetting matters.
- Why GTA-style scenes are useful.
- Why generic keyframe memory was weak.
- Why landmark memory is better.
- Why approved road-sign memory is the final chosen case.

How teammates should use it:

- Use for Slide 1–3: motivation, problem, direction.

---

## `docs/story/evidence_ladder_v2.md`

Purpose:

- Organizes evidence by strength.

Data/content inside:

- Level 1: pipeline feasibility.
- Level 2: generic memory weak evidence.
- Level 3: landmark memory.
- Level 4: approved road-sign memory.
- Level 5: expanded controls and demo v2.

How teammates should use it:

- Use for the “experiment progression” slide.
- It explains why the project evolved from generic memory to object-level memory.

---

## `docs/story/limitations_and_next_experiments.md`

Purpose:

- Lists limitations and future experiments.

Data/content inside:

- External reranking only.
- No internal memory injection.
- Qualitative / case-study evidence.
- Limited scene count.
- Memory score is a proxy, not perfect human perception.
- Manual annotation bias.
- Future work: more objects, more seeds, random trials, human evaluation, 3D memory, internal conditioning.

How teammates should use it:

- Use for the limitations and future work slides.
- This protects us from overclaiming.

---

# 5. Presentation documents

## `docs/presentation/presentation_outline_for_teammates.md`

Purpose:

- Slide-by-slide outline.

Data/content inside:

- Suggested 12-slide structure.
- Motivation, base model, memory insertion, lifecycle, data structure, experiment design, demo, results, interpretation, limitations, future work, conclusion.

How teammates should use it:

- Use as the PPT skeleton.

---

## `docs/presentation/slide_content_draft.md`

Purpose:

- Slide-ready bullet points.

Data/content inside:

- Short bullets per slide.

How teammates should use it:

- Copy into PowerPoint and rewrite for style.

---

## `docs/presentation/speaker_notes_draft.md`

Purpose:

- Chinese speaker notes.

Data/content inside:

- What to say for each slide.

How teammates should use it:

- Use for oral presentation rehearsal.

---

# 6. Result tables

## `results/final/expanded_memory_strategy_scores.csv`

Purpose:

- Strategy-level result table.

Data/content inside:

Each row corresponds to a memory strategy, such as:

- no_memory
- uniform_memory
- recent_only
- random_memory
- wrong_scene_memory
- auto_landmark_memory
- manual_landmark_memory_v2
- approved_roadsign_memory

Typical columns:

- strategy
- candidate_pool
- selected_seed
- memory_score
- rank
- control_type
- source
- interpretation

How teammates should use it:

- Use for the main results slide.
- This table answers: “Which memory strategy selected which candidate?”

Important interpretation:

```text
approved_roadsign_memory selects seed8, while no_memory selects seed1.
```

---

## `results/final/all_candidate_scores_by_strategy.csv`

Purpose:

- Candidate-level score table.

Data/content inside:

Each row is a candidate seed under a memory strategy.

Typical columns:

- strategy
- seed
- score
- rank
- selected
- candidate_path

How teammates should use it:

- Use to show that we are not only reporting the selected seed.
- Use for backup if judge asks for full candidate pool.

Current limitation:

```text
Candidate pool is seed1..8. seed9..16 are not included in this package.
```

---

## `results/final/final_memory_ablation_table.csv`

Purpose:

- Compact earlier ablation table.

Data/content inside:

- A smaller summary of strategy vs selected seed.

How teammates should use it:

- Use only if you need a simpler table.
- Prefer `expanded_memory_strategy_scores.csv` for the final PPT.

---

## `results/final/expanded_memory_strategy_scores.md`

Purpose:

- Markdown-readable version of the expanded strategy table.

How teammates should use it:

- Easier to read in GitHub than the CSV.

---

# 7. Evaluation tables

## `results/evaluation/random_memory_trials.csv`

Purpose:

- Random-memory control table.

Data/content inside:

- Existing 10 random-memory trials.
- Which seed random memory selected in each trial.
- Scores and notes if available.

How teammates should use it:

- Use to show we included a chance / nonspecific-memory control.

Important limitation:

```text
Only 10 existing random trials are included.
This is a control check, not a statistical proof.
```

---

## `results/evaluation/random_memory_distribution.md`

Purpose:

- Human-readable summary of random-memory results.

Data/content inside:

- Distribution of selected seeds across random trials.
- Whether random memory selected the same seed as approved road-sign memory.

How teammates should use it:

- Use for backup Q&A.

---

## `results/evaluation/automatic_proxy_metrics.csv`

Purpose:

- Automatic proxy metric table.

Data/content inside:

- Memory similarity score.
- Road-sign similarity or related proxy score.
- Candidate rank.
- Notes.

How teammates should use it:

- Use to show we attempted quantitative-style evaluation.

Important limitation:

```text
These are proxy metrics. They do not perfectly equal human visual judgment.
```

---

## `results/evaluation/automatic_proxy_metrics.md`

Purpose:

- Explanation of the proxy metrics.

How teammates should use it:

- Read before presenting the metric table, so we do not overclaim.

---

## `results/evaluation/manual_review_table_template.csv`

Purpose:

- Manual visual evaluation template.

Data/content inside:

Columns such as:

- seed
- strategy
- road_sign_present
- road_sign_position_consistent
- road_sign_appearance_consistent
- scene_quality
- artifact_level
- overall_preference
- reviewer_notes

How teammates should use it:

- If time allows, manually fill this table after watching the demo videos and contact sheets.
- If not filled, call it a template only.

Important limitation:

```text
Do not present this as completed human evaluation unless it has been filled by actual reviewers.
```

---

# 8. Figures and visualizations

## `figures/demo_v2/demo_v2_contact_sheet.png`

Purpose:

- Main still-image visual summary of demo v2.

Data/content inside:

- Road-sign memory target.
- No-memory selected frame.
- Memory-selected frame.
- Score/rank summary if included.

How teammates should use it:

- Use in the main demo/results slide.

---

## `figures/demo_v2/demo_v2_contact_sheet.html`

Purpose:

- HTML version of the demo contact sheet.

How teammates should use it:

- Open in browser if PNG is too small.

---

## `figures/demo_v2/manual_review_contact_sheet.png`

Purpose:

- Contact sheet for manual visual review.

Data/content inside:

- Representative frames from candidate videos.
- Used to inspect road-sign presence, consistency, and visual quality.

How teammates should use it:

- Use with `manual_review_table_template.csv`.

---

## `figures/final/no_memory_vs_memory_contact_sheet.png`

Purpose:

- Earlier final contact sheet comparing no-memory and memory.

How teammates should use it:

- Use as a backup visual if demo v2 contact sheet is not clear.

---

## `figures/final/roadsign_memory_target.png`

Purpose:

- Shows the approved road-sign memory target.

How teammates should use it:

- Use when explaining what the memory stores.

---

## `figures/final/memory_pipeline_diagram.md`

Purpose:

- Text diagram of the memory pipeline.

Data/content inside:

- Frozen Matrix-Game-2.
- first_visit generation.
- memory write.
- memory read.
- rerank candidates.
- selected final output.

How teammates should use it:

- Convert this into a PPT diagram.

---

## `figures/final/final_ablation_summary.md`

Purpose:

- Markdown summary of the final ablation.

How teammates should use it:

- Use as a simple result table in slides.

---

# 9. Reproduction and code files

## `scripts/run/reproduce_gta_roadsign_memory.sh`

Purpose:

- Main reproduction entrypoint.

Data/content inside:

- Environment checks.
- Checkpoint checks.
- GTA first-visit generation.
- Candidate generation.
- Memory bank construction.
- Retrieval.
- Reranking.
- Contact sheet/report generation.

How teammates should use it:

- Use only if they want to reproduce the experiment.
- For PPT writing, they do not need to run it.

---

## `scripts/external_memory/extract_keyframes.py`

Purpose:

- Memory Writer helper.

Data/content inside:

- Extracts keyframes from first-visit videos.

---

## `scripts/external_memory/build_memory_bank.py`

Purpose:

- Memory Encoder helper.

Data/content inside:

- Encodes frames/crops into features and writes memory entries.

---

## `scripts/external_memory/build_landmark_memory.py`

Purpose:

- Landmark / road-sign memory builder.

Data/content inside:

- Uses keyframes or crops to construct memory bank entries.

---

## `scripts/external_memory/retrieve_memory.py`

Purpose:

- Memory Retriever.

Data/content inside:

- Retrieves memory entries using similarity.

---

## `scripts/external_memory/rerank_candidates.py`

Purpose:

- Memory Reranker.

Data/content inside:

- Scores candidate videos and selects final output.

---

## `scripts/external_memory/evaluate_contact_sheet.py`

Purpose:

- Visualization helper.

Data/content inside:

- Creates contact sheets for selected candidates.

---

# 10. Setup / reproducibility docs

## `docs/00_FOR_TEAMMATES_READ_THIS_FIRST.md`

Purpose:

- General teammate onboarding.

How teammates should use it:

- Read if they need project-level context.

---

## `docs/01_TEAMMATE_SETUP_GUIDE.md`

Purpose:

- Setup guide for cloning Matrix-Game-2 and this repo.

How teammates should use it:

- Use only if they need to run the code.

---

## `docs/02_MEMORY_MODULE_LOCATION.md`

Purpose:

- Explains exactly where memory is added.

Data/content inside:

- Memory is outside Matrix-Game-2.
- No internal architecture modification.
- Writer / Encoder / Retriever / Reranker code map.

How teammates should use it:

- Use for the “where memory is added” slide.

---

## `docs/03_REPRODUCTION_COMMANDS.md`

Purpose:

- Lists commands for environment check, checkpoint check, smoke, and full mode.

How teammates should use it:

- Use only if reproducing.

---

## `docs/04_CHECKPOINT_DOWNLOAD_PAGE.md`

Purpose:

- Explains Matrix-Game-2 checkpoint layout.

How teammates should use it:

- Use only if reproducing.

---

## `docs/05_KNOWN_LIMITATIONS_FOR_REPRO.md`

Purpose:

- Reproduction limitations.

How teammates should use it:

- Use when debugging environment or checkpoint issues.

---

# 11. What to use for each slide

## Slide: Motivation

Use:

- `docs/story/experiment_story_and_direction.md`
- `docs/story/evidence_ladder_v2.md`

Main point:

```text
World models can forget persistent objects during long-horizon generation.
```

---

## Slide: Method

Use:

- `docs/02_MEMORY_MODULE_LOCATION.md`
- `figures/final/memory_pipeline_diagram.md`

Main point:

```text
Memory is external: write memory, retrieve memory, rerank candidates.
```

---

## Slide: Data structure

Use:

- `docs/final/final_assignment_memory_results_v2_expanded.md`
- `figures/final/roadsign_memory_target.png`

Main point:

```text
Memory stores keyframes, road-sign crops, bounding boxes, feature vectors, and metadata.
```

---

## Slide: Demo

Use:

- `media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4`
- `figures/demo_v2/demo_v2_contact_sheet.png`

Main point:

```text
No-memory selects seed1; approved road-sign memory selects seed8.
```

---

## Slide: Results

Use:

- `results/final/expanded_memory_strategy_scores.csv`
- `results/final/all_candidate_scores_by_strategy.csv`
- `results/evaluation/random_memory_trials.csv`

Main point:

```text
Object-level approved memory is more targeted than generic memory controls.
```

---

## Slide: Evaluation and controls

Use:

- `results/evaluation/automatic_proxy_metrics.csv`
- `results/evaluation/manual_review_table_template.csv`
- `figures/demo_v2/manual_review_contact_sheet.png`

Main point:

```text
We include proxy metrics and a manual review protocol, but we do not claim a complete benchmark.
```

---

## Slide: Limitations and future work

Use:

- `docs/story/limitations_and_next_experiments.md`

Main point:

```text
This is external reranking and case-study evidence; future work should add more scenes, more seeds, human evaluation, and 3D/internal memory.
```

---

# 12. Final presentation warning

Use these exact safe claims:

```text
We add memory outside Matrix-Game-2.
The base world model remains frozen.
The memory stores first-visit visual evidence.
The memory is read during candidate reranking.
The final selected output changes from no-memory seed1 to approved-memory seed8.
This is case-study evidence that external object-level memory can influence generation selection.
```

Avoid these unsafe claims:

```text
Matrix-Game-2 learned long-term memory.
We solved spatial forgetting.
The model internally remembers the road sign.
This result is statistically proven.
```
