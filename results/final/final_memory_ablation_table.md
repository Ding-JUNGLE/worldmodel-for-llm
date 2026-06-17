# Final Assignment Ablation Table (Compact)

This table summarizes the final ablation variants used for assignment-style comparison.

| strategy | selected_seed | memory_score | notes |
|---|---:|---:|---|
| no_memory | 1 | -- | Baseline selection without memory retrieval |
| uniform_memory | 1 | 0.941255 | Uniform memory from keyframes |
| auto_landmark_memory | 6 | 0.836442 | Auto-landmark crops |
| recent_only | 7 | 0.899912 | Memory from recent 3 keyframes |
| wrong_scene_memory | 5 | 0.661841 | Wrong-scene control |
| manual_landmark_memory_v2 | 3 | 0.975133 | PROVISIONAL manual landmark proxy |
| approved_roadsign_memory | 8 | 0.799019 | HUMAN_APPROVED road-sign memory |
| random_memory | 1 (mode) | 0.926306(mean) | Random-control distribution: seed1=7/10, seed7=3/10 |
