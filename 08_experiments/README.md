# M18K V2 experiments — Day 2 to Day 5

**Day 2 completed:** two independent YOLOv8n-seg experiments on the indexed V2 release at RGB 640, 10 epochs, seed 42, Tesla T4; test split contains 450 images. The completed two-class experiment evaluates BB and WB; the WB-only experiment uses WB-only labels. Both are recorded in `experiment_registry.csv` and `configs/day2_*.yaml`.

- `notebooks/` has uploaded executed pipelines. **Read its caveat first:** the two-class baseline notebook includes incomplete early output, and Khang's old test cell points at the two-class dataset; the **corrected** WB-only test was evaluated separately and is documented in logs and JSON.
- `configs/wb_dataset_TEMPLATE.yaml` is only a placeholder (path `__WB_ROOT__`); do not pass it directly to `YOLO.val()`. Rebuild the WB runtime dataset and use its generated `/content/M18K_V2_work/yolo_v2_wb/data.yaml`.
- `07_source_code/data/build_wb_dataset.py --mode rebuild` requires the separate WB labels ZIP and source RGB paths. Original model weights and raw data stay in Drive.
- Test metrics are in `09_results/metrics/` and Day 2 interpretation in `09_results/reports/`.

**Day 3 completed:** 30-image sample area diagnostic and 12-image qualitative review using the existing WB-only checkpoint. They are **not additional full-test model AP scores**.

**Benchmark limitation:** V2 is not the original M18K paper's 2,000-image dataset; methods/protocols/metric definitions differ. Do not infer superior performance from the numerical AP values alone.

## Day 4 (November 4) — no new training

- **WB inference MVP:** `notebooks/Day4_WB_Only_Final_Inference_Executed.ipynb`; 10 reproducibly sampled test images, predicted instance masks/counts/px² areas and outputs. Summary under `09_results/inference_demo/`.
- **Otsu baseline + ablations:** `notebooks/Day4_Otsu_Baseline_Ablation_Executed.ipynb`; scratch Otsu vs OpenCV 10/10 exact matches, same 10 images as YOLO, foreground union IoU/Dice and count error. Summary under `09_results/otsu_baseline/`.
- **Full-test area:** submitted script `07_source_code/evaluation/day4_full_test_area_evaluation.py`, 450-image matched-mask diagnostics under `09_results/area_evaluation/day4_full_test/`.

Day 4 experiments are recorded in `experiment_registry.csv`. Their sampling/evaluation definitions differ; do not compare Otsu union IoU to full-test YOLO instance mAP as if identical.


## Day 5 — follow-up experiments and live demo

- `configs/day5_dense_counting.json` records Khang's eight-image NMS comparison. The only changed inference setting was NMS IoU (0.70 to 0.50). The counting MAE fell from 3.375 to 1.875 on this selected sample; full-test validation is still needed.
- `notebooks/Day5_WB_Only_Gradio_Demo.ipynb` launches the interactive app around the existing WB-only checkpoint. The user confirmed that it worked in Colab. It is a demo, not a new benchmark.
- Thịnh's RGB-D feasibility scripts are in `07_source_code/features/day5_rgbd_feasibility/`; outputs are in `09_results/rgbd_feasibility/day5/`. The study did not verify depth scale or intrinsics, so it reports no mm² values.

## Day 7 — oyster-paper notebooks

- [Charisis notebook](notebooks/Charisis_Oyster_Cluster_Growth_Tracking.ipynb): time-lapse cluster segmentation and tracking.
- [MushR notebook](notebooks/MushR_Oyster_Maturity_Instance_Segmentation.ipynb): maturity segmentation and spatial flush grouping.

Both use TorchVision adaptations. They are prepared but have not been run on the real datasets or in Colab. See the [run guide](notebooks/NOTEBOOK_GUIDE.md).
