# Verified source scripts (submitted by team)

- `data/build_wb_dataset.py`: prepare WB-only labels from source COCO, create/rebuild symlink-backed YOLO dataset, and validate exported labels. `--mode rebuild` requires the **separate** `wb_yolo_labels.zip` and accessible original RGB directory. The archive itself is not committed.
- `evaluation/mask_area.py`: calculate original-resolution mask area as `count_nonzero(mask > 0)`; includes synthetic and real-COCO checks.
- `evaluation/area_evaluation.py`: sample 30 WB test images, infer from a saved checkpoint, match masks to COCO GT at IoU >= 0.5, calculate px² error and export tables/overlays. Does not train a model.

These scripts were supplied in `wb_task_repo-20261103T073720Z-1-001.zip`. Python bytecode caches are excluded. The uploaded notebook shows the executed area experiment; this repository integration did not rerun it against the Drive dataset. The training notebook also used a separately packaged WB label archive (`image_map.csv` mapping); do not assume identical archive manifests without comparing them.
