# Colab / Drive reproduction guide — status through Day 5 (2026-11-05)

## Input locations and dependencies

The working dataset source was reported under Google Drive at `/content/drive/MyDrive/M18K_Reproduction/M18K_V2_data/M18KV2/` with `train/`, `valid/`, `test/` each containing RGB, depth and `annotations_coco.json`. Team members also used alternate `MyDrive/Colab Notebooks/M18K_Reproduction/` or `M18K_Reproduction (1)` paths. **Do not assume these all resolve in a fresh Colab runtime**. Mount Drive and verify source RGB and COCO paths first. Some shared Drive shortcuts were not visible and test data had to be accessed through Google Drive shared-folder API.

Day 2: train on 3,596 images, validate on 449 and test on 450; YOLOv8n-seg RGB, input 640, 10 epochs, batch 8, seed 42, pretrained initialization. GPU used: Tesla T4; reported training durations: 1.569 h two-class and 1.396 h WB-only. Checkpoints (not bundled):

- Two-class checkpoint: `MyDrive/M18K_Reproduction/model_runs/v2_yolov8n_seg_640_e10_s42/weights/best.pt`
- WB-only checkpoint: https://drive.google.com/file/d/1Q5iq_-j-RwOTkyiiXyTOc80Cf_xwk7K-/view (the Day 3 area report recorded SHA-256 `93d993ec6b48c1fca9d59178afe11377ef20afa3ed0c304841e4d6b36d447961`)
- WB labels archive: separate `wb_yolo_labels.zip`, not included in repository. Thịnh's reconstruction script `07_source_code/data/build_wb_dataset.py --mode rebuild` uses source RGB, source paths and ZIP; it creates runtime `data.yaml`. **Template** `08_experiments/configs/wb_dataset_TEMPLATE.yaml` is not directly runnable.

## Important notebook provenance warnings

- `Day2_Two_Class_Baseline_Workflow.ipynb` only contains a saved partial training cell from an early run. For the completed run use `logs/two_class_train_and_test_log_summary.txt` and the test JSON, not that cell as proof of completion.
- `Day2_WB_Only_Training_and_Day3_Error_Analysis.ipynb` completes training and exports prediction examples, but a pre-existing test cell references the **two-class** `YOLO_ROOT/data.yaml`. The corrected WB-only test was performed separately and documented in `logs/WB_only_corrected_heldout_test_log_summary.txt`.
- `Day3_WB_Predicted_Area_Evaluation.ipynb` runs 30-image area inference with the WB-only checkpoint and COCO ground-truth rasterization. It does not retrain the model.

## Available evidence, gaps and evaluation settings

- User-supplied test logs: `12_reproducibility/logs/` and `09_results/metrics/Day2_*`.
- Day 3 area subset: deterministic `random.Random(42).sample` of 30 test images, `conf=0.25`, NMS IoU=0.7, `max_det=1000`, original-resolution masks, greedy one-to-one mask IoU>=0.5, MAE computed on matched masks only.
- Day 3 Khang images: 12 stratified examples, `conf=0.25`, NMS IoU=0.7, `max_det=3000`; not identical max_det to area subset.
- No checkpoint binaries, raw RGB-D, large COCO JSON or the 269MB-class WB labels archive are included.
- Reproducing the paper's original numerical AP is **not** supported, nor is physical area in mm²; camera intrinsics/depth units remain unverified.
- Exact image hashes and scene-level independence are incomplete. Five zero-distance dHash pairs are screening candidates only; do not call them verified leakage.

Run repository checks with `python scripts/validate_workspace.py` and `python -m unittest discover -s tests -v`. These are **metadata consistency checks**, not Colab/GPU replication or a full dataset audit.

## Day 4 additions

Use `08_experiments/notebooks/Day4_WB_Only_Final_Inference_Executed.ipynb` for a clean WB-only Colab demonstration; it downloads the same checkpoint (ID `1Q5iq_-j-RwOTkyiiXyTOc80Cf_xwk7K-`) and samples 10 images from the V2 test RGB folder using seed 42. Exports a CSV and demonstration ZIP in `/content/M18K_WB_Final_Results/` and `/content/M18K_WB_Final_Results.zip`.

Use `08_experiments/notebooks/Day4_Otsu_Baseline_Ablation_Executed.ipynb` for the scratch Otsu/OpenCV check, classical baseline, ablations and YOLO comparison; needs `test/annotations_coco.json`. Its output destination is `/content/M18K_Otsu_Comparison/`. The excerpted CSV reflects rounded notebook output; re-execute if more precision is needed.

Full-test area evaluator source `07_source_code/evaluation/day4_full_test_area_evaluation.py` is preserved with submitted metrics in `09_results/area_evaluation/day4_full_test/`. Its recorded inference uses 640 px, confidence 0.25, NMS IoU 0.7, max_det 1000, original-resolution masks, greedy one-to-one IoU≥0.5. The area unit is **px²**, not mm².

Review `12_reproducibility/manifests/DAY4_EVIDENCE_2026-11-04.json` for exact source ZIP/notebook hashes. Day 4 code and metrics were submitted as executed by the team; this integration did **not** rerun full Colab execution. Dataset QC flags remain open. See `09_results/reports/Day4_QC_Interpretation_2026-11-04.md`.


## Day 5 paths and commands

### Dense-scene NMS comparison

Khang's script is `07_source_code/evaluation/day5_dense_counting/improve_counting.py`. In Colab, mount Drive and ensure the script can find the existing WB-only checkpoint, WB-only `data.yaml`, `test/rgb` and `test/annotations_coco.json`. It compares NMS IoU 0.70 with 0.50 at confidence 0.25 and image size 640. The submitted eight-image results are in `09_results/dense_counting/day5_nms/`; the full 450-image test split has not been evaluated at the modified setting.

### RGB-D feasibility

The scripts `07_source_code/features/day5_rgbd_feasibility/depth_area.py` and `extra_checks.py` inspect the depth maps and calibration evidence. Run them with the V2 root, for example:

```bash
python depth_area.py --data-root "/content/drive/MyDrive/Colab Notebooks/M18K_Reproduction/M18KV2" --split test --n 30 --seed 42
python extra_checks.py --data-root "/content/drive/MyDrive/Colab Notebooks/M18K_Reproduction/M18KV2" --split test
```

The scripts check feasibility only. Depth scale, intrinsics and RGB-depth alignment remain unverified, so the output does not contain physical mm².

### Gradio demo

Open `08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb` in Colab and run all cells. It mounts Drive, uses `/content/drive/MyDrive/M18K_Reproduction/M18K_V2_data/M18KV2/test/rgb`, downloads the existing WB-only checkpoint, and starts a temporary Gradio share URL. The app and its dependencies are in `07_source_code/demo/`. The user confirmed the app worked on 5 November. The checkpoint and raw dataset are not in Git.
