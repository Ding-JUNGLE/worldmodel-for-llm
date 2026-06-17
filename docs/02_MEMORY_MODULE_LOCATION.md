# Where the Memory Module Is Added

## Short answer

The memory module is not inside Matrix-Game-2.

We do not modify:
- Matrix-Game-2 DiT
- attention layers
- checkpoint weights
- training code
- internal model architecture

Our memory module is an external inference-time controller.

## Pipeline

```text
Matrix-Game-2 frozen world model
        ↓
generate first_visit video
        ↓
Memory Writer stores keyframes / crops
        ↓
Memory Encoder extracts features
        ↓
Memory Retriever reads relevant memories
        ↓
Matrix-Game-2 generates candidate continuations
        ↓
Memory Reranker selects candidate most consistent with memory
```

## Memory Writer

Purpose:

Store historical information from the first-visit video.

Scripts:

```text
scripts/external_memory/extract_keyframes.py
scripts/external_memory/build_landmark_memory.py
```

Stored data:

```text
full keyframes
landmark crops
approved road-sign crops
frame index
bbox coordinates
feature path
metadata
```

## Memory Encoder

Purpose:

Convert images or crops into feature vectors.

Scripts:

```text
scripts/external_memory/build_memory_bank.py
scripts/external_memory/effectiveness_utils.py
scripts/external_memory/memory_utils.py
```

Feature encoder used in our strongest local run:

```text
torchvision_resnet18
```

Fallbacks may be used if dependencies are missing, but reports must state this.

## Memory Retriever

Purpose:

Read historical memory entries and compute similarity.

Scripts:

```text
scripts/external_memory/retrieve_memory.py
```

Input:

```text
query frame or candidate frame
memory_bank.jsonl
feature files
```

Output:

```text
top-k retrieved memory
similarity scores
retrieval visualization
```

## Memory Reranker

Purpose:

Use retrieved memory to select among multiple candidate continuations.

Scripts:

```text
scripts/external_memory/rerank_candidates.py
scripts/run/reproduce_gta_roadsign_memory.sh
```

Input:

```text
candidate_seed1.mp4
candidate_seed2.mp4
...
memory_bank.jsonl
```

Output:

```text
rerank_scores.csv
selected candidate
contact sheet
report.md
diagnosis.txt
```

## Memory variants

We tested:

1. no_memory
2. uniform_memory
3. recent_only
4. random_memory
5. wrong_scene_memory
6. auto landmark memory
7. provisional manual landmark memory
8. approved road-sign memory

## Strongest result

```text
PASS_APPROVED_ROADSIGN_MEMORY_RERANK
```

Approved right-side road-sign memory selected seed 8.

## Why this counts as memory

The system stores historical information, reads it later, and changes the final selected generation output.

## Limitation

This is external candidate reranking, not internal memory-token injection.
