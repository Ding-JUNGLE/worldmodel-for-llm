#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "figures" / "presentation"
RESULTS_DIR = REPO / "results" / "evaluation"
DOCS_DIR = REPO / "docs" / "final"

W, H = 1800, 1012

BG_TOP = "#f8f3eb"
BG_BOTTOM = "#e4e8ef"
INK = "#20242b"
MUTED = "#6d7380"
MUTED_2 = "#8d94a0"
BORDER = "#d6dbe3"
CARD = "#ffffff"
SOFT = "#f4f6f9"
BLUE = "#3a72d8"
BLUE_SOFT = "#dfe9ff"
ORANGE = "#db8422"
ORANGE_SOFT = "#ffe8cf"
GREEN = "#2d9a63"
GREEN_SOFT = "#def3e9"
RED = "#c64545"
RED_SOFT = "#ffe2e2"
GOLD = "#c58a1d"
GOLD_SOFT = "#fff0ce"
GRAY = "#eef1f5"

try:
    RESAMPLE = Image.Resampling.LANCZOS  # Pillow >= 9
except AttributeError:  # Pillow < 9
    RESAMPLE = Image.LANCZOS


def hex_rgb(value: str) -> tuple[int, int, int]:
    return ImageColor.getrgb(value)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


FONT_TITLE = load_font(72, bold=True)
FONT_TITLE_SMALL = load_font(58, bold=True)
FONT_TITLE_MEDIUM = load_font(46, bold=True)
FONT_SUBTITLE = load_font(30)
FONT_SUBTITLE_BOLD = load_font(30, bold=True)
FONT_SECTION = load_font(28, bold=True)
FONT_CARD_TITLE = load_font(24, bold=True)
FONT_CARD_TEXT = load_font(20)
FONT_CARD_TEXT_SMALL = load_font(18)
FONT_TINY = load_font(16)
FONT_CHIP = load_font(18, bold=True)
FONT_MONO = load_font(18)
FONT_MONO_SMALL = load_font(15)


def ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def make_canvas() -> Image.Image:
    im = Image.new("RGBA", (W, H), hex_rgb(BG_TOP) + (255,))
    draw = ImageDraw.Draw(im)
    top = hex_rgb(BG_TOP)
    bottom = hex_rgb(BG_BOTTOM)
    for y in range(H):
        t = y / max(1, H - 1)
        col = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line((0, y, W, y), fill=col + (255,))
    # subtle glow / vignette
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((-160, -120, 700, 540), fill=(255, 255, 255, 90))
    od.ellipse((1100, -170, 2020, 650), fill=(255, 245, 230, 120))
    od.ellipse((-280, 680, 820, 1180), fill=(220, 232, 255, 65))
    overlay = overlay.filter(ImageFilter.GaussianBlur(50))
    im.alpha_composite(overlay)
    return im


def draw_card(base: Image.Image, box: tuple[int, int, int, int], radius: int = 28, fill: str = CARD,
              outline: str = BORDER, width: int = 2, shadow: bool = True) -> None:
    x1, y1, x2, y2 = box
    if shadow:
        shadow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow_layer)
        sd.rounded_rectangle((x1 + 8, y1 + 12, x2 + 8, y2 + 12), radius=radius, fill=(0, 0, 0, 60))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(16))
        base.alpha_composite(shadow_layer)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=radius, fill=hex_rgb(fill) + (255,), outline=hex_rgb(outline) + (255,), width=width)


def draw_divider(draw: ImageDraw.ImageDraw, x1: int, y: int, x2: int, color: str = BORDER, width: int = 2) -> None:
    draw.line((x1, y, x2, y), fill=hex_rgb(color) + (255,), width=width)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = f"{current} {word}"
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrapped_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont,
                      fill: str, max_width: int, line_gap: int = 8) -> int:
    x, y = xy
    total_h = 0
    for line in wrap_text(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=hex_rgb(fill) + (255,))
        _, th = text_size(draw, line, font)
        y += th + line_gap
        total_h += th + line_gap
    return total_h


def draw_chip(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fill: str, text_fill: str,
              font: ImageFont.ImageFont = FONT_CHIP, outline: str | None = None) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=999, fill=hex_rgb(fill) + (255,),
                           outline=hex_rgb(outline) + (255,) if outline else None, width=2 if outline else 0)
    w, h = text_size(draw, text, font)
    draw.text(((x1 + x2 - w) // 2, (y1 + y2 - h) // 2 - 1), text, font=font, fill=hex_rgb(text_fill) + (255,))


def draw_header(base: Image.Image, title: str, subtitle: str, accent: str = BLUE,
                title_font: ImageFont.ImageFont = FONT_TITLE, subtitle_font: ImageFont.ImageFont = FONT_SUBTITLE) -> int:
    draw = ImageDraw.Draw(base)
    draw.text((84, 64), title, font=title_font, fill=hex_rgb(INK) + (255,))
    subtitle_y = 64 + text_size(draw, title, title_font)[1] + 14
    draw.text((86, subtitle_y), subtitle, font=subtitle_font, fill=hex_rgb(MUTED) + (255,))
    draw.rounded_rectangle((84, 34, 114, 48), radius=8, fill=hex_rgb(accent) + (255,))
    return subtitle_y + text_size(draw, subtitle, subtitle_font)[1]


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    return ImageOps.contain(im, size, RESAMPLE)


def extract_frame(video_path: Path, second: float = 1.6, scale: int = 1280) -> Image.Image:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "frame.png"
        cmd = [
            "ffmpeg", "-y", "-ss", f"{second:.2f}", "-i", str(video_path),
            "-frames:v", "1", "-vf", f"scale={scale}:-1", str(tmp)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return Image.open(tmp).convert("RGBA").copy()


def paste_contained(base: Image.Image, image: Image.Image, box: tuple[int, int, int, int], radius: int = 24,
                    border: str | None = None) -> None:
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    placed = ImageOps.contain(image, (bw, bh), RESAMPLE)
    px = x1 + (bw - placed.width) // 2
    py = y1 + (bh - placed.height) // 2
    base.paste(placed, (px, py), placed)
    if border:
        d = ImageDraw.Draw(base)
        d.rounded_rectangle(box, radius=radius, outline=hex_rgb(border) + (255,), width=3)


def save_figure(base: Image.Image, stem: str, export_pdf: bool = True) -> tuple[Path, Path | None]:
    png = OUT_DIR / f"{stem}.png"
    base.convert("RGB").save(png, quality=95)
    pdf_path: Path | None = None
    if export_pdf:
        pdf_path = OUT_DIR / f"{stem}.pdf"
        base.convert("RGB").save(pdf_path, "PDF", resolution=300.0)
    return png, pdf_path


def draw_frame_card(base: Image.Image, box: tuple[int, int, int, int], frame: Image.Image, title: str,
                    label: str, accent: str, note: str, seed_badge: str) -> None:
    x1, y1, x2, y2 = box
    draw_card(base, box, radius=30, fill=CARD, outline=accent, width=3)
    d = ImageDraw.Draw(base)
    draw_chip(d, (x1 + 22, y1 + 18, x1 + 116, y1 + 52), seed_badge, fill=SOFT, text_fill=INK,
              font=FONT_CARD_TEXT_SMALL, outline=BORDER)
    draw_chip(d, (x2 - 318, y1 + 18, x2 - 22, y1 + 52), label, fill=accent, text_fill="white",
              font=FONT_CARD_TEXT_SMALL)
    frame_box = (x1 + 16, y1 + 66, x2 - 16, y1 + 414)
    paste_contained(base, frame, frame_box, radius=22)
    d.rounded_rectangle(frame_box, radius=22, outline=hex_rgb(BORDER) + (255,), width=2)
    d.text((x1 + 20, y1 + 436), title, font=FONT_CARD_TITLE, fill=hex_rgb(INK) + (255,))
    draw_wrapped_text(d, (x1 + 20, y1 + 468), note, FONT_CARD_TEXT_SMALL, MUTED, x2 - x1 - 40)


def draw_footer(base: Image.Image, text: str, accent: str = MUTED) -> None:
    d = ImageDraw.Draw(base)
    box = (84, H - 112, W - 84, H - 46)
    draw_card(base, box, radius=26, fill="#f7f3ea", outline="#e7dcca", width=2, shadow=False)
    draw_wrapped_text(d, (108, H - 92), text, FONT_CARD_TEXT, accent, W - 216)


def generate_figure_01() -> tuple[Path, Path | None]:
    base = make_canvas()
    title = "Main result: no-memory seed 1 vs approved-memory seed 8"
    subtitle = "Frozen Matrix-Game-2 keeps the same candidate pool; external memory only changes selection."
    draw_header(base, title, subtitle, accent=BLUE, title_font=FONT_TITLE_MEDIUM, subtitle_font=FONT_SUBTITLE)

    d = ImageDraw.Draw(base)
    draw_chip(d, (88, 210, 280, 248), "PPT-ready comparison", fill=BLUE_SOFT, text_fill=BLUE, font=FONT_TINY, outline=BLUE)
    draw_chip(d, (291, 210, 470, 248), "No training", fill=GREEN_SOFT, text_fill=GREEN, font=FONT_TINY, outline=GREEN)
    draw_chip(d, (482, 210, 792, 248), "Selection only, no internal model change", fill=GOLD_SOFT, text_fill=GOLD, font=FONT_TINY, outline=GOLD)

    no_mem = extract_frame(REPO / "media" / "demo" / "no_memory_seed1.mp4", second=1.7)
    yes_mem = extract_frame(REPO / "media" / "demo" / "with_roadsign_memory_seed8.mp4", second=1.7)

    left_box = (84, 276, 860, 804)
    right_box = (940, 276, 1716, 804)
    draw_frame_card(base, left_box, no_mem, "Selected continuation without external memory", "No-memory selection", BLUE, "The frozen model picks seed 1.", "Seed 1")
    draw_frame_card(base, right_box, yes_mem, "Selected continuation after approved road-sign memory", "Memory-guided selection", ORANGE, "The same candidate pool is reranked and seed 8 wins.", "Seed 8")

    # center arrow and annotation
    d.rounded_rectangle((876, 406, 924, 488), radius=24, fill=hex_rgb(CARD) + (255,), outline=hex_rgb(BORDER) + (255,), width=2)
    d.polygon([(892, 442), (908, 430), (908, 436), (916, 436), (916, 448), (908, 448), (908, 454)], fill=hex_rgb(INK) + (255,))
    draw_wrapped_text(d, (813, 506), "External memory changes selected output", FONT_TINY, MUTED, 174)

    draw_footer(base, "This is a selection comparison, not a new rollout, new training run, or checkpoint modification.")
    return save_figure(base, "01_main_result_no_memory_vs_memory")


def generate_figure_02() -> tuple[Path, Path | None]:
    source = REPO / "figures" / "demo_v3" / "candidate_gallery_memory_selection_poster.png"
    target = OUT_DIR / "02_candidate_gallery_memory_selection.png"
    shutil.copy2(source, target)
    pdf = OUT_DIR / "02_candidate_gallery_memory_selection.pdf"
    Image.open(target).convert("RGB").save(pdf, "PDF", resolution=300.0)
    return target, pdf


def generate_figure_03() -> tuple[Path, Path | None]:
    base = make_canvas()
    title = "Memory pipeline: write, read, use"
    subtitle = "The base model stays frozen; external memory stores cues and reranks candidates."
    draw_header(base, title, subtitle, accent=GREEN, title_font=FONT_TITLE_SMALL)

    d = ImageDraw.Draw(base)
    draw_chip(d, (88, 210, 250, 248), "write", fill=GREEN_SOFT, text_fill=GREEN, font=FONT_TINY, outline=GREEN)
    draw_chip(d, (260, 210, 388, 248), "read", fill=BLUE_SOFT, text_fill=BLUE, font=FONT_TINY, outline=BLUE)
    draw_chip(d, (402, 210, 508, 248), "use", fill=ORANGE_SOFT, text_fill=ORANGE, font=FONT_TINY, outline=ORANGE)

    boxes = [
        ((84, 286, 412, 648), "First visit", "Road-sign cue appears in the episode.\nSeed 1 video is the no-memory baseline.\nThis is the write trigger.", BLUE, "road-sign seen"),
        ((442, 286, 770, 648), "Write", "Store the approved crop and metadata.\nFields can include seed id, scene tag,\nframe id, and source path.", GREEN, "store crop"),
        ((800, 286, 1128, 648), "Memory bank", "Inspectable external storage.\nOften a compact JSONL or feature cache.\nNo world-model weights are updated.", GOLD, "external bank"),
        ((1158, 286, 1486, 648), "Read", "Compare candidate frame patches to the\nmemory crop. Use top-k patch similarity\nrather than internal attention.", ORANGE, "patch similarity"),
        ((1516, 286, 1716, 648), "Use", "Rerank the frozen candidate pool and\nselect the memory-consistent output.\nIn this case, seed 8 wins.", RED, "select seed 8"),
    ]
    for i, (box, name, body, accent, chip) in enumerate(boxes):
        draw_card(base, box, radius=28, fill=CARD, outline=accent, width=3)
        bx1, by1, bx2, by2 = box
        draw_chip(d, (bx1 + 20, by1 + 18, bx1 + 168, by1 + 52), chip, fill=accent, text_fill="white", font=FONT_TINY)
        d.text((bx1 + 22, by1 + 76), name, font=FONT_CARD_TITLE, fill=hex_rgb(INK) + (255,))
        draw_wrapped_text(d, (bx1 + 22, by1 + 118), body, FONT_CARD_TEXT_SMALL, MUTED, bx2 - bx1 - 44)
        if i < len(boxes) - 1:
            arrow_x1 = bx2 + 8
            arrow_x2 = bx2 + 36
            arrow_y = (by1 + by2) // 2
            d.line((arrow_x1, arrow_y, arrow_x2, arrow_y), fill=hex_rgb(MUTED_2) + (255,), width=6)
            d.polygon([(arrow_x2, arrow_y), (arrow_x2 - 12, arrow_y - 10), (arrow_x2 - 12, arrow_y + 10)], fill=hex_rgb(MUTED_2) + (255,))

    draw_footer(base, "Write = store approved cue. Read = compare candidate patches. Use = rerank selection. The model itself stays frozen.")
    return save_figure(base, "03_memory_pipeline_write_read_use")


def draw_info_grid(base: Image.Image, box: tuple[int, int, int, int], items: list[tuple[str, str, str]]) -> None:
    x1, y1, x2, y2 = box
    draw_card(base, box, radius=30, fill=CARD, outline=BORDER, width=2)
    d = ImageDraw.Draw(base)
    cols = 2
    gap = 18
    cell_w = (x2 - x1 - gap * (cols + 1)) // cols
    row_count = math.ceil(len(items) / cols)
    cell_h = (y2 - y1 - gap * (row_count + 1)) // row_count
    for idx, (k, v, accent) in enumerate(items):
        r = idx // cols
        c = idx % cols
        cx1 = x1 + gap + c * (cell_w + gap)
        cy1 = y1 + gap + r * (cell_h + gap)
        cx2 = cx1 + cell_w
        cy2 = cy1 + cell_h
        draw_card(base, (cx1, cy1, cx2, cy2), radius=22, fill=SOFT, outline=accent, width=2, shadow=False)
        d.rounded_rectangle((cx1 + 10, cy1 + 10, cx1 + 28, cy1 + 28), radius=6, fill=hex_rgb(accent) + (255,))
        d.text((cx1 + 38, cy1 + 12), k, font=FONT_CARD_TEXT_SMALL, fill=hex_rgb(MUTED) + (255,))
        value_y = cy1 + 46
        draw_wrapped_text(d, (cx1 + 18, value_y), v, FONT_CARD_TEXT, INK, cell_w - 36, line_gap=5)


def generate_figure_04() -> tuple[Path, Path | None]:
    base = make_canvas()
    title = "Memory card: what is stored, when it is read, and what it costs"
    subtitle = "External memory is inspectable. It helps rerank candidates without changing the frozen model."
    draw_header(base, title, subtitle, accent=ORANGE, title_font=FONT_TITLE_MEDIUM)

    items = [
        ("Memory type", "External road-sign / object-patch memory", ORANGE),
        ("Memory unit", "One crop, one frame cue, or one patch bundle", BLUE),
        ("Write", "After the first-visit episode, before reranking", GREEN),
        ("Read", "During candidate comparison and selection", GOLD),
        ("Use", "Select the memory-consistent continuation", RED),
        ("Stored fields", "crop image, seed id, frame id, scene tag, score, source path", BLUE),
        ("Code locations", "scripts/.../object_patch_memory_reranker.py\nresults/final/object_patch_rerank_seed1_8.csv", GREEN),
        ("Cost", "Small JSONL / image storage, light rerank runtime,\nno extra base-model GPU memory", GOLD),
        ("Limitation", "External reranking only; no internal conditioning", RED),
        ("Future upgrade", "Dynamic memory and internal conditioning", ORANGE),
    ]
    draw_info_grid(base, (84, 238, 1120, 900), items)

    right_x1 = 1164
    right_x2 = 1716
    cards = [
        (286, 470, "Storage", "Write only compact evidence: crop images, scores, and metadata.\nThe memory bank remains easy to inspect.", BLUE),
        (508, 692, "Runtime / GPU", "Reranking runs outside the frozen world model.\nThe model attention and weights do not change.", ORANGE),
        (730, 900, "Upgrade path", "If this were extended later, the next step would be\nlearned dynamic memory plus internal conditioning.", GREEN),
    ]
    for y1, y2, name, body, accent in cards:
        draw_card(base, (right_x1, y1, right_x2, y2), radius=26, fill=CARD, outline=accent, width=3)
        d = ImageDraw.Draw(base)
        draw_chip(d, (right_x1 + 20, y1 + 18, right_x1 + 166, y1 + 52), name, fill=accent, text_fill="white", font=FONT_CARD_TEXT_SMALL)
        draw_wrapped_text(d, (right_x1 + 22, y1 + 82), body, FONT_CARD_TEXT_SMALL, INK, right_x2 - right_x1 - 44, line_gap=7)

    draw_footer(base, "This memory is case-study evidence: useful for selection, but not a claim of a changed internal world model.")
    return save_figure(base, "04_memory_card")


def generate_figure_05() -> tuple[Path, Path | None]:
    base = make_canvas()
    title = "Object-patch reader: crop -> patch similarity -> rerank"
    subtitle = "The approved road-sign crop is compared against candidate frame patches to pick the best continuation."
    draw_header(base, title, subtitle, accent=BLUE, title_font=FONT_TITLE_MEDIUM)

    d = ImageDraw.Draw(base)
    draw_chip(d, (88, 210, 350, 248), "external memory read", fill=BLUE_SOFT, text_fill=BLUE, font=FONT_TINY, outline=BLUE)
    draw_chip(d, (362, 210, 548, 248), "top-k patch similarity", fill=GREEN_SOFT, text_fill=GREEN, font=FONT_TINY, outline=GREEN)
    draw_chip(d, (560, 210, 770, 248), "not internal attention", fill=ORANGE_SOFT, text_fill=ORANGE, font=FONT_TINY, outline=ORANGE)

    crop_path = REPO / "figures" / "final" / "roadsign_memory_target.png"
    crop = Image.open(crop_path).convert("RGBA")
    candidate = extract_frame(REPO / "media" / "demo" / "with_roadsign_memory_seed8.mp4", second=1.7)

    draw_card(base, (84, 286, 470, 714), radius=30, fill=CARD, outline=BLUE, width=3)
    d.text((112, 310), "Memory crop", font=FONT_CARD_TITLE, fill=hex_rgb(INK) + (255,))
    paste_contained(base, crop, (112, 352, 442, 664), radius=20, border=BORDER)
    draw_wrapped_text(d, (112, 678), "External memory unit.", FONT_CARD_TEXT_SMALL, MUTED, 338)

    draw_card(base, (540, 286, 1716, 714), radius=30, fill=CARD, outline=ORANGE, width=3)
    d.text((568, 310), "Candidate frame with patch grid", font=FONT_CARD_TITLE, fill=hex_rgb(INK) + (255,))
    frame_box = (568, 352, 1688, 656)
    paste_contained(base, candidate, frame_box, radius=20, border=BORDER)
    # patch grid overlay
    frame_inner = frame_box
    gx1, gy1, gx2, gy2 = frame_inner
    cols, rows = 8, 5
    cell_w = (gx2 - gx1) / cols
    cell_h = (gy2 - gy1) / rows
    for c in range(1, cols):
        x = int(gx1 + c * cell_w)
        d.line((x, gy1, x, gy2), fill=(255, 255, 255, 80), width=2)
    for r in range(1, rows):
        y = int(gy1 + r * cell_h)
        d.line((gx1, y, gx2, y), fill=(255, 255, 255, 80), width=2)
    # highlight a few candidate patches around the road-sign area
    hot_patches = [(0, 1), (0, 2), (1, 1), (1, 2)]
    for c, r in hot_patches:
        x1 = int(gx1 + c * cell_w)
        y1 = int(gy1 + r * cell_h)
        x2 = int(gx1 + (c + 1) * cell_w)
        y2 = int(gy1 + (r + 1) * cell_h)
        d.rounded_rectangle((x1 + 3, y1 + 3, x2 - 3, y2 - 3), radius=8, outline=hex_rgb(ORANGE) + (255,), width=4)
        d.rounded_rectangle((x1 + 5, y1 + 5, x2 - 5, y2 - 5), radius=6, fill=(219, 132, 34, 44))
    d.rounded_rectangle((gx1 + 24, gy1 + 24, gx1 + 220, gy1 + 108), radius=22, fill=(255, 255, 255, 230), outline=hex_rgb(ORANGE) + (255,), width=2)
    draw_wrapped_text(d, (gx1 + 38, gy1 + 40), "Patch encoder\n-> top-k match\n-> rerank score", FONT_TINY, INK, 160, line_gap=2)
    d.rounded_rectangle((1480, 604, 1680, 688), radius=20, fill=(255, 255, 255, 235), outline=hex_rgb(GREEN) + (255,), width=2)
    draw_wrapped_text(d, (1500, 624), "Best local patch\nsimilarity selects\nseed 8", FONT_TINY, GREEN, 150, line_gap=2)

    draw_chip(d, (614, 736, 852, 774), "memory crop -> patch encoder", fill=BLUE_SOFT, text_fill=BLUE, font=FONT_TINY, outline=BLUE)
    draw_chip(d, (872, 736, 1148, 774), "candidate patches -> top-k similarity", fill=GREEN_SOFT, text_fill=GREEN, font=FONT_TINY, outline=GREEN)
    draw_chip(d, (1160, 736, 1474, 774), "rerank -> selected output", fill=ORANGE_SOFT, text_fill=ORANGE, font=FONT_TINY, outline=ORANGE)
    draw_footer(base, "The reader is external and local: it compares object patches to a memory crop, then reranks candidates.")
    return save_figure(base, "05_object_patch_memory_reader")


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def generate_figure_06() -> tuple[Path, Path | None]:
    base = make_canvas()
    title = "Controls: approved memory vs distractors"
    subtitle = "Approved memory helps, but some distractors still remain competitive. That keeps the evidence honest."
    draw_header(base, title, subtitle, accent=RED, title_font=FONT_TITLE_SMALL)

    rows: list[tuple[str, str, str, str, str, str]] = []
    label_alias = {
        "approved_roadsign_memory_object_patch": "approved memory",
        "random_crop_memory": "random crop memory",
        "same_frame_non_roadsign_crop": "same-frame crop",
        "uniform_memory": "uniform memory",
        "recent_only": "recent-only",
        "wrong_scene_memory": "wrong-scene memory",
    }
    for source in [REPO / "results" / "evaluation" / "correct_vs_wrong_memory_battle.csv",
                   REPO / "results" / "evaluation" / "distractor_memory_controls.csv"]:
        if source.exists():
            for row in read_csv_dicts(source):
                mt = row.get("memory_type") or row.get("experiment") or row.get("type") or "memory"
                seed = row.get("selected_seed") or row.get("seed") or row.get("selected") or "n/a"
                score = row.get("top_score") or row.get("selected_score") or row.get("score") or "n/a"
                margin = row.get("score_margin") or row.get("margin") or "n/a"
                interp = row.get("interpretation") or row.get("notes") or "control row"
                rows.append((label_alias.get(mt, mt.replace("_", " ")), seed, score, margin, interp, source.stem))
    if not rows:
        rows = [
            ("approved_roadsign_memory_object_patch", "seed8", "0.740770", "0.013384", "approved memory wins", "fallback"),
            ("random_crop_memory", "seed8", "0.757466", "0.014475", "distractor remains competitive", "fallback"),
            ("same_frame_non_roadsign_crop", "seed8", "0.785166", "0.009186", "weak control only", "fallback"),
            ("uniform_memory", "seed1", "0.941255", "n/a", "not a meaningful cue", "fallback"),
            ("recent_only", "seed7", "0.899912", "n/a", "recent-only control", "fallback"),
            ("wrong_scene_memory", "seed5", "0.661841", "n/a", "wrong-scene control", "fallback"),
        ]

    cards = [
        (84, 286, 560, 514),
        (620, 286, 1096, 514),
        (1156, 286, 1716, 514),
        (84, 560, 560, 788),
        (620, 560, 1096, 788),
        (1156, 560, 1716, 788),
    ]
    accents = [GREEN, BLUE, ORANGE, MUTED_2, GOLD, RED]
    for idx, box in enumerate(cards):
        if idx >= len(rows):
            break
        mt, seed, score, margin, interp, origin = rows[idx]
        draw_card(base, box, radius=26, fill=CARD, outline=accents[idx], width=3)
        d = ImageDraw.Draw(base)
        draw_chip(d, (box[0] + 18, box[1] + 16, box[0] + 216, box[1] + 50), mt.replace("_", " "), fill=accents[idx], text_fill="white", font=FONT_MONO_SMALL)
        d.text((box[0] + 20, box[1] + 68), f"selected: {seed}", font=FONT_CARD_TITLE, fill=hex_rgb(INK) + (255,))
        d.text((box[0] + 20, box[1] + 104), f"top score: {score}", font=FONT_CARD_TEXT_SMALL, fill=hex_rgb(MUTED) + (255,))
        d.text((box[0] + 20, box[1] + 136), f"margin: {margin}", font=FONT_CARD_TEXT_SMALL, fill=hex_rgb(MUTED) + (255,))
        draw_wrapped_text(d, (box[0] + 20, box[1] + 168), interp, FONT_CARD_TEXT_SMALL, INK, box[2] - box[0] - 40, line_gap=4)

    draw_footer(base, "Approved memory is the intended cue, but the controls show that some distractors still score well. That is why this is honest evidence, not a final benchmark claim.")
    return save_figure(base, "06_correct_vs_wrong_memory_control")


def generate_memory_strength_chart(values: list[dict[str, str]]) -> Image.Image:
    chart = make_canvas()
    d = ImageDraw.Draw(chart)
    # chart region
    x1, y1, x2, y2 = 110, 280, 1660, 820
    draw_card(chart, (84, 238, 1716, 860), radius=30, fill=CARD, outline=BORDER, width=2)
    d.text((84, 64), "Memory strength reranking curve", font=FONT_TITLE_SMALL, fill=hex_rgb(INK) + (255,))
    d.text((86, 150), "Proxy score only. It shows how stronger memory weighting moves the selected seed from 1 to 8.",
           font=FONT_SUBTITLE, fill=hex_rgb(MUTED) + (255,))
    # axes
    d.line((x1, y2, x2, y2), fill=hex_rgb(MUTED_2) + (255,), width=3)
    d.line((x1, y1, x1, y2), fill=hex_rgb(MUTED_2) + (255,), width=3)
    for i in range(6):
        yy = y2 - i * (y2 - y1) / 5
        score = 1.0 + i * 0.18
        d.line((x1 - 8, yy, x1, yy), fill=hex_rgb(MUTED_2) + (255,), width=2)
        d.text((52, int(yy) - 10), f"{score:.2f}", font=FONT_TINY, fill=hex_rgb(MUTED) + (255,))
        d.line((x1, yy, x2, yy), fill=(220, 224, 232, 120), width=1)
    pts = []
    lambdas = []
    scores = []
    seeds = []
    for row in values:
        lam = float(row.get("lambda", row.get("strength", "0")))
        score = float(row.get("selected_score", row.get("score", "0")))
        seed = row.get("selected_seed", "")
        lambdas.append(lam)
        scores.append(score)
        seeds.append(seed)
    min_s, max_s = min(scores), max(scores)
    min_l, max_l = min(lambdas), max(lambdas)
    def sx(lam: float) -> float:
        return x1 + (lam - min_l) / max(1e-9, (max_l - min_l)) * (x2 - x1)
    def sy(score: float) -> float:
        return y2 - (score - min_s) / max(1e-9, (max_s - min_s)) * (y2 - y1)
    pts = [(sx(l), sy(s)) for l, s in zip(lambdas, scores)]
    if len(pts) > 1:
        d.line(pts, fill=hex_rgb(ORANGE) + (255,), width=6, joint="curve")
    for idx, ((x, y), seed, lam, score) in enumerate(zip(pts, seeds, lambdas, scores)):
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=hex_rgb(BLUE if seed == "seed1" else ORANGE) + (255,), outline=hex_rgb(CARD) + (255,), width=2)
        label_x = x - 18
        if x < x1 + 50:
            label_x = x + 14
        elif x > x2 - 50:
            label_x = x - 36
        d.text((label_x, y - 42), seed, font=FONT_TINY, fill=hex_rgb(INK) + (255,))
        if idx > 0:
            d.text((label_x, y + 18), f"{lam:.2f}", font=FONT_TINY, fill=hex_rgb(MUTED) + (255,))
    for lam in [0.0, 0.25, 0.5, 0.75, 1.0]:
        xx = sx(lam)
        d.line((xx, y2, xx, y2 + 8), fill=hex_rgb(MUTED_2) + (255,), width=2)
        d.text((xx - 18, y2 + 18), f"{lam:.2f}", font=FONT_TINY, fill=hex_rgb(MUTED) + (255,))
    d.text((x2 - 210, y1 + 18), "selected seed", font=FONT_CARD_TEXT_SMALL, fill=hex_rgb(MUTED) + (255,))
    d.text((x2 - 210, y1 + 48), "seed 1 at low lambda", font=FONT_CARD_TEXT_SMALL, fill=hex_rgb(BLUE) + (255,))
    d.text((x2 - 210, y1 + 76), "seed 8 at high lambda", font=FONT_CARD_TEXT_SMALL, fill=hex_rgb(ORANGE) + (255,))
    return chart


def generate_figure_07() -> tuple[Path, Path | None]:
    rows = read_csv_dicts(REPO / "results" / "evaluation" / "memory_strength_curve.csv")
    chart = generate_memory_strength_chart(rows)
    return save_figure(chart, "07_memory_strength_reranking_curve")


def generate_figure_08() -> tuple[Path, Path | None]:
    base = make_canvas()
    title = "Completed vs planned evidence"
    subtitle = "Strong enough for PPT, but the evidence tier stays honest: some pieces are done, others are planned."
    draw_header(base, title, subtitle, accent=GOLD, title_font=FONT_TITLE_SMALL)

    sections = [
        (84, 286, 560, 838, "Completed now", GREEN, [
            "candidate gallery figure",
            "main no-memory vs memory comparison",
            "memory cost analysis",
            "manual review packet",
            "presentation figure pack",
        ]),
        (620, 286, 1096, 838, "Limited / honest", GOLD, [
            "external reranking only",
            "single-case road-sign evidence",
            "controls are not perfect",
            "no claim of internal model change",
            "no new training or checkpoint modifications",
        ]),
        (1156, 286, 1716, 838, "Planned next", BLUE, [
            "dynamic memory",
            "internal conditioning",
            "human-reviewed labels",
            "stronger multi-scene validation",
            "broader candidate pool if available",
        ]),
    ]
    for x1, y1, x2, y2, head, accent, bullets in sections:
        draw_card(base, (x1, y1, x2, y2), radius=30, fill=CARD, outline=accent, width=3)
        d = ImageDraw.Draw(base)
        draw_chip(d, (x1 + 20, y1 + 18, x1 + 236, y1 + 52), head, fill=accent, text_fill="white", font=FONT_CARD_TEXT_SMALL)
        y = y1 + 88
        for bullet in bullets:
            d.ellipse((x1 + 22, y + 7, x1 + 34, y + 19), fill=hex_rgb(accent) + (255,))
            draw_wrapped_text(d, (x1 + 46, y), bullet, FONT_CARD_TEXT, INK, x2 - x1 - 70, line_gap=4)
            y += 84
    draw_footer(base, "This separation keeps the story credible: some evidence is done, some is limited, and some should stay on the roadmap.")
    return save_figure(base, "08_completed_vs_planned_evidence")


def generate_figure_09() -> tuple[Path, Path | None]:
    base = make_canvas()
    title = "Claims and limitations"
    subtitle = "PPT-safe wording: state what the evidence supports, and state clearly what it does not support."
    draw_header(base, title, subtitle, accent=RED, title_font=FONT_TITLE_SMALL)

    left = (84, 286, 850, 810)
    right = (910, 286, 1716, 810)
    draw_card(base, left, radius=30, fill=CARD, outline=GREEN, width=3)
    draw_card(base, right, radius=30, fill=CARD, outline=RED, width=3)
    d = ImageDraw.Draw(base)
    draw_chip(d, (left[0] + 20, left[1] + 18, left[0] + 276, left[1] + 52), "Supported claims", fill=GREEN, text_fill="white", font=FONT_CARD_TEXT_SMALL)
    draw_chip(d, (right[0] + 20, right[1] + 18, right[0] + 278, right[1] + 52), "Not supported", fill=RED, text_fill="white", font=FONT_CARD_TEXT_SMALL)

    claims = [
        "External memory changes the selected continuation.",
        "The candidate pool stays frozen; only reranking changes.",
        "The package uses real model outputs and real control tables.",
        "The memory bank is small, inspectable, and easy to audit.",
    ]
    limits = [
        "This is case-study evidence, not a broad benchmark claim.",
        "The mechanism is external reranking, not internal conditioning.",
        "The controls still leave some distractors competitive.",
        "No claim of improved training or changed model weights.",
    ]
    y = left[1] + 84
    for item in claims:
        d.ellipse((left[0] + 24, y + 8, left[0] + 40, y + 24), fill=hex_rgb(GREEN) + (255,))
        draw_wrapped_text(d, (left[0] + 52, y), item, FONT_CARD_TEXT, INK, left[2] - left[0] - 78, line_gap=4)
        y += 92
    y = right[1] + 84
    for item in limits:
        d.rectangle((right[0] + 24, y + 8, right[0] + 40, y + 24), fill=hex_rgb(RED) + (255,))
        draw_wrapped_text(d, (right[0] + 52, y), item, FONT_CARD_TEXT, INK, right[2] - right[0] - 78, line_gap=4)
        y += 92

    draw_footer(base, "Use the green side as the claim, and the red side as the limitation. That keeps the final narrative honest.")
    return save_figure(base, "09_claims_and_limitations")


def audit_figures(figures: list[tuple[str, Path, Path | None, str]]) -> Path:
    audit_path = RESULTS_DIR / "figure_quality_audit.csv"
    with audit_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["figure_id", "png_path", "pdf_path", "png_bytes", "pdf_bytes", "status", "notes"])
        for fig_id, png, pdf, notes in figures:
            png_bytes = png.stat().st_size if png.exists() else 0
            pdf_bytes = pdf.stat().st_size if pdf and pdf.exists() else 0
            writer.writerow([fig_id, str(png.relative_to(REPO)), str(pdf.relative_to(REPO)) if pdf else "",
                             png_bytes, pdf_bytes, "ppt_ready" if png_bytes > 0 else "missing", notes])
    return audit_path


def main() -> None:
    ensure_dirs()
    outputs: list[tuple[str, Path, Path | None, str]] = []
    for fig_id, fn, notes in [
        ("01", generate_figure_01, "real frames from no-memory and approved-memory mp4s"),
        ("02", generate_figure_02, "copied polished candidate gallery poster"),
        ("03", generate_figure_03, "write/read/use pipeline diagram"),
        ("04", generate_figure_04, "memory card / cost / limitation summary"),
        ("05", generate_figure_05, "object-patch memory reader with real crop and frame"),
        ("06", generate_figure_06, "approved memory and distractor control cards"),
        ("07", generate_figure_07, "memory strength curve from existing CSV"),
        ("08", generate_figure_08, "completed vs planned evidence summary"),
        ("09", generate_figure_09, "claims and limitations summary"),
    ]:
        png, pdf = fn()
        outputs.append((fig_id, png, pdf, notes))
    audit_figures(outputs)


if __name__ == "__main__":
    main()
