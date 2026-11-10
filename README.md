# Mushroom Research 2026 — Team 10

This repository is the research workspace for the mushroom-monitoring project: literature and source reviews, dataset audits, experiments, evaluation evidence, reproducibility and field-validation planning. The first five days focused on M18K V2; Day 6 onward defines and investigates the broader mushroom growth-monitoring system.

**Updated 10 November 2026.** M18K results below remain scoped to the white-button dataset. The Day 8 local application is a prototype; its presence does not establish model accuracy, physical-size measurement or AMD acceleration.

## Daily reports

| Day | Work | Report |
|---|---|---|
| 1 | M18K V2 EDA | [M18K V2 EDA](09_results/reports/M18K_V2_EDA_2026-10-30.md) |
| 2 | YOLOv8n-seg runs and dataset checks | [Model runs](09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md) · [Dataset and masks](09_results/reports/Day2_WB_Dataset_and_Mask_Validation_2026-11-02.md) |
| 3 | Prediction review and area analysis | [Area and error analysis](09_results/reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md) · [Qualitative review](09_results/reports/Day3_WB_Qualitative_Review_2026-11-03.md) |
| 4 | Full-test area evaluation, inference demo and Otsu baseline | [Full-test area and MVP](09_results/reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md) · [QC review](09_results/reports/Day4_QC_Interpretation_2026-11-04.md) |
| 5 | Dense-scene NMS test, RGB-D check and Gradio demo | [Research development](09_results/reports/Day5_Research_Development_2026-11-05.md) |
| 6 | Oyster-paper and source review | [Paper and source review](09_results/reports/Day6_Paper_Source_Review_2026-11-08.md) |
| 7 | Charisis and MushR notebook preparation | [Notebook preparation](09_results/reports/Day7_Notebook_Preparation_2026-11-09.md) |
| 8 | Local application prototype and research handoff | [Application prototype](09_results/reports/Day8_Local_Application_Prototype_2026-11-10.md) |

## M18K V2 results

- The two-class model reached mask AP@50 **0.4995** and AP@50:95 **0.3963**. WB results were high; BB results were low under the severe class imbalance.
- The WB-only model reached mask AP@50 **0.9906** and AP@50:95 **0.7974** on the 450-image held-out test set.
- Full-test WB area evaluation matched **68,794** instances. MAE was **211.41 px²** and mean relative absolute error was **8.81%**, on matched instances only.
- On eight selected dense images, NMS IoU 0.50 reduced count MAE from **3.375** to **1.875** compared with 0.70. This has not been checked on the full test set.
- The RGB-D check covered 30 images and 4,970 WB masks. Depth scale, camera intrinsics and RGB-depth alignment were not verified, so area remains in px².

The WB-only [Gradio demo](08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb) was launched successfully in Colab. It runs inference with the saved checkpoint; it does not train a model.

## Oyster-paper research

Day 6 reviewed Charisis et al. for temporal cluster tracking and MushR for maturity-labelled segmentation and spatial grouping. Day 7 documented two separate TorchVision notebook adaptations. They are not exact MMDetection/Detectron2 reproductions, and the source-specific labels and metrics must remain separate. See the [Day 6 source review](09_results/reports/Day6_Paper_Source_Review_2026-11-08.md), [Day 7 notebook preparation](09_results/reports/Day7_Notebook_Preparation_2026-11-09.md) and [notebook run notes](08_experiments/notebooks/NOTEBOOK_GUIDE.md). Notebook files and real-data training evidence are not included in this source archive.

## Local application

A Streamlit prototype now connects cultivation records, image capture, model bundles, segmentation inference, tracking, pixel-area measurements, maturity grouping, environmental records and human review. The Day 8 code snapshot is retained in [`13_local_application/`](13_local_application/) for reference; it is not the intended home for ongoing app development.

**Application development repository:** _URL pending — add the separate app repository here._

The bundled app tests pass **7/7**. However, this source archive contains model-registry metadata without a trained checkpoint, so it does not verify trained-model inference. AMD acceleration, physical-area calibration and field performance remain open. The Charisis tracker and MushR per-image flush grouping are different workflows, not interchangeable IDs.

## Repository links

- [Daily reports and result files](09_results/README.md)
- [Experiment notebooks and configs](08_experiments/README.md)
- [Current research tasks](00_project_management/TASK_BOARD.md)
- [Project status](00_project_management/RESEARCH_STATUS.md)
- [Colab and Drive notes](12_reproducibility/CLOUD_EXECUTION_GUIDE.md)

Raw datasets, large annotation files and model checkpoints are stored outside Git. The working M18K V2 export contains **4,495 indexed RGB images** and **700,589 annotations**; the difference from the upstream V2 count of 4,652 images remains unexplained. Dataset QC, source permissions and physical-area calibration remain open.
