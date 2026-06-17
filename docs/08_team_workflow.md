# Team Workflow

## Branching

```bash
git checkout -b teammate/<task-name>-YYYYMMDD
```

## Before work

```bash
git status
```

## After work

```bash
git status
git diff --stat
git diff
```

## Do not

- do not commit checkpoints
- do not commit videos
- do not use git reset
- do not use git clean
- do not delete outputs/runs on the workstation
- do not modify Matrix-Game-2 internals unless discussed

## Where to put new experiments

On workstation:

```text
Matrix-Game-2/outputs/runs/YYYYMMDD_NNN_short_name/
```

In GitHub:

```text
docs/
scripts/
results/
figures/
```
