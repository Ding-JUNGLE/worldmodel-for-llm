# Known Limitations for Reproduction

## Not fully self-contained

This repo does not include:
- Matrix-Game-2 original source
- pretrained checkpoints
- generated videos
- full outputs

## External memory only

The memory module is external and inference-time only.

It does not modify Matrix-Game-2 internals.

## Environment dependency

The reproduction script must be run inside a Matrix-Game-2 environment.

If you see:

```text
No module named diffusers
```

then your Matrix-Game-2 environment is incomplete.

Fix:

```bash
cd /path/to/Matrix-Game/Matrix-Game-2
conda activate matrix-game-2.0
pip install -r requirements.txt
python setup.py develop
```

Then check:

```bash
python -c "import diffusers, transformers, accelerate, safetensors, omegaconf, torch, torchvision, numpy, PIL"
```

## Script status

Some scripts are wrappers or helpers. The main teammate entrypoint is:

```text
scripts/run/reproduce_gta_roadsign_memory.sh
```

Always start with `--mode smoke`.
