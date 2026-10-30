# Reproducibility protocol — M18K

## Evidence available today

- Executed V2 notebook preserved at `04_dataset_candidates/C03_m18k_v2/analysis/` with saved cell outputs.
- Source notebooks run in Colab with Google Drive dataset mounted; Python 3.13.18 appears in the recorded output. GPU model training was **disabled**.
- Summary count CSVs and selected notebook figures are versioned under `09_results/`.

## Requirements for future runs

Record complete source code and environment, PyTorch/Ultralytics versions, model initialization and weight source, Git commit, seeds and split manifests/hashes, train/validation/test definitions, GPU, training hyperparameters, checkpoint provenance and held-out raw metrics. Store large files on Drive, only lightweight configs/manifests in Git. Do not silently change class mapping or exclude anomalous annotations.

The full V2 data and 2.5 GB COCO JSON files are not bundled; therefore the recorded EDA output **cannot be independently recomputed from this Git archive alone**. Treat it as a traceable original run, not independent confirmation.
