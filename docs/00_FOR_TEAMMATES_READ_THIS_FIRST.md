# For Teammates: Read This First

## What this repo is

This repo is our project overlay for a world-model memory experiment.

It is not a full copy of Matrix-Game-2.
It does not include pretrained checkpoints.
It does not include generated videos.
It does not include full outputs.

## What you need to reproduce

You need two repositories:

1. Original Matrix-Game repo:
   `SkyworkAI/Matrix-Game`, subfolder `Matrix-Game-2`

2. Our memory project repo:
   `Ding-JUNGLE/worldmodel-for-llm`

## Base world model

We use Matrix-Game-2 as the frozen world model.

We do not train it.
We do not modify its internal architecture.

## Our memory module

Our memory module is external and inference-time only.

It stores historical keyframes / landmark crops / road-sign crops, retrieves them later, and reranks candidate continuations.

## Fast path

1. Read `docs/01_TEAMMATE_SETUP_GUIDE.md`
2. Download checkpoints using `docs/04_CHECKPOINT_DOWNLOAD_PAGE.md`
3. Run environment and checkpoint checks
4. Run GTA smoke
5. Run road-sign memory smoke or full experiment

## Important current status

The repo is designed for reproduction guidance and external memory overlay.

Some scripts may still require local path adaptation depending on your Matrix-Game-2 setup. Always run the checks first.
