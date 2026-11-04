# Day 4 - Predicted mask-area evaluation (all M18K V2 test images)

Evaluates the existing WB-only YOLOv8n-seg checkpoint: how close is the area (px²) of each predicted instance mask to the area of
the matching COCO ground-truth WB polygon mask. Inference only; no training, no EDA. Area is in **px²**, not mm².

## References (not copied here)
- Checkpoint: https://drive.google.com/file/d/1Q5iq_-j-RwOTkyiiXyTOc80Cf_xwk7K-/view  (sha256 `93d993ec6b48c1fca9d59178afe11377ef20afa3ed0c304841e4d6b36d447961`)
- Dataset: M18K V2, split `test` (`<data_root>/test/rgb/` and `annotations_coco.json`); WB-only labels were built earlier (`wb_yolo_labels.zip`).

## Run (Colab)
```python
from google.colab import drive; drive.mount("/content/drive")
!pip -q install ultralytics gdown pycocotools ijson
import gdown; gdown.download(id="1Q5iq_-j-RwOTkyiiXyTOc80Cf_xwk7K-", output="/content/wb_yolov8n_seg.pt")
!python area_evaluation.py --data-root <.../M18KV2> --checkpoint /content/wb_yolov8n_seg.pt
```
Default: all 450 test images (`--n 30` etc. for a random subset, seed 42). Outputs are written next to the script;
an interrupted run resumes from `--work-dir` (default `/content/day4_work`).

## Settings
- imgsz 640 (checkpoint train_args), conf 0.25, NMS IoU 0.7, max_det 1000, retina_masks=True (masks at original resolution); device used: cpu.
- Matching: one-to-one greedy by descending mask IoU, IoU >= 0.5; masks at original resolution; GT = pycocotools-rasterised COCO polygons (non-crowd, non-zero area).
- Area: A_px2 = sum(mask > 0) per instance; unit px2 (not mm2); relative_error_pct = 100*|pred-GT|/GT.

## Files
`area_metrics.json` (summary, size bins, comparison with the 30-image run), `area_per_image.csv` (one row per image, `in_previous_30` flags the earlier subset),
`area_matches.csv.gz` (all matched pairs; optional, lets the size analysis and medians be recomputed), `figures/`, `area_findings.md`.
