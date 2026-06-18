# Distractor Memory Controls

Source table: `results/evaluation/distractor_memory_controls.csv`

## What was compared

- approved road-sign memory with object-patch reranking
- deterministic random crop memory
- same-frame non-road-sign crop memory
- existing `uniform_memory`
- existing `recent_only`
- existing `wrong_scene_memory`
- existing `random_memory`

## Main finding

This is the most important weak-evidence result in V3:

- approved object-patch memory selects `seed8`
- random crop object-patch memory also selects `seed8`
- same-frame non-road-sign object-patch memory also selects `seed8`

## Interpretation

The object-patch reranker is operational, but **not yet fully specific** to the intended road-sign target.

That means:

- the memory-size curve is useful evidence
- leave-one-out robustness is useful evidence
- distractor specificity remains a limitation

## Safe claim

We can say that external object-patch memory affects candidate ranking behavior.

We cannot say that the current patch scorer uniquely isolates the target road sign under all distractor conditions.
