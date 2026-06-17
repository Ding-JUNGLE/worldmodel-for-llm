#!/usr/bin/env bash
set -euo pipefail

# Usage:
# bash scripts/run/run_gta_landmark_memory_v1_template.sh /path/to/memory_project_root /path/to/Matrix-Game-2 [run_id]

PROJECT_ROOT="$1"
MG_ROOT="${2:-}"
RUN_ID="${3:-20260617_007_gta_landmark_memory_v1}"

cd "$PROJECT_ROOT"

echo "Step-by-step guidance for GTA landmark memory experiment."
echo "Edit command arguments to match your local setup."

echo "1) Build first-visit memory bank (use available keyframe script):"
echo "python scripts/external_memory/build_landmark_memory.py --run_id $RUN_ID"

echo "2) Generate candidates and rerank (edit checkpoint/output paths in the script as needed):"
echo "python scripts/external_memory/rerank_candidates.py --strategy landmark_memory --seed_list 1 2 3 4 5 6 7 8"

echo "3) Save results into:"
echo "${MG_ROOT%/}/outputs/runs/$RUN_ID"

if [ -n "$MG_ROOT" ]; then
  mkdir -p "$MG_ROOT/outputs/runs/$RUN_ID"
fi
