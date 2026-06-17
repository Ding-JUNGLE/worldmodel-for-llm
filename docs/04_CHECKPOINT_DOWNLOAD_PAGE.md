# Checkpoint Download Page

## Hugging Face repo

```text
https://huggingface.co/Skywork/Matrix-Game-2.0/tree/main
```

## Common files

Place under Matrix-Game-2 root:

```text
Wan2.1_VAE.pth
models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth
xlm-roberta-large/
```

## GTA files

```text
gta_distilled_model/config.json
gta_distilled_model/gta_keyboard2dim.safetensors
```

## TempleRun files

```text
templerun_distilled_model/config.json
templerun_distilled_model/templerun_7dim_onlykey.safetensors
```

## Base files

```text
base_distilled_model/config.json
base_distilled_model/base_distill.safetensors
```

## Recommended for this project

For the main memory experiment, download GTA first.

## Verify

```bash
python scripts/setup/check_checkpoints.py --matrix_game2_root /path/to/Matrix-Game-2
```
