# Ready for PPT

## 1. One-sentence project claim

```text
We use Matrix-Game-2 as a frozen world model and add an external inference-time memory module. The memory stores first-visit visual evidence and reranks candidate continuations. In the GTA road-sign case study, no-memory selects seed1, while approved road-sign memory selects seed8.
```

Chinese:

```text
我们把 Matrix-Game-2 作为 frozen world model，不训练、不改内部结构；在推理阶段外接 memory module，存 first-visit 的关键帧和人工确认的路牌 crop，并用它 rerank 后续 candidate videos。最终 no-memory 选择 seed1，而 approved road-sign memory 选择 seed8。
```

## 2. PPT slide structure

| Slide | Title | Core message | Main file |
|---|---|---|---|
| 1 | Motivation | World models suffer from spatial forgetting | `docs/story/experiment_story_and_direction.md` |
| 2 | Base Model | Matrix-Game-2 is frozen | `docs/final/final_assignment_memory_results_v2_expanded.md` |
| 3 | Memory Location | Memory is external, not inside Matrix-Game-2 | `docs/02_MEMORY_MODULE_LOCATION.md` |
| 4 | Memory Lifecycle | write / read / update / use | `docs/final/memory_card_and_cost_analysis.md` |
| 5 | Memory Data | keyframes, crops, bbox, feature vectors | `figures/final/roadsign_memory_target.png` |
| 6 | Experiment Design | baseline + controls + final method | `results/final/expanded_memory_strategy_scores.csv` |
| 7 | Demo | no-memory seed1 vs memory seed8 | `media/demo_v2/demo_v2_no_memory_vs_memory_annotated.mp4` |
| 8 | Results | memory changes selected candidate | `results/final/all_candidate_scores_by_strategy.csv` |
| 9 | Evidence Strength | case-study + controls | `docs/story/evidence_ladder_v2.md` |
| 10 | Limitations | not internal memory, not universal proof | `docs/story/limitations_and_next_experiments.md` |
| 11 | Future Work | more seeds, more objects, 3D memory | `docs/story/limitations_and_next_experiments.md` |
| 12 | Conclusion | external object memory can guide frozen world models | README safe claim |

## 3. Demo narration

Use this when playing:

```text
This demo shows the same frozen Matrix-Game-2 generation setup. The left side is the no-memory baseline selected candidate, seed1. The right side is the candidate selected by approved road-sign memory, seed8. The base model is unchanged. The memory module stores first-visit road-sign evidence and reranks candidate videos after generation.
```

Chinese:

```text
这个 demo 展示同一个 frozen Matrix-Game-2 生成流程下，外部 memory controller 如何改变最终候选选择。左边是 no-memory baseline，对应 seed1。右边是 approved road-sign memory 选择的结果，对应 seed8。Memory 不改变模型参数，只是在候选生成后根据 first-visit road-sign memory 进行 reranking。
```

## 4. Results to emphasize

Main completed result:

```text
no_memory -> seed1
approved_roadsign_memory -> seed8
```

Control evidence:

```text
uniform_memory
recent_only
random_memory
wrong_scene_memory
auto_landmark_memory
manual_landmark_memory_v2
approved_roadsign_memory
```

Main table:

```text
results/final/expanded_memory_strategy_scores.csv
```

Backup candidate-level table:

```text
results/final/all_candidate_scores_by_strategy.csv
```

Current evidence tier:

```text
MINIMUM_PASS / case-study + controls evidence
```

Do not present this as a large-scale benchmark.

## 5. Teacher / TA Q&A

### Q: Is Matrix-Game-2 trained or modified?

```text
No. Matrix-Game-2 is frozen. We do not modify its DiT, attention layers, checkpoints, or training code.
```

### Q: Where is the memory added?

```text
The memory is added outside Matrix-Game-2, at the inference-time candidate-selection layer.
```

### Q: Why does it count as memory?

```text
It stores historical visual evidence, reads it later, and uses it to change final candidate selection.
```

### Q: What is stored?

```text
first-visit keyframes, landmark crops, approved road-sign crops, bbox metadata, feature vectors, and JSONL memory entries.
```

### Q: What is the main result?

```text
No-memory baseline selects seed1. Approved road-sign memory selects seed8.
```

### Q: Did we solve spatial forgetting?

```text
No. We provide case-study evidence that external object-level memory can influence candidate selection. We do not claim spatial forgetting is universally solved.
```

### Q: How do you avoid cherry-picking?

```text
We include strategy-level results, candidate-level scores, random-memory controls, wrong-scene control, recent-only control, proxy metrics, and a manual review template.
```

## 6. Safe claims

Can say:

```text
External object-level memory can change final candidate selection in a frozen world model.
```

Can say:

```text
The method is an external memory controller, not internal model modification.
```

Cannot say:

```text
Matrix-Game-2 internally learned long-term memory.
We solved spatial forgetting.
This is statistically significant large-scale proof.
Manual review is completed if only the template exists.
```

## 7. Current limitations

```text
Candidate pool is seed1..8.
Random-memory trials are existing 10 trials.
Manual review is a fillable template unless reviewers actually fill it.
Memory is external reranking only.
```

## 8. Future upgrades

```text
seed1..16 / seed1..32 candidate pool
30 / 50 random-memory trials
multi-object memory targets
filled human visual review
cost analysis table
3D memory using depth / point cloud / Gaussian scaffold
internal memory conditioning in future work
```
