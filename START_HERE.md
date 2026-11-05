# Start here

The project is now documented through **Day 5 (5 November 2026)**. Start with `README.md` for the short overview.

## Most useful files

- `09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md` — the two YOLO reproduction results.
- `09_results/reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md` — full-test area results and the course MVP experiments.
- `09_results/reports/Day5_Research_Development_2026-11-05.md` — the dense-scene NMS comparison, RGB-D feasibility study and Gradio demo status.
- `08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb` — launches the interactive WB-only demo in Colab.
- `10_research_paper/submission/` — current course report and presentation files. The documents were prepared before the Day 5 findings and may need a final update.

## Running the demo

Open the Day 5 Gradio notebook in Colab, run it from top to bottom, and authorize Drive access. It uses the existing WB-only checkpoint and the M18K V2 `test/rgb` folder. No training is required. See `07_source_code/demo/README.md` for details.

## Important caveats

- The Day 5 NMS comparison covers eight selected dense images only; full-test validation is pending.
- The RGB-D study did not establish depth units, intrinsics or alignment. Physical area in mm² is not reported.
- Dataset QC, source/license approval and the separate demo video remain open.

Run `python scripts/validate_workspace.py` and `python -m unittest discover -s tests -v` for repository checks. These do not rerun model inference or audit the raw dataset.
