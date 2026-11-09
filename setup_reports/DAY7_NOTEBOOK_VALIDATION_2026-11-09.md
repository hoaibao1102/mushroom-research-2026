# Day 7 notebook checks — 9 November 2026

| Check | Result |
|---|---|
| Notebook JSON / nbformat and Python-cell parsing | PASS — both notebooks |
| ConvNeXt-Tiny-FPN Mask R-CNN forward/backward | PASS — synthetic CPU tensors |
| ResNet-50-FPN Mask R-CNN forward/backward | PASS — synthetic CPU tensors |
| Tracker keeps ID across an empty frame | PASS — synthetic masks |
| DBSCAN separates nearby and distant instances | PASS — synthetic centroids |
| Checkpoint save and reload | PASS — synthetic model state |
| Repository unit tests | PASS — 13 tests |
| Workspace validator | PASS — 170 PASS / 4 INFO / 0 FAIL |

Checks ran locally on Python 3.13.5, PyTorch 2.10.0+cpu and TorchVision 0.25.0+cpu.

Not tested: real Zenodo download/layout, MushR GitHub/Kaggle image join, Colab execution, GPU training, AP, real-data tracking, Kaggle image terms, or local AMD/DirectML inference. These checks establish notebook syntax and selected synthetic code paths only.
