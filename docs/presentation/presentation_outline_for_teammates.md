# Presentation Outline for Teammates

## Slide 1: Project Motivation
World models can forget short-term spatial cues in long horizon transitions.

## Slide 2: Base Model
We use Matrix-Game-2 as a frozen interactive world model.

## Slide 3: Where Memory Is Added
Memory is added outside Matrix-Game-2, at inference-time candidate selection.

## Slide 4: Memory Lifecycle
Write / Read / Update / Use.

## Slide 5: Memory Data Structure
keyframes, road-sign crops, bbox annotations, feature vectors, JSONL memory bank.

## Slide 6: Experiment Design
no_memory, uniform_memory, recent_only, random_memory, wrong_scene_memory, landmark_memory, approved_roadsign_memory.

## Slide 7: Main Demo
Compare no_memory seed1 against approved_roadsign_memory seed8.

## Slide 8: Results
Ablation table and selected seeds.

## Slide 9: Interpretation
External memory changes selected output and improves object-level consistency signals.

## Slide 10: Limitations
External reranking only, no internal model change, qualitative evidence and limited controls.

## Slide 11: Future Work
Dynamic memory updates, 3D memory, internal conditioning, stronger revisit metrics.

## Slide 12: Conclusion
External object-level memory is a practical way to improve consistency for frozen world models.
