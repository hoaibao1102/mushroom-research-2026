
# WB-Only YOLOv8n-seg Error Analysis Findings

## 1. Scope

- Checkpoint: `best.pt`
- Dataset: M18K V2 supplied test split.
- Inference performed only on 12 selected images.
- No retraining was performed.
- Full 450-image test evaluation was not rerun.
- WB class mapping: class ID 0 = WB.

## 2. Existing Test Metrics

- Test images: 450
- WB instances: 70,192
- Mask AP@50: 0.990639
- Mask AP@50:95: 0.797363
- Mask Recall: 0.963078

These values are existing metrics supplied for this analysis.
They were not recalculated in this notebook.

## 3. Selected Examples

- 4 dense images: selected by highest GT instance counts.
- 4 sparse images: selected by lowest non-zero GT instance counts.
- 4 difficult candidates: selected using bbox area and bbox overlap heuristics.

The difficult candidates require visual confirmation.
BBox overlap alone does not prove physical occlusion.

## 4. Automated Sample Analysis

Mask matching threshold: IoU >= 0.50.

- Unmatched GT masks (possible misses): 42
- Unmatched prediction masks (possible false positives or duplicates): 94
- Images with boundary-review candidates: 0
- Images without count mismatch at the matching threshold: 0

These are sample-level diagnostics for 12 images.
They are not the official mAP calculation.

All rows in `error_observations.csv` remain marked PENDING
until a person visually reviews the corresponding PNG.

## 5. Similarity Spot-check

Status: `SPOT_CHECKED_DHASH_NOT_FULL_LEAKAGE_CLEARANCE`.

The dHash check is a preliminary near-duplicate screen
for selected test images against available train images.
It is not a full train/test leakage audit and cannot prove
that the complete dataset is leakage-free.

## 6. Interpretation

The existing held-out metrics indicate strong aggregate WB
segmentation performance, particularly at IoU 0.50.

The lower AP@50:95 compared with AP@50 makes stricter mask
overlap and boundary alignment useful areas for qualitative
inspection.

The 12 selected images are a small heuristic-based sample.
They should not be treated as a statistically representative
estimate of all test scenes.

No two-class baseline comparison is included.

## 7. Completion Status

PARTIAL until the 12 comparison figures have been visually
reviewed and the manual-review fields in error_observations.csv
have been completed.
