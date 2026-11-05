# Research task board — status through Day 5 (2026-11-05)

| Work | Status | Evidence / next step |
|---|---|---|
| Day 1 — M18K V2 EDA | Done | `09_results/reports/M18K_V2_EDA_2026-10-30.md` |
| Day 2 — two-class and WB-only YOLO tests | Done | `09_results/metrics/Day2_*` |
| Day 3 — mask-area sample and qualitative review | Done | `09_results/area_evaluation/`, `09_results/wb_error_analysis/` |
| Day 4 — full-test area, Otsu baseline/ablation and inference notebook | Done | `09_results/area_evaluation/day4_full_test/`, `09_results/otsu_baseline/`, `08_experiments/notebooks/` |
| Day 5 — NMS counting comparison | Preliminary result | Eight selected dense images; validate on all 450 test images before making a general claim. |
| Day 5 — RGB-D feasibility | Done | Calibration information is insufficient for mm²; see `09_results/rgbd_feasibility/day5/`. |
| Day 5 — WB-only Gradio demo | Working | User confirmed successful Colab run; app and launcher are in `07_source_code/demo/` and `08_experiments/notebooks/`. |
| English report and presentation | Prepared | `10_research_paper/submission/`; add team details, course-lesson mapping and the Day 5 findings if they are to appear in the final report. |
| Demo video | Open | Can be recorded from the working Gradio app. |
| Dataset duplicate/annotation QC | Open | Original flags have not been conclusively resolved. |
| Dataset source/license review | Open | Formal approval remains a separate project gate. |

## Next research work

- Check whether the NMS 0.50 result holds on the full 450-image test set using the same checkpoint and fixed evaluation settings.
- Look for original depth-scale, camera-intrinsics and alignment metadata; if unavailable, plan a small calibrated measurement capture rather than reporting guessed mm² values.
