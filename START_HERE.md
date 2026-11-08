# Start here

The current system specification is in place through **Day 6 — Increment 0**. The project is a local-first, multi-species mushroom growth monitor with Colab-based training and AMD-first local inference.

## Read these first

1. [`README.md`](README.md) — project overview and repository navigation.
2. [`00_project_management/PROJECT_CHARTER.md`](00_project_management/PROJECT_CHARTER.md) — system goal and scope.
3. [`00_project_management/SYSTEM_REQUIREMENTS.md`](00_project_management/SYSTEM_REQUIREMENTS.md) — functional and deployment requirements.
4. [`00_project_management/SYSTEM_ARCHITECTURE.md`](00_project_management/SYSTEM_ARCHITECTURE.md) — training/inference split and component boundaries.
5. [`03_dataset_discovery/SOURCE_DATA_AUDIT_DAY6.md`](03_dataset_discovery/SOURCE_DATA_AUDIT_DAY6.md) — source and dataset facts, direct links and known gaps.
6. [`00_project_management/RESEARCH_STATUS.md`](00_project_management/RESEARCH_STATUS.md) — current progress and next work.

## Existing working material

- `08_experiments/notebooks/Day2_WB_Only_Training_and_Day3_Error_Analysis.ipynb` — executed WB-only YOLOv8n-seg training and analysis material; note the incorrect legacy test cell documented in `12_reproducibility/CLOUD_EXECUTION_GUIDE.md`.
- `08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb` and `07_source_code/demo/app.py` — previously run WB-only inference demo.
- `07_source_code/evaluation/` — mask-area evaluation, dense-scene NMS comparison and RGB-D feasibility utilities.

These are useful starting components. Their M18K results and checkpoints remain specific to the white-button/baby-bella dataset.

## Repository checks

```bash
python scripts/validate_workspace.py
python -m unittest discover -s tests -v
```

## Next work package

**Increment 1 — dataset integration:** implement repeatable public-data downloads, archive checks, dataset inventory, annotation validation and mask visualizations. Training starts only after the data loaders pass on actual downloaded samples.
