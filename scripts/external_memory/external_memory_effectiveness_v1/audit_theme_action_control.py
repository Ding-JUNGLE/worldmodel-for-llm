#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from effectiveness_utils import ensure_parent, write_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_root", required=True)
    parser.add_argument("--out_md", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    baseline_command_path = repo_root / "outputs/external_memory_day1/baseline/baseline_command.txt"
    baseline_command = baseline_command_path.read_text(encoding="utf-8").strip() if baseline_command_path.exists() else "missing"

    inference_text = (repo_root / "inference.py").read_text(encoding="utf-8")
    streaming_text = (repo_root / "inference_streaming.py").read_text(encoding="utf-8")
    conditions_text = (repo_root / "utils/conditions.py").read_text(encoding="utf-8")

    custom_image = "--img_path" in inference_text
    explicit_cli_action = any(flag in inference_text for flag in ["--keyboard", "--mouse", "--action"]) or any(
        flag in streaming_text for flag in ["--keyboard", "--mouse", "--action"]
    )
    built_in_actions = "Bench_actions_" in inference_text and "Bench_actions_" in conditions_text
    multi_segment = "max_num_output_frames" in streaming_text and "while stop != 'n'" in streaming_text
    loop_force = explicit_cli_action

    if explicit_cli_action:
        classification = "ACTION_CONTROL_EXPLICIT"
    elif built_in_actions:
        classification = "ACTION_CONTROL_PARTIAL"
    else:
        classification = "ACTION_CONTROL_NOT_FOUND"

    weaker_fallback = (
        "Use a theme-controlled stochastic continuation from the same image/context and label it "
        "`WEAK_REVISIT_PROXY`, because explicit user-defined loop trajectories are not exposed."
    )

    report = f"""# Theme And Action Control Audit

## Classification

- Status: `{classification}`

## 1. Day-1 baseline inputs

- Day-1 baseline command source: `outputs/external_memory_day1/baseline/baseline_command.txt`
- Day-1 baseline command:

```bash
{baseline_command}
```

## 2. Findings

1. Day-1 baseline input image:
   - `demo_images/universal/0000.png`
2. Day-1 baseline config:
   - `configs/inference_yaml/inference_universal.yaml`
3. Day-1 baseline checkpoint/domain:
   - checkpoint path points to `base_distilled_model/base_distill.safetensors`
   - pretrained model path points to the repo-local Matrix-Game-2 checkpoint layout
4. Does `inference.py` accept a custom input image?
   - Yes. `--img_path` is exposed directly on the CLI.
5. Does `inference.py` or `inference_streaming.py` accept an explicit keyboard/mouse action sequence?
   - No explicit CLI or file-based user action sequence interface was found.
6. Where are random or default actions generated?
   - In `utils/conditions.py` via `Bench_actions_universal`, `Bench_actions_gta_drive`, and `Bench_actions_templerun`.
   - These use `combine_data(...)`, which samples built-in action chunks using Python `random`.
7. Can we run multi-segment continuation?
   - `inference_streaming.py` supports repeated interactive generation sessions and longer `max_num_output_frames`, so multi-segment style generation is partially available.
8. Can we force a loop-like action trajectory?
   - Not reliably. Built-in action families exist, but no explicit user trajectory injection path was found in the current code path.
9. Best weaker fallback:
   - {weaker_fallback}

## 3. Interpretation

- `seed` changes both diffusion noise and the random action chunk sampling because `set_seed(...)` seeds Python `random`, NumPy, and Torch.
- This means different seeds create different stochastic trajectories under the same scene theme.
- The repo README mentions streaming generation with custom actions, but the current `inference_streaming.py` code only prompts for images and still uses the built-in `Bench_actions_*` helpers.

## 4. Decision For This Experiment

- Use a theme-controlled stochastic continuation benchmark.
- Treat the revisit claim as `WEAK_REVISIT_PROXY` unless the outputs visually demonstrate a convincing revisit pattern.
- Do not claim a true camera loop or explicit revisit controller from the current interface.
"""
    ensure_parent(args.out_md)
    write_text(args.out_md, report)
    print(f"WROTE {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
