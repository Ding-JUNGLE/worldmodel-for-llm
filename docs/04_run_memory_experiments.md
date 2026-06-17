# Running Memory Experiments

## Overview

Our memory experiments do not train the world model. We freeze Matrix-Game-2 and run external memory reranking.

## Experiment A: GTA Landmark Memory V1

Goal:

Compare no-memory, uniform-memory, recent-only, random-memory, wrong-scene-memory, and landmark-memory.

Expected previous result:

```text
PASS_MEDIUM_GTA_MEMORY_ABLATION
No-memory selected: seed 1
Uniform-memory selected: seed 1
Landmark-memory selected: seed 6
Recent-only selected: seed 7
Wrong-scene selected: seed 5
Random-memory distribution: {1: 7, 7: 3}
```

## Experiment B: GTA Approved Road-Sign Memory V3

Goal:

Use a human-approved right-side road-sign crop as the memory target.

Expected previous result:

```text
PASS_APPROVED_ROADSIGN_MEMORY_RERANK
Approved road-sign memory selected seed 8
```

## Recommended run order

1. Run GTA smoke.
2. Build first-visit frames.
3. Build uniform memory.
4. Build landmark memory.
5. Generate candidate seeds 1 through 8.
6. Run memory strategies.
7. Inspect contact sheet.
8. Fill manual review table.

## Outputs to check

```text
selection_summary.csv
roadsign_annotation_APPROVED.json
roadsign_contact_sheet.png
roadsign_approved_memory_v3_report.md
```
