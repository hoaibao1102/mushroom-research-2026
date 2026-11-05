# Results — Day 1 EDA through Day 5 research follow-up

**Day 1 — EDA**: `reports/M18K_V2_EDA_2026-10-30.md`, `metrics/v2_eda_*.csv`, `visualizations/*.png`. V2: 4,495 indexed images; 700,589 annotations.

**Day 2 — model reproduction on V2**: `reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md`, two test JSON files under `metrics/Day2_*`, and checked WB data-conversion records under `metrics/wb_*`. Includes 450-image held-out test results for BB+WB and WB-only. Raw logs are recorded as structured user-supplied excerpts under `12_reproducibility/logs/`.

**Day 3 — additional analysis**: `reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md`, 30-image numeric data in `area_evaluation/`, 12-image matched-mask outputs in `wb_error_analysis/`, and reviewed qualitative findings in `reports/Day3_WB_Qualitative_Review_2026-11-03.md`. Curated original figures are under `10_research_paper/figures/` for tracked publication review.

Do not conflate Day 3 sample metrics with the Day 2 full-test AP scores. The 30-image area result uses only matched masks and reports **px²**, not physical units. Suspected annotation errors and five perceptual-hash matches are unconfirmed.

## Day 4 — Full-test area, inference MVP, classical comparison (2026-11-04)

- [`reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md`](reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md) summarizes the new evidence and distinguishes it from the earlier samples.
- [`area_evaluation/day4_full_test/`](area_evaluation/day4_full_test/) preserves the submitted **450-image WB area evaluation**, JSON, per-image CSV, compressed 68,794 matched-instance records, source-derived README, and 4 figures. MAE **211.41 px²**, mean relative absolute error **8.81%** (on matched masks only).
- [`inference_demo/`](inference_demo/) preserves the **10-image WB-only demo** result log transcription, 2 sample figures and checkpoint details; 1,551 predicted instances, not ground-truth counts.
- [`otsu_baseline/`](otsu_baseline/) contains the **10-image Otsu baseline/ablation** summary, OpenCV matching note and 3 example figures; this is a foreground-union comparison, not instance AP.
- [`dataset_qc/day4_submitted/`](dataset_qc/day4_submitted/) keeps the team's original QC submission. **See the separate caveats** in [`reports/Day4_QC_Interpretation_2026-11-04.md`](reports/Day4_QC_Interpretation_2026-11-04.md) before citing its conclusions.


## Day 5 — research follow-up (2026-11-05)

- `reports/Day5_Research_Development_2026-11-05.md` brings together both member submissions and the live demo status.
- `dense_counting/day5_nms/` contains the eight-image comparison of NMS IoU 0.70 and 0.50. Counting MAE improved from 3.375 to 1.875, but the sample was selected for dense scenes and is not a full-test result.
- `rgbd_feasibility/day5/` contains the 30-image / 4,970-mask depth feasibility study, the 450-file depth dtype inventory, source findings and figures. Calibration is not verified; physical area remains unreported.
- `gradio_demo/` records the user's confirmation that the WB-only app ran successfully in Colab. It is not an accuracy benchmark.
