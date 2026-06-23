# Gate 3.2 Redraw Figures Report

## Diagnosis

PASS_FIGURES_REDRAWN_NO_OVERLAP_WITHIN_4P

## Figure 1 fixes

- Replaced the compressed five-panels-in-one-row layout with a two-row paper block diagram.
- Top row now uses `(a) Setup`, `(b) Write/store`, `(c) Generate candidates`.
- Bottom row now uses `(d) Read by patch matching`, `(e) Rerank candidates`.
- Removed the panel-title collision between the old `(b)` and `(c)` regions.
- Restored visible right margin in panel `(e)` so the seed labels are not clipped.
- Kept the same technical story: frozen MatrixGame-2, external memory, regular-grid patches, candidate reranking, and seed1 -> seed8.

## Figure 2 fixes

- Replaced the crowded multi-panel layout with a simplified single-column figure.
- Kept only three stages: `(a) Memory crop`, `(b) Candidate frame with regular grid`, `(c) Best-matching patch`.
- Removed the extra candidate-comparison subpanel because Figure 1 and Table 1 already cover seed1 vs seed8.
- Removed the long no-segmentation note and formula from the figure body; the no-segmentation statement now lives in the caption.
- Increased readability by using larger labels and wider panel spacing.

## PDF page count

- 3 pages
- `page_count.txt`: `PASS_PAGE_LIMIT`

## Remaining issues

- No major overlap or clipping remains in the rebuilt PDF.
- Figure 2 is intentionally minimal and could be stylized further in a later camera-ready polish pass, but it is readable in the current single-column form.

## Files changed

- `paper/cvpr2026_ap0006_memory_modules/scripts/make_paper_figures.py`
- `paper/cvpr2026_ap0006_memory_modules/figures/fig1_method_overview.png`
- `paper/cvpr2026_ap0006_memory_modules/figures/fig1_method_overview.pdf`
- `paper/cvpr2026_ap0006_memory_modules/figures/fig2_patch_matching_evidence.png`
- `paper/cvpr2026_ap0006_memory_modules/figures/fig2_patch_matching_evidence.pdf`
- `paper/cvpr2026_ap0006_memory_modules/main.tex`
- `paper/cvpr2026_ap0006_memory_modules/main.pdf`
- `paper/cvpr2026_ap0006_memory_modules/page_count.txt`
- `paper/cvpr2026_ap0006_memory_modules/gate3_2_redraw_figures_report.md`
