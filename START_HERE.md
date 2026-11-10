# Start here

This repository is the research workspace: literature review, dataset/source checks, experiment records, metrics and reproducibility notes.

- [Project overview and results](README.md)
- [Daily reports](09_results/README.md)
- [Current research tasks](00_project_management/TASK_BOARD.md)
- [Research status](00_project_management/RESEARCH_STATUS.md)
- [Colab and Drive execution guide](12_reproducibility/CLOUD_EXECUTION_GUIDE.md)

## Local application

The Day 8 Streamlit prototype is retained as a reference snapshot in [`13_local_application/`](13_local_application/README.md). Ongoing app development is intended to live in a separate repository; its URL has not yet been added. The research repo should hold research methods and evidence, not the active app backlog.

## Notebook notes

Day 7 records the Charisis and MushR notebook preparation. The notebook files themselves and real-data training evidence are not included in this source archive. See the [Day 7 report](09_results/reports/Day7_Notebook_Preparation_2026-11-09.md) and [notebook notes](08_experiments/notebooks/README.md).

## Existing M18K demo

Open [Day5_WB_Only_Gradio_Demo.ipynb](08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb), mount the team's Drive and use the existing WB-only checkpoint. It runs inference only; see [demo instructions](07_source_code/demo/README.md).

## Checks

```bash
python scripts/validate_workspace.py
python -m unittest discover -s tests -v
```
