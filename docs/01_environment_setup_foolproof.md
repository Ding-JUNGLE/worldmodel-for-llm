# Foolproof Environment Setup

## 0. What you need

- Linux workstation
- NVIDIA GPU, recommended 24GB+ VRAM
- 64GB RAM recommended
- Conda or Mamba
- Git
- Hugging Face access
- Enough disk space for Matrix-Game-2 checkpoints

## 1. Clone original Matrix-Game repo

```bash
mkdir -p ~/external_repos
cd ~/external_repos
git clone https://github.com/SkyworkAI/Matrix-Game.git
cd Matrix-Game/Matrix-Game-2
```

## 2. Create conda environment

```bash
conda create -n matrix-game-2.0 python=3.10 -y
conda activate matrix-game-2.0
pip install -r requirements.txt
python setup.py develop
```

## 3. Extra dependency used by our memory scripts

```bash
pip install typing_extensions
```

Why:

```text
typing_extensions was needed so our torchvision_resnet18 feature encoder could import cleanly.
```

## 4. Clone our project repo

```bash
cd ~/external_repos
git clone https://github.com/Ding-JUNGLE/worldmodel-for-llm.git
cd worldmodel-for-llm
```

## 5. Recommended directory layout

```text
~/external_repos/
  Matrix-Game/
    Matrix-Game-2/
  worldmodel-for-llm/
```

## 6. Configure local paths

```bash
cd ~/external_repos/worldmodel-for-llm
cp configs/paths.example.yaml configs/paths.local.yaml
```

Edit:

```yaml
matrix_game2_root: /path/to/Matrix-Game/Matrix-Game-2
memory_project_root: /path/to/worldmodel-for-llm
```

## 7. Check environment

```bash
python scripts/setup/check_environment.py
```

Example original workstation path:

```text
/mnt/data1/dgw/external_repos/Matrix-Game/Matrix-Game-2
```
