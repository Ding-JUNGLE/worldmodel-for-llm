#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path('/mnt/data1/dgw/github_upload/worldmodel-for-llm')
PAPER = ROOT / 'paper/cvpr2026_ap0006_memory_modules'
FIGDIR = PAPER / 'figures'
SRC1 = ROOT / 'figures/presentation/01_main_result_no_memory_vs_memory.png'

RESAMPLE = getattr(Image, 'Resampling', Image).LANCZOS
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

BLACK = (30, 34, 42)
GRAY = (100, 107, 117)
LIGHT = (247, 248, 250)
BORDER = (198, 204, 214)
MEM = (230, 126, 34)
RESULT = (36, 99, 235)
HILITE = (220, 38, 38)
GREEN = (22, 163, 74)


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


F_PANEL = load_font(FONT_BOLD, 22)
F_LABEL = load_font(FONT_BOLD, 26)
F_TEXT = load_font(FONT_REG, 18)
F_SMALL = load_font(FONT_REG, 16)
F_NOTE = load_font(FONT_REG, 15)
F_TINY = load_font(FONT_REG, 14)


def fit(img, size):
    return ImageOps.fit(img, size, method=RESAMPLE)


def rounded(draw, xy, outline=BORDER, fill=(255, 255, 255), width=2, radius=18):
    draw.rounded_rectangle(xy, radius=radius, outline=outline, fill=fill, width=width)


def add_text(draw, xy, text, font, fill=BLACK):
    draw.text(xy, text, font=font, fill=fill)


def add_center_text(draw, center, text, font, fill=BLACK):
    box = draw.textbbox((0, 0), text, font=font)
    x = center[0] - (box[2] - box[0]) / 2
    y = center[1] - (box[3] - box[1]) / 2
    draw.text((x, y), text, font=font, fill=fill)


def arrow(draw, start, end, color=GRAY, width=4, head=12):
    draw.line((start[0], start[1], end[0], end[1]), fill=color, width=width)
    if end[0] >= start[0]:
        pts = [(end[0], end[1]), (end[0] - head, end[1] - head // 2), (end[0] - head, end[1] + head // 2)]
    else:
        pts = [(end[0], end[1]), (end[0] + head, end[1] - head // 2), (end[0] + head, end[1] + head // 2)]
    draw.polygon(pts, fill=color)


def save_outputs(img, stem):
    png = FIGDIR / f'{stem}.png'
    pdf = FIGDIR / f'{stem}.pdf'
    img.save(png)
    img.convert('RGB').save(pdf, 'PDF', resolution=300.0)


src = Image.open(SRC1).convert('RGB')
seed1 = src.crop((125, 345, 790, 725))
seed8 = src.crop((1010, 345, 1685, 725))
first_visit = fit(seed8, (210, 130))
memory_crop = seed8.crop((395, 28, 650, 190))
memory_crop = fit(memory_crop, (150, 110))

# Patch-matching support assets.
frame = fit(seed8, (520, 290))
fw, fh = frame.size
cols, rows = 5, 3
cell = (3, 0)
px1 = int(cell[0] * fw / cols)
py1 = int(cell[1] * fh / rows)
px2 = int((cell[0] + 1) * fw / cols)
py2 = int((cell[1] + 1) * fh / rows)
best_patch = frame.crop((px1, py1, px2, py2))
best_patch = fit(best_patch, (180, 120))

# Figure 1: paper-style method overview.
W1, H1 = 1800, 620
fig1 = Image.new('RGB', (W1, H1), 'white')
d1 = ImageDraw.Draw(fig1)

panels = {
    'a': (40, 60, 290, 400),
    'b': (340, 60, 560, 400),
    'c': (610, 60, 900, 400),
    'd': (950, 60, 1410, 400),
    'e': (1460, 60, 1760, 400),
}
for key in panels:
    rounded(d1, panels[key])

# Connecting arrows.
order = ['a', 'b', 'c', 'd', 'e']
for left, right in zip(order[:-1], order[1:]):
    lx = panels[left][2]
    rx = panels[right][0]
    y = (panels[left][1] + panels[left][3]) // 2
    arrow(d1, (lx + 8, y), (rx - 12, y), color=GRAY)

# (a) Problem setup.
a = panels['a']
add_text(d1, (a[0] + 16, a[1] + 12), '(a) Problem setup', F_PANEL, BLACK)
fig1.paste(first_visit, (a[0] + 18, a[1] + 54))
d1.rectangle((a[0] + 18, a[1] + 54, a[0] + 228, a[1] + 184), outline=BORDER, width=1)
fig1.paste(memory_crop, (a[0] + 92, a[1] + 210))
d1.rectangle((a[0] + 92, a[1] + 210, a[0] + 242, a[1] + 320), outline=MEM, width=3)
arrow(d1, (a[0] + 124, a[1] + 184), (a[0] + 146, a[1] + 204), color=MEM)
add_text(d1, (a[0] + 18, a[1] + 330), 'First-visit visual evidence', F_TEXT, BLACK)
add_text(d1, (a[0] + 18, a[1] + 356), 'road-sign crop written once', F_SMALL, GRAY)

# (b) Memory bank.
b = panels['b']
add_text(d1, (b[0] + 16, b[1] + 12), '(b) Memory write/store', F_PANEL, BLACK)
for i, label in enumerate(['crop path', 'feature vector', 'metadata']):
    y = b[1] + 90 + i * 70
    rounded(d1, (b[0] + 24, y, b[2] - 24, y + 46), outline=MEM, fill=LIGHT, width=2, radius=12)
    add_text(d1, (b[0] + 42, y + 12), label, F_TEXT, BLACK)
add_text(d1, (b[0] + 24, b[1] + 318), 'External memory', F_LABEL, MEM)
add_text(d1, (b[0] + 24, b[1] + 350), 'inference-time only', F_SMALL, GRAY)

# (c) Candidate generation.
c = panels['c']
add_text(d1, (c[0] + 16, c[1] + 12), '(c) Candidate generation', F_PANEL, BLACK)
add_text(d1, (c[0] + 16, c[1] + 48), 'Frozen MatrixGame-2', F_LABEL, BLACK)
thumb1 = fit(seed1, (78, 78))
thumb8 = fit(seed8, (78, 78))
fig1.paste(thumb1, (c[0] + 24, c[1] + 110))
d1.rectangle((c[0] + 24, c[1] + 110, c[0] + 102, c[1] + 188), outline=BORDER, width=1)
fig1.paste(thumb8, (c[0] + 188, c[1] + 110))
d1.rectangle((c[0] + 188, c[1] + 110, c[0] + 266, c[1] + 188), outline=BORDER, width=1)
add_center_text(d1, (c[0] + 145, c[1] + 150), '...', F_LABEL, GRAY)
add_text(d1, (c[0] + 28, c[1] + 198), 'seed1', F_SMALL, BLACK)
add_text(d1, (c[0] + 192, c[1] + 198), 'seed8', F_SMALL, BLACK)
add_text(d1, (c[0] + 24, c[1] + 262), 'candidate seed1 ... seed8', F_TEXT, BLACK)
add_text(d1, (c[0] + 24, c[1] + 294), 'same pool before reranking', F_SMALL, GRAY)

# (d) Patch matching.
d = panels['d']
add_text(d1, (d[0] + 16, d[1] + 12), '(d) Memory read by patch matching', F_PANEL, BLACK)
fig1.paste(frame, (d[0] + 18, d[1] + 70))
g = ImageDraw.Draw(fig1)
fx, fy = d[0] + 18, d[1] + 70
for i in range(1, cols):
    x = fx + int(i * fw / cols)
    g.line((x, fy, x, fy + fh), fill=(255, 255, 255), width=2)
for j in range(1, rows):
    y = fy + int(j * fh / rows)
    g.line((fx, y, fx + fw, y), fill=(255, 255, 255), width=2)
hx1, hy1 = fx + px1, fy + py1
hx2, hy2 = fx + px2, fy + py2
g.rectangle((hx1, hy1, hx2, hy2), outline=RESULT, width=4)
add_text(d1, (d[0] + 18, d[1] + 372), 'Regular grid patches', F_TEXT, BLACK)
add_text(d1, (d[0] + 242, d[1] + 372), 'Feature encoder', F_TEXT, BLACK)
add_text(d1, (d[0] + 18, d[1] + 402), 'Cosine similarity', F_TEXT, BLACK)
add_text(d1, (d[0] + 242, d[1] + 402), 'best local patch', F_TEXT, BLACK)

# (e) Reranking result.
e = panels['e']
add_text(d1, (e[0] + 16, e[1] + 12), '(e) Candidate reranking', F_PANEL, BLACK)
mini1 = fit(seed1, (118, 78))
mini8 = fit(seed8, (118, 78))
fig1.paste(mini1, (e[0] + 22, e[1] + 78))
d1.rectangle((e[0] + 22, e[1] + 78, e[0] + 140, e[1] + 156), outline=BORDER, width=1)
fig1.paste(mini8, (e[0] + 22, e[1] + 232))
d1.rectangle((e[0] + 22, e[1] + 232, e[0] + 140, e[1] + 310), outline=RESULT, width=3)
arrow(d1, (e[0] + 176, e[1] + 118), (e[0] + 176, e[1] + 270), color=RESULT)
add_text(d1, (e[0] + 162, e[1] + 86), 'No memory: seed1', F_TEXT, BLACK)
add_text(d1, (e[0] + 162, e[1] + 240), 'With memory: seed8', F_TEXT, BLACK)
add_text(d1, (e[0] + 24, e[1] + 344), 'seed1 -> seed8', F_LABEL, RESULT)
add_text(d1, (e[0] + 24, e[1] + 376), 'selected output changes', F_SMALL, GRAY)

# Notes.
rounded(d1, (80, 500, 840, 550), outline=BORDER, fill=LIGHT, width=1, radius=12)
add_text(d1, (100, 516), 'No object segmentation. Patches are regular grid cells.', F_TEXT, BLACK)
rounded(d1, (940, 500, 1710, 550), outline=BORDER, fill=LIGHT, width=1, radius=12)
add_text(d1, (960, 516), 'ResNet / DINO / CLIP are feature extractors.', F_TEXT, BLACK)
save_outputs(fig1, 'fig1_method_overview')

# Figure 2: patch-matching evidence.
W2, H2 = 1100, 900
fig2 = Image.new('RGB', (W2, H2), 'white')
d2 = ImageDraw.Draw(fig2)
pan2 = {
    'a': (40, 40, 320, 290),
    'b': (360, 40, 1060, 410),
    'c': (40, 340, 540, 720),
    'd': (580, 470, 1060, 820),
}
for key in pan2:
    rounded(d2, pan2[key])

# (a) memory crop
pa = pan2['a']
add_text(d2, (pa[0] + 16, pa[1] + 12), '(a) Memory crop', F_PANEL, BLACK)
mc = fit(memory_crop, (220, 150))
fig2.paste(mc, (pa[0] + 28, pa[1] + 72))
d2.rectangle((pa[0] + 28, pa[1] + 72, pa[0] + 248, pa[1] + 222), outline=MEM, width=3)
add_text(d2, (pa[0] + 28, pa[1] + 238), 'stored local visual cue', F_SMALL, GRAY)

# (b) candidate frame with grid
pb = pan2['b']
add_text(d2, (pb[0] + 16, pb[1] + 12), '(b) Candidate frame', F_PANEL, BLACK)
frame_big = fit(seed8, (650, 250))
fig2.paste(frame_big, (pb[0] + 24, pb[1] + 72))
d2.rectangle((pb[0] + 24, pb[1] + 72, pb[0] + 674, pb[1] + 322), outline=BORDER, width=1)
fw2, fh2 = frame_big.size
fx2, fy2 = pb[0] + 24, pb[1] + 72
for i in range(1, cols):
    x = fx2 + int(i * fw2 / cols)
    d2.line((x, fy2, x, fy2 + fh2), fill=(255, 255, 255), width=2)
for j in range(1, rows):
    y = fy2 + int(j * fh2 / rows)
    d2.line((fx2, y, fx2 + fw2, y), fill=(255, 255, 255), width=2)
qx1 = fx2 + int(cell[0] * fw2 / cols)
qy1 = fy2 + int(cell[1] * fh2 / rows)
qx2 = fx2 + int((cell[0] + 1) * fw2 / cols)
qy2 = fy2 + int((cell[1] + 1) * fh2 / rows)
d2.rectangle((qx1, qy1, qx2, qy2), outline=RESULT, width=5)
add_text(d2, (pb[0] + 24, pb[1] + 336), 'Regular grid patches', F_TEXT, BLACK)
add_text(d2, (pb[0] + 454, pb[1] + 336), 'Best-matching patch', F_TEXT, RESULT)

# (c) patch similarity
pc = pan2['c']
add_text(d2, (pc[0] + 16, pc[1] + 12), '(c) Patch similarity', F_PANEL, BLACK)
fig2.paste(mc, (pc[0] + 26, pc[1] + 76))
d2.rectangle((pc[0] + 26, pc[1] + 76, pc[0] + 206, pc[1] + 196), outline=MEM, width=3)
fig2.paste(best_patch, (pc[0] + 286, pc[1] + 76))
d2.rectangle((pc[0] + 286, pc[1] + 76, pc[0] + 466, pc[1] + 196), outline=RESULT, width=3)
arrow(d2, (pc[0] + 214, pc[1] + 136), (pc[0] + 276, pc[1] + 136), color=GRAY)
add_text(d2, (pc[0] + 52, pc[1] + 212), 'Memory crop', F_SMALL, BLACK)
add_text(d2, (pc[0] + 318, pc[1] + 212), 'Best-matching patch', F_SMALL, BLACK)
rounded(d2, (pc[0] + 30, pc[1] + 262, pc[0] + 470, pc[1] + 336), outline=BORDER, fill=LIGHT, width=1, radius=12)
add_center_text(d2, ((pc[0] + 250), pc[1] + 300), 's_{j,t,k} = cos(f(m), f(p_{j,t,k}))', F_TEXT, BLACK)
add_text(d2, (pc[0] + 30, pc[1] + 356), 'No object segmentation: one grid cell is selected as the best local match.', F_SMALL, GRAY)

# (d) seed comparison
pd = pan2['d']
add_text(d2, (pd[0] + 16, pd[1] + 12), '(d) Candidate comparison', F_PANEL, BLACK)
small1 = fit(seed1, (190, 120))
small8 = fit(seed8, (190, 120))
fig2.paste(small1, (pd[0] + 26, pd[1] + 72))
d2.rectangle((pd[0] + 26, pd[1] + 72, pd[0] + 216, pd[1] + 192), outline=BORDER, width=1)
fig2.paste(small8, (pd[0] + 264, pd[1] + 72))
d2.rectangle((pd[0] + 264, pd[1] + 72, pd[0] + 454, pd[1] + 192), outline=RESULT, width=3)
add_text(d2, (pd[0] + 34, pd[1] + 208), 'No-memory: seed1', F_TEXT, BLACK)
add_text(d2, (pd[0] + 272, pd[1] + 208), 'Memory-guided: seed8', F_TEXT, BLACK)
arrow(d2, (pd[0] + 220, pd[1] + 132), (pd[0] + 252, pd[1] + 132), color=RESULT)
add_text(d2, (pd[0] + 26, pd[1] + 266), 'Patch evidence contributes to reranking', F_SMALL, GRAY)
save_outputs(fig2, 'fig2_patch_matching_evidence')

print('Created paper-style figures in', FIGDIR)
