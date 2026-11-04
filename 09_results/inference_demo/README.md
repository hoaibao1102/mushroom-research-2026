# Day 4: Executed WB-only inference MVP

Open [`Day4_WB_Only_Final_Inference_Executed.ipynb`](../../08_experiments/notebooks/Day4_WB_Only_Final_Inference_Executed.ipynb) in Colab. It loads Khang's existing WB-only checkpoint from Drive, selects 10 random test images (seed 42), predicts instance masks, counts mushrooms, measures original-resolution pixel mask areas, and exports CSVs plus a result ZIP. It does **not** train the model.

Results from executed notebook: **1,551 WB detections on 10 images**, mean predicted area **3,520.11 px²**. `Day4_WB_Demo_Image_Counts.csv` was transcribed from its execution output. These counts are predictions, not GT-verified counts. The original 14.22 MB Colab export ZIP is not bundled; the notebook regenerates it.

`figures/` includes 2 original prediction previews extracted from the executed notebook for illustrations.
