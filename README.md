# World Model External Memory Project

## Use this branch

```text
final-assignment-demo-v2-expanded-evidence-20260617
```

## Start here

1. Watch:

```text
media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4
```

2. Read:

```text
docs/final/TEAMMATE_FILE_DATA_GUIDE.md
```

3. Main report:

```text
docs/final/final_assignment_memory_results_v2_expanded.md
```

4. Assignment mapping:

```text
docs/final/assignment_requirement_mapping_v2.md
```

5. Result tables:

```text
results/final/expanded_memory_strategy_scores.csv
results/final/all_candidate_scores_by_strategy.csv
results/evaluation/random_memory_trials.csv
results/evaluation/automatic_proxy_metrics.csv
```

6. Figures:

```text
figures/demo_v2/demo_v2_contact_sheet.png
figures/final/roadsign_memory_target.png
figures/final/memory_pipeline_diagram.md
```

## Main claim

Matrix-Game-2 is frozen.
Memory is external.
No-memory selects seed1.
Approved road-sign memory selects seed8.
External object-level memory changes the final selected generation output.

## Safe limitation

This is case-study and control-based evidence.
It is not a universal proof that spatial forgetting is solved.
It is external candidate reranking, not internal Matrix-Game-2 memory injection.

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

## Reproduction entrypoint

```bash
bash scripts/run/reproduce_gta_roadsign_memory.sh \
  --matrix-game2-root /path/to/Matrix-Game-2 \
  --output-root /path/to/repro_outputs \
  --mode smoke
```

## What Is Not Included

- No model checkpoints.
- No full-resolution generated videos.
- No full output folders.
- No private credentials.
- No training artifacts.

Only compressed demo videos are included under `media/demo/` and `media/demo_v2/`.
