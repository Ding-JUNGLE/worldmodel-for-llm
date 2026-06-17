# AP0006 Assignment Requirement Mapping V2

## Requirement: Memory Module Analysis

We define an external memory module with:

- Writer
- Encoder
- Retriever
- Reranker

## What is stored

- first-visit keyframes
- landmark crops
- approved road-sign crops
- bbox metadata
- feature vectors
- JSONL memory bank entries

## When memory is written

After first_visit generation.

## When memory is read

During candidate reranking.

## How memory is updated

Static within current run.
Future version can update after each selected segment.

## How memory affects generation

It changes final selected candidate from no-memory seed1 to memory-selected seed8.

## Requirement: Memory Visualization

We include:

- memory pipeline diagram
- road-sign memory target
- no-memory vs with-memory demo video
- contact sheet
- ablation table

## Requirement: New Memory Strategy

We move from generic full-frame memory to object-level approved road-sign memory.

## Evaluation

We include:

- ablation table
- random-memory trials
- wrong-scene memory control
- recent-only control
- manual review contact sheet
- automatic proxy metrics

## Honest conclusion

External memory improves candidate selection signal in a case study.
It does not prove universal spatial consistency.
