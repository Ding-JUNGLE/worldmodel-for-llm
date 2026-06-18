# Evidence Ladder V2

## Stage A/B/C alignment

- **Stage A (memory analysis)**: memory module components, what is stored, and what each strategy does.
- **Stage B (visualization)**: memory pipeline diagram, target card, and demo side-by-side.
- **Stage C (strategy design)**: progression from controls to approved object-level memory.

### Current PASS map

| Stage | Status | Package anchor |
|---|---|---|
| Stage A | PASS | `docs/final/memory_card_and_cost_analysis.md` |
| Stage B | PASS | `figures/final/memory_pipeline_diagram.md`, `media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4` |
| Stage C | PASS | `docs/final/final_assignment_memory_results_v2_expanded.md`, `results/final/expanded_memory_strategy_scores.csv` |

## Level 1: Pipeline works

External memory can be attached to Matrix-Game-2 and used during candidate selection.

## Level 2: Generic memory weak

Full-frame / uniform memory changes scores, but the signal is not specific enough to be decisive.

## Level 3: Landmark memory stronger

Auto landmark memory changes the selected seed away from the no-memory baseline.

## Level 4: Approved road-sign memory strongest

Human-approved object-level memory selects seed8 instead of no-memory seed1.

## Level 5: Expanded controls and demo v2

The expanded package adds:

- a complete seed1..8 candidate-pool report
- repeated random-memory controls (existing 10 trials)
- wrong-scene and recent-only controls
- manual-review contact-sheet template
- automatic proxy metrics
- a clearer annotated demo video

## Evidence weakness (explicit for PPT)

- This package is one road-sign case study with seeds `1..8`.
- Manual review is currently a fillable template (`review_type=template_only`) and has not been fully completed as a human panel corpus.
- Random-memory control is limited (10 trials).
- The table and script-only claim is explicitly documented in `results/evaluation/manual_review_table_template.csv`.
- These limits must be stated in slide notes for honest reporting.
