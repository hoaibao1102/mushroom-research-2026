# Mushroom Research 2026 — Team 10

Research workspace for **M18K mushroom detection, instance segmentation, RGB-D analysis and prospective 3D pose estimation**. We retain the shared 00–12 research-project directory structure used by other groups.

**Status (30 October 2026):** M18K V2 is the **active working candidate (C03)**. A reproducible exploratory data analysis was executed on Colab, but **the candidate has not been formally approved**, license/identity review is incomplete, and **no M18K V2 model accuracy or paper reproduction is claimed**. Candidate C01/C02 records are preserved as earlier alternatives; they are not today's work.

## Results to date

The executed notebook reports **4,495 annotated RGB images**, **700,589 polygon annotation records**, and **4,495/4,495 filename-stem-matched depth files**. The supplied split is 3,596 train / 449 validation / 450 test (approximately 80/10/10). Raw COCO category names map ID 1 to BB and ID 2 to WB; the reported instance counts are **858 BB (0.122%)** and **699,731 WB (99.878%)**. Six bounding boxes have non-positive dimensions. The complete image-content and scene-level leakage audits were **not executed**. These values are notebook-derived observations; no independent full dataset rerun was possible in this repository snapshot.

- [Full EDA research record](09_results/reports/M18K_V2_EDA_2026-10-30.md)
- [Executed Colab notebook](04_dataset_candidates/C03_m18k_v2/analysis/M18K_V2_Research_EDA_Executed_2026-10-30.ipynb)
- [Provisional M18K candidate](04_dataset_candidates/C03_m18k_v2/README.md)
- [Next steps and human decisions](00_project_management/TASK_BOARD.md)

## Research direction

1. Inspect and validate dataset composition, labels, RGB/depth pairing, and group/scene independence.
2. Establish a **YOLOv8n-seg RGB baseline on V2**, with model selection on validation and one-time evaluation on held-out test.
3. Compare against the 2025 M18K paper **only after resolving differences in release, split, metric and training protocol**. The original paper's 2,000-image subset and 70/10/20 protocol are not identical to the V2 release.
4. If feasible, test whether **depth-assisted segmentation or 3D pose estimation** adds measurable value, under matched conditions. These are hypotheses, not proven improvements.

Reference paper: Zakeri et al., *Computers* 14(5), 199 (2025), [doi:10.3390/computers14050199](https://doi.org/10.3390/computers14050199). Source code/dataset entry point: [abdollahzakeri/m18k](https://github.com/abdollahzakeri/m18k).

## Repository map

| Path | Purpose |
| --- | --- |
| `00_project_management` | Work plan, current status, approval questions, decisions |
| `01_domain_research` | Mushroom-domain assumptions and open questions |
| `02_literature_review` | Paper registry and research-gap hypotheses |
| `03_dataset_discovery` | Candidate records and dataset source verification |
| `04_dataset_candidates/C03_m18k_v2` | Primary dataset audit, notebook and QC evidence |
| `05_research_protocols` | Dataset QC, leakage and experiment requirements |
| `06_selected_research` | Provisional focus; formal selection remains pending |
| `07_source_code` | Reusable code to add after it is developed/tested |
| `08_experiments` | Future training protocols and run registry (no completed V2 run) |
| `09_results` | EDA tables, report and curated figures |
| `10_research_paper` | Future manuscript (not yet written) |
| `11_field_validation` | Possible independent validation, only with consent |
| `12_reproducibility` | Colab/runtime instructions, evidence manifests |

## Getting started

See [START_HERE.md](START_HERE.md). The uploaded executed notebook uses Google Drive at `MyDrive/M18K_Reproduction/M18K_V2_data/M18KV2/`. Raw images, COCO JSON files, depth maps and checkpoints are **not in Git**. GitHub stores scripts, notebooks, lightweight figures and auditable results.

Use `python scripts/validate_workspace.py`, `python scripts/show_project_status.py`, and `python -m unittest discover -s tests -v` to validate repository metadata. This validator checks repository consistency, **not** the full V2 dataset.
