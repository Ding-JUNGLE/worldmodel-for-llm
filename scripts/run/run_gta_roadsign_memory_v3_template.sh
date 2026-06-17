#!/usr/bin/env bash
set -euo pipefail

# Usage:
# bash scripts/run/run_gta_roadsign_memory_v3_template.sh /path/to/memory_project_root /path/to/Matrix-Game-2 [run_id]

PROJECT_ROOT="$1"
MG_ROOT="${2:-}"
RUN_ID="${3:-20260617_009_gta_roadsign_approved_memory_v3}"

cd "$PROJECT_ROOT"

echo "Step-by-step guidance for GTA approved road-sign memory experiment."
echo "Edit command arguments to match your local setup."

echo "1) Build approved roadsign memory bank:"
echo "python scripts/external_memory/build_memory_bank.py --project_root "$PROJECT_ROOT" --annotation results/roadsign_annotation_APPROVED.json"

echo "2) Generate candidates and rerank:"
echo "python scripts/external_memory/rerank_candidates.py --strategy approved_roadsign_memory --seed_list 1 2 3 4 5 6 7 8"

echo "3) Store outputs in:"
echo "${MG_ROOT%/}/outputs/runs/$RUN_ID"

if [ -n "$MG_ROOT" ]; then
  mkdir -p "$MG_ROOT/outputs/runs/$RUN_ID"
fi
