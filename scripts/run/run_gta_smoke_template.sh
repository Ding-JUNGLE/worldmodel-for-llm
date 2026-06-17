#!/usr/bin/env bash
set -euo pipefail

# Usage:
# bash scripts/run/run_gta_smoke_template.sh /path/to/Matrix-Game-2 [run_id]

MG_ROOT="$1"
RUN_ID="${2:-smoke}"  # e.g. 20260617_XXX_gta_smoke

cd "$MG_ROOT"

echo "Run this command manually based on your Matrix-Game-2 entrypoint."
echo "Example placeholder with 48 frames and seed 0:"
cat <<'CMD'
# bash your_matrix_game2_entrypoint.sh --frames 48 --seed 0 --style gta --run_id "${RUN_ID}"
CMD

mkdir -p "outputs/runs/${RUN_ID}/gta_smoke"
printf 'Expected: outputs/runs/%s/gta_smoke/gta_smoke_seed0.mp4\n' "$RUN_ID"
