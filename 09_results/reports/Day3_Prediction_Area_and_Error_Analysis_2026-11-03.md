# Day 3 — Predicted-mask area and qualitative error analysis

**Date:** 2026-11-03  
**Models:** Reuse the trained WB-only YOLOv8n-seg checkpoint; **no retraining**.

## Area analysis (Thịnh; random 30-image sample)

- Ground-truth WB masks: **4,970**; predicted masks: **5,146**.
- One-to-one greedy matching of original-resolution masks using IoU >= 0.50: **4,900 matched**, **70 unmatched GT**, **246 unmatched predictions**.
- Ground-truth matching coverage: **98.59%** (NOT recall for the full 450-image benchmark).
- Mean absolute predicted-versus-GT area error: **207.4 px²** among matched masks.
- Mean relative absolute error: **8.80%**; median: **7.34%**.
- Mean matched mask IoU: **0.890**.
- Matched predicted area sums / GT area sums = **1.045**, indicating an approximately 4.5% overall positive area bias on matched instances.
- Pixel-area only: `A_px² = sum(mask > 0)`; **no mm² calibration or 3D surface area**.
- The 30-image area analysis used fixed `conf=0.25`, NMS IoU `0.7`, `imgsz=640`, `retina_masks=True`, `max_det=1000`. Error metrics exclude unmatched objects, which are reported separately.
- Exact rows and plots: `09_results/area_evaluation/`; 4 examples are curated in `10_research_paper/figures/Day3_Area_*.png`.

## Prediction review (Khang; stratified 12-image selection)

- 12 sample images: 4 dense, 4 sparse, 4 heuristically difficult (not a random test subset).
- WB masks: **1,303 GT**, **1,355 predicted**; matched IoU >= 0.50: **1,261**.
- **42 unmatched GT** and **94 unmatched predictions**; matching results do not by themselves establish real false positives/negatives.
- The original automated notebook summary incorrectly reported zero boundary candidates; the CSV shows **10 of 12 images** have at least one matched mask below 0.75 IoU.
- Visually, most caps are traced well; largest uncertainties involve touching caps, small/partially visible mushrooms and image borders. All 12 original figures were reviewed via the exported panels.
- Full reviewed notes: `09_results/reports/Day3_WB_Qualitative_Review_2026-11-03.md` and `09_results/wb_error_analysis/Khang_error_observations_REVIEWED.csv`; 12 curated figures in `10_research_paper/figures/Day3_WB_Prediction_*.png`.

## Open verification items (do NOT report as confirmed defects)

1. `004252.png` and `004472.png`: apparently inconsistent WB ground-truth overlays, which may reflect annotation errors, renderer behavior or other causes. **Requires raw COCO polygon inspection.**
2. Five train/test pairs have identical 64-bit perceptual dHash in a sample similarity check. **This does not prove exact duplication or leakage**; review paired RGB images, SHA-256 hashes and acquisition/scene groups.
3. Full test-set mask-area error was **not** computed. The Day 3 area score is a sample diagnostic, not a full benchmark.
4. Dataset source/license review, V2 4,652 vs 4,495 discrepancy, complete class-label audit and depth calibration remain unresolved.

## Outcome

The Day 3 analysis produced verified sample-level area-error statistics, quantitative/qualitative prediction examples and a paper-ready evidence base. The milestone is complete at the planned scope, but the verification items above remain open before stronger generalization claims.
