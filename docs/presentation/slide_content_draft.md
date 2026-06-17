# Slide Content Draft

## Slide 1
- Motivation: frozen world models lose detail over long rollouts
- Need lightweight, inference-time consistency improvement

## Slide 2
- Base model: Matrix-Game-2 (frozen)
- No code-level training changes to model

## Slide 3
- Memory module is external
- Inference control layer only: write → retrieve → rerank

## Slide 4
- First visit generation writes memory
- Candidate generation remains unchanged
- Retrieval selects relevant memory vectors
- Reranker chooses final continuation

## Slide 5
- Memory entries: keyframes + crops + bbox + vectors
- Stored as JSONL for deterministic loading

## Slide 6
- Baseline: no_memory
- Controls: uniform, recent_only, wrong_scene, random_memory
- Semantic: approved_roadsign_memory

## Slide 7
- Show 2-column comparison contact sheet
- Left: No memory seed1
- Right: Approved memory seed8

## Slide 8
- Highlight ablation table:
  - no_memory seed1
  - uniform_memory seed1
  - auto_landmark_memory seed6
  - recent_only seed7
  - wrong_scene seed5
  - approved_roadsign_memory seed8

## Slide 9
- Candidate rerank changes selected seed, indicating memory-aware continuation bias
- Road-sign target appears preserved in selected memory-guided run

## Slide 10
- No internal transformer edits
- No retraining
- Limited diversity of scenes

## Slide 11
- Extend to adaptive memory windows
- Add 3D memory and metric-based rerank confidence

## Slide 12
- External memory controller offers practical path for reproducible consistency gains
