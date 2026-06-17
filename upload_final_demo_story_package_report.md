# Final Demo Story Package Upload Report

## Diagnosis

- PASS_FINAL_DEMO_STORY_PACKAGE_UPLOADED

## Branch

final-assignment-demo-video-and-story-20260617

## Commit

ead7f2e

## Pushed

Yes

## Uploaded demo videos

- `media/demo/no_memory_seed1.mp4`
- `media/demo/with_roadsign_memory_seed8.mp4`
- `media/demo/no_memory_vs_roadsign_memory_side_by_side.mp4`

## Uploaded assignment docs

- `docs/final/assignment_requirement_mapping.md`
- `docs/final/final_assignment_memory_results_expanded.md`

## Uploaded story docs

- `docs/story/experiment_story_and_direction.md`
- `docs/story/evidence_ladder.md`
- `docs/story/limitations_and_next_experiments.md`

## Result tables

- `results/final/final_memory_ablation_table.csv`
- `results/final/final_memory_ablation_table.md`

## Figures

- `figures/final/no_memory_vs_memory_contact_sheet.png`
- `figures/final/roadsign_memory_target.png`
- `figures/final/memory_pipeline_diagram.md`
- `figures/final/final_ablation_summary.md`

## Safety scan

```text
Repo size: 6.0M
No files >50MB found.
No .safetensors/.pth/.pt/.avi/.mov/.webm files found.
Allowed .mp4 files are present only under media/demo/ and all are far below 50MB.
No credential leakage found; grep hits were only the scan pattern text inside existing documentation.
```

## What teammates should read first

1. `docs/final/assignment_requirement_mapping.md`
2. `docs/story/experiment_story_and_direction.md`
3. `docs/story/evidence_ladder.md`
4. `docs/final/final_assignment_memory_results_expanded.md`

## What teammates should watch first

- `media/demo/no_memory_vs_roadsign_memory_side_by_side.mp4`

## Remaining limitations

- External reranking only, not internal model memory injection
- Case-study style evidence, not a universal benchmark claim
- Manual road-sign approval introduces some human bias
