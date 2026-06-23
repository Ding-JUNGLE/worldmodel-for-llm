# Gate 3.1 Figure Layout Fix Report

## Diagnosis

PASS_FIGURE_LAYOUT_FIXED_WITHIN_4P

## Fig1 fixes

- Increased overall canvas height to create more vertical breathing room below the method panels.
- Widened panel `(e)` and shifted its labels leftward.
- Split the right-side result labels into two lines (`No memory / seed1`, `With memory / seed8`) to avoid edge crowding.
- Adjusted the reranking arrow placement in panel `(e)` for cleaner spacing.
- Reduced the bottom label font in panel `(d)` and increased horizontal separation between the two columns of labels.
- Moved the two bottom note boxes lower so the panel `(d)` labels no longer feel pressed against them.

## Fig2 fixes

- Moved `stored local visual cue` upward inside panel `(a)`.
- Increased panel `(c)` bottom padding.
- Enlarged the formula font slightly and moved the formula box upward.
- Moved the `No object segmentation...` note upward and split it across two lines for safer margins.
- Kept all text inside panel boundaries with visibly clearer padding.

## PDF check

- page count: 3
- overlap found: no figure-text overlap found in the rebuilt PDF
- remaining tight areas: no major obstruction; only normal compact paper-scale text remains in the two figures

## Files changed

- `paper/cvpr2026_ap0006_memory_modules/scripts/make_paper_figures.py`
- `paper/cvpr2026_ap0006_memory_modules/figures/fig1_method_overview.png`
- `paper/cvpr2026_ap0006_memory_modules/figures/fig1_method_overview.pdf`
- `paper/cvpr2026_ap0006_memory_modules/figures/fig2_patch_matching_evidence.png`
- `paper/cvpr2026_ap0006_memory_modules/figures/fig2_patch_matching_evidence.pdf`
- `paper/cvpr2026_ap0006_memory_modules/main.pdf`
- `paper/cvpr2026_ap0006_memory_modules/page_count.txt`
- `paper/cvpr2026_ap0006_memory_modules/gate3_1_figure_layout_fix_report.md`

## Remaining tasks

- Optional future polish could simplify tiny labels further if a camera-ready pass is needed.
- Stage A remains a teammate placeholder and was intentionally not changed in this pass.
