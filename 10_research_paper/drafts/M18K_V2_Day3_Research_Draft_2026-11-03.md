# Reproducing YOLOv8-Based Mushroom Detection and Instance Segmentation on M18K V2

**Research paper draft — updated November 3, 2026**  
*Working draft. Only the reported experiments were performed; flagged data-integrity questions remain open.*

## Abstract

This study reproduces a YOLOv8-based mushroom detection and instance segmentation workflow based on the M18K study of Zakeri et al. (2025), using the expanded M18K V2 image release. Two YOLOv8n-seg models were trained for ten epochs: a two-class Baby Bella (BB)/White Button (WB) model and a WB-only model. The locally indexed dataset contained 4,495 RGB images and 700,589 original object annotations, of which approximately 99.88% belonged to WB. On the 450-image held-out test split, the two-class model attained overall segmentation mAP@50 of 0.4995 and mAP@50:95 of 0.3963; its WB mask AP@50 was approximately 0.989, while BB mask AP@50 was 0.0095. The WB-only model achieved mask AP@50 of 0.9906 and AP@50:95 of 0.7974 over 70,192 WB test annotations. In an additional 30-image measurement study, 4,900 predicted and ground-truth masks were matched with mean area absolute error of 207.4 px² and mean relative area error of 8.80%. A qualitative audit of 12 selected scenes found broadly aligned instance masks but also unresolved annotation and dataset-similarity questions. These results establish a working reproduction of the model training and evaluation procedure on M18K V2, rather than an exact numerical reproduction of the original dataset benchmark.

**Keywords:** M18K V2; YOLOv8n-seg; mushroom detection; instance segmentation; mask area; reproduction.

## 1. Introduction

Reliable detection and segmentation of cultivated mushrooms may support automated counting, size measurement and robotic harvesting. Dense growing beds present substantial challenges because many mushroom caps overlap or touch, and objects can be partially cropped at image boundaries.

Zakeri et al. [1] introduced M18K for mushroom detection, instance segmentation, pose estimation and growth monitoring. The present reproduction concentrates on the RGB-based detection and instance segmentation tasks using YOLOv8n-seg on the available expanded V2 dataset. Our objectives are to establish a documented experimental baseline, assess the dominant WB category and the rare BB category separately, and evaluate projected image area extracted from predicted instance masks. Depth-based physical area, 3D pose estimation and growth prediction are outside this study's scope.

## 2. Data and preparation

The extracted and COCO-indexed M18K V2 data used here comprised 3,596 training, 449 validation and 450 test images (4,495 in total). The annotations contained 699,731 WB instances and 858 BB instances (700,589 in total). The original COCO category mapping was converted into the two-class YOLO configuration (`BB=0`, `WB=1`). A separate WB-only configuration mapped original WB annotations to YOLO class 0 and omitted BB target annotations while retaining the image splits.

| Split | Images | BB instances | WB instances | Total instances |
|---|---:|---:|---:|---:|
| Train | 3,596 | 686 | 558,859 | 559,545 |
| Validation | 449 | 75 | 70,680 | 70,755 |
| Test | 450 | 97 | 70,192 | 70,289 |
| Total | 4,495 | 858 | 699,731 | 700,589 |

The WB-only converter discarded six zero-area/degenerate polygons from training and retained 699,725 valid WB polygons across splits. The dataset inventory used in this work does not reconcile the separate public V2 documentation figure of 4,652 images, and a full scene-level train/test split audit is not complete. Potential annotation anomalies discussed below also require inspection of the source COCO polygons.

## 3. Models and evaluation

Both experiments used pretrained YOLOv8n-seg at image size 640, batch size 8, AdamW with initial learning rate 1e-4, cosine learning-rate scheduling, seed 42 and 10 training epochs. Experiments ran on a Google Colab NVIDIA Tesla T4. The two-class baseline required 1.569 hours, and WB-only training required 1.396 hours. Training settings were similar but not exhaustively identical in every augmentation default; the comparison is therefore descriptive rather than a controlled ablation.

The selected checkpoints were evaluated using the predefined 450-image test split. We report Ultralytics bounding-box and segmentation AP@50 and AP@50:95, where the latter averages over multiple IoU thresholds. Precision, recall and approximate inference time are also recorded. The two-class test uses both BB and WB ground-truth labels, whereas the WB-only test uses WB-only labels.

## 4. Test results

### 4.1 Two-class model (BB + WB)

| Category | Box AP@50 | Box AP@50:95 | Mask AP@50 | Mask AP@50:95 |
|---|---:|---:|---:|---:|
| BB | 0.0213 | — | 0.0095 | 0.0057 |
| WB | 0.9920 | 0.8490 | 0.9890 | 0.7870 |
| **Overall class-mean** | **0.5066** | **0.4313** | **0.4995** | **0.3963** |

The two-class model performed well for the dominant WB class but very poorly for BB. This is compatible with the pronounced class imbalance (WB approximately 99.88% of annotations), although a causal explanation would require a separately controlled experiment. Overall mAP is the mean across classes rather than an instance-frequency-weighted average, explaining why low BB performance strongly depresses the aggregate score.

### 4.2 WB-only model

| Metric | Held-out test result |
|---|---:|
| Test images / WB GT instances | 450 / 70,192 |
| Box AP@50 | 0.9921 |
| Box AP@50:95 | 0.8399 |
| Mask AP@50 | **0.9906** |
| Mask AP@50:95 | **0.7974** |
| Mask precision | 0.9756 |
| Mask recall | 0.9631 |

The WB-only model showed strong single-class segmentation. The original test log reported 8.3 ms model inference time per image on Tesla T4, not including preprocessing, postprocessing or data transfer. Compared with the two-class model's WB-specific results, mask AP@50:95 was modestly higher; however, model data-label configurations and some training settings differed, so the change is not a controlled estimate of a class-removal benefit.

## 5. Qualitative WB-only predictions

Twelve test images were deliberately selected for visual review: four with high GT object counts, four with low nonzero counts, and four candidates flagged as difficult by bounding-box size/overlap heuristics. They are not a random or representative subsample. Prediction, COCO ground-truth and RGB panels were reviewed side-by-side.

The 12 scenes contained 1,303 GT masks and 1,355 predicted masks. One-to-one greedy matching at mask IoU ≥ 0.50 produced 1,261 matched pairs, with 42 GT masks and 94 predictions unmatched. Ten scenes had at least one matched pair with IoU below 0.75. Three scenes had identical predicted and GT counts, but none achieved zero unmatched instances, demonstrating why count agreement alone cannot establish segmentation correctness.

Qualitatively, the predicted masks often followed the locations and boundaries of mushroom caps in both densely populated scenes and more sparsely populated scenes. Discrepancies were most evident around small mushrooms, touching caps and frame edges. Nevertheless, these figures do not identify unmatched objects individually, so unmatched predictions cannot be confidently labeled as true false positives or incomplete annotations without inspection of the source image and COCO polygons.

Two images are of particular concern. In test image `004252.png`, a visible person/floor region appears covered by large WB GT mask overlays; predictions cover similar areas. In image `004472.png`, a GT overlay appears to extend into a non-mushroom foreground region at the image edge. These are *suspected visual annotation anomalies*, not confirmed COCO errors, and raw polygon review remains necessary.

**Figure 1.** Dense WB scene: RGB, GT and predictions for `004078.png` (`figures/khang/img_32_004078.png`).

**Figure 2.** Sparse WB scene: RGB, GT and predictions for `004484.png` (`figures/khang/img_438_004484.png`).

**Figure 3.** Suspected annotation anomaly for `004252.png`; source annotation confirmation pending (`figures/khang/img_206_004252.png`).

## 6. Mask area measurement

Projected mask area was measured for each instance at original image resolution as the number of foreground pixels: `A_px² = Σ_{x,y} 1[M(x,y) > 0]`. No depth-map scaling or physical calibration was applied; all reported measurements are in pixels squared (px²), not mm².

The implementation had previously passed ten synthetic area tests and matched COCO's rasterization-based area for three real annotations. The present evaluation applied the same function to WB-only model predictions from 30 reproducibly sampled test images (seed 42). Ground-truth WB polygons were rasterized using `pycocotools`. Inference used `imgsz=640`, confidence 0.25, NMS IoU 0.7, `max_det=1000` and full-resolution (`retina_masks=True`) masks. Predictions and GT were greedily matched at mask IoU ≥ 0.50; area errors are computed only on the 4,900 matched instances.

| Area metric (30 sampled images) | Result |
|---|---:|
| GT annotations | 4,970 |
| Predicted instances | 5,146 |
| Matched instances | 4,900 |
| Unmatched GT / predictions | 70 / 246 |
| Matching coverage of GT | 98.59% |
| Mean absolute area error (MAE) | **207.4 px²** |
| Mean relative absolute error | **8.80%** |
| Median relative absolute error | **7.34%** |
| Mean matched-mask IoU | **0.890** |

Approximately 85.6% of matched predicted masks had greater area than their GT partner, and total predicted area was 1.045 times the GT area across matched pairs. Relative error was substantially higher for small (15.2%) than large (3.4%) GT objects in a three-way size grouping, while absolute error remained near 200 px² across groups. The observed mean errors exclude unmatched GT/predicted objects, and instance areas summed per image may double-count overlapping regions.

These results are **a 30-image area-analysis sample**, not a full-test benchmark or physical mushroom size measurement. Annotation rasterization convention, polygon boundary differences, confidence thresholds and matching decisions affect the reported errors.

**Figure 4.** GT/prediction overlays and area labels from the largest sampled per-image MAE case (`figures/area/worst_mae_327_004373.png`).

**Figure 5.** Example with many unmatched objects (`figures/area/most_unmatched_216_004262.png`).

## 7. Discussion and comparison with the original publication

The M18K paper of Zakeri et al. [1] reports YOLOv8-N instance segmentation AP values of 0.712 at 640 and 0.846 at 1280. Our experiment uses expanded M18K V2, different image membership/class frequencies and an independent training protocol. The metric named AP in the original paper has not been confirmed to be equivalent to the Ultralytics mask AP@50:95 in our runs. Thus neither our overall two-class nor WB-only result should be described as outperforming or underperforming the published numbers on an equivalent benchmark.

Our supported conclusion is procedural: both training and independent held-out test evaluation completed successfully, and WB-focused instance masks can support approximate projected-area measurement. The two-class run revealed a severe BB limitation, while qualitative examination identified boundary challenges and unresolved annotation-quality questions.

The dHash spot-check of 12 selected test images against available training images returned five nearest pairs with identical 64-bit perceptual hashes. A dHash collision or strong visual similarity is **not proof of an identical file or scene leakage**. The corresponding raw train/test images were not provided for exact-byte or scene-level inspection during this review. Therefore, split independence remains **NOT VERIFIED** at the scene level, and generalization claims must remain cautious.

## 8. Limitations

The experiments used only 10 epochs and a single resolution. WB dominates the annotation count while BB is scarce. The two class configurations were not evaluated as a controlled ablation using identical target-label protocols. The 12-image qualitative selection and 30-image area sample are limited and differ in maximum detection settings (`max_det=3000` vs `1000`). Visual inspection flagged possible non-mushroom GT regions, but verification against raw COCO annotations is pending. The dHash screening is not a full duplicate- or scene-leakage audit. Mask-area results rely on matching, exclude unmatched objects from MAE and are restricted to projected image-area units. No depth-based mm² measurement, 3D mushroom surface area, growth monitoring or mushroom-quality classification was performed.

## 9. Conclusion

We successfully implemented and evaluated two YOLOv8n-seg mushroom detection/segmentation experiments on M18K V2. On the held-out test split, the WB-only model achieved mask AP@50 of 0.9906 and AP@50:95 of 0.7974; the two-class model performed strongly on WB but poorly on BB. In an additional 30-image study, WB predicted-mask area differed from matched COCO mask area by a mean of 207.4 px² (8.80% mean relative absolute error), with greater relative error for smaller instances. These are evidence-backed reproduction and measurement results, not a claim of superior performance to the published M18K benchmark. The remaining work is targeted verification of suspected annotation anomalies and potential train/test near-duplicates, rather than further training.

## References

[1] Zakeri, A., Fawakherji, M., Kang, J., Koirala, B., Balan, V., Zhu, W., Benhaddou, D., and Merchant, F. A. (2025). *M18K: A Multi-Purpose Real-World Dataset for Mushroom Detection, 3D Pose Estimation, and Growth Monitoring*. Computers, 14(5), 199. https://doi.org/10.3390/computers14050199

[2] Ultralytics. *YOLOv8 Documentation*. https://docs.ultralytics.com/models/yolov8/

### Reproducibility evidence

- Two-class best checkpoint and held-out test log: `model_runs/v2_yolov8n_seg_640_e10_s42/weights/best.pt`; `model_runs/heldout_test/`.
- WB-only best checkpoint: shared Drive file ID `1Q5iq_-j-RwOTkyiiXyTOc80Cf_xwk7K-`; held-out evaluation log `model_runs/khang_wb_heldout_test/test_metrics.json`.
- WB-only checkpoint SHA-256 recorded identically in both analysis submissions: `93d993ec6b48c1fca9d59178afe11377ef20afa3ed0c304841e4d6b36d447961`.
- Khang's outputs: `Khang_error_observations_reviewed.csv` and `Khang_visual_review_2026-11-03.md`.
- Thịnh's outputs: `area_evaluation/mask_area_matches.csv`, `mask_area_summary.json`, `area_findings.md` and four example overlays.
