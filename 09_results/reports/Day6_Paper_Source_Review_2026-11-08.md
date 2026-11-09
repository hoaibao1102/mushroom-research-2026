# Day 6 — paper and source review (8 November 2026)

Today we checked three oyster-mushroom papers for data and code that could support work beyond the M18K V2 experiments. No source dataset was downloaded and no model was trained.

## Charisis — cluster growth tracking

The 2025 paper tracks *Pleurotus ostreatus* clusters in time-lapse images. Its Zenodo record lists 6,382 images and 37,004 cluster instances across four experiments. The paper uses sequence-level train/test separation and mask-based tracking. This is the closest match to the project's cluster-growth task.

The paper uses train sequences 2 and 4 and test sequences 1 and 3. The notebook will use that split only if the downloaded files confirm the sequence mapping. The paper's reported scores are not results from our implementation.

## MushR — maturity and flush grouping

The 2023 MushR paper provides a Mask R-CNN workflow with `not-ready`, `ready` and `overdue` classes. Its code repository contains separate COCO train/test annotations and a GPL-3.0 license. The raw oyster images are linked separately through Kaggle, so the image paths need to be matched to the annotation JSONs before training.

The Kaggle identifier in the paper is not the same as the identifier already recorded for candidate C02. We have kept them separate. The repository's code license does not establish the license for the Kaggle images.

## Wang et al. — growth stages

The 2025 *Pleurotus pulmonarius* paper studies seven growth stages for environmental control. Its dataset is described as available on request; we did not find a public dataset or author repository to use. The methods may inform later work, but the paper is not a data source for the current notebooks.

## Next step

We kept Charisis and MushR as separate experiments. Their datasets, labels, capture setups and tasks are different. The next check is to download the actual data, inspect the annotation formats and verify every annotation-to-image path before training.

## Files

- [Paper/source details](../../03_dataset_discovery/source_verification/CHARISIS_AND_MUSHR_PAPER_SOURCES_2026-11-09.md)
- [Paper registry](../../02_literature_review/PAPER_REGISTRY.csv)
- [Dataset candidate registry](../../03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv)
