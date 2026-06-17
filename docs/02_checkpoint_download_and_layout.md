# Checkpoint Download and Layout

## Hugging Face Source

All required files are in:

```text
Skywork/Matrix-Game-2.0
```

## Required files

Common:

```text
Matrix-Game-2/
  Wan2.1_VAE.pth
  models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth
  xlm-roberta-large/
    sentencepiece.bpe.model
    special_tokens_map.json
    tokenizer.json
    tokenizer_config.json
```

Base:

```text
base_distilled_model/
  config.json
  base_distill.safetensors
```

GTA:

```text
 gta_distilled_model/
   config.json
   gta_keyboard2dim.safetensors
```

TempleRun:

```text
templerun_distilled_model/
  config.json
  templerun_7dim_onlykey.safetensors
```

## Direct download URLs

Common:

```text
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/Wan2.1_VAE.pth
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/xlm-roberta-large/sentencepiece.bpe.model
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/xlm-roberta-large/special_tokens_map.json
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/xlm-roberta-large/tokenizer.json
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/xlm-roberta-large/tokenizer_config.json
```

Base:

```text
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/base_distilled_model/config.json
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/base_distilled_model/base_distill.safetensors
```

GTA:

```text
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/gta_distilled_model/config.json
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/gta_distilled_model/gta_keyboard2dim.safetensors
```

TempleRun:

```text
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/templerun_distilled_model/config.json
https://huggingface.co/Skywork/Matrix-Game-2.0/resolve/main/templerun_distilled_model/templerun_7dim_onlykey.safetensors
```

## Stable download advice

For large files, browser download + `rsync -avP` is often more stable than repeated CLI attempts.

## Verify layout

```bash
python scripts/setup/check_checkpoints.py --matrix_game2_root /path/to/Matrix-Game-2
```
