# Ablation Summary (Final Assignment)

| strategy | selected_seed | memory_score | note |
|---|---:|---:|---|
| no_memory | 1 | N/A | Baseline frozen rerank disabled |
| uniform_memory | 1 | 0.941255 | All 12 first-visit frames, uniform landmark memory |
| auto_landmark_memory | 6 | 0.836442 | Auto landmark crops |
| recent_only | 7 | 0.899912 | Recent 3 keyframes |
| wrong_scene_memory | 5 | 0.661841 | Wrong-scene negative-control memory |
| manual_landmark_memory_v2 | 3 | 0.975133 | Provisional manual landmark proxy |
| approved_roadsign_memory | 8 | 0.799019 | Human-approved road-sign memory |
| random_memory | 1 (mode) / 7 | 0.926306(mean of 10 trials), max 0.944455 | Seed distribution: {1:7, 7:3} |
