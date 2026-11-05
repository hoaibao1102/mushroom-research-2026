# WB-only interactive demo

The team ran the Gradio app in Google Colab on 5 November 2026 and confirmed that the app launched, loaded a random M18K V2 test image, and completed WB-only inference. The app shows instance masks and counts, reports per-instance mask areas in px², and exports annotated images and CSV files.

This is a working inference demonstration, not a new accuracy evaluation. The checkpoint remains in Google Drive and is not included in the repository. Source code, dependencies and the Colab launcher are in `07_source_code/demo/` and `08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb`.
