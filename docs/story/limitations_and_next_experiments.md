# Limitations and Next Experiments

## Current limitations

1. External reranking only
2. No internal memory injection
3. Qualitative / case-study evidence
4. Limited number of scenes
5. Memory score does not fully equal human perception
6. Manual road-sign annotation introduces human bias
7. Videos are compressed for GitHub demo

### Failure-case / weak-evidence explanation (required for final presentation)

- Primary claim is from a single GTA road-sign scenario.
- Candidate pool is only seeds `1..8`.
- Random-memory control has 10 trials only.
- Manual-review table is mostly template state unless human reviewers fill all frame-stage rows.
- The package therefore supports controlled case-study conclusions, not general long-horizon-memory claims.

## Why this is still valid for the assignment

The assignment asks us to study memory modules in world models.

Our project satisfies this by implementing and analyzing an external memory module:

- storage: keyframes and crops
- read: retrieval and similarity scoring
- use: candidate reranking
- effect: final selected generation changes

## How to phrase limits in AP0006 slides

Use one line in slide notes:

```text
This design demonstrates a working external reranking memory module in one case study; evidence is strengthened by controls but bounded by a small seed pool and pending human review completion.
```

## Failure case / weak evidence

- This claim is demonstrated in a single GTA case with one approved road-sign object.
- Random-memory control is limited to 10 trials; this is not a full statistical control.
- Candidate pool is seed1..8 in this package, not seed1..16.
- Manual review table is primarily a template and can be filled by human reviewers before claiming completed human validation.
- The strongest valid wording remains "case-study + control-based evidence."

## Next experiments

### Experiment 1: More object-level memories

Use multiple road signs, cars, lane markers, and building corners.

### Experiment 2: Larger seed pool

Generate seeds 1 to 32 to make reranking more robust.

### Experiment 3: Repeated random-memory trials

Run 50 random-memory trials to estimate chance baseline.

### Experiment 4: Human evaluation

Ask annotators whether the remembered object is present and consistent.

### Experiment 5: 3D memory

Use depth, point clouds, or Gaussian scaffolds as memory.

### Experiment 6: Internal memory conditioning

Future work can inject retrieved memory into model conditioning rather than only reranking.
