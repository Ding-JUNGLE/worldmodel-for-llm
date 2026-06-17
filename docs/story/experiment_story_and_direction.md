# Experiment Story and Direction

## Motivation

Long-horizon world models often suffer from spatial forgetting: an object seen earlier may disappear or change after the camera moves.

## Why GTA-style scene

GTA driving scenes contain persistent landmarks: road signs, buildings, roads, turns, and lane boundaries.

This makes them suitable for testing whether memory helps object persistence.

## Initial attempt: generic memory

We first tested generic keyframe memory.

Result:

- pipeline worked
- memory affected selection
- but evidence was weak because generic memory could tie with random memory

## Second attempt: landmark memory

We moved from full-frame memory to landmark-aware memory.

Reason:

Full frames include too much background.
Landmark crops make memory more object-specific.

## Final attempt: approved road-sign memory

We manually identified a right-side road sign that appears in first_visit.

This is a clear object-persistence target.

Result:

```text
No memory selected seed1.
Approved road-sign memory selected seed8.
```

## Experimental direction

The project direction is not to retrain Matrix-Game-2.

The direction is to test whether an external memory controller can improve consistency of a frozen world model.

## Future experiments

1. More GTA road signs and traffic objects
2. More seeds and repeated random-memory trials
3. Landmark-level human evaluation
4. 3D memory from depth or point clouds
5. Learned reranker instead of handcrafted feature similarity
6. Internal conditioning or memory tokens in future work
