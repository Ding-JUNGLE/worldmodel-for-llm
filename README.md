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

1. Read `docs/01_environment_setup_foolproof.md`
2. Download checkpoints using `docs/02_checkpoint_download_and_layout.md`
3. Run smoke tests using `docs/03_run_smoke_tests.md`
4. Run memory experiments using `docs/04_run_memory_experiments.md`
5. Read memory code changes in `docs/05_memory_module_where_we_changed.md`

## What Is Not Included

- No model checkpoints
- No generated videos
- No full output folders
- No private credentials
- No training artifacts
