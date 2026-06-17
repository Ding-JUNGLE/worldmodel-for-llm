# World Model External Memory Project

## Overview

This project studies inference-time memory mechanisms for world models.

We use Matrix-Game-2 as a frozen interactive world model and add an external memory module at inference time. The memory stores historical keyframes and landmark crops, retrieves them later, and reranks candidate continuations.

No model training is used.
No Matrix-Game-2 internal architecture is modified.

## Main Idea

Long-horizon world models can forget objects or regions that appeared earlier. In our GTA-style experiment, a right-side road sign appears before passing but disappears in later continuations. We use this road sign as an approved memory target.

## Memory Module

The external memory module has four parts:

1. Memory Writer: stores first-visit keyframes and landmark crops.
2. Memory Encoder: extracts visual features.
3. Memory Retriever: reads relevant historical memory.
4. Memory Reranker: selects the candidate generation most consistent with memory.

## Key Results

- Day 1: external memory bank can affect Matrix-Game-2 output selection.
- GTA landmark memory: landmark-aware memory selected a candidate different from no-memory, recent-only, random-memory, and wrong-scene memory.
- Approved road-sign memory: human-approved road-sign memory selected seed 8.

## What Is Not Included

- No pretrained checkpoints.
- No generated videos.
- No large outputs.
- No training code.
- No internal memory injection into Matrix-Game-2.

## Reproduction

See:
- docs/environment_setup.md
- docs/running_notes.md
- docs/experiment_summary.md
