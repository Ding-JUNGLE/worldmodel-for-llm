# Experiment Summary

## Main Runs

### Day 1 External Memory

Diagnosis:

```text
PASS_FULL_MEMORY_RERANK
```

Result:

```text
External memory could affect candidate selection.
```

### GTA Landmark Memory V1

Diagnosis:

```text
PASS_MEDIUM_GTA_MEMORY_ABLATION
```

Selection results:

```text
No-memory selected: seed 1
Uniform-memory selected: seed 1
Landmark-memory selected: seed 6
Recent-only selected: seed 7
Wrong-scene selected: seed 5
Random-memory distribution: seed 1 seven times, seed 7 three times
```

### GTA Road-Sign Approved Memory V3

Diagnosis:

```text
PASS_APPROVED_ROADSIGN_MEMORY_RERANK
```

Result:

```text
Approved road-sign memory selected seed 8.
```

## Interpretation

The approved road-sign experiment is the strongest current evidence. It uses a specific object-level memory target: a right-side road sign that is visible before passing but missing in later continuations.

This gives a clear qualitative case of spatial forgetting / object persistence failure.
