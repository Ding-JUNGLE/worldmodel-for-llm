# Experiment Results and Interpretation

## Main Result

The strongest current result is:

```text
PASS_APPROVED_ROADSIGN_MEMORY_RERANK
```

Approved road-sign memory selected seed 8.

## Why the road sign matters

The right-side road sign is visible before the vehicle passes it, but disappears in later continuations. This is a clear object persistence / spatial forgetting case.

## Key Runs

### Day 1 External Memory

```text
PASS_FULL_MEMORY_RERANK
```

External memory could affect candidate selection.

### GTA Landmark Memory V1

```text
PASS_MEDIUM_GTA_MEMORY_ABLATION
```

Selection:

```text
No-memory selected: seed 1
Uniform-memory selected: seed 1
Landmark-memory selected: seed 6
Recent-only selected: seed 7
Wrong-scene selected: seed 5
Random-memory distribution: seed 1 seven times, seed 7 three times
```

### GTA Road-Sign Approved Memory V3

```text
PASS_APPROVED_ROADSIGN_MEMORY_RERANK
```

Approved road-sign memory selected seed 8.

## Interpretation

The experiment shows that a specific approved memory target can change candidate selection.

## Do not overclaim

This does not prove that Matrix-Game-2 has internal memory.
This does not fully solve spatial forgetting.
This is an inference-time external memory reranking mechanism.
