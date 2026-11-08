# C03 — M18K V2 RGB-D mushroom dataset

**Role in the current system:** supporting software/data reference and historical experiment baseline. It is not the selected general-mushroom production dataset.

- Dataset family: M18K; prior V2 release; original files are stored outside this source-only repository.
- Species: button mushroom (*Agaricus bisporus*), including Baby Bella (BB) and White Button (WB) labels in the prior V2 experiments.
- The prior local V2 audit indexed 4,495 annotated RGB entries and 700,589 annotations. The upstream repository advertises a 4,652-image V2 archive; the discrepancy remains documented in the historical QC record.
- Prior local split: 3,596 train / 449 validation / 450 test images; the submitted split was retained without reshuffling.
- The upstream repository separately lists a 2,121-image growth-monitoring subset. It is a distinct asset and must not be conflated with the V2 detection archive.
- RGB-D scale, intrinsics and exact alignment in the prior local export remain unverified; no physical mm² result was produced.

## Reusable evidence and components

- [`analysis/`](analysis/): executed M18K V2 EDA notebook with saved outputs; not independently rerun in this repository update.
- [`dataset_metadata/`](dataset_metadata/): historical V2 inventory and scope.
- [`qc/`](qc/): open data-quality and provenance questions.
- [`reports/`](reports/): links to earlier EDA reports.
- [`source/`](source/): provenance and source-review records.
- Existing Day 2–5 notebooks, evaluation code, WB-only checkpoint references and Gradio demo remain in the main experiment/source folders.

## Reuse boundaries

- Reuse the YOLOv8-seg data conversion, model training, evaluation, area measurement and UI workflows as engineering starting points.
- Use the existing WB-only checkpoint only as a regression/demo artifact for its own domain.
- Inspect the separate growth-monitoring subset before using it in temporal analytics.
- Do not infer multi-species capability from M18K metrics or mix its source-specific classes with oyster maturity labels without an explicit mapping.
- Do not convert depth to physical measurements until the sensor scale, intrinsics and RGB-depth alignment are verified.

All raw files and checkpoints remain outside Git. The source repository is listed as Apache-2.0; dataset-specific terms must be checked separately.
