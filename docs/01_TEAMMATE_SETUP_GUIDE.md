# Teammate Setup Guide

## 1. Clone Matrix-Game

```bash
git clone https://github.com/SkyworkAI/Matrix-Game.git
cd Matrix-Game/Matrix-Game-2
```

## 2. Create environment

```bash
conda create -n matrix-game-2.0 python=3.10 -y
conda activate matrix-game-2.0
pip install -r requirements.txt
python setup.py develop
```

## 3. Install small extra dependency for our memory scripts

```bash
pip install typing_extensions omegaconf
```

If clean-clone smoke reports missing Matrix-Game deps, install Matrix-Game requirements again:

```bash
cd /path/to/Matrix-Game/Matrix-Game-2
pip install -r requirements.txt
python setup.py develop
```

## 4. Clone our repo

```bash
cd ~/external_repos
git clone https://github.com/Ding-JUNGLE/worldmodel-for-llm.git
cd worldmodel-for-llm
```

Use the teammate reproduction branch:

```bash
git checkout repro-tutorial-memory-guide-20260617
```

## 5. Configure local paths

```bash
cp configs/paths.example.yaml configs/paths.local.yaml
```

Edit:

```yaml
matrix_game2_root: "/path/to/Matrix-Game/Matrix-Game-2"
memory_project_root: "/path/to/worldmodel-for-llm"
outputs_root: "/path/to/Matrix-Game-2/outputs/runs"
```

## 6. Check environment

```bash
python scripts/setup/check_environment.py
```

## 7. Check checkpoints

```bash
python scripts/setup/check_checkpoints.py --matrix_game2_root /path/to/Matrix-Game/Matrix-Game-2
```

## 8. Run smoke first

```bash
bash scripts/run/reproduce_gta_roadsign_memory.sh \
  --matrix-game2-root /path/to/Matrix-Game/Matrix-Game-2 \
  --output-root /path/to/repro_outputs \
  --mode smoke
```

Only run full mode after smoke passes.
