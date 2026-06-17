# Final Assignment Memory Results Expanded

## One-sentence claim

External object-level memory can change the selected continuation of a frozen Matrix-Game-2 world model.

## Base model

Matrix-Game-2, frozen.

## Memory insertion point

External inference-time candidate-selection layer.

## Memory lifecycle

### Write

After first_visit generation.

### Store

keyframes, crops, bbox, feature vectors, metadata.

### Read

During candidate reranking.

### Update

Static within current run.

### Use

Rerank multiple generated candidates.

## Final ablation table

| strategy | selected_seed | memory_score | notes |
|---|---:|---:|---|
| no_memory | 1 | -- | Baseline selection without memory retrieval |
| uniform_memory | 1 | 0.941255 | Uniform memory from keyframes |
| auto_landmark_memory | 6 | 0.836442 | Auto-landmark crops |
| recent_only | 7 | 0.899912 | Memory from recent 3 keyframes |
| wrong_scene_memory | 5 | 0.661841 | Wrong-scene control |
| manual_landmark_memory_v2 | 3 | 0.975133 | PROVISIONAL manual landmark proxy |
| approved_roadsign_memory | 8 | 0.799019 | HUMAN_APPROVED road-sign memory |
| random_memory | 1 (mode) | 0.926306 (mean) | Random-control distribution: seed1=7/10, seed7=3/10 |

## Demo videos

- no_memory_seed1.mp4
- with_roadsign_memory_seed8.mp4
- no_memory_vs_roadsign_memory_side_by_side.mp4

## Interpretation

Approved road-sign memory selects a different candidate from no-memory baseline.

## Assignment alignment

This project follows the AP0006 final project theme by analyzing memory modules in world models and designing a new memory strategy.
