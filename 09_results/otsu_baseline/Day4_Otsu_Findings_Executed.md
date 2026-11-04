# M18K V2: Otsu Baseline and Ablation (small sample)

- Test images: 10 randomly sampled images (seed 42) from the held-out split.
- Methods: classical grayscale/Gaussian/Otsu/morphology/connected-components baseline,
  ablations removing blur or morphology, and existing WB-only YOLOv8n-seg checkpoint.
- All methods evaluated on the **same images** against the **WB COCO ground-truth foreground union**.
- Otsu implemented from scratch; OpenCV verification: 10/10 exact binary matches;
  minimum pixel agreement 1.00000.

| Method | Mean union IoU | Mean union Dice | Count MAE | Mean runtime (ms/image) |
|---|---:|---:|---:|---:|
| Otsu_full | 0.8662 | 0.9269 | 121.20 | 19.3 |
| Otsu_no_blur | 0.8709 | 0.9296 | 122.10 | 16.5 |
| Otsu_no_morph | 0.8648 | 0.9260 | 122.50 | 17.4 |
| YOLO_WB_only | 0.9201 | 0.9583 | 7.30 | 2797.8 |

**Interpretation:** These are foreground-union IoU and Dice scores, **not instance mask mAP**.
For the classical method, connected components approximate object counts and can merge adjacent mushrooms.
The sample is small, and some M18K V2 annotations may contain anomalies.
YOLO and classical runtimes use different devices if CUDA is available, so speed is descriptive.
The reported process RSS is **not** an isolated per-method peak memory measurement.

Saved results: /content/M18K_Otsu_Comparison_Results.zip
