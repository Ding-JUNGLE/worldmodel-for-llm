#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MG_ROOT=""
OUTPUT_ROOT=""
MODE="smoke"
SEED_LIST=""
FRAMES=48
ROADSIGN_ANNOTATION="${PROJECT_ROOT}/results/roadsign_annotation_APPROVED.json"
FIRST_VISIT_VIDEO_REL="first_visit/gta_smoke_seed0.mp4"

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/run/reproduce_gta_roadsign_memory.sh \
    --matrix-game2-root /path/to/Matrix-Game-2 \
    --output-root /path/to/repro_outputs \
    [--mode smoke|full] \
    [--candidate-seeds 1,2,3,4,5,6,7,8] \
    [--frames 48] \
    [--roadsign-annotation results/roadsign_annotation_APPROVED.json]

Smoke mode reproduces with seeds 1 and 2 by default.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --matrix-game2-root)
      MG_ROOT="$2"
      shift 2
      ;;
    --output-root)
      OUTPUT_ROOT="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    --candidate-seeds)
      SEED_LIST="$2"
      shift 2
      ;;
    --frames)
      FRAMES="$2"
      shift 2
      ;;
    --roadsign-annotation)
      ROADSIGN_ANNOTATION="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$MG_ROOT" || -z "$OUTPUT_ROOT" ]]; then
  usage >&2
  exit 1
fi

if [[ "$MODE" != "smoke" && "$MODE" != "full" ]]; then
  echo "FAIL_REPRO_SCRIPT"
  exit 1
fi

if [[ -z "$SEED_LIST" ]]; then
  if [[ "$MODE" == "smoke" ]]; then
    SEED_LIST="1,2"
  else
    SEED_LIST="1,2,3,4,5,6,7,8"
  fi
fi

GTA_CONFIG="$MG_ROOT/configs/inference_yaml/inference_gta_drive.yaml"
GTA_CHECKPOINT="$MG_ROOT/gta_distilled_model/gta_keyboard2dim.safetensors"
GTA_IMAGE="$MG_ROOT/demo_images/gta_drive/0000.png"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ROOT="${OUTPUT_ROOT%/}/repro_${MODE}_${TIMESTAMP}"
mkdir -p "$RUN_ROOT"
COMMAND_FILE="$RUN_ROOT/commands.sh"
DIAG_FILE="$RUN_ROOT/diagnosis.txt"
MANIFEST_FILE="$RUN_ROOT/run_manifest.json"
REPORT_FILE="$RUN_ROOT/report.md"
: > "$COMMAND_FILE"

fail() {
  local label="$1"
  echo "$label" | tee "$DIAG_FILE"
  exit 1
}

write_cmd() { printf '%s\n' "$*" >> "$COMMAND_FILE"; }

log_header() {
  {
    echo "# Reproduction flow"
    echo "matrix_game2_root: $MG_ROOT"
    echo "mode: $MODE"
    echo "frames: $FRAMES"
    echo "candidate_seeds: $SEED_LIST"
    echo "roadsign_annotation: $ROADSIGN_ANNOTATION"
    echo "run_root: $RUN_ROOT"
    echo
  } > "$REPORT_FILE"
}

run_cmd() {
  local log_file="$1"
  shift
  write_cmd "$*"
  if ! "$@" > >(tee "$log_file") 2>&1; then
    return 1
  fi
}

run_inference() {
  local output_dir="$1"
  local seed="$2"
  local config="$3"
  local ckpt="$4"
  local img="$5"
  local log_path="$6"
  mkdir -p "$output_dir"
  run_cmd "$log_path" \
    python "$MG_ROOT/inference.py" \
    --config_path "$config" \
    --checkpoint_path "$ckpt" \
    --img_path "$img" \
    --output_folder "$output_dir" \
    --num_output_frames "$FRAMES" \
    --seed "$seed" \
    --pretrained_model_path "$MG_ROOT"
}

assert_file() {
  local path="$1"
  local label="$2"
  if [[ ! -f "$path" ]]; then
    fail "$label"
  fi
}

write_manifest() {
  cat > "$MANIFEST_FILE" <<EOF
{
  "mode": "$MODE",
  "matrix_game2_root": "$MG_ROOT",
  "run_root": "$RUN_ROOT",
  "frames": $FRAMES,
  "candidate_seeds": "$SEED_LIST",
  "roadsign_annotation": "$ROADSIGN_ANNOTATION",
  "diagnosis": "$DIAG",
  "outputs": {
    "memory_bank": "$MEMORY_DIR/memory_bank.jsonl",
    "rerank_scores": "$RUN_ROOT/rerank_scores.csv",
    "selected_candidate": "$RUN_ROOT/selected_candidate.mp4",
    "contact_sheet_png": "$RUN_ROOT/contact_sheet.png",
    "contact_sheet_html": "$RUN_ROOT/contact_sheet.html",
    "commands": "$COMMAND_FILE"
  }
}
EOF
}

write_summary() {
  {
    echo "# GTA Road-Sign Memory Reproduction Report"
    echo
    echo "Mode: $MODE"
    echo "Diagnosis: $DIAG"
    if [[ "$USE_AUTO_ONLY" -eq 1 ]]; then
      echo "Landmark source: auto-landmark (no annotation fallback)."
    else
      echo "Landmark source: approved annotation."
    fi
    echo
    echo "## Outputs"
    echo "- run_manifest.json"
    echo "- commands.sh"
    echo "- diagnosis.txt"
    echo "- memory_bank.jsonl"
    echo "- rerank_scores.csv"
    echo "- selected_candidate.mp4"
    echo "- contact_sheet.png"
    echo "- contact_sheet.html"
    echo "- report.md"
  } >> "$REPORT_FILE"
}

log_header
echo "PASS_STARTED" | tee "$DIAG_FILE"

if [[ ! -f "$GTA_CONFIG" || ! -f "$GTA_CHECKPOINT" || ! -f "$GTA_IMAGE" ]]; then
  fail "FAIL_REPRO_SCRIPT"
fi

echo "=== Gate 0: environment check ==="
if ! python "$PROJECT_ROOT/scripts/setup/check_environment.py" > "$RUN_ROOT/check_environment.log" 2>&1; then
  fail "FAIL_ENVIRONMENT"
fi

echo "=== Gate 1: checkpoint check ==="
if ! python "$PROJECT_ROOT/scripts/setup/check_checkpoints.py" --matrix_game2_root "$MG_ROOT" > "$RUN_ROOT/check_checkpoints.log" 2>&1; then
  fail "FAIL_CHECKPOINTS"
fi

echo "=== Gate 2: first-visit smoke ==="
FIRST_VISIT_VIDEO="$RUN_ROOT/$FIRST_VISIT_VIDEO_REL"
if [[ -s "$FIRST_VISIT_VIDEO" ]]; then
  echo "reusing existing first-visit: $FIRST_VISIT_VIDEO" > "$RUN_ROOT/gate2_smoke.log"
else
  if ! bash "$PROJECT_ROOT/scripts/run/run_gta_smoke_template.sh" \
    --matrix-game2-root "$MG_ROOT" \
    --output-root "$RUN_ROOT" \
    --seed 0 \
    --frames "$FRAMES" \
    --run-id first_visit \
    > "$RUN_ROOT/gate2_smoke.log" 2>&1; then
    fail "FAIL_GTA_GENERATION"
  fi
fi
assert_file "$FIRST_VISIT_VIDEO" "FAIL_GTA_GENERATION"

echo "=== Gate 3: build keyframe memory ==="
KEYFRAME_DIR="$RUN_ROOT/first_visit_frames"
MEMORY_DIR="$RUN_ROOT/memory"
CANDIDATE_DIR="$RUN_ROOT/candidates"
mkdir -p "$KEYFRAME_DIR" "$MEMORY_DIR" "$CANDIDATE_DIR"
if ! run_cmd "$RUN_ROOT/keyframe_extract.log" \
  python "$PROJECT_ROOT/scripts/external_memory/extract_keyframes.py" \
  --video "$FIRST_VISIT_VIDEO" \
  --out_dir "$KEYFRAME_DIR" \
  --mode uniform \
  --num_keyframes 12; then
  fail "FAIL_REPRO_SCRIPT"
fi

read -r -a SEEDS <<< "$(echo "$SEED_LIST" | tr ',' ' ')"
if [[ "${#SEEDS[@]}" -lt 2 ]]; then
  fail "FAIL_GTA_GENERATION"
fi

for SEED in "${SEEDS[@]}"; do
  run_dir="$CANDIDATE_DIR/run_seed${SEED}"
  if ! run_inference "$run_dir" "$SEED" \
    "$GTA_CONFIG" \
    "$GTA_CHECKPOINT" \
    "$GTA_IMAGE" \
    "$RUN_ROOT/candidate_seed${SEED}.log"; then
    fail "FAIL_GTA_GENERATION"
  fi
  if [[ -f "$run_dir/demo.mp4" ]]; then
    cp "$run_dir/demo.mp4" "$CANDIDATE_DIR/candidate_seed${SEED}.mp4"
  else
    fail "FAIL_GTA_GENERATION"
  fi
done

ANNOTATION_FILE="$RUN_ROOT/approved_landmark_frames"
ROADSIGN_CROP_DIR="$RUN_ROOT/approved_landmark_frames"
mkdir -p "$ROADSIGN_CROP_DIR"
USE_AUTO_ONLY=1

if [[ -f "$ROADSIGN_ANNOTATION" ]]; then
  if python - "$ROADSIGN_ANNOTATION" "$KEYFRAME_DIR" "$ROADSIGN_CROP_DIR" "$PROJECT_ROOT" > "$RUN_ROOT/annotation_status.txt" <<'PY'
import json
import sys
from pathlib import Path
from PIL import Image

annotation_path = Path(sys.argv[1])
frame_dir = Path(sys.argv[2])
out_dir = Path(sys.argv[3])
project_root = Path(sys.argv[4])

try:
    data = json.loads(annotation_path.read_text(encoding="utf-8"))
except Exception:
    raise SystemExit(0)

count = 0
for item in data.get("landmarks", []):
    frame_ref = item.get("frame_path")
    frame_index = item.get("frame_index", 0)
    frame_path = Path(frame_ref) if frame_ref else None
    if frame_path is None or not frame_path.exists():
        if frame_path is not None and not frame_path.is_absolute():
            candidate = (project_root / frame_path).resolve()
            if candidate.exists():
                frame_path = candidate
        if frame_path is None or not frame_path.exists():
            frame_path = frame_dir / f"keyframe_{int(frame_index):06d}.png"
    if not frame_path.exists():
        continue
    bbox = item.get("bbox_xyxy", [])
    if len(bbox) != 4:
        continue
    x1, y1, x2, y2 = map(int, bbox)
    img = Image.open(frame_path).convert("RGB")
    crop = img.crop((max(0, x1), max(0, y1), max(0, x2), max(0, y2)))
    out_path = out_dir / f"keyframe_{count:06d}.png"
    crop.save(out_path)
    count += 1
print(count)
PY
  then
    CROPS="$(cat "$RUN_ROOT/annotation_status.txt" | tr -d '[:space:]')"
    if [[ "$CROPS" =~ ^[0-9]+$ ]] && [[ "$CROPS" -gt 0 ]]; then
      USE_AUTO_ONLY=0
    fi
  fi
fi

if [[ "$USE_AUTO_ONLY" -eq 0 ]]; then
  MEMORY_SOURCE="$ROADSIGN_CROP_DIR"
else
  MEMORY_SOURCE="$KEYFRAME_DIR"
fi

if ! python "$PROJECT_ROOT/scripts/external_memory/build_landmark_memory.py" \
  --keyframes_dir "$MEMORY_SOURCE" \
  --features_dir "$MEMORY_DIR/features" \
  --out_jsonl "$MEMORY_DIR/memory_bank.jsonl" \
  --encoder auto \
  > "$RUN_ROOT/build_memory.log" 2>&1; then
  fail "FAIL_REPRO_SCRIPT"
fi

QUERY_FRAME="$(find "$KEYFRAME_DIR" -maxdepth 1 -type f -name 'keyframe_*.png' -print | sort | head -n 1 || true)"
assert_file "$QUERY_FRAME" "FAIL_REPRO_SCRIPT"

echo "=== Gate 5: rerank candidates ==="
if ! python "$PROJECT_ROOT/scripts/external_memory/retrieve_memory.py" \
  --query_frame "$QUERY_FRAME" \
  --memory_bank "$MEMORY_DIR/memory_bank.jsonl" \
  --top_k 6 \
  --out_csv "$RUN_ROOT/retrieved_memory.csv" \
  --out_html "$RUN_ROOT/retrieved_memory.html" > "$RUN_ROOT/retrieve.log" 2>&1; then
  fail "FAIL_REPRO_SCRIPT"
fi

if ! python "$PROJECT_ROOT/scripts/external_memory/rerank_candidates.py" \
  --candidates_dir "$CANDIDATE_DIR" \
  --memory_bank "$MEMORY_DIR/memory_bank.jsonl" \
  --retrieved_csv "$RUN_ROOT/retrieved_memory.csv" \
  --out_csv "$RUN_ROOT/rerank_scores.csv" \
  --out_selected "$RUN_ROOT/selected_candidate.mp4" \
  --out_html "$RUN_ROOT/rerank_report.html" > "$RUN_ROOT/rerank.log" 2>&1; then
  fail "FAIL_RERANK"
fi

if ! python - "$RUN_ROOT/rerank_scores.csv" "$RUN_ROOT/selected_videos.json" <<'PY'
import csv
import json
from pathlib import Path
import sys

rerank_csv = Path(sys.argv[1])
out_json = Path(sys.argv[2])
rows = []
selected = []
with rerank_csv.open("r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rows.append(row)
        if row.get("selected") == "1":
            selected.append({
                "candidate_path": row.get("candidate_path"),
                "seed": row.get("seed"),
                "memory_score": row.get("memory_score"),
            })

top = {
    "selected": selected,
    "all": rows,
}
out_json.write_text(json.dumps(top, indent=2, ensure_ascii=True), encoding="utf-8")
print("written")
PY
then
  fail "FAIL_REPRO_SCRIPT"
fi

if ! python "$PROJECT_ROOT/scripts/external_memory/evaluate_contact_sheet.py" \
  --first_visit_frame "$QUERY_FRAME" \
  --selected_videos_json "$RUN_ROOT/selected_videos.json" \
  --out_png "$RUN_ROOT/contact_sheet.png" \
  --out_html "$RUN_ROOT/contact_sheet.html" > "$RUN_ROOT/contact_sheet.log" 2>&1; then
  fail "FAIL_REPRO_SCRIPT"
fi

if [[ "$MODE" == "smoke" ]]; then
  DIAG="PASS_CLEAN_CLONE_REPRO_SMOKE"
else
  DIAG="PASS_REPRO_FULL"
fi

if [[ "$USE_AUTO_ONLY" -eq 1 && "$MODE" == "smoke" ]]; then
  DIAG_NOTE="(smoke used auto-landmark fallback only)"
else
  DIAG_NOTE=""
fi

assert_file "$MEMORY_DIR/memory_bank.jsonl" "FAIL_REPRO_SCRIPT"
assert_file "$RUN_ROOT/rerank_scores.csv" "FAIL_REPRO_SCRIPT"
assert_file "$RUN_ROOT/selected_candidate.mp4" "FAIL_REPRO_SCRIPT"
if [[ ! -f "$RUN_ROOT/contact_sheet.png" && ! -f "$RUN_ROOT/contact_sheet.html" ]]; then
  fail "FAIL_REPRO_SCRIPT"
fi

echo "=== Gate 7: manifest/report ==="
write_summary
write_manifest
echo "$DIAG $DIAG_NOTE" | tee "$DIAG_FILE"
cat "$REPORT_FILE"
