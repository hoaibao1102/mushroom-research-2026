# Results — Day 1 EDA, Day 2 reproduction, Day 3 additional evaluation

**Day 1 — EDA**: `reports/M18K_V2_EDA_2026-10-30.md`, `metrics/v2_eda_*.csv`, `visualizations/*.png`. V2: 4,495 indexed images; 700,589 annotations.

**Day 2 — model reproduction on V2**: `reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md`, two test JSON files under `metrics/Day2_*`, and checked WB data-conversion records under `metrics/wb_*`. Includes 450-image held-out test results for BB+WB and WB-only. Raw logs are recorded as structured user-supplied excerpts under `12_reproducibility/logs/`.

**Day 3 — additional analysis**: `reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md`, 30-image numeric data in `area_evaluation/`, 12-image matched-mask outputs in `wb_error_analysis/`, and reviewed qualitative findings in `reports/Day3_WB_Qualitative_Review_2026-11-03.md`. Curated original figures are under `10_research_paper/figures/` for tracked publication review.

Do not conflate Day 3 sample metrics with the Day 2 full-test AP scores. The 30-image area result uses only matched masks and reports **px²**, not physical units. Suspected annotation errors and five perceptual-hash matches are unconfirmed.
