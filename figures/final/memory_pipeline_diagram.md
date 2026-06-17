# Memory Pipeline Diagram

```text
Matrix-Game-2 frozen world model
        ↓
first_visit generation
        ↓
[MEMORY WRITE]
keyframes / landmark crops / road-sign crops
        ↓
candidate generation with multiple seeds
        ↓
[MEMORY READ]
retrieve historical visual memory
        ↓
[MEMORY USE]
rerank candidates
        ↓
selected final output
```

Memory is external.
No Matrix-Game-2 internal architecture change.
