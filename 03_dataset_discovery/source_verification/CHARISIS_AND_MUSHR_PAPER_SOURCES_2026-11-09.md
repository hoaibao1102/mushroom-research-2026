# Charisis and MushR paper sources (9 November 2026)

## Charisis et al. (2025)

*A novel Mask R-CNN-based tracking pipeline for oyster mushroom cluster growth monitoring in time-lapse image datasets.* DOI: `10.1016/j.compag.2025.110590`.

- Dataset: [Zenodo record 15041243](https://zenodo.org/records/15041243), DOI `10.5281/zenodo.15041243`.
- Paper-reported data: 6,382 images, 37,004 cluster instances, four time-lapse experiments; classes `immature`, `well-defined`, `overstayed`.
- Paper split: train sequences 2 and 4; test sequences 1 and 3. The notebook checks the downloaded file/sequence mapping before applying it.
- Paper implementation: Mask R-CNN with ConvNeXt-Tiny or Swin-Small in MMDetection 3.3.0; mask-based temporal association and substrate-aware processing.
- Notebook implementation: TorchVision Mask R-CNN with ConvNeXt-Tiny-FPN and a separate mask-IoU/centroid/area association method. This is an adaptation, not an exact reproduction.
- The notebook records Zenodo license metadata and the downloaded file manifest at runtime. No license conclusion is made before that check.

## MushR (2023)

*A Smart, Automated, and Scalable Indoor Harvesting System for Gourmet Mushrooms.* *Agriculture* 13(8), 1533. DOI: `10.3390/agriculture13081533`.

- Model and annotation code: [ETCE-LAB/mushr-mask-r-cnn](https://github.com/ETCE-LAB/mushr-mask-r-cnn). The repository includes train/test COCO annotations and a GPL-3.0 license file.
- Raw images linked by the paper: Kaggle `etcelab/mushr-project-raw-image-dataset-oyster-mushrooms`.
- Paper classes: `not-ready`, `ready`, `overdue`; 2,759 train and 541 test fruitbody instances.
- Paper model: Mask R-CNN R-50-FPN. Flush grouping uses DBSCAN over predicted fruitbody locations and class-wise area totals.
- Notebook implementation: TorchVision Mask R-CNN R-50-FPN; GitHub annotations and Kaggle images are downloaded separately and joined by image path. DBSCAN uses binary-mask centroids.
- The GPL-3.0 repository license does not establish the license of the separate Kaggle image dataset. Review Kaggle terms before redistribution.

## Registry note

The Kaggle identifier already recorded for candidate C02 is `etcelab/mushr-annotated-dataset-oyster-mushrooms`. It is different from the paper-linked raw-image identifier above. They remain separate records.

The existing exclusion D001 (`hf55tkx489`) remains in force; none of the data or findings in that excluded dataset are used here.

## Status

Neither notebook has downloaded and checked its real data in this environment. The source pairing is for a paper-method experiment only; it does not select a project-wide dataset or clear a research gate.
