# Troubleshooting

## Checkpoint missing

```bash
python scripts/setup/check_checkpoints.py --matrix_game2_root /path/to/Matrix-Game-2
```

## 49 frames error

Use 48 frames. Our baseline wrapper was fixed from 49 to 48.

## typing_extensions missing

```bash
pip install typing_extensions
```

## CUDA OOM

Use fewer candidates, shorter frame count, or one style checkpoint at a time.

## GTA / TempleRun not working

Run smoke tests first. Do not run memory experiments until smoke passes.

## GitHub upload

Do not commit checkpoints or videos.
