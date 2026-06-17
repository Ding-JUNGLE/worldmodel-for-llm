# World Model External Memory Project

## Stronger Final Evidence Package

Use branch:

```text
final-assignment-demo-v2-expanded-evidence-20260617
```

Recommended presentation video:

```text
media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4
```

Main evidence docs:

```text
docs/final/assignment_requirement_mapping_v2.md
docs/final/final_assignment_memory_results_v2_expanded.md
docs/story/evidence_ladder_v2.md
docs/final/demo_v2_report.md
```

Expanded results:

```text
results/final/expanded_memory_strategy_scores.csv
results/final/all_candidate_scores_by_strategy.csv
results/evaluation/random_memory_trials.csv
results/evaluation/automatic_proxy_metrics.csv
results/evaluation/manual_review_table_template.csv
```

Claim:

External object-level memory changes final candidate selection in a frozen Matrix-Game-2 world model.

Limit:

This is a case-study and control-based result, not a universal proof that spatial forgetting is solved.

## Final Assignment Package

Use branch:

```text
final-assignment-demo-video-and-story-20260617
```

This branch contains the complete final assignment package:

```text
docs/final/assignment_requirement_mapping.md
docs/final/final_assignment_memory_results_expanded.md
docs/story/experiment_story_and_direction.md
docs/story/evidence_ladder.md
docs/story/limitations_and_next_experiments.md
media/demo/no_memory_vs_roadsign_memory_side_by_side.mp4
results/final/final_memory_ablation_table.csv
figures/final/
```

## Demo video

Recommended presentation demo:

```text
media/demo/no_memory_vs_roadsign_memory_side_by_side.mp4
```

This compares:

```text
No memory: seed1
Approved road-sign memory: seed8
```

## Main assignment claim

We use Matrix-Game-2 as a frozen world model and add an external inference-time memory module.

The memory stores first-visit keyframes and approved road-sign crops, retrieves them later, and reranks candidate continuations.

This shows that external object-level memory can change the final selected generation output.

## Overview

This project studies inference-time memory mechanisms for world models.

We use Matrix-Game-2 as a frozen interactive world model. We do not retrain the model and do not modify its internal architecture.

Our memory module is external. It stores historical keyframes and landmark crops, retrieves them later, and reranks candidate continuations.

## Base World Model

- World model: Matrix-Game-2
- Original code: `SkyworkAI/Matrix-Game`, subdirectory `Matrix-Game-2`
- Pretrained weights: `Skywork/Matrix-Game-2.0` on Hugging Face
- Styles tested:
  - universal / base
  - GTA driving
  - TempleRun

## Main Idea

Long-horizon world models can forget objects or regions that appeared earlier. In our GTA-style experiments, a right-side road sign appears before passing but disappears in later continuations.

We add an external memory mechanism:

1. Generate a first-visit sequence.
2. Build memory from keyframes and approved road-sign crops.
3. Generate multiple candidate continuations.
4. Rerank candidates by memory similarity.
5. Select the best candidate.

## Current Strongest Result

Diagnosis:

```text
PASS_APPROVED_ROADSIGN_MEMORY_RERANK
```

Approved road-sign memory selected seed 8.

## Quick Start for Teammates

1. Read `docs/00_FOR_TEAMMATES_READ_THIS_FIRST.md`
2. Set up in `docs/01_TEAMMATE_SETUP_GUIDE.md`
3. Read `docs/04_run_memory_experiments.md`
4. Read memory module details in `docs/02_MEMORY_MODULE_LOCATION.md`
5. Run smoke and memory commands via `docs/03_REPRODUCTION_COMMANDS.md`

## For Group Members

Start here:

`docs/00_FOR_TEAMMATES_READ_THIS_FIRST.md`

Most important setup guide:

`docs/01_TEAMMATE_SETUP_GUIDE.md`

Where the memory module is added:

`docs/02_MEMORY_MODULE_LOCATION.md`

Main reproduction command:

```bash
bash scripts/run/reproduce_gta_roadsign_memory.sh \
  --matrix-game2-root /path/to/Matrix-Game-2 \
  --output-root /path/to/repro_outputs \
  --mode smoke
```

## Where is the memory module added?

The memory module is **not** added inside Matrix-Game-2.

We do **not** modify:

- Matrix-Game-2 DiT / transformer
- attention layers
- model checkpoints
- training code
- `inference.py` core generation logic

Instead, we add memory **outside the frozen world model**, at the inference-control layer.

The pipeline is:

```text
Matrix-Game-2 frozen world model
        ↓
generate first_visit video
        ↓
external Memory Writer stores keyframes / landmark crops / road-sign crops
        ↓
Matrix-Game-2 generates multiple candidate continuations with different seeds
        ↓
external Memory Retriever reads historical memory
        ↓
external Memory Reranker scores candidates
        ↓
selected candidate becomes the final output
```


## Final Assignment Results Package

For teammates preparing the presentation/PPT, use:

```text
docs/final/final_assignment_memory_results.md
docs/presentation/presentation_outline_for_teammates.md
docs/presentation/slide_content_draft.md
docs/presentation/speaker_notes_draft.md
results/final/final_memory_ablation_table.csv
figures/final/
```

Main result:

```text
No memory: seed1
Approved road-sign memory: seed8

```

This repository also includes compressed demo videos under `media/demo/`.

## What Is Not Included

- No model checkpoints
- No generated videos
- No full output folders
- No private credentials
- No training artifacts
