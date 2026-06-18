# Memory Size Curve

Source table: `results/evaluation/memory_size_curve.csv`

## Summary

| Memory entries | Selected seed | Score | Interpretation |
|---:|---:|---:|---|
| 1 | 1 | 0.710167 | Single crop is too weak; selection stays near the no-memory baseline |
| 2 | 8 | 0.729899 | Two approved crops are enough to switch selection to `seed8` |
| 4 | 8 | 0.740770 | Full approved bank keeps `seed8` |
| all (=4) | 8 | 0.740770 | Same as 4 crops in the current package |

## Interpretation

The strongest clean V3 signal is not raw realism, but **memory-bank size sensitivity**:

- `1 crop` is not enough
- `2+ crops` push selection to `seed8`

This supports the claim that the external memory bank is being used, while still staying within case-study scope.
