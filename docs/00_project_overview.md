# Project Overview

## Project Topic

Memory modules in world models.

## Our Choice

We use Matrix-Game-2 as a frozen world model.

## Why Matrix-Game-2

Matrix-Game-2 supports interactive world generation and provides GTA / TempleRun style checkpoints. These styles contain visible landmarks such as road signs, vehicles, buildings, traffic lights, and road layout.

## Project Question

Can an inference-time external memory module help a frozen world model preserve previously seen objects or landmarks?

## Our Answer

We add external keyframe / landmark / road-sign memory. The memory does not modify the world model internally. Instead, it reranks candidate continuations based on similarity to remembered objects.

## Main Case Study

In GTA-style generation, a right-side road sign is visible before the vehicle passes it but can disappear in later continuations. We use this road sign as an approved memory target.
