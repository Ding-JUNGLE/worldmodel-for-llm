# Environment Setup Notes

## Base Repository

The experiments are built on Matrix-Game-2.

Original project location on workstation:

```bash
/mnt/data1/dgw/external_repos/Matrix-Game/Matrix-Game-2
```

## Hardware Used

* Linux workstation
* NVIDIA GPU
* Existing Matrix-Game-2 environment
* GTA and TempleRun distilled checkpoints installed locally

## Important Dependency Note

One run required installing:

```bash
typing_extensions
```

to use `torchvision_resnet18` as the feature encoder.

## Checkpoints

Checkpoints are not included in this Git repo.

Required Matrix-Game-2 checkpoint files must be downloaded separately:

```text
Wan2.1_VAE.pth
models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth
base_distilled_model/base_distill.safetensors
gta_distilled_model/gta_keyboard2dim.safetensors
templerun_distilled_model/templerun_7dim_onlykey.safetensors
```

Do not commit checkpoint files to Git.
