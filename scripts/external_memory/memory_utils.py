#!/usr/bin/env python3
from __future__ import annotations

import base64
import csv
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import cv2
import numpy as np
from PIL import Image


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent(path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def path_for_report(path: str | Path) -> str:
    path = Path(path)
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def read_jsonl(path: str | Path) -> list[dict]:
    items: list[dict] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def write_jsonl(path: str | Path, items: Iterable[dict]) -> None:
    ensure_parent(path)
    with Path(path).open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=True) + "\n")


def write_csv(path: str | Path, fieldnames: Sequence[str], rows: Sequence[dict]) -> None:
    ensure_parent(path)
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_json(path: str | Path, data: dict) -> None:
    ensure_parent(path)
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=True)


def normalize_features(array: np.ndarray) -> np.ndarray:
    array = np.asarray(array, dtype=np.float32)
    if array.ndim == 1:
        array = array[None, :]
    norms = np.linalg.norm(array, axis=1, keepdims=True)
    norms = np.where(norms == 0.0, 1.0, norms)
    return array / norms


def cosine_similarity(query: np.ndarray, bank: np.ndarray) -> np.ndarray:
    q = normalize_features(query)[0]
    b = normalize_features(bank)
    return b @ q


def read_video_info(video_path: str | Path) -> dict:
    video_path = str(video_path)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    cap.release()
    duration = frame_count / fps if fps > 0 else 0.0
    return {
        "video_path": video_path,
        "frame_count": frame_count,
        "fps": fps,
        "width": width,
        "height": height,
        "duration": duration,
    }


def _clamp_frame_index(frame_count: int, index: int) -> int:
    if frame_count <= 0:
        raise RuntimeError("Video reports zero frames.")
    return max(0, min(frame_count - 1, int(index)))


def read_frame_at(video_path: str | Path, index: int) -> np.ndarray:
    info = read_video_info(video_path)
    index = _clamp_frame_index(info["frame_count"], index)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
    ok, frame = cap.read()
    cap.release()
    if not ok or frame is None:
        raise RuntimeError(f"Could not read frame {index} from {video_path}")
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def save_frame(frame_rgb: np.ndarray, out_path: str | Path) -> None:
    ensure_parent(out_path)
    Image.fromarray(frame_rgb).save(out_path)


def uniform_indices(frame_count: int, num_samples: int) -> list[int]:
    if frame_count <= 0:
        raise RuntimeError("Video reports zero frames.")
    if num_samples <= 0:
        raise ValueError("num_samples must be positive")
    if num_samples == 1:
        return [0]
    max_samples = min(frame_count, num_samples)
    values = np.linspace(0, frame_count - 1, num=max_samples)
    indices = [int(round(v)) for v in values]
    deduped: list[int] = []
    seen: set[int] = set()
    for idx in indices:
        idx = _clamp_frame_index(frame_count, idx)
        if idx not in seen:
            seen.add(idx)
            deduped.append(idx)
    return deduped


def triplet_indices(frame_count: int) -> list[int]:
    if frame_count <= 0:
        raise RuntimeError("Video reports zero frames.")
    return sorted(
        {
            0,
            _clamp_frame_index(frame_count, frame_count // 2),
            frame_count - 1,
        }
    )


def sample_frames(video_path: str | Path, indices: Sequence[int]) -> list[np.ndarray]:
    return [read_frame_at(video_path, idx) for idx in indices]


def image_to_base64(path: str | Path, max_size: tuple[int, int] | None = (320, 320)) -> str:
    image = Image.open(path).convert("RGB")
    if max_size is not None:
        image.thumbnail(max_size)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def frame_to_base64(frame_rgb: np.ndarray, max_size: tuple[int, int] | None = (320, 320)) -> str:
    image = Image.fromarray(frame_rgb)
    if max_size is not None:
        image.thumbnail(max_size)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def make_html_page(title: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    h1, h2 {{ margin-bottom: 0.4rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }}
    .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 12px; background: #fafafa; }}
    img {{ width: 100%; height: auto; border-radius: 6px; border: 1px solid #ccc; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 16px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f0f0f0; }}
    .selected {{ border-color: #1a7f37; box-shadow: 0 0 0 2px rgba(26,127,55,0.15); }}
    code {{ background: #f3f3f3; padding: 0 4px; border-radius: 4px; }}
  </style>
</head>
<body>
{body_html}
</body>
</html>
"""


@dataclass
class EncoderSpec:
    name: str
    feature_dim: int
    device: str


class BaseEncoder:
    spec: EncoderSpec

    def encode_images(self, images: Sequence[Image.Image]) -> np.ndarray:
        raise NotImplementedError


class RGBFallbackEncoder(BaseEncoder):
    def __init__(self, image_size: int = 32):
        self.image_size = image_size
        self.spec = EncoderSpec(
            name=f"rgb_fallback_{image_size}x{image_size}",
            feature_dim=image_size * image_size * 3,
            device="cpu",
        )

    def encode_images(self, images: Sequence[Image.Image]) -> np.ndarray:
        feats: list[np.ndarray] = []
        for image in images:
            arr = np.asarray(image.convert("RGB").resize((self.image_size, self.image_size)), dtype=np.float32)
            feats.append((arr / 255.0).reshape(-1))
        return normalize_features(np.stack(feats, axis=0))


class TorchvisionResNet18Encoder(BaseEncoder):
    def __init__(self):
        import torch
        from torchvision.models import ResNet18_Weights, resnet18

        weights = ResNet18_Weights.DEFAULT
        model = resnet18(weights=weights)
        model.fc = torch.nn.Identity()
        model.eval()
        self._torch = torch
        self._model = model.cpu()
        self._transform = weights.transforms()
        self.spec = EncoderSpec(name="torchvision_resnet18", feature_dim=512, device="cpu")

    def encode_images(self, images: Sequence[Image.Image]) -> np.ndarray:
        batch = self._torch.stack([self._transform(image.convert("RGB")) for image in images], dim=0)
        with self._torch.inference_mode():
            feats = self._model(batch).detach().cpu().numpy().astype(np.float32)
        return normalize_features(feats)


class TransformerDinoV2Encoder(BaseEncoder):
    def __init__(self):
        import torch
        from transformers import AutoImageProcessor, AutoModel

        model_id = "facebook/dinov2-base"
        self._processor = AutoImageProcessor.from_pretrained(model_id, local_files_only=True)
        self._model = AutoModel.from_pretrained(model_id, local_files_only=True).cpu().eval()
        self._torch = torch
        hidden = getattr(self._model.config, "hidden_size", 768)
        self.spec = EncoderSpec(name="dinov2_base_local", feature_dim=int(hidden), device="cpu")

    def encode_images(self, images: Sequence[Image.Image]) -> np.ndarray:
        inputs = self._processor(images=[image.convert("RGB") for image in images], return_tensors="pt")
        with self._torch.inference_mode():
            outputs = self._model(**inputs)
        if hasattr(outputs, "pooler_output") and outputs.pooler_output is not None:
            feats = outputs.pooler_output.detach().cpu().numpy().astype(np.float32)
        else:
            feats = outputs.last_hidden_state[:, 0].detach().cpu().numpy().astype(np.float32)
        return normalize_features(feats)


class TransformerClipEncoder(BaseEncoder):
    def __init__(self):
        import torch
        from transformers import CLIPModel, CLIPProcessor

        model_id = "openai/clip-vit-base-patch32"
        self._processor = CLIPProcessor.from_pretrained(model_id, local_files_only=True)
        self._model = CLIPModel.from_pretrained(model_id, local_files_only=True).cpu().eval()
        self._torch = torch
        dim = getattr(self._model.config, "projection_dim", 512)
        self.spec = EncoderSpec(name="clip_vit_b32_local", feature_dim=int(dim), device="cpu")

    def encode_images(self, images: Sequence[Image.Image]) -> np.ndarray:
        inputs = self._processor(images=[image.convert("RGB") for image in images], return_tensors="pt")
        pixel_values = inputs["pixel_values"]
        with self._torch.inference_mode():
            feats = self._model.get_image_features(pixel_values=pixel_values).detach().cpu().numpy().astype(np.float32)
        return normalize_features(feats)


def create_encoder(name: str) -> BaseEncoder:
    requested = name.lower()
    errors: list[str] = []

    def try_build(label: str, fn):
        try:
            return fn()
        except Exception as exc:  # pragma: no cover - best effort fallback logging
            errors.append(f"{label}: {type(exc).__name__}: {exc}")
            return None

    if requested in {"auto", "dinov2", "dinov2_local"}:
        encoder = try_build("dinov2_local", TransformerDinoV2Encoder)
        if encoder is not None:
            return encoder
        if requested not in {"auto"}:
            raise RuntimeError("; ".join(errors))

    if requested in {"auto", "clip", "clip_local"}:
        encoder = try_build("clip_local", TransformerClipEncoder)
        if encoder is not None:
            return encoder
        if requested not in {"auto"}:
            raise RuntimeError("; ".join(errors))

    if requested in {"auto", "torchvision", "torchvision_resnet18", "resnet18"}:
        encoder = try_build("torchvision_resnet18", TorchvisionResNet18Encoder)
        if encoder is not None:
            return encoder
        if requested not in {"auto"}:
            raise RuntimeError("; ".join(errors))

    if requested in {"auto", "rgb", "rgb_fallback"}:
        return RGBFallbackEncoder()

    raise ValueError(f"Unknown encoder request: {name}. Errors: {'; '.join(errors)}")
