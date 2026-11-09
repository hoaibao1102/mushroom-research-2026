# Verified source scripts (submitted by team)

- `data/build_wb_dataset.py`: prepare WB-only labels from source COCO, create/rebuild symlink-backed YOLO dataset, and validate exported labels. `--mode rebuild` requires the **separate** `wb_yolo_labels.zip` and accessible original RGB directory. The archive itself is not committed.
- `evaluation/mask_area.py`: calculate original-resolution mask area as `count_nonzero(mask > 0)`; includes synthetic and real-COCO checks.
- `evaluation/area_evaluation.py`: sample 30 WB test images, infer from a saved checkpoint, match masks to COCO GT at IoU >= 0.5, calculate px² error and export tables/overlays. Does not train a model.

These scripts were supplied in `wb_task_repo-20261103T073720Z-1-001.zip`. Python bytecode caches are excluded. The uploaded notebook shows the executed area experiment; this repository integration did not rerun it against the Drive dataset. The training notebook also used a separately packaged WB label archive (`image_map.csv` mapping); do not assume identical archive manifests without comparing them.

## Day 4 source additions

- `evaluation/day4_full_test_area_evaluation.py`: Thịnh's submitted script for full **450-image** WB predicted-vs-GT mask-area error analysis; outputs JSON, compressed matched-mask CSV, per-image CSV and figures. Needs the original dataset/COCO JSON and WB-only checkpoint.
- `evaluation/day4_submitted_dataset_qc.py`: original Day 4 QC script. Its report compares a **different set of five image pairs** than Khang's original Day 3 dHash flags, so it is preserved as submitted but **not** a verified clearance of split leakage.
- Scratch Otsu is in the executed `08_experiments/notebooks/Day4_Otsu_Baseline_Ablation_Executed.ipynb`; this is the authoritative implementation and comparison run.


## Day 5 additions

- `evaluation/day5_dense_counting/improve_counting.py`: compares the existing WB-only checkpoint at NMS IoU 0.70 and 0.50 on eight selected dense test images. Outputs are preserved under `09_results/dense_counting/day5_nms/`.
- `features/day5_rgbd_feasibility/depth_area.py` and `extra_checks.py`: inspect depth-file formats, valid depth inside WB masks and possible RGB-depth alignment. These scripts do not calculate mm².
- `demo/app.py`: Gradio app for WB-only inference, counting, px² mask areas and CSV/image export. Run instructions and demo dependencies are in `demo/README.md` and `demo/requirements.txt`.
