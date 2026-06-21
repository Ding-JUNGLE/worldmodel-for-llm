# True Generated Demo Classification Report

## Diagnosis

PASS_TRUE_GENERATED_DEMOS_IDENTIFIED

## Human finding

- Old V2 annotated comparison has a persistent overlay issue and should not be used for final presentation.
- Existing V3 files are visualization/analysis videos, not raw world-model generated rollouts.
- True generated demos are tracked separately under `media/generated_demos_checked/`.

## True generated demos

- `media/generated_demos_checked/01_main_clean_no_memory_vs_memory_generated_comparison.mp4`
  - Main recommended comparison.
  - Built from true generated no-memory seed1 and approved-memory seed8 clips.
- `media/generated_demos_checked/02_generated_candidate_pool_gallery.mp4`
  - Optional moving gallery.
  - Assembled from true generated candidate clips rather than static images.
- `media/generated_demos_checked/03_backup_generated_sample_a.mp4`
  - Single true generated no-memory seed1 clip kept as backup evidence.
- `media/generated_demos_checked/04_backup_generated_sample_b.mp4`
  - Single true generated approved-memory seed8 clip kept as backup evidence.

## Visualization-only demos

- `media/demo_v3/demo_v3_object_patch_memory_story.mp4`
- `media/demo_v3/candidate_gallery_memory_selection.mp4`
- `media/demo_v3/memory_strength_slider_demo.mp4`
- `media/demo_v3/correct_vs_wrong_memory_battle.mp4`
- `media/demo_v3/object_patch_heatmap_demo.mp4`

## Deprecated demos

- `media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4`
  - Deprecated because the overlay may block the right-side panel.

## README update

- Quick-path guidance now starts with `media/generated_demos_checked/01_main_clean_no_memory_vs_memory_generated_comparison.mp4`.
- README separates true generated demos from visualization/analysis videos.
- README lists backup true generated clips without calling visualization videos generated rollouts.

## Remaining limitation

- The memory method is still external reranking on top of a frozen Matrix-Game-2 world model.
- The candidate gallery is assembled from true generated clips; it is not itself a single raw rollout from the model.
