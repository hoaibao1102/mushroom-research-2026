# WB-only YOLOv8n-seg — reviewed qualitative error analysis

**Review date:** 2026-11-03  
**Status:** 12 exported comparison PNGs visually reviewed; original raw annotation audit and train/test similarity clearance **NOT VERIFIED**.  
**Source:** `M18K_V2_Training_WB_Only(1).ipynb` and its submitted `09_results/wb_error_analysis/` folder. Model was **not retrained** or re-evaluated on all 450 images during this review.

## Existing held-out test metrics (from earlier evaluation, not recalculated here)

- WB-only model: YOLOv8n-seg; 450 test images, 70,192 WB GT instances.
- Mask AP@50 = **0.990639**, mask AP@50:95 = **0.797363**, mask recall = **0.963078**.
- The evaluation of 12 selected images below is descriptive. It is *not* a second test-set mAP estimate.

## Sample-level quantitative findings

Khang deliberately chose 4 dense, 4 sparse and 4 heuristic difficult images; the difficult category comes from bbox size/overlap heuristics rather than verified occlusion labels. Using greedy one-to-one matching of original-resolution masks at IoU >= 0.50:

| Quantity (12 selected images) | Result |
|---|---:|
| GT WB masks | 1,303 |
| Predicted WB masks | 1,355 |
| Matched masks | 1,261 |
| Unmatched GT masks | 42 |
| Unmatched predicted masks | 94 |
| Images with a recorded matched-mask IoU below 0.75 | **10 of 12** |
| Images with equal raw GT and predicted counts | **3 of 12** |
| Images with zero unmatched masks | **0 of 12** |

**Correction:** The notebook-generated report erroneously said zero images had boundary-review candidates. Its CSV observations contain the below-0.75-IoU note for **10 of 12 images**. The script counted an `issue_type` marker that was never written. Equal raw image counts do not imply one-to-one matching: `004484.png`, `004472.png`, and `004350.png` still have unmatched masks.

## Visual review of all 12 figures

These are direct observations from the exported **Original / Ground Truth / Prediction** panels. The figures do *not* highlight unmatched masks individually. Thus the labels "missed" and "extra" describe failures of IoU matching, not confirmed false negatives or false positives.

- **004078.png** (222 GT / 221 predicted, 5 unmatched GT / 4 unmatched prediction): Dense bed; predictions visually follow most overlapping caps and approximate the GT coverage. Some small/crowded regions differ; exact 5 unmatched GT and 4 unmatched predictions cannot be individually identified from these three panels.
- **004072.png** (220 GT / 229 predicted, 4 unmatched GT / 13 unmatched prediction): Dense bed; most caps are segmented separately. Prediction overlays appear more numerous around tightly packed small caps and at the crop boundary (13 unmatched predictions); the figures alone cannot establish whether they are false positives, duplicate fragments, or unlabeled true mushrooms.
- **004134.png** (219 GT / 230 predicted, 3 unmatched GT / 14 unmatched prediction): Very dense center/left clusters; predicted masks broadly follow cap positions, with differences in small adjacent cap boundaries and 14 unmatched prediction masks. Individual unmatched objects are not highlighted in the image.
- **004211.png** (219 GT / 222 predicted, 3 unmatched GT / 6 unmatched prediction): Very dense group with large caps near the image edges. Most large and medium caps align visually between GT and prediction; small tightly packed caps show differing coverage, with 3 unmatched GT and 6 unmatched predictions.
- **004252.png** (5 GT / 6 predicted, 0 unmatched GT / 1 unmatched prediction): IMPORTANT ANOMALY: only five WB GT masks, but the GT overlay appears to include large non-mushroom floor/clothing regions near the visible person; the prediction overlay covers similar regions. Raw COCO polygon coordinates/category IDs must be checked before treating this as valid WB segmentation or asserting a model mistake. One unmatched prediction under IoU matching.
- **004484.png** (36 GT / 36 predicted, 1 unmatched GT / 1 unmatched prediction): Sparse scene with many caps cut by top/side borders. GT and predictions have the same raw count (36 each), but matching still leaves one unmatched on each side; exact mask pairing cannot be judged from side-by-side overlays alone.
- **004391.png** (42 GT / 51 predicted, 2 unmatched GT / 11 unmatched prediction): Sparse/clustered scene with many tiny bright spots. Predictions include more separate objects than GT (51 vs 42), especially among small scattered caps; some white spots also remain without green overlays. Whether extra masks represent false positives or omitted labels is unverified.
- **004239.png** (46 GT / 49 predicted, 1 unmatched GT / 4 unmatched prediction): Sparse scene with a narrow column of adjacent caps toward the left. The major cap groups visually align, while smaller caps and partial border objects differ; 1 GT and 4 predicted masks remain unmatched.
- **004324.png** (62 GT / 71 predicted, 6 unmatched GT / 15 unmatched prediction): Heuristic difficult scene with clustered small mushrooms in several groups. Broad group locations agree, but counts differ (62 GT vs 71 predictions) and 6 GT/15 predictions remain unmatched. Boundary separations in touching caps warrant closer inspection.
- **004298.png** (65 GT / 73 predicted, 6 unmatched GT / 14 unmatched prediction): Heuristic difficult scene dominated by small caps and partial mushrooms along the top/bottom edges. Predictions broadly track GT groups but are more numerous (73 vs 65); 6 unmatched GT and 14 unmatched predictions.
- **004472.png** (83 GT / 83 predicted, 7 unmatched GT / 7 unmatched prediction): Heuristic difficult scene with many caps near the image edge and visible tray/frame/floor. A large green GT overlay at bottom-left appears to extend into non-mushroom foreground, warranting raw polygon inspection. Equal raw counts (83/83) conceal 7 unmatched on each side.
- **004350.png** (84 GT / 84 predicted, 4 unmatched GT / 4 unmatched prediction): Heuristic difficult scene with multiple small and touching caps around the top and bottom edges. GT and prediction counts are equal (84/84), but the IoU matching still finds 4 unmatched masks on each side, indicating count agreement is not sufficient for accurate instance correspondence.

## Dataset / annotation caveat requiring attention

- `004252.png` visibly contains a person's lower body and concrete floor. The GT overlay appears to label relatively large non-mushroom regions as WB, and the prediction overlay also covers them. This may reflect a COCO polygon, an overlay/rasterization issue, or something else; the raw source image + polygon coordinates and categories are needed to determine the cause. **Suspected, not verified.**
- `004472.png` has a GT overlay apparently extending into the floor/frame at the bottom-left; likewise merits a raw annotation review.
- The 12-image dHash spot-check lists **five** test/train nearest pairs at Hamming distance zero: test `004078` ↔ train `001896`, `004072` ↔ `002583`, `004134` ↔ `000486`, `004211` ↔ `002085`, and `004252` ↔ `000323`. Matching 64-bit dHashes is **not** proof of duplicate images; no train-image pixel comparison or exact hashes are available in the submitted evidence. Full scene-level split overlap remains **NOT VERIFIED**.

## Overall interpretation

The model's predicted masks visually trace most annotated mushroom caps in both dense and sparse settings, supporting the high existing WB AP@50. Difficult regions include crowded touching caps, small/partially visible mushrooms and image boundaries. However, the apparent label anomalies and train/test similarity candidates limit what can be concluded about independent generalization and annotation reliability. No claim of a confirmed false-positive rate, definitive leakage, or pixel-accurate mask quality follows from this 12-image selection.

## Evidence and reproducibility

- `Khang_error_observations_reviewed.csv`: 12-row visual notes with the raw machine statistics retained.
- `similarity_spotcheck.csv`: original screening results, not definitive duplicate detection.
- `figures/khang/*.png`: all 12 side-by-side exported figures.
- Khang's inference settings: `imgsz=640`, `conf=0.25`, NMS IoU `0.7`, `max_det=3000`, `retina_masks=True`, model class `WB`, mask IoU matching threshold `0.50`.
- Thịnh's separate 30-image area evaluation used `max_det=1000`, also `conf=0.25`, so their sample measurements should not be conflated.
