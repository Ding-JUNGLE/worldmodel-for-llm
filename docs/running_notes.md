# Running Notes

## Important Runtime Notes

1. Use 48 frames, not 49.
2. Do not train the model.
3. Do not modify Matrix-Game-2 internals.
4. Use local checkpoint paths.
5. Keep all new runs under `outputs/runs/<run_id>/`.
6. Always record:
   - command
   - seed
   - checkpoint path
   - config path
   - output path
   - diagnosis label

## Memory Experiment Flow

```text
first_visit video
    ↓
extract keyframes / landmark crops
    ↓
build memory_bank.jsonl
    ↓
generate candidate videos with different seeds
    ↓
rerank candidates using memory score
    ↓
select final candidate
```
