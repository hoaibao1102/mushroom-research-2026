# Day 5 research update — 5 November 2026

Today the team explored two follow-up questions from the M18K V2 baseline: whether inference settings can improve counting in crowded scenes, and whether the available depth maps are calibrated well enough for physical size measurement. We also got the WB-only Gradio demo running in Colab.

## 1. Dense-scene counting: lower NMS IoU

Khang compared the existing WB-only YOLOv8n-seg checkpoint at NMS IoU 0.70 and 0.50. The checkpoint, images, confidence threshold (0.25), image size (640), class filter and maximum detections were held constant. Only the NMS IoU threshold changed.

| Measure | NMS 0.70 | NMS 0.50 |
|---|---:|---:|
| Ground-truth instances | 1,713 | 1,713 |
| Predicted instances | 1,736 | 1,714 |
| Counting MAE (per image) | 3.375 | **1.875** |
| Matched instances (mask IoU ≥ 0.50) | 1,674 | 1,673 |
| Unmatched prediction candidates | 62 | **41** |
| Unmatched ground-truth candidates | 39 | 40 |

The modified setting reduced the eight-image counting MAE by 1.50 mushrooms per image (44.4%). Six images improved and two worsened. The result is promising, but the eight images were selected as dense/crowded candidates using instance count and bounding-box overlap. The selection file still marks visual confirmation as pending. Unmatched predictions are not automatically confirmed duplicates, and unmatched ground-truth instances are not automatically confirmed misses. This is a small exploratory result, not evidence of improved performance across the full 450-image test set. No retraining or full-test mAP evaluation was performed.

The source script, settings, selected-image list, comparison CSV and three figures are in `09_results/dense_counting/day5_nms/`.

## 2. RGB-D feasibility for physical area

Thịnh inspected 30 test images and 4,970 WB masks, and checked the depth-file types across all 450 test images. The mean valid-depth fraction inside masks was 93.1%, but 301 masks had less than 50% valid depth and 132 had no valid depth. The test depth folder contained 340 `float32` files and 110 `uint16` files.

The supplied export did not establish the depth scale or camera intrinsics. The alignment checks suggested possible non-zero offsets but were not decisive; alignment remains unverified. The depth values also did not support a reliable unit conversion. Thịnh therefore did not calculate mm². That is the appropriate conclusion: the current area results remain in px² until calibration information and an independent measurement check are available.

Detailed findings, the original Vietnamese report, scripts, CSV/JSON outputs and figures are in `09_results/rgbd_feasibility/day5/`.

## 3. Interactive demo

The WB-only Gradio app was launched successfully in the team's Colab environment. It can load a random image from the M18K V2 test RGB folder or accept an uploaded RGB image, run the existing checkpoint, display masks and counts, and export image/CSV outputs. This confirms the app is usable as a live demo; it is not a new benchmark result. The checkpoint remains external in Google Drive.

## 4. What the results mean

The NMS experiment gives us a specific improvement worth validating on all 450 test images. It should not be described as a general improvement until that larger evaluation is done. The RGB-D work identifies the information needed before physical measurement can be attempted: verified depth units, camera intrinsics, depth-to-RGB alignment and an independent scale check. Until then, px² is the only defensible area unit.

The course report and presentation files in `10_research_paper/submission/` were prepared earlier on 5 November, before these Day 5 submissions arrived. They do not yet include the NMS or RGB-D findings.
