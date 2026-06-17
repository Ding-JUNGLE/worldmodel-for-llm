#!/usr/bin/env bash
set -euo pipefail

# Usage:
# bash scripts/run/run_templerun_smoke_template.sh /path/to/Matrix-Game-2 [run_id]

MG_ROOT="$1"
RUN_ID="${2:-smoke}"

cd "$MG_ROOT"

echo "Run this command manually based on your Matrix-Game-2 entrypoint."
echo "Example placeholder with 48 frames and seed 0:"
cat <<'CMD'
# bash your_matrix_game2_entrypoint.sh --frames 48 --seed 0 --style templerun --run_id "${RUN_ID}"
CMD

mkdir -p "outputs/runs/${RUN_ID}/templerun_smoke"
printf 'Expected: outputs/runs/%s/templerun_smoke/templerun_smoke_seed0.mp4\n' "$RUN_ID"
