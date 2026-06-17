# Final Assignment Start Here

For PPT and report, read in this order:

```text
docs/final/assignment_requirement_mapping.md
docs/story/experiment_story_and_direction.md
docs/story/evidence_ladder.md
docs/final/final_assignment_memory_results_expanded.md
docs/presentation/presentation_outline_for_teammates.md
```

Watch demo:

```text
media/demo/no_memory_vs_roadsign_memory_side_by_side.mp4
```

Use result table:

```text
results/final/final_memory_ablation_table.csv
```

Use figures:

```text
figures/final/
```

## Start Here — Teammate Guide

1. For teammates, read:

```text
docs/00_FOR_TEAMMATES_READ_THIS_FIRST.md
```

2. Then follow:

```text
docs/01_TEAMMATE_SETUP_GUIDE.md
docs/02_MEMORY_MODULE_LOCATION.md
docs/03_REPRODUCTION_COMMANDS.md
docs/04_CHECKPOINT_DOWNLOAD_PAGE.md
docs/05_KNOWN_LIMITATIONS_FOR_REPRO.md
```

3. Reproduction entry command:

```bash
bash scripts/run/reproduce_gta_roadsign_memory.sh \
  --matrix-game2-root /path/to/Matrix-Game-2 \
  --output-root /path/to/repro_outputs \
  --mode smoke
```

## For PPT / presentation

Read:

```text
docs/presentation/presentation_outline_for_teammates.md
docs/presentation/slide_content_draft.md
docs/presentation/speaker_notes_draft.md
```

Use figures from:

```text
figures/final/
```

Use result table from:

```text
results/final/final_memory_ablation_table.csv
```
