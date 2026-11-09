# Day 7 — two oyster-paper notebooks (9 November 2026)

Today we prepared two separate Colab notebooks from the Charisis and MushR papers. The existing M18K V2 notebooks and results were left as they were.

## Charisis cluster tracking

The notebook uses the Charisis Zenodo source, a sequence-based split, Mask R-CNN with a ConvNeXt-Tiny-FPN backbone, and mask-based association for tracking clusters between captures. The published sequence split is applied only if the downloaded metadata confirms the sequence IDs.

## MushR maturity segmentation

The notebook uses the MushR GitHub COCO annotations and the paper-linked Kaggle raw images. It trains Mask R-CNN with a ResNet-50-FPN backbone, predicts the `not-ready`, `ready` and `overdue` classes, then groups fruitbodies spatially using DBSCAN.

Both notebooks use TorchVision implementations. They are adaptations of the papers' model families, not exact MMDetection or Detectron2 reproductions. Their labels and datasets remain separate.

## Checks

Both notebooks passed JSON/nbformat validation and Python-cell parsing. Synthetic CPU checks passed for the two model architectures, checkpoint save/reload, tracking across a missed frame and DBSCAN grouping. The repository tests passed **13/13** and the workspace validator reported **170 PASS / 4 INFO / 0 FAIL**.

These checks did not use the real datasets. We have not verified the Zenodo archive layout, the MushR image/annotation join, Colab compatibility or GPU training. No accuracy or tracking result is available yet.

## Files

- [Charisis notebook](../../08_experiments/notebooks/Charisis_Oyster_Cluster_Growth_Tracking.ipynb)
- [MushR notebook](../../08_experiments/notebooks/MushR_Oyster_Maturity_Instance_Segmentation.ipynb)
- [Run guide](../../08_experiments/notebooks/NOTEBOOK_GUIDE.md)
- [Source review](Day6_Paper_Source_Review_2026-11-08.md)
