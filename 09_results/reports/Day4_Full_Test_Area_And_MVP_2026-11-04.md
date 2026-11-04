# Day 4 — Full-test area, inference MVP, and classical processing experiment (2026-11-04)

## Full-test predicted WB mask area

Thịnh's submitted results cover **all 450** M18K V2 test images: **70,192 WB GT objects**, **72,182 predicted objects**, **68,794 one-to-one IoU>=0.50 matches**, **3,388 unmatched predictions** and **1,398 unmatched GT**. On the **matched** masks only, mean absolute area error was **211.4143 px²**, mean relative absolute error **8.8147%**, median relative error **7.3116%** and mean mask IoU **0.8904**. Match coverage was **98.0083%** of GT. Small/middle/large GT-area terciles had mean relative errors **15.40% / 7.89% / 3.53%** respectively. The full submitted JSON, CSV.gz, code and four overlays are in `09_results/area_evaluation/day4_full_test/`.

These are *projected image mask areas (px²)*, not physical cap areas (mm²). False/missed objects are accounted for separately, and GT polygon quality can affect these results.

## Inference MVP

The executed WB-only Colab demo sampled **10 of 450** test RGB images (seed 42) and produced **1,551 predicted WB instances**, original-size masks, overlay figures, per-instance areas, image counts, CSV output and a ZIP. Its mean predicted per-instance area was **3,520.11 px²**. This is a demo, not a separate accuracy benchmark. Source: `08_experiments/notebooks/Day4_WB_Only_Final_Inference_Executed.ipynb`.

## Classical baseline, algorithm verification, ablations

A 10-image same-data comparison used a scratch implementation of **Otsu thresholding** (verified against OpenCV on **10/10** images), grayscale/Gaussian preprocessing, morphology and connected-component counting. The baseline obtained union IoU **0.8662**, Dice **0.9269**, count MAE **121.2**; WB-only YOLO obtained union IoU **0.9201**, Dice **0.9583**, count MAE **7.3**. Removing Gaussian blur improved Otsu union IoU to **0.8709**; removing morphology changed it to **0.8648**. These foreground-union scores differ from per-instance mask AP; this is a small illustrative experiment, not a full-test comparison. Source: `09_results/otsu_baseline/`.

## Dataset QC (submitted; NOT independently cleared)

The Day 4 dataset-QC submission contains five hash comparisons and two annotation-review entries. However, **the five pair filenames do not match the original five Day 3 dHash candidate pairs**, and one submitted test hash is `FILE_NOT_FOUND`. Hash inequality rules out byte-identical files only for successfully read corresponding pairs; it cannot rule out temporal/scene overlap. Suspicious WB masks on `004252.png` and `004472.png` remain inconclusive; the submitted `VERIFIED_GOOD` labels are not treated as independent verification. See `09_results/dataset_qc/day4_submitted/` and `09_results/reports/Day4_QC_Interpretation_2026-11-04.md`.

## Course-project deliverables

The **English course report** was drafted in Word and PDF under `10_research_paper/drafts/`. Requirements for 4 techniques across 3 lessons and other report items still need the actual syllabus mapping and final editorial review. The executed Colab notebook is a working inference MVP; the **short demo video, final presentation, and final submission checks remain pending**. No additional model training was performed on Day 4.
