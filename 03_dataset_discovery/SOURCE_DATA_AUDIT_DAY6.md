# Source and dataset audit — Day 6 (8 November 2026)

## Audit outcome

The public sources provide enough material to begin the core implementation without another user upload. Their roles differ: temporal cluster tracking, instance segmentation/maturity, software/data-loading patterns, stage concepts and optional depth. They must be ingested through source-specific adapters; categories and maturity labels must not be silently merged. Raw dataset archives and checkpoints stay outside this repository.

## Dataset sources

### 1. Charisis et al. (2025) — primary temporal-tracking source

- Paper: [A novel Mask R-CNN-based tracking pipeline for oyster mushroom cluster growth monitoring in time-lapse image datasets](https://doi.org/10.1016/j.compag.2025.110590)
- Dataset: [Zenodo record 15041243](https://zenodo.org/records/15041243)
- Paper-reported data: 6,382 high-resolution images and 37,004 annotated cluster instances from four time-lapse experiments; species is *Pleurotus ostreatus*.
- Reported method: Mask R-CNN with ConvNeXt and Swin backbones; post-processing for visual anomalies/overlap/partial harvest; mask-based temporal association; relative cluster sizing using substrate dimensions; growth trajectory visualization.
- The paper reports ConvNeXt as its best configuration and MOTA 0.967 for tracking. These are paper-reported results, not results reproduced in this project.
- Code availability: no standalone author repository for this paper was verified. The UCD thesis identifies Annex D as supplementary code for the tracking chapter; its runnable completeness remains to be inspected.
- Increment 1 checks: retrieve archive metadata and a small sample; inspect file layout, experiment/camera/sequence identifiers, capture order/timestamps, category mapping, segmentation format, persistent GT track IDs (if any), license and archive hash.
- Intended role: strongest public temporal cluster-tracking foundation. The paper's oyster-farm geometry is not assumed to match the target cultivation columns.

### 2. MushR (2023) — reusable instance-segmentation and maturity source

- Paper: [MushR: A Smart, Automated, and Scalable Indoor Harvesting System for Gourmet Mushrooms](https://doi.org/10.3390/agriculture13081533)
- Model repository: [ETCE-LAB/mushr-mask-r-cnn](https://github.com/ETCE-LAB/mushr-mask-r-cnn)
- Parent system: [ETCE-LAB/MushR](https://github.com/ETCE-LAB/MushR)
- Raw hourly images: [Kaggle oyster mushroom dataset](https://www.kaggle.com/datasets/etcelab/mushr-project-raw-image-dataset-oyster-mushrooms)
- Paper reports 34,400 full-scene images collected hourly over ten months from three views across two grow tents. Its annotated model set contains 2,759 training and 541 test fruitbody instances in three source-specific maturity classes: Not-Ready, Ready and Overdue.
- The model repository exposes two COCO annotation JSON files, Detectron2 training/inference/evaluation scripts, configuration files and a release named `p1` with three assets.
- Method ideas: Mask R-CNN instance segmentation, fruitbody maturity classification, DBSCAN grouping into flushes and area-weighted maturity aggregation.
- Code licence listings: model repository GPL-3.0; parent system AGPL-3.0. The raw dataset terms must be checked separately on the dataset page before reuse or redistribution.
- Increment 1 checks: fetch code/annotation files first; inspect categories, image references and release asset metadata; then obtain only a matching raw-image subset and confirm dataset terms.
- Intended role: reusable segmentation/maturity component and temporal image source. Oyster-specific maturity classes remain distinct from other species and from the target site's stage labels.

### 3. M18K — supporting software and domain-specific baseline

- Paper: [M18K: A Multi-Purpose Real-World Dataset for Mushroom Detection, 3D Pose Estimation, and Growth Monitoring](https://doi.org/10.3390/computers14050199)
- Repository: [abdollahzakeri/m18k](https://github.com/abdollahzakeri/m18k)
- Repository describes *Agaricus bisporus* data, a V2 archive advertised as 4,652 images, a separate 2,121-image growth-monitoring subset and RGB-D resources. Its model zoo is listed as forthcoming, so do not assume pretrained weights are provided.
- Existing local Day 1–5 V2 audit indexed 4,495 annotated RGB entries and 700,589 annotations; the difference from the advertised 4,652 remains a historical QC issue.
- Existing experiments: YOLOv8n-seg training/evaluation, WB-only area analysis, small NMS pilot, RGB-D feasibility and a working WB-only Gradio demo.
- Repository licence: Apache-2.0. Dataset terms and archive version must still be checked separately.
- Intended role: reusable code/data-loader patterns and historical model/UI regression fixture; optional growth subset after schema inspection. The current WB checkpoint is not a general mushroom model.

### 4. Wang et al. (2025) — developmental-stage concepts

- Paper: [Real-Time Detection and Instance Segmentation Models for the Growth Stages of *Pleurotus pulmonarius* for Environmental Control in Mushroom Houses](https://doi.org/10.3390/agriculture15101033)
- The paper reports 1,261 in-situ images, seven growth stages and COCO-style instance annotations; images were collected at four-hour intervals from three mushroom houses.
- Data availability: the paper says the data will be made available on reasonable request. No public author-linked dataset repository was verified.
- Intended role: inform optional stage definitions and model design. The project will not claim exact training reproduction or require access to the request-only dataset.

### 5. MushroomSegDepth (2026) — optional depth extension

- Paper: [MushroomSegDepth](https://doi.org/10.1016/j.compag.2026.111680)
- Code: [meiqing-wang/MushroomSegDepth](https://github.com/meiqing-wang/MushroomSegDepth)
- Repository exposes `Train.py`, a multitask model and a dataloader. Its README describes RGB-only input for joint segmentation and depth prediction, with ConvNeXt/FPN-based features.
- The paper reports 705 RGB-depth pairs; the repository says the raw RGB-depth images and masks will be released after publication/acceptance, but a public dataset download was not found in the inspected listing. A reusable code licence was not confirmed.
- Intended role: optional architecture reference only; do not copy code before licence review and do not block the RGB detection/tracking system on the dataset.

### 6. Optional six-species image collection

- [Mushroom Image Dataset (Bangladesh, 2024)](https://data.mendeley.com/datasets/dt6d4v33fp/1), DOI `10.17632/dt6d4v33fp.1`.
- Public listing describes 1,860 images across six cultivated mushroom types: white oyster, pink oyster, golden oyster, oyster, button and yellow oyster.
- The description supports image/species classification context, not temporal cluster tracking or full-scene instance segmentation. Keep optional; verify archive terms and inspect images before any use.

## Source-code inventory

| Source | Publicly visible contents | Licence / reuse note | Planned use |
|---|---|---|---|
| [MushR Mask R-CNN](https://github.com/ETCE-LAB/mushr-mask-r-cnn) | COCO train/test JSON, Detectron2 train/inference/evaluation scripts, configs, release `p1` | GPL-3.0 listing; check compatibility before copying or redistribution | Reference/adapt maturity and instance-segmentation workflow |
| [MushR parent system](https://github.com/ETCE-LAB/MushR) | Automated capture, grow-chamber, lifecycle calculations and hardware modules | AGPL-3.0 listing | Reference camera/cultivation workflow; not a required dependency |
| [M18K](https://github.com/abdollahzakeri/m18k) | Dataset package, loaders and download links for detection/growth/RGB-D subsets | Apache-2.0 repository; check data terms separately | Reuse data-loader patterns and prior baseline components |
| [Charisis methods/data](https://doi.org/10.1016/j.compag.2025.110590) | Paper methodology and Zenodo dataset; no separate author GitHub repository verified | Dataset terms are separate from the article | Implement/adapt tracking ideas in project-owned code after schema inspection |
| [MushroomSegDepth](https://github.com/meiqing-wang/MushroomSegDepth) | Model, training script and dataloader | Repository licence not confirmed | Optional design reference only until terms are known |
| Wang GSP-RTMDet | Paper architecture and stage definitions | No public author repository/dataset download verified | Use findings, not external code or exact reproduction |

## Data-use controls

- Only sources in the candidate registry with an active acquisition role proceed to Increment 1.
- Excluded sources remain in `03_dataset_discovery/excluded_datasets/EXCLUDED_DATASETS.csv` as identity/decision controls only. Do not retrieve or use their dataset-derived content.
- Keep raw data, checkpoints, Kaggle credentials and large archives outside Git.
- Record source URL, version/release, retrieval date, archive SHA-256, licence and any source-specific label map for every retrieved asset.

## Increment 1 retrieval order

1. Retrieve Charisis Zenodo metadata and a small sample; inspect timestamp, sequence and annotation schema.
2. Retrieve the MushR repository files and annotation JSONs; verify the matching raw image references and dataset terms before downloading a subset.
3. Inspect M18K's separately listed growth-monitoring subset and its data format; use only if it contributes to the agreed target pipeline.
4. Consider the six-species collection only if the first general detector needs more species breadth; do not use it for temporal tracking claims.
5. Defer Wang's request-only dataset and MushroomSegDepth depth data; neither blocks the core RGB system.

**Audit status:** public source links and their intended roles are recorded. No dataset archives were downloaded and no upstream model code was executed in Increment 0. Dataset schema, actual image matching, data terms and local runtime are Increment 1+ checks.
