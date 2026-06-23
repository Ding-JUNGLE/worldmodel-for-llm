#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path('/mnt/data1/dgw/github_upload/worldmodel-for-llm')
PAPER = ROOT / 'paper/cvpr2026_ap0006_memory_modules'
FIGDIR = PAPER / 'figures'
SRC = ROOT / 'figures/presentation/01_main_result_no_memory_vs_memory.png'

RESAMPLE = getattr(Image, 'Resampling', Image).LANCZOS
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

BLACK = (32, 37, 45)
GRAY = (103, 112, 122)
LIGHT = (247, 248, 250)
BORDER = (196, 203, 214)
MEM = (221, 122, 42)
SEL = (41, 98, 255)
ARROW = (120, 128, 138)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


F_PANEL = font(FONT_BOLD, 26)
F_HEAD = font(FONT_BOLD, 24)
F_TEXT = font(FONT_REG, 22)
F_SMALL = font(FONT_REG, 19)
F_TINY = font(FONT_REG, 17)
F_NOTE = font(FONT_REG, 20)


def fit(img, size):
    return ImageOps.fit(img, size, method=RESAMPLE)


def rounded(draw, xy, outline=BORDER, fill=(255, 255, 255), width=2, radius=18):
    draw.rounded_rectangle(xy, radius=radius, outline=outline, fill=fill, width=width)


def text(draw, xy, msg, fnt, fill=BLACK):
    draw.text(xy, msg, font=fnt, fill=fill)


def centered(draw, center, msg, fnt, fill=BLACK):
    box = draw.textbbox((0, 0), msg, font=fnt)
    draw.text((center[0] - (box[2] - box[0]) / 2, center[1] - (box[3] - box[1]) / 2), msg, font=fnt, fill=fill)


def arrow(draw, start, end, color=ARROW, width=5, head=14):
    draw.line((start[0], start[1], end[0], end[1]), fill=color, width=width)
    if abs(end[0] - start[0]) >= abs(end[1] - start[1]):
        if end[0] >= start[0]:
            pts = [(end[0], end[1]), (end[0] - head, end[1] - head // 2), (end[0] - head, end[1] + head // 2)]
        else:
            pts = [(end[0], end[1]), (end[0] + head, end[1] - head // 2), (end[0] + head, end[1] + head // 2)]
    else:
        if end[1] >= start[1]:
            pts = [(end[0], end[1]), (end[0] - head // 2, end[1] - head), (end[0] + head // 2, end[1] - head)]
        else:
            pts = [(end[0], end[1]), (end[0] - head // 2, end[1] + head), (end[0] + head // 2, end[1] + head)]
    draw.polygon(pts, fill=color)


def save_outputs(img, stem):
    png = FIGDIR / f'{stem}.png'
    pdf = FIGDIR / f'{stem}.pdf'
    img.save(png)
    img.convert('RGB').save(pdf, 'PDF', resolution=300.0)


src = Image.open(SRC).convert('RGB')
seed1 = src.crop((125, 345, 790, 725))
seed8 = src.crop((1010, 345, 1685, 725))
first_visit = fit(seed8, (320, 170))
memory_crop = fit(seed8.crop((392, 22, 650, 190)), (220, 140))
setup_frame = fit(seed8, (280, 150))
setup_crop = fit(memory_crop, (190, 120))
thumb1 = fit(seed1, (140, 90))
thumb8 = fit(seed8, (140, 90))
frame = fit(seed8, (520, 240))
cols, rows = 5, 3
fw, fh = frame.size
cell = (3, 0)
px1 = int(cell[0] * fw / cols)
py1 = int(cell[1] * fh / rows)
px2 = int((cell[0] + 1) * fw / cols)
py2 = int((cell[1] + 1) * fh / rows)
best_patch = fit(frame.crop((px1, py1, px2, py2)), (200, 130))

# Figure 1: two-row paper block diagram.
W1, H1 = 1800, 1040
fig1 = Image.new('RGB', (W1, H1), 'white')
d1 = ImageDraw.Draw(fig1)

a = (50, 50, 576, 410)
b = (636, 50, 1162, 410)
c = (1222, 50, 1748, 410)
d = (50, 500, 910, 870)
e = (970, 500, 1750, 870)
for panel in [a, b, c, d, e]:
    rounded(d1, panel, radius=20)

# top-row arrows
arrow(d1, (a[2] + 12, (a[1] + a[3]) // 2), (b[0] - 12, (b[1] + b[3]) // 2))
arrow(d1, (b[2] + 12, (b[1] + b[3]) // 2), (c[0] - 12, (c[1] + c[3]) // 2))
# row transition and rerank arrow
arrow(d1, ((c[0] + c[2]) // 2, c[3] + 12), ((c[0] + c[2]) // 2, d[1] - 18))
arrow(d1, (d[2] + 12, (d[1] + d[3]) // 2), (e[0] - 12, (e[1] + e[3]) // 2))

# panel (a)
text(d1, (a[0] + 28, a[1] + 24), '(a) Setup', F_PANEL)
fig1.paste(setup_frame, (a[0] + 108, a[1] + 76))
d1.rectangle((a[0] + 108, a[1] + 76, a[0] + 388, a[1] + 226), outline=BORDER, width=1)
centered(d1, (a[0] + 248, a[1] + 252), 'first-visit frame', F_SMALL)
fig1.paste(setup_crop, (a[0] + 153, a[1] + 270))
d1.rectangle((a[0] + 153, a[1] + 270, a[0] + 343, a[1] + 390), outline=MEM, width=3)
arrow(d1, (a[0] + 248, a[1] + 226), (a[0] + 248, a[1] + 258), color=MEM, width=4)
centered(d1, (a[0] + 248, a[1] + 404), 'road-sign crop / visual cue', F_TINY, MEM)

# panel (b)
text(d1, (b[0] + 28, b[1] + 24), '(b) Write/store', F_PANEL)
for idx, label in enumerate(['crop path', 'feature vector', 'metadata']):
    yy = b[1] + 110 + idx * 82
    rounded(d1, (b[0] + 88, yy, b[2] - 88, yy + 50), outline=MEM, fill=LIGHT, width=2, radius=14)
    text(d1, (b[0] + 130, yy + 13), label, F_TEXT)
text(d1, (b[0] + 88, b[1] + 328), 'External memory', F_HEAD, MEM)
text(d1, (b[0] + 88, b[1] + 360), 'inference-time storage', F_SMALL, GRAY)

# panel (c)
text(d1, (c[0] + 28, c[1] + 24), '(c) Generate candidates', F_PANEL)
text(d1, (c[0] + 40, c[1] + 86), 'Frozen MatrixGame-2', F_HEAD)
fig1.paste(thumb1, (c[0] + 52, c[1] + 156))
d1.rectangle((c[0] + 52, c[1] + 156, c[0] + 192, c[1] + 246), outline=BORDER, width=1)
centered(d1, (c[0] + 262, c[1] + 202), '...', F_HEAD, GRAY)
fig1.paste(thumb8, (c[0] + 332, c[1] + 156))
d1.rectangle((c[0] + 332, c[1] + 156, c[0] + 472, c[1] + 246), outline=BORDER, width=1)
text(d1, (c[0] + 58, c[1] + 258), 'candidate_seed1', F_TINY)
text(d1, (c[0] + 336, c[1] + 258), 'candidate_seed8', F_TINY)
text(d1, (c[0] + 52, c[1] + 318), 'same candidate pool before reranking', F_SMALL, GRAY)

# panel (d)
text(d1, (d[0] + 28, d[1] + 24), '(d) Read by patch matching', F_PANEL)
fig1.paste(frame, (d[0] + 40, d[1] + 82))
d1.rectangle((d[0] + 40, d[1] + 82, d[0] + 560, d[1] + 322), outline=BORDER, width=1)
fx, fy = d[0] + 40, d[1] + 82
for i in range(1, cols):
    xx = fx + int(i * fw / cols)
    d1.line((xx, fy, xx, fy + fh), fill=(255, 255, 255), width=2)
for j in range(1, rows):
    yy = fy + int(j * fh / rows)
    d1.line((fx, yy, fx + fw, yy), fill=(255, 255, 255), width=2)
hx1, hy1 = fx + px1, fy + py1
hx2, hy2 = fx + px2, fy + py2
d1.rectangle((hx1, hy1, hx2, hy2), outline=SEL, width=4)
fig1.paste(best_patch, (d[0] + 620, d[1] + 132))
d1.rectangle((d[0] + 620, d[1] + 132, d[0] + 820, d[1] + 262), outline=SEL, width=3)
text(d1, (d[0] + 628, d[1] + 274), 'best local patch', F_SMALL, SEL)
for x0, label in zip([d[0] + 48, d[0] + 250, d[0] + 452, d[0] + 654], ['Regular grid patches', 'Feature encoder', 'Cosine similarity', 'Best local patch']):
    rounded(d1, (x0, d[1] + 336, x0 + 164, d[1] + 390), outline=BORDER, fill=LIGHT, width=1, radius=14)
    centered(d1, (x0 + 82, d[1] + 363), label, F_TINY)

# panel (e)
text(d1, (e[0] + 28, e[1] + 24), '(e) Rerank candidates', F_PANEL)
fig1.paste(thumb1, (e[0] + 58, e[1] + 104))
d1.rectangle((e[0] + 58, e[1] + 104, e[0] + 198, e[1] + 194), outline=BORDER, width=1)
text(d1, (e[0] + 250, e[1] + 124), 'No memory: seed1', F_TEXT)
fig1.paste(thumb8, (e[0] + 58, e[1] + 244))
d1.rectangle((e[0] + 58, e[1] + 244, e[0] + 198, e[1] + 334), outline=SEL, width=3)
text(d1, (e[0] + 250, e[1] + 264), 'With memory: seed8', F_TEXT)
arrow(d1, (e[0] + 520, e[1] + 154), (e[0] + 520, e[1] + 294), color=SEL, width=4)
text(d1, (e[0] + 58, e[1] + 420), 'selected output changes', F_SMALL, GRAY)
text(d1, (e[0] + 58, e[1] + 386), 'seed1 -> seed8', F_HEAD, SEL)

save_outputs(fig1, 'fig1_method_overview')

# Figure 2: simplified single-column evidence figure.
W2, H2 = 900, 760
fig2 = Image.new('RGB', (W2, H2), 'white')
d2 = ImageDraw.Draw(fig2)
pa = (40, 40, 860, 205)
pb = (40, 255, 860, 485)
pc = (40, 535, 860, 720)
for panel in [pa, pb, pc]:
    rounded(d2, panel, radius=20)
arrow(d2, ((pa[0] + pa[2]) // 2, pa[3] + 10), ((pb[0] + pb[2]) // 2, pb[1] - 12), width=4)
arrow(d2, ((pb[0] + pb[2]) // 2, pb[3] + 10), ((pc[0] + pc[2]) // 2, pc[1] - 12), width=4)

# panel a
text(d2, (pa[0] + 28, pa[1] + 22), '(a) Memory crop', F_PANEL)
fig2.paste(memory_crop, (pa[0] + 320, pa[1] + 42))
d2.rectangle((pa[0] + 320, pa[1] + 42, pa[0] + 540, pa[1] + 182), outline=MEM, width=3)

# panel b
text(d2, (pb[0] + 28, pb[1] + 22), '(b) Candidate frame with regular grid', F_PANEL)
frame_big = fit(seed8, (700, 150))
fig2.paste(frame_big, (pb[0] + 60, pb[1] + 56))
d2.rectangle((pb[0] + 60, pb[1] + 56, pb[0] + 760, pb[1] + 206), outline=BORDER, width=1)
fwb, fhb = frame_big.size
fxb, fyb = pb[0] + 60, pb[1] + 56
for i in range(1, cols):
    xx = fxb + int(i * fwb / cols)
    d2.line((xx, fyb, xx, fyb + fhb), fill=(255, 255, 255), width=2)
for j in range(1, rows):
    yy = fyb + int(j * fhb / rows)
    d2.line((fxb, yy, fxb + fwb, yy), fill=(255, 255, 255), width=2)
hbx1 = fxb + int(cell[0] * fwb / cols)
hby1 = fyb + int(cell[1] * fhb / rows)
hbx2 = fxb + int((cell[0] + 1) * fwb / cols)
hby2 = fyb + int((cell[1] + 1) * fhb / rows)
d2.rectangle((hbx1, hby1, hbx2, hby2), outline=SEL, width=4)
text(d2, (pb[0] + 60, pb[1] + 214), 'Regular grid patches', F_SMALL)

# panel c
text(d2, (pc[0] + 28, pc[1] + 22), '(c) Best-matching patch', F_PANEL)
fig2.paste(best_patch, (pc[0] + 72, pc[1] + 36))
d2.rectangle((pc[0] + 72, pc[1] + 36, pc[0] + 272, pc[1] + 166), outline=SEL, width=3)
rounded(d2, (pc[0] + 370, pc[1] + 54, pc[0] + 760, pc[1] + 106), outline=BORDER, fill=LIGHT, width=1, radius=14)
centered(d2, ((pc[0] + 565), pc[1] + 80), 'Feature encoder', F_SMALL)
rounded(d2, (pc[0] + 370, pc[1] + 122, pc[0] + 760, pc[1] + 174), outline=BORDER, fill=LIGHT, width=1, radius=14)
centered(d2, ((pc[0] + 565), pc[1] + 148), 'Cosine similarity', F_SMALL)
arrow(d2, (pc[0] + 286, pc[1] + 100), (pc[0] + 352, pc[1] + 100), color=ARROW, width=4)
text(d2, (pc[0] + 72, pc[1] + 182), 'Best-matching patch', F_SMALL, SEL)

save_outputs(fig2, 'fig2_patch_matching_evidence')
print('Created paper-style figures in', FIGDIR)
