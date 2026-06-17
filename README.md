# World Model External Memory Project

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

The videos are not uploaded to GitHub. Only lightweight figures, CSVs, JSON manifests, and Markdown reports are included.

## What Is Not Included

- No model checkpoints
- No generated videos
- No full output folders
- No private credentials
- No training artifacts
