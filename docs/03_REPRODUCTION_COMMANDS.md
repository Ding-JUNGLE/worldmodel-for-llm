# Reproduction Commands

## 1. Environment check

```bash
python scripts/setup/check_environment.py
```

## 2. Checkpoints check

```bash
python scripts/setup/check_checkpoints.py --matrix_game2_root /path/to/Matrix-Game/Matrix-Game-2
```

## 3. GTA road-sign memory smoke

```bash
bash scripts/run/reproduce_gta_roadsign_memory.sh \
  --matrix-game2-root /path/to/Matrix-Game/Matrix-Game-2 \
  --output-root /path/to/repro_outputs \
  --mode smoke
```

Expected outputs:

```text
diagnosis.txt
report.md
memory_bank.jsonl or equivalent memory output
rerank_scores.csv
selected candidate path or selected candidate file
contact sheet or html summary
```

## 4. Full experiment

```bash
bash scripts/run/reproduce_gta_roadsign_memory.sh \
  --matrix-game2-root /path/to/Matrix-Game/Matrix-Game-2 \
  --output-root /path/to/repro_outputs \
  --mode full
```

Run full mode only after smoke passes.

## Diagnosis labels

```text
PASS_REPRO_SMOKE
PASS_REPRO_FULL
FAIL_ENVIRONMENT
FAIL_MATRIX_GAME_ENV_MISSING_DEPS
FAIL_CHECKPOINTS
FAIL_GTA_GENERATION
FAIL_MEMORY_BANK
FAIL_RERANK
FAIL_CONTACT_SHEET
```

## Important

Use 48 frames, not 49.
