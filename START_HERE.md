# Start here — M18K V2, Days 1–4 (as of 2026-11-04)

Read [`README.md`](README.md) for the project timeline and caveats. The main results are [`Day 2 — reproduction`](09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md), [`Day 3 — additional analysis`](09_results/reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md), and [`Day 4 — final MVP and course experiment`](09_results/reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md). Day 1 EDA is in `09_results/reports/`.

**Use the Day 4 notebooks** under [`08_experiments/notebooks/`](08_experiments/notebooks/README.md): one executed WB-only inference demo and one executed Otsu-from-scratch comparison/ablation. Both are designed for Colab; the inference notebook needs test RGB images and the checkpoint, while Otsu also needs test COCO annotations. No retraining.

**Main Day 4 figures and metrics:** [`09_results/`](09_results/README.md). Full 450-image area evaluation: `09_results/area_evaluation/day4_full_test/`; sample Otsu comparison: `09_results/otsu_baseline/`; executed inference summaries: `09_results/inference_demo/`. Day 4 dataset QC remains qualified: [`interpretation`](09_results/reports/Day4_QC_Interpretation_2026-11-04.md).

**English course report draft:** [`10_research_paper/drafts/`](10_research_paper/drafts/README.md), available in `.docx` and `.pdf`. This is a draft, not submission proof. Demo video, slides, final report editing and course-lesson mapping are still outstanding.

The raw M18K V2 RGB-D dataset, COCO JSON, label archive and `.pt` weights remain outside Git. See [`12_reproducibility/CLOUD_EXECUTION_GUIDE.md`](12_reproducibility/CLOUD_EXECUTION_GUIDE.md) for paths and provenance. Run `python scripts/validate_workspace.py` and `python -m unittest discover -s tests -v` for **repository consistency** checks (not a fresh GPU model run).

**Merging:** this archive/patch does not push or commit for you. Review changes before applying to your live Git clone; see [`INTEGRATION_NOTES.md`](INTEGRATION_NOTES.md).
