# Assignment Requirement Mapping

## Project Topic

Memory Modules in World Models

## Base world model

We use Matrix-Game-2 as the frozen interactive world model.

## What memory means in this project

The memory module is an external image/feature retrieval bank plus candidate reranker.

It stores first-visit keyframes, landmark crops, and approved right-side road-sign crops.

## Requirement A: Memory Module Analysis

We identify:

- what is stored
- where it is stored
- when memory is written
- when memory is read
- how memory affects generation output

## Requirement B: Memory Visualization

We provide:

- memory pipeline diagram
- road-sign memory target image
- no-memory vs with-memory contact sheet
- compressed side-by-side demo video

## Requirement C: New Memory Strategy Design

We compare:

- no_memory
- uniform_memory
- recent_only
- random_memory
- wrong_scene_memory
- auto_landmark_memory
- approved_roadsign_memory

The new strategy is object-level approved road-sign memory.

## Evaluation

We use qualitative and ablation-style evaluation.

Main result:

```text
No memory: seed1
Approved road-sign memory: seed8
```

## Honest claim

We show that external memory changes final candidate selection.

We do not claim that Matrix-Game-2 internal architecture has long-term memory.
We do not claim that spatial forgetting is fully solved.
