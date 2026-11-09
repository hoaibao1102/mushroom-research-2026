# Start here

- [Project overview and results](README.md)
- [Daily reports](09_results/README.md)
- [Current tasks](00_project_management/TASK_BOARD.md)
- [New notebook run guide](08_experiments/notebooks/NOTEBOOK_GUIDE.md)

## New oyster notebooks

Run each notebook in a fresh Colab GPU runtime, starting with `RUN_MODE = 'smoke'`:

- [Charisis cluster tracking](08_experiments/notebooks/Charisis_Oyster_Cluster_Growth_Tracking.ipynb)
- [MushR maturity segmentation](08_experiments/notebooks/MushR_Oyster_Maturity_Instance_Segmentation.ipynb)

## Existing M18K demo

Open [Day5_WB_Only_Gradio_Demo.ipynb](08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb), mount the team's Drive and use the existing WB-only checkpoint. It runs inference only; see [demo instructions](07_source_code/demo/README.md).

## Checks

```bash
python scripts/validate_workspace.py
python -m unittest discover -s tests -v
```
