#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$ROOT_DIR/outputs/external_memory_day1/candidates}"
MODEL_DIR="${MODEL_DIR:-$ROOT_DIR}"
CHECKPOINT_PATH="${CHECKPOINT_PATH:-$ROOT_DIR/base_distilled_model/base_distill.safetensors}"
IMG_PATH="${IMG_PATH:-$ROOT_DIR/demo_images/universal/0000.png}"
CONFIG_PATH="${CONFIG_PATH:-$ROOT_DIR/configs/inference_yaml/inference_universal.yaml}"
NUM_OUTPUT_FRAMES="${NUM_OUTPUT_FRAMES:-48}"
CONDA_ENV="${CONDA_ENV:-gr00t_n16_env}"
SEEDS_STRING="${CANDIDATE_SEEDS:-0 1 2 3}"

mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR/candidate_commands.txt"

source /home/test/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV" >/dev/null 2>&1
export PYTHONPATH="$ROOT_DIR/experiments/external_memory_day1/compat:${PYTHONPATH:-}"

for SEED in $SEEDS_STRING; do
  RUN_DIR="$OUTPUT_DIR/run_seed${SEED}"
  mkdir -p "$RUN_DIR"
  CMD=(
    python "$ROOT_DIR/inference.py"
    --config_path "$CONFIG_PATH"
    --checkpoint_path "$CHECKPOINT_PATH"
    --img_path "$IMG_PATH"
    --output_folder "$RUN_DIR"
    --num_output_frames "$NUM_OUTPUT_FRAMES"
    --seed "$SEED"
    --pretrained_model_path "$MODEL_DIR"
  )

  {
    printf '%q ' "${CMD[@]}"
    printf '\n'
  } >> "$OUTPUT_DIR/candidate_commands.txt"

  "${CMD[@]}" \
    > >(tee "$OUTPUT_DIR/candidate_seed${SEED}.stdout.log") \
    2> >(tee "$OUTPUT_DIR/candidate_seed${SEED}.stderr.log" >&2)

  if [[ ! -f "$RUN_DIR/demo.mp4" ]]; then
    echo "FAIL_CANDIDATE_GENERATION: missing $RUN_DIR/demo.mp4 for seed $SEED" >&2
    exit 1
  fi

  cp "$RUN_DIR/demo.mp4" "$OUTPUT_DIR/candidate_seed${SEED}.mp4"
  if [[ -f "$RUN_DIR/demo_icon.mp4" ]]; then
    cp "$RUN_DIR/demo_icon.mp4" "$OUTPUT_DIR/candidate_seed${SEED}_icon.mp4"
  fi
done

echo "PASS_CANDIDATE_GENERATION"
