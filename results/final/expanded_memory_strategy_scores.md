# Expanded Memory Strategy Scores

Evidence tier for the current package: `MINIMUM_PASS`.

| strategy | candidate_pool | selected_seed | memory_score | control_type | interpretation |
|---|---|---:|---:|---|---|
| no_memory | seed1..8 | 1 | -- | baseline | Baseline without memory retrieval; default lowest-seed selected. |
| uniform_memory | seed1..8 | 1 | 0.941255 | generic_memory_control | Generic keyframe memory selected the same seed as baseline. |
| recent_only | seed1..8 | 7 | 0.899912 | short_term_control | Short-term memory changed the selected seed away from baseline. |
| random_memory | seed1..8 | 1(mode);7(3/10) | 0.926306 | chance_control | Existing 10 random-memory trials select seed1 seven times and seed7 three times; seed8 was never selected. |
| wrong_scene_memory | seed1..8 | 5 | 0.661841 | negative_control | Wrong-scene memory produces a different but scene-misaligned choice. |
| auto_landmark_memory | seed1..8 | 6 | 0.836442 | objectish_memory | Auto landmark memory changes selection to seed6. |
| manual_landmark_memory_v2 | seed1..8 | 3 | 0.975133 | provisional_manual_memory | Manual proxy is stronger than generic memory but remains provisional. |
| approved_roadsign_memory | seed1..8 | 8 | 0.799019 | approved_object_memory | Human-approved road-sign memory selects seed8 and differs from baseline and random controls. |
