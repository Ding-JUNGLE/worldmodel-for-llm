# Limitations and Next Experiments

## Current limitations

1. External reranking only
2. No internal memory injection
3. Qualitative / case-study evidence
4. Limited number of scenes
5. Memory score does not fully equal human perception
6. Manual road-sign annotation introduces human bias
7. Videos are compressed for GitHub demo

## Why this is still valid for the assignment

The assignment asks us to study memory modules in world models.

Our project satisfies this by implementing and analyzing an external memory module:

- storage: keyframes and crops
- read: retrieval and similarity scoring
- use: candidate reranking
- effect: final selected generation changes

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
