# C03 — M18K V2 RGB-D mushroom dataset

**Status:** active working candidate; **not** formally selected / gate-approved.

- Dataset family: M18K; working V2 release; archived on analyst's Google Drive, not in this repository.
- Problem: 2D detection and instance segmentation of Baby Bella (BB) and White Button (WB) mushrooms; RGB-D information for future fusion/pose experiments.
- COCO annotations observed: `train/annotations_coco.json`, `valid/annotations_coco.json`, `test/annotations_coco.json`; paired `rgb/` and `depth/` directories.
- Split: 3,596 train / 449 val / 450 test (the repository-provided split, no reshuffling).
- Scientific comparison: V2 is not interchangeable with the original paper's 2,000-image, 70/10/20 benchmark.

## Contents

- [`analysis/`](analysis/): the *executed* research notebook with saved outputs (not independently rerun).
- [`dataset_metadata/`](dataset_metadata/): dataset composition and metadata limitations.
- [`qc/`](qc/): quality-control findings and outstanding reviews.
- [`reports/`](reports/): link to the central EDA research report in `09_results/`.
- [`source/`](source/): provenance checklist; needs archive hash and license confirmation.
- `raw/`: ignored directory reserved for local data; do not add raw files or checkpoints to Git.

## Immediate questions

1. Why does the V2 COCO audit give only **858 BB** versus **699,731 WB**?
2. Are frames near-duplicates across train/val/test or from shared trays/scenes?
3. Are RGB-depth arrays calibrated and aligned, beyond filename correspondence?
4. How does the advertised release total of **4,652** relate to 4,495 annotated RGB entries?

No new training result is claimed in this folder.
