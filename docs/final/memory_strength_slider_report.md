# Memory Strength Slider

This is a visualization demo for **external reranking weight**, not a model-conditioning parameter.

- Fallback used: seed-order baseline proxy because a direct quality score is unavailable.
- Result: low lambda keeps `seed1`, stronger memory weight switches to `seed8`.
