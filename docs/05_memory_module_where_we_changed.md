# Where We Changed the Memory Mechanism

## Did we modify Matrix-Game-2 internals?

No.

We did not modify the core Matrix-Game-2 DiT, attention, checkpoints, or training code.

## What did we add?

We added an external inference-time memory controller.

## Memory Writer

Stores first-visit frames and landmark crops.

## Memory Encoder

Extracts visual features from full frames or crops.

## Memory Retriever

Reads historical memory entries and computes similarity.

## Memory Reranker

The frozen world model generates multiple candidate continuations. The memory module scores each candidate against historical memory and selects the best candidate.

## Memory variants tested

1. no_memory
2. uniform_memory
3. recent_only
4. random_memory
5. wrong_scene_memory
6. auto landmark memory
7. provisional manual landmark memory
8. approved road-sign memory

## Why this satisfies the project

The memory module stores historical information, reads it later, and changes the selected generation output.

## Important limitation

This is external reranking, not internal memory injection.

## Code map

```text
scripts/external_memory/
  extract_keyframes.py
  build_memory_bank.py
  retrieve_memory.py
  rerank_candidates.py
  build_landmark_memory.py
  evaluate_contact_sheet.py
```

If exact script names differ, check `scripts/external_memory/README.md`.
