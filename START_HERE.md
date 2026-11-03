# Start here — Day 1 to Day 3 research evidence

1. Read [README.md](README.md) and the two day reports: [`Day 2`](09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md) and [`Day 3`](09_results/reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md). Day 1 EDA remains preserved in the original dataset-candidate analysis and results folders.
2. Open `10_research_paper/drafts/M18K_V2_Day3_Research_Draft_2026-11-03.docx` to edit the manuscript; Markdown source is alongside it.
3. Review experimental metrics under `09_results/metrics` and complete raw/reviewed error-analysis outputs under `09_results/area_evaluation` and `09_results/wb_error_analysis`.
4. If rerunning, use notebooks under `08_experiments/notebooks`. **Read that folder's README first:** the saved two-class baseline notebook is an early interrupted workflow, and an old WB notebook test cell incorrectly references two-class labels. Use the separately recorded correct held-out logs rather than that cell.
5. Raw RGB/depth and COCO annotations remain on Drive. The large `wb_yolo_labels.zip` and `best.pt` are required to rerun some steps and are not included here; see `12_reproducibility/CLOUD_EXECUTION_GUIDE.md`.
6. Run `python scripts/validate_workspace.py` and `python -m unittest discover -s tests -v`. The checks validate repository content and aggregate evidence consistency, **not** a fresh model inference or complete upstream dataset QC.

**For merging into the live Git repository:** review `INTEGRATION_NOTES.md` and the Day 2/3 integration manifest. Merge carefully into your existing `.git` clone; this archive does not push or commit for you. Do not overwrite newer files without comparing changes.
