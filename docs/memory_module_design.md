# Memory Module Design

## Memory Type

Inference-time external memory.

## Memory Storage

The memory stores:

- full keyframes
- landmark crops
- approved road-sign crops
- feature vectors
- metadata such as frame index and crop coordinates

## Memory Write

Memory is written after first-visit generation.

## Memory Read

Memory is read during candidate reranking.

## Memory Update

Current memory is mostly static for a run. Future work can update memory after selected candidates.

## Memory Use

The frozen Matrix-Game-2 model generates multiple candidate continuations. The external memory module scores each candidate against historical memory and selects the best candidate.

## Why This Counts as Memory

The memory stores historical information, retrieves it later, and changes the selected generation result.
