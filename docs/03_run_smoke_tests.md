# Smoke Tests

Smoke tests verify that Matrix-Game-2 and checkpoints work.

## Important

Use 48 frames, not 49.

## GTA smoke

```bash
bash scripts/run/run_gta_smoke_template.sh /path/to/Matrix-Game-2
```

Expected:

```text
outputs/runs/<run_id>/gta_smoke/gta_smoke_seed0.mp4
```

## TempleRun smoke

```bash
bash scripts/run/run_templerun_smoke_template.sh /path/to/Matrix-Game-2
```

Expected:

```text
outputs/runs/<run_id>/templerun_smoke/templerun_smoke_seed0.mp4
```

## PASS meaning

A PASS smoke means the style checkpoint can run generation. It does not mean memory experiments have passed.
