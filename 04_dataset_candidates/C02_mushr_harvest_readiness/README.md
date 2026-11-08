# C02 — MushR oyster mushroom image and maturity source

## Source identity

- Paper: [MushR: A Smart, Automated, and Scalable Indoor Harvesting System for Gourmet Mushrooms](https://doi.org/10.3390/agriculture13081533)
- Model/code: [ETCE-LAB/mushr-mask-r-cnn](https://github.com/ETCE-LAB/mushr-mask-r-cnn)
- Parent system: [ETCE-LAB/MushR](https://github.com/ETCE-LAB/MushR)
- Raw hourly full-scene images: [Kaggle dataset](https://www.kaggle.com/datasets/etcelab/mushr-project-raw-image-dataset-oyster-mushrooms)
- Species: oyster mushroom (*Pleurotus* spp.; paper-specific setup).

## What is verified from public sources

- The paper describes 34,400 hourly full-scene images captured over ten months from three views in two grow tents.
- The annotated model dataset contains 2,759 training and 541 test fruitbody instances in three maturity classes: `Not-Ready`, `Ready` and `Overdue`.
- The public model repository exposes two COCO annotation JSON files, Detectron2 training/inference/evaluation scripts and model configurations.
- The repository links to release `p1`, which lists three assets; the actual weights still need to be downloaded and inspected.
- Model repository licence is listed as GPL-3.0. The parent system repository is listed as AGPL-3.0. Raw dataset terms must be checked separately before data reuse or redistribution.

## Intended system contribution

C02 can supply an established instance-segmentation implementation and source-specific maturity examples. Its raw images also provide repeated views over time. The three maturity labels are **not** a universal mushroom-stage taxonomy and must not be merged directly with Wang's seven stages or labels from other species.

Potential reusable methods include fruitbody Mask R-CNN inference, DBSCAN-style grouping into flushes and area-weighted maturity aggregation. Grouping and maturity outputs should be adapted to the system's cluster records rather than treated as persistent cross-day track identities.

## Increment 1 checks — not yet completed

1. Download only the repository source and two annotation JSONs first; record commit/release and SHA-256.
2. Inspect COCO category IDs/names, image paths, segmentation format, annotation counts and train/test separation.
3. Inspect the `p1` assets and determine architecture/runtime compatibility before obtaining model weights.
4. Resolve the referenced raw-image filenames against the Kaggle archive and acquire only a matching subset needed for schema and visual tests.
5. Verify Kaggle data terms separately from repository code licences.

## Status

**Source identified; data schema and file matching pending.** No raw images, annotations or checkpoints are stored in this repository. See `03_dataset_discovery/SOURCE_DATA_AUDIT_DAY6.md` for the overall source audit.
