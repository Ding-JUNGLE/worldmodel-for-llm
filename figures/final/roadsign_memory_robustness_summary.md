# Road-Sign Memory Robustness Summary

Source table: `results/evaluation/roadsign_memory_robustness.csv`

## Summary

| Variant | Selected seed | Score | Interpretation |
|---|---:|---:|---|
| all approved boxes | 8 | 0.740770 | baseline object-patch approved-memory result |
| single box | 1 | 0.710167 | one crop is too weak; falls back toward baseline |
| leave-one-out (4 variants) | 8 | 0.733486 - 0.739282 | selection stays on `seed8` |
| bbox jitter 5% | 8 | 0.755073 | small annotation movement does not break selection |
| bbox jitter 10% | 8 | 0.767084 | selection remains `seed8` in this case |

## Interpretation

This package shows a mixed but useful robustness story:

- removing memory down to a single box weakens the effect
- keeping three approved crops is still enough
- small bbox jitter does not break the chosen seed

## Caution

Higher scores under jitter do **not** prove a better object-memory mechanism by themselves.
They may also indicate that the patch scorer benefits from nearby context, not only the road sign itself.
