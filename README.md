# Mushroom Research 2026 — Team 10

The first five days focused on M18K V2: dataset checks, YOLOv8n-seg experiments, mask-area evaluation and an inference demo. On Day 6 we reviewed oyster-mushroom papers and their data/code sources. Day 7 produced two separate Colab notebooks for testing those workflows.

**Updated 9 November 2026.** The M18K results below are from the earlier experiments. The Charisis and MushR notebooks are prepared but have not been run on their real datasets.

## Daily reports

| Day | Work | Report |
|---|---|---|
| 1 | M18K V2 EDA | [M18K V2 EDA](09_results/reports/M18K_V2_EDA_2026-10-30.md) |
| 2 | YOLOv8n-seg runs and dataset checks | [Model runs](09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md) · [Dataset and masks](09_results/reports/Day2_WB_Dataset_and_Mask_Validation_2026-11-02.md) |
| 3 | Prediction review and area analysis | [Area and error analysis](09_results/reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md) · [Qualitative review](09_results/reports/Day3_WB_Qualitative_Review_2026-11-03.md) |
| 4 | Full-test area evaluation, inference demo and Otsu baseline | [Full-test area and MVP](09_results/reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md) · [QC review](09_results/reports/Day4_QC_Interpretation_2026-11-04.md) |
| 5 | Dense-scene NMS test, RGB-D check and Gradio demo | [Research development](09_results/reports/Day5_Research_Development_2026-11-05.md) |
| 6 | Oyster-paper and source review | [Paper and source review](09_results/reports/Day6_Paper_Source_Review_2026-11-08.md) |
| 7 | Two paper-based Colab notebooks | [Notebook preparation](09_results/reports/Day7_Notebook_Preparation_2026-11-09.md) |

## M18K V2 results

- The two-class model reached mask AP@50 **0.4995** and AP@50:95 **0.3963**. WB results were high; BB results were low under the severe class imbalance.
- The WB-only model reached mask AP@50 **0.9906** and AP@50:95 **0.7974** on the 450-image held-out test set.
- Full-test WB area evaluation matched **68,794** instances. MAE was **211.41 px²** and mean relative absolute error was **8.81%**, on matched instances only.
- On eight selected dense images, NMS IoU 0.50 reduced count MAE from **3.375** to **1.875** compared with 0.70. This has not been checked on the full test set.
- The RGB-D check covered 30 images and 4,970 WB masks. Depth scale, camera intrinsics and RGB-depth alignment were not verified, so area remains in px².

The WB-only [Gradio demo](08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb) was launched successfully in Colab. It runs inference with the saved checkpoint; it does not train a model.

## Oyster-paper notebooks

- [Charisis — cluster growth tracking](08_experiments/notebooks/Charisis_Oyster_Cluster_Growth_Tracking.ipynb): time-lapse oyster-cluster segmentation and tracking.
- [MushR — maturity segmentation](08_experiments/notebooks/MushR_Oyster_Maturity_Instance_Segmentation.ipynb): fruitbody maturity segmentation and spatial flush grouping.

Both use TorchVision adaptations of the papers' Mask R-CNN model families. Neither is an exact MMDetection/Detectron2 reproduction. The real data downloads, Colab smoke runs and GPU training are still pending. Keep their datasets, class names and metrics separate from each other and from M18K V2. Run instructions are in the [notebook guide](08_experiments/notebooks/NOTEBOOK_GUIDE.md).

## Repository links

- [Daily reports and result files](09_results/README.md)
- [Experiment notebooks and configs](08_experiments/README.md)
- [Current tasks](00_project_management/TASK_BOARD.md)
- [Colab and Drive notes](12_reproducibility/CLOUD_EXECUTION_GUIDE.md)

Raw datasets, large annotation files and model checkpoints are stored outside Git. The working M18K V2 export contains **4,495 indexed RGB images** and **700,589 annotations**; the difference from the upstream V2 count of 4,652 images remains unexplained. Dataset QC, source permissions and physical-area calibration remain open.
