# Mushroom Research 2026 — Team 10

This repository contains our M18K V2 mushroom detection and instance-segmentation work, from the initial dataset audit through the first follow-up experiments.

**Updated 5 November 2026.** We reproduced the YOLOv8n-seg workflow on M18K V2, measured WB mask-area error in px², built a working WB-only Gradio demo, and tried a lower NMS IoU on eight selected crowded images. We also checked whether the exported depth maps can support physical measurements; the required calibration details are not verified, so we have not reported mm².

## What we did

| Day | Work |
|---|---|
| **Day 1 — EDA** | Inspected M18K V2 images, RGB/depth pairing, annotations and class balance. |
| **Day 2 — Reproduction** | Trained and evaluated two-class and WB-only YOLOv8n-seg models on M18K V2. This reproduces the paper's approach on V2, not its exact benchmark protocol. |
| **Day 3 — Model analysis** | Reviewed predictions and measured mask-area error on a 30-image sample. |
| **Day 4 — Course MVP** | Evaluated WB mask area across all 450 test images, implemented Otsu from scratch, ran a small baseline/ablation, and completed the inference notebook. |
| **Day 5 — Follow-up research** | Compared NMS settings on eight dense images, checked RGB-D measurement feasibility, and launched the WB-only Gradio demo. |

## Main results

- The two-class model's overall mask AP@50 was **0.4995** and AP@50:95 was **0.3963**. WB performance was high; BB performance was very low because the V2 annotations are extremely imbalanced.
- The independently trained WB-only model reached mask AP@50 **0.9906** and AP@50:95 **0.7974** on 450 held-out test images.
- The full-test WB mask-area analysis matched **68,794** instances. Mean absolute area error was **211.41 px²** and mean relative absolute error was **8.81%**, calculated on matched instances only.
- On the eight-image dense-scene sample, changing NMS IoU from **0.70 to 0.50** reduced counting MAE from **3.375 to 1.875**. This is preliminary; the full 450-image test set has not been checked at the new setting.
- The RGB-D feasibility study covered **30 images and 4,970 WB masks**. Depth units and camera intrinsics are not verified, and RGB-depth alignment is uncertain. We did not calculate mm².

## Interactive demo

The WB-only Gradio app was run successfully in Colab. Open [`08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb`](08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb) and run it with the team's Drive dataset. The app loads a random test image or accepts an RGB upload, shows instance masks and counts, measures mask area in px², and exports images and CSVs. The model checkpoint stays in Drive.

## Where things are

- Experiment notebooks and configurations: [`08_experiments`](08_experiments/README.md)
- Source code: [`07_source_code`](07_source_code/README.md)
- Results and reports: [`09_results`](09_results/README.md)
- Course report and slides: [`10_research_paper/submission`](10_research_paper/submission/README.md)
- Colab paths and reproducibility notes: [`12_reproducibility/CLOUD_EXECUTION_GUIDE.md`](12_reproducibility/CLOUD_EXECUTION_GUIDE.md)
- Current status: [`00_project_management/RESEARCH_STATUS.md`](00_project_management/RESEARCH_STATUS.md)

The report and slide deck were prepared earlier on 5 November, before the Day 5 member results arrived. Those new findings are documented separately and have not yet been added to the course report. A separate demo video is still outstanding.

## Dataset and model files

The M18K V2 RGB-D dataset, COCO JSON files, WB-label archive and model checkpoints are stored outside Git in the team's Google Drive. No raw dataset or checkpoint is included here. The working V2 export contains **4,495 indexed RGB images** and **700,589 original annotations**; the difference from the upstream V2 count of 4,652 images remains unexplained.

We do not claim an exact numerical reproduction of the original M18K paper, verified scene-level split independence, formal dataset/license approval, calibrated physical area, or full-test improvement from the eight-image NMS experiment.
