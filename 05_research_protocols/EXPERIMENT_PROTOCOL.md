# Planned M18K model experiment protocol — not executed

## Proposed first benchmark

- **Model:** pretrained YOLOv8n-seg, RGB input; simple reproducible pilot before larger architectures.
- **Dataset:** M18K V2 using the supplied 3,596 / 449 / 450 train/val/test images, after QC review.
- **Primary metrics:** segmentation mAP@50:95 and per-class AP (with clear implementation/IoU definition), plus recall, precision and small-instance performance.
- **Operational checks:** monitor per-class BB rarity, input resolution, loss of multipart masks during COCO→YOLO conversion, training speed and resource limits.
- **Model selection:** validation only, evaluate held-out test after settings frozen.
- **Logging:** fixed seeds, dataset and split manifest, input resolution, batches, epochs, optimizer and learning rate, library/CUDA versions, Git commit, checkpoint hash and raw predictions where feasible.

## Planned follow-ups

1. Increase resolution to 1280 with comparable training budget and documented memory limitations.
2. Compare RGB-only and RGB-D/depth-assisted segmentation under matched datasets, seeds and computational limits.
3. Inspect the available M18K 3D dataset and calibrated depth information before attempting pose estimation; use orientation error metrics and held-out labels.
4. Compare to the **original paper only if the dataset release, split and metric definitions are aligned**. Published AP is not a substitute for our test AP.

## Missing prerequisites

Team approval/licensing as needed; BB label review; scene-level leakage audit; frozen protocol and runtime budget. The uploaded notebook intentionally had `RUN_TRAIN=False`. There is **no V2 accuracy, checkpoint or experiment run** to register yet.
