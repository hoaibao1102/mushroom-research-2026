
# Day 5 — Dense Mushroom Segmentation & Counting

## 1. Scope

- Model: existing WB-only YOLOv8n-seg checkpoint.
- Checkpoint: `best.pt`
- Test sample: 8 fixed M18K V2 test images.
- Retraining: No.
- Full 450-image evaluation: Not rerun.

## 2. Failure hypothesis

The targeted hypothesis is duplicate or highly overlapping detections
that can cause over-counting in crowded scenes.

This is a hypothesis to test; it must be checked against the figures.

## 3. One targeted change

NMS IoU threshold:

- Baseline: 0.7
- Modified: 0.5

All other inference settings remain the same:

- imgsz = 640
- conf = 0.25
- class = WB (0)
- same checkpoint and same images

Lower NMS IoU suppresses overlapping boxes more aggressively. It may
reduce duplicates but may also suppress nearby real mushrooms.

## 4. Counting results

- Baseline counting MAE: **3.3750**
- Modified counting MAE: **1.8750**
- Difference (modified - baseline): **-1.5000**
- Images improved: 6
- Images worsened: 2
- Images unchanged: 0

MAE = mean(abs(predicted instance count - COCO GT instance count)).

**Outcome:** MAE improved on selected sample.

## 5. Matched-instance diagnostics

The CSV includes one-to-one matching at IoU >= 0.5.
Mask IoU is used when valid COCO segmentation masks are available;
otherwise bbox IoU is used and identified as a fallback.

Unmatched predictions are only FP candidates. They are not automatically
confirmed duplicates. Unmatched GT masks are only FN candidates.

## 6. Limitations

- Only 8 selected dense/crowded candidates were tested.
- Selection uses COCO instance count and bbox overlap heuristics.
- Bbox overlap does not prove physical touching or occlusion.
- The result does not establish general improvement on the full test set.
- No model retraining or full-test mAP evaluation was performed.
