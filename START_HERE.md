# Start here — Team 10 M18K

1. Open the project in Git. To integrate this update into the group's real GitHub repository, copy/merge the contents from the delivered archive into an existing clone **without replacing its `.git` directory**. Review differences before committing; this file bundle does not push to GitHub.
2. Read `README.md`, `09_results/reports/M18K_V2_EDA_2026-10-30.md`, and `00_project_management/RESEARCH_STATUS.md`.
3. Run `python scripts/validate_workspace.py` and `python -m unittest discover -s tests -v`. These check metadata and file structure only.
4. Open `04_dataset_candidates/C03_m18k_v2/analysis/M18K_V2_Research_EDA_Executed_2026-10-30.ipynb` in Colab for the **already executed record**. It is not a training result. The original full dataset remains on Google Drive and will not be bundled into Git.
5. Before model training, perform the **human-review items** in `00_project_management/TASK_BOARD.md`: confirm the chosen dataset/paper with the team lead, the intended license/use rights, anomalous BB labels, group leakage, and any training budget.
6. To work with the existing notebook, mount Drive and confirm `DATA_ROOT = /content/drive/MyDrive/M18K_Reproduction/M18K_V2_data/M18KV2` with `train`, `valid`, `test` containing `rgb`, `depth` and `annotations_coco.json`.
7. Keep test data for final evaluation; select model checkpoints only on validation. Store large datasets/checkpoints on Drive, version lightweight experimental metadata here.

**Scope note:** Existing C01 and C02 are earlier alternatives, not renamed M18K datasets. `setup_reports/` contains an archived clean-workspace WP-00 report; it predates this V2 EDA and must not be read as current research status.
