# Day 4: Otsu classical baseline and ablations

Executed source: [`Day4_Otsu_Baseline_Ablation_Executed.ipynb`](../../08_experiments/notebooks/Day4_Otsu_Baseline_Ablation_Executed.ipynb). The notebook contains the scratch-written `otsu_scratch`, its OpenCV comparison, and the complete evaluation code.

The submitted run used **10 held-out test images** (seed 42). Scratch Otsu matched OpenCV on **10/10 images** with binary pixel agreement 1.0. `method_summary_from_notebook.csv` transcribes the rounded values printed in the executed notebook, not an independently rerun CSV; re-execute the notebook to export full precision and per-image records.

Comparisons use **foreground-union IoU and Dice**, not instance-mask AP. Otsu connected components is a rough count estimator on touching mushrooms. Runtime was measured on CPU, with initialization and model runtime differences; these values are illustrative and not an optimized hardware benchmark. The RSS value is process-wide, not model-only memory.

`figures/` contains 3 original PNG outputs extracted from the executed notebook.
