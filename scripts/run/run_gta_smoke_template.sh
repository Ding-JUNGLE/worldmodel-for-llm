#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEFAULT_MG_ROOT=""
DEFAULT_OUTPUT_ROOT=""
SEED=0
FRAMES=48
RUN_ID="gta_smoke_$(date +%Y%m%d_%H%M%S)"

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/run/run_gta_smoke_template.sh \
    --matrix-game2-root /path/to/Matrix-Game-2 \
    --output-root /path/to/output/root \
    [--seed 0] [--frames 48] [--run-id gta_smoke_x]

Notes:
  --frames defaults to 48 and output is written to:
  <output-root>/<run-id>/gta_smoke/gta_smoke_seed<seed>.mp4
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --matrix-game2-root)
      DEFAULT_MG_ROOT="$2"
      shift 2
      ;;
    --output-root)
      DEFAULT_OUTPUT_ROOT="$2"
      shift 2
      ;;
    --seed)
      SEED="$2"
      shift 2
      ;;
    --frames)
      FRAMES="$2"
      shift 2
      ;;
    --run-id)
      RUN_ID="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$DEFAULT_MG_ROOT" || -z "$DEFAULT_OUTPUT_ROOT" ]]; then
  usage >&2
  exit 1
fi

MG_ROOT="$DEFAULT_MG_ROOT"
OUTPUT_ROOT="$DEFAULT_OUTPUT_ROOT"
CHECKPOINT="${DEFAULT_MG_ROOT%/}/gta_distilled_model/gta_keyboard2dim.safetensors"
CONFIG="${DEFAULT_MG_ROOT%/}/configs/inference_yaml/inference_gta_drive.yaml"
IMG_PATH="${DEFAULT_MG_ROOT%/}/demo_images/gta_drive/0000.png"

if [[ ! -f "$MG_ROOT/inference.py" ]]; then
  echo "FAIL_REPRO_COMMAND_UNKNOWN: missing $MG_ROOT/inference.py"
  exit 1
fi
if [[ ! -f "$CHECKPOINT" ]]; then
  echo "FAIL_CHECKPOINTS: missing $CHECKPOINT"
  exit 1
fi
if [[ ! -f "$CONFIG" ]]; then
  echo "FAIL_REPRO_COMMAND_UNKNOWN: missing $CONFIG"
  exit 1
fi
if [[ ! -f "$IMG_PATH" ]]; then
  IMG_PATH="$MG_ROOT/demo_images/universal/0000.png"
fi

RUN_DIR="$OUTPUT_ROOT/$RUN_ID/gta_smoke"
mkdir -p "$RUN_DIR"
mkdir -p "$PROJECT_ROOT"
LOG_FILE="$RUN_DIR/run_command.log"

{
  echo "# Reproduction smoke command"
  echo "python3 \"$MG_ROOT/inference.py\" \\"
  echo "  --config_path \"$CONFIG\" \\"
  echo "  --checkpoint_path \"$CHECKPOINT\" \\"
  echo "  --img_path \"$IMG_PATH\" \\"
  echo "  --output_folder \"$RUN_DIR\" \\"
  echo "  --num_output_frames \"$FRAMES\" \\"
  echo "  --seed \"$SEED\" \\"
  echo "  --pretrained_model_path \"$MG_ROOT\""
} > "$LOG_FILE"

if ! python3 "$MG_ROOT/inference.py" \
  --config_path "$CONFIG" \
  --checkpoint_path "$CHECKPOINT" \
  --img_path "$IMG_PATH" \
  --output_folder "$RUN_DIR" \
  --num_output_frames "$FRAMES" \
  --seed "$SEED" \
  --pretrained_model_path "$MG_ROOT" > >(tee -a "$LOG_FILE") 2>&1; then
  echo "FAIL_GTA_SMOKE: inference command failed"
  exit 1
fi

if [[ ! -f "$RUN_DIR/demo.mp4" ]]; then
  echo "FAIL_GTA_SMOKE: missing generated video at $RUN_DIR/demo.mp4"
  exit 1
fi

cp "$RUN_DIR/demo.mp4" "$RUN_DIR/gta_smoke_seed${SEED}.mp4"

printf 'PASS_GTA_SMOKE\n'
printf 'Expected: %s\n' "$RUN_DIR/gta_smoke_seed${SEED}.mp4"
