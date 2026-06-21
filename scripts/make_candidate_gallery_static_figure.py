#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

RESAMPLE_LANCZOS = getattr(Image, "Resampling", Image).LANCZOS


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLIP_DIR = Path(
    "/mnt/data1/dgw/external_repos/Matrix-Game/Matrix-Game-2/outputs/runs/"
    "20260617_007_gta_landmark_memory_v1/candidates"
)

POSTER_PATH = REPO_ROOT / "figures/demo_v3/candidate_gallery_memory_selection_poster.png"
SLIDE_PATH = REPO_ROOT / "figures/demo_v3/candidate_gallery_memory_selection_slide_16x9.png"
THUMBNAIL_PATH = REPO_ROOT / "figures/demo_v3/candidate_gallery_memory_selection_thumbnail.png"
PDF_PATH = REPO_ROOT / "figures/demo_v3/candidate_gallery_memory_selection_poster.pdf"

TITLE_LINES = [
    "Candidate Pool and",
    "Memory-Guided Selection",
]
SUBTITLE = (
    "Frozen Matrix-Game-2 generates multiple candidate continuations; "
    "external memory reranks them."
)
FOOTER = (
    "External memory reranks candidate continuations. This figure visualizes "
    "candidate-level comparison and selection; it is not itself a new world-model rollout."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create PPT-ready candidate gallery figure.")
    parser.add_argument("--clip-dir", type=Path, default=DEFAULT_CLIP_DIR)
    parser.add_argument("--frame-time", type=float, default=8.0)
    parser.add_argument("--poster-width", type=int, default=2400)
    parser.add_argument("--poster-height", type=int, default=1350)
    parser.add_argument("--thumbnail-width", type=int, default=1280)
    parser.add_argument("--thumbnail-height", type=int, default=720)
    parser.add_argument("--skip-pdf", action="store_true")
    return parser.parse_args()


def ffmpeg_extract_frame(clip: Path, output: Path, frame_time: float) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{frame_time:.2f}",
        "-i",
        str(clip),
        "-frames:v",
        "1",
        "-vf",
        "scale=1280:-2",
        str(output),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    font_name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{font_name}", size=size)


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, top)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / max(height - 1, 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line((0, y, width, y), fill=color)
    return image


def add_soft_glow(base: Image.Image, box: tuple[int, int, int, int], color: tuple[int, int, int], blur: int = 24) -> None:
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.rounded_rectangle(box, radius=32, fill=(*color, 72))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=blur))
    base.alpha_composite(glow)


def fit_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = image.size
    scale = max(target_w / src_w, target_h / src_h)
    resized = image.resize((int(src_w * scale), int(src_h * scale)), RESAMPLE_LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.FreeTypeFont, fill: tuple[int, int, int]) -> None:
    draw.text(xy, text, font=font, fill=fill)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = []
    for word in words:
        trial = " ".join(current + [word])
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def pill(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: tuple[int, int, int], text: str, font: ImageFont.FreeTypeFont, text_fill: tuple[int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_x = box[0] + (box[2] - box[0] - (bbox[2] - bbox[0])) // 2
    text_y = box[1] + (box[3] - box[1] - (bbox[3] - bbox[1])) // 2 - 1
    draw.text((text_x, text_y), text, font=font, fill=text_fill)


def compose_figure(frame_paths: list[Path], poster_path: Path, slide_path: Path, thumbnail_path: Path, pdf_path: Path | None, poster_size: tuple[int, int], thumbnail_size: tuple[int, int]) -> None:
    width, height = poster_size
    bg = vertical_gradient((width, height), (248, 245, 238), (236, 232, 225)).convert("RGBA")

    accent_blue = (47, 109, 200)
    accent_orange = (203, 118, 46)
    text_main = (28, 30, 35)
    text_muted = (94, 98, 108)
    card_fill = (255, 252, 248, 255)
    card_border = (217, 213, 206)
    footer_fill = (245, 240, 233)

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Soft background shapes to avoid a flat slide.
    draw.ellipse((width - 520, -80, width + 180, 500), fill=(232, 188, 124, 82))
    draw.ellipse((-240, height - 380, 340, height + 120), fill=(124, 162, 213, 54))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=40))
    bg.alpha_composite(overlay)

    draw = ImageDraw.Draw(bg)
    title_font = load_font(62, bold=True)
    subtitle_font = load_font(28)
    header_font = load_font(22, bold=True)
    card_title_font = load_font(24, bold=True)
    card_meta_font = load_font(20)
    pill_font = load_font(18, bold=True)
    footer_font = load_font(22)

    margin_x = 110
    title_y = 72
    draw_text(draw, (margin_x, title_y), TITLE_LINES[0], title_font, text_main)
    draw_text(draw, (margin_x, title_y + 74), TITLE_LINES[1], title_font, text_main)
    draw_text(draw, (margin_x, title_y + 154), SUBTITLE, subtitle_font, text_muted)

    summary_h = 92
    summary_box = (margin_x, 266, width - margin_x, 266 + summary_h)
    add_soft_glow(bg, summary_box, accent_blue, blur=28)
    draw.rounded_rectangle(summary_box, radius=34, fill=(255, 252, 248, 224), outline=(221, 217, 210), width=2)
    draw_text(draw, (summary_box[0] + 28, summary_box[1] + 18), "Selection Story", header_font, text_main)
    pill(draw, (summary_box[0] + 300, summary_box[1] + 16, summary_box[0] + 508, summary_box[1] + 50), (231, 239, 255), "No-memory -> Seed 1", pill_font, accent_blue)
    pill(draw, (summary_box[0] + 522, summary_box[1] + 16, summary_box[0] + 820, summary_box[1] + 50), (255, 238, 221), "Road-sign memory -> Seed 8", pill_font, accent_orange)
    draw_text(draw, (summary_box[0] + 28, summary_box[1] + 54), "Candidate pool shown once; selection changes with memory.", card_meta_font, text_muted)

    grid_top = 390
    grid_left = margin_x
    grid_right = width - margin_x
    grid_bottom = height - 176
    cols = 4
    rows = 2
    gutter_x = 34
    gutter_y = 34
    card_w = int((grid_right - grid_left - gutter_x * (cols - 1)) / cols)
    card_h = int((grid_bottom - grid_top - gutter_y * (rows - 1)) / rows)
    image_h = 270

    for idx, frame_path in enumerate(frame_paths):
        row = idx // cols
        col = idx % cols
        x = grid_left + col * (card_w + gutter_x)
        y = grid_top + row * (card_h + gutter_y)
        card_box = (x, y, x + card_w, y + card_h)

        accent = None
        pill_text = "Candidate"
        pill_fill = (240, 238, 233)
        pill_text_fill = text_muted
        border_color = card_border
        border_width = 2
        shadow_color = (160, 160, 160)

        if idx == 0:
            accent = accent_blue
            pill_text = "Selected by no-memory"
            pill_fill = (231, 239, 255)
            pill_text_fill = accent_blue
            border_color = accent_blue
            border_width = 4
            shadow_color = accent_blue
        elif idx == 7:
            accent = accent_orange
            pill_text = "Selected by road-sign memory"
            pill_fill = (255, 238, 221)
            pill_text_fill = accent_orange
            border_color = accent_orange
            border_width = 4
            shadow_color = accent_orange

        add_soft_glow(bg, card_box, shadow_color, blur=24 if accent else 18)
        draw.rounded_rectangle(card_box, radius=28, fill=card_fill, outline=border_color, width=border_width)

        seed_image = fit_cover(Image.open(frame_path).convert("RGB"), (card_w - 28, image_h))
        mask = rounded_mask((card_w - 28, image_h), 22)
        image_x = x + 14
        image_y = y + 14
        bg.paste(seed_image, (image_x, image_y), mask)

        seed_pill_w = 108
        pill(draw, (x + 26, y + 28, x + 26 + seed_pill_w, y + 64), (255, 252, 248), f"Seed {idx + 1}", pill_font, text_main)

        if idx == 0:
            pill(draw, (x + card_w - 254, y + 28, x + card_w - 26, y + 64), pill_fill, "No-memory selection", pill_font, pill_text_fill)
        elif idx == 7:
            pill(draw, (x + card_w - 308, y + 28, x + card_w - 26, y + 64), pill_fill, "Memory-guided selection", pill_font, pill_text_fill)

        footer_y = y + image_h + 34
        draw_text(draw, (x + 20, footer_y), f"Candidate {idx + 1}", card_title_font, text_main)
        meta_text = "Candidate continuation"
        if idx == 0:
            meta_text = "Chosen without external memory"
        elif idx == 7:
            meta_text = "Chosen after approved road-sign memory"

        draw_text(draw, (x + 20, footer_y + 38), meta_text, card_meta_font, text_muted)

    footer_box = (margin_x, height - 122, width - margin_x, height - 54)
    draw.rounded_rectangle(footer_box, radius=28, fill=footer_fill, outline=(220, 214, 207), width=2)
    footer_lines = wrap_text(draw, FOOTER, footer_font, footer_box[2] - footer_box[0] - 60)
    footer_y = footer_box[1] + 18
    for line in footer_lines[:2]:
        draw_text(draw, (footer_box[0] + 28, footer_y), line, footer_font, text_muted)
        footer_y += 28

    poster_path.parent.mkdir(parents=True, exist_ok=True)
    slide_path.parent.mkdir(parents=True, exist_ok=True)
    thumbnail_path.parent.mkdir(parents=True, exist_ok=True)

    rgb_image = bg.convert("RGB")
    rgb_image.save(poster_path, quality=96)
    rgb_image.save(slide_path, quality=96)
    rgb_image.resize(thumbnail_size, RESAMPLE_LANCZOS).save(thumbnail_path, quality=94)

    if pdf_path is not None:
        rgb_image.save(pdf_path, resolution=200.0)


def main() -> None:
    args = parse_args()
    clip_paths = [args.clip_dir / f"candidate_seed{i}.mp4" for i in range(1, 9)]
    missing = [str(path) for path in clip_paths if not path.exists()]
    if missing:
        raise SystemExit(f"Missing candidate clips: {missing}")

    with tempfile.TemporaryDirectory(prefix="candidate_gallery_static_") as tmp_dir:
        temp_root = Path(tmp_dir)
        frame_paths = []
        for idx, clip_path in enumerate(clip_paths, start=1):
            frame_path = temp_root / f"seed{idx}.png"
            ffmpeg_extract_frame(clip_path, frame_path, args.frame_time)
            frame_paths.append(frame_path)

        pdf_path = None if args.skip_pdf else PDF_PATH
        compose_figure(
            frame_paths=frame_paths,
            poster_path=POSTER_PATH,
            slide_path=SLIDE_PATH,
            thumbnail_path=THUMBNAIL_PATH,
            pdf_path=pdf_path,
            poster_size=(args.poster_width, args.poster_height),
            thumbnail_size=(args.thumbnail_width, args.thumbnail_height),
        )


if __name__ == "__main__":
    main()
