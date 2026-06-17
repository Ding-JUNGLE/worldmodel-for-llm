# FAQ for Teammates

## Do I need to train the world model?

No.

## Which world model do we use?

Matrix-Game-2.

## Which checkpoint should I use first?

GTA distilled checkpoint.

## Why GTA?

GTA scenes contain road signs, vehicles, traffic lights, buildings, and road layout, which are easier to evaluate for memory.

## What is our memory module?

An external inference-time keyframe / landmark / road-sign memory bank plus candidate reranking.

## Where did we modify memory?

In external scripts, not inside Matrix-Game-2.

## Why use 48 frames?

Our working smoke and baseline use 48 frames; 49 caused an invalid default issue.

## Can I upload checkpoints to GitHub?

No.

## What is our best current evidence?

Approved road-sign memory selected seed 8 in the GTA road-sign memory experiment.
