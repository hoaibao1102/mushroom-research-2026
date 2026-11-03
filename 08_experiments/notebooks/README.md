# Executed Colab notebooks and provenance

- `Day2_Two_Class_Baseline_Workflow.ipynb`: YOLO/EDA pipeline. **Its saved training cell is an incomplete early run**; the completed two-class model's evidence is the separately supplied Day 2 console-log excerpt and held-out test metrics. Do not present this particular notebook output as a finished training log.
- `Day2_WB_Only_Training_and_Day3_Error_Analysis.ipynb`: completed WB-only training; later cells (28–31) export 12 qualitative prediction comparisons and an automated report. **Cell 24 mistakenly points to a two-class `YOLO_ROOT`**; its stored evaluation output is NOT the valid WB-only held-out result. The corrected WB-only test result was run separately and supplied in the console excerpt under `12_reproducibility/logs/`.
- `Day3_WB_Predicted_Area_Evaluation.ipynb`: separate 30-image area experiment and inspection, without retraining.

Saved Colab output is evidence of execution, but runtime Drive paths must be adapted and not every cell is intended for sequential fresh execution. Check the source scripts, data ZIP requirements and logs before reuse.
