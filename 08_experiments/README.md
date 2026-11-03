# M18K V2 experiments — Day 2 training, Day 3 analyses

**Day 2 completed:** two independent YOLOv8n-seg experiments on the indexed V2 release at RGB 640, 10 epochs, seed 42, Tesla T4; test split contains 450 images. The completed two-class experiment evaluates BB and WB; the WB-only experiment uses WB-only labels. Both are recorded in `experiment_registry.csv` and `configs/day2_*.yaml`.

- `notebooks/` has uploaded executed pipelines. **Read its caveat first:** the two-class baseline notebook includes incomplete early output, and Khang's old test cell points at the two-class dataset; the **corrected** WB-only test was evaluated separately and is documented in logs and JSON.
- `configs/wb_dataset_TEMPLATE.yaml` is only a placeholder (path `__WB_ROOT__`); do not pass it directly to `YOLO.val()`. Rebuild the WB runtime dataset and use its generated `/content/M18K_V2_work/yolo_v2_wb/data.yaml`.
- `07_source_code/data/build_wb_dataset.py --mode rebuild` requires the separate WB labels ZIP and source RGB paths. Original model weights and raw data stay in Drive.
- Test metrics are in `09_results/metrics/` and Day 2 interpretation in `09_results/reports/`.

**Day 3 completed:** 30-image sample area diagnostic and 12-image qualitative review using the existing WB-only checkpoint. They are **not additional full-test model AP scores**.

**Benchmark limitation:** V2 is not the original M18K paper's 2,000-image dataset; methods/protocols/metric definitions differ. Do not infer superior performance from the numerical AP values alone.
