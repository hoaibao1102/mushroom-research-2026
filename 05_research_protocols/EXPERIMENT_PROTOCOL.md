# M18K model experiment protocol — planned protocol and executed status

## Day 2 (executed, 2026-11-02)

- **Models:** pretrained YOLOv8n-seg RGB, two-class (BB + WB) and single-class WB-only.
- **Data:** M18K V2 indexed subset, train=3,596, val=449, held-out test=450 images. WB-only COCO-to-YOLO conversion excludes six degenerate WB train polygons; BB labels excluded.
- **Parameters:** 640 input, 10 epochs, batch 8, AdamW at lr0=0.0001, seed 42, Tesla T4. Specific recorded configs are stored under `08_experiments/configs/` and original notebooks under `08_experiments/notebooks/`.
- **Metrics:** box and instance-mask AP@50, AP@50:95, precision and recall; distinguish BB, WB and overall class-macro averages.
- **Actual result evidence:** `09_results/metrics/Day2_*_Heldout_Test_2026-11-02.json`, user-provided structured console excerpts in `12_reproducibility/logs/`.

This was a short reproduction of the *YOLOv8 segmentation workflow on M18K V2*, not an exact re-execution of the published paper (different original subset/split/metric and possibly augmentation settings). The saved WB-only training notebook's old test cell points at a two-class YAML; the corrected separate WB-only evaluation is recorded independently.

## Day 3 (executed sampled analysis, 2026-11-03)

- **Area:** 30 deterministically sampled test images; WB-only model inference at imgsz=640, conf=0.25, NMS IoU=0.7, `max_det=1000`, original-size masks. One-to-one greedy pairing at mask IoU>=0.50, area in px². Report MAE and relative errors **for matched instances only**, with unmatched totals separately.
- **Qualitative:** 12 chosen dense/sparse/heuristically difficult test images; WB-only segmentation output and error review. Screening dHash matches and apparent annotation issues require separate verification; do not infer formal leakage from dHash alone.

## Unfinished governance and future extensions

- Source/reuse license and official dataset selection remain unrecorded; scene-level independent split verification is outstanding. Original protocol was drafted before these model experiments; execution does not itself clear formal project gates.
- Future controlled studies could consider longer schedules, 1280 resolution, external validation and calibrated RGB-D, but **none were executed here**. Depth-based physical area and 3D pose are outside the completed V1 results.
