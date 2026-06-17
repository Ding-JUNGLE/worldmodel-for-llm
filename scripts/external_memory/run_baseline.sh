#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$ROOT_DIR/outputs/external_memory_day1/baseline}"
MODEL_DIR="${MODEL_DIR:-$ROOT_DIR/../Matrix-Game-2.0}"
CHECKPOINT_PATH="${CHECKPOINT_PATH:-$MODEL_DIR/base_distilled_model/base_distill.safetensors}"
IMG_PATH="${IMG_PATH:-$ROOT_DIR/demo_images/universal/0000.png}"
CONFIG_PATH="${CONFIG_PATH:-$ROOT_DIR/configs/inference_yaml/inference_universal.yaml}"
NUM_OUTPUT_FRAMES="${NUM_OUTPUT_FRAMES:-48}"
SEED="${SEED:-42}"
CONDA_ENV="${CONDA_ENV:-gr00t_n16_env}"

mkdir -p "$OUTPUT_DIR"

source /home/test/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV" >/dev/null 2>&1

export PYTHONPATH="$ROOT_DIR/experiments/external_memory_day1/compat:${PYTHONPATH:-}"

CMD=(
  python "$ROOT_DIR/inference.py"
  --config_path "$CONFIG_PATH"
  --checkpoint_path "$CHECKPOINT_PATH"
  --img_path "$IMG_PATH"
  --output_folder "$OUTPUT_DIR"
  --num_output_frames "$NUM_OUTPUT_FRAMES"
  --seed "$SEED"
  --pretrained_model_path "$MODEL_DIR"
)

printf '%q ' "${CMD[@]}" > "$OUTPUT_DIR/baseline_command.txt"
printf '\n' >> "$OUTPUT_DIR/baseline_command.txt"

"${CMD[@]}"

if [[ -f "$OUTPUT_DIR/demo.mp4" ]]; then
  cp "$OUTPUT_DIR/demo.mp4" "$OUTPUT_DIR/baseline_seed${SEED}.mp4"
fi
