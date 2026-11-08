# Source code and implementation assets

This directory keeps project-owned utilities and adapters. Historical M18K code remains available as a reference, but dataset-specific class assumptions must not leak into the general system.

## Existing components

- `data/inspect_dataset.py`: dependency-light inventory tool for folders, image types, COCO JSON, image references, categories, segmentation types and basic annotation consistency.
- `data/build_wb_dataset.py`: M18K V2 White Button-only COCO-to-YOLO conversion/rebuild utility. Keep it isolated as a historical data-preparation tool; do not use its WB-only filtering for general data.
- `evaluation/`: mask-area, full-test area and dataset-QC scripts from Days 1–5.
- `features/day5_rgbd_feasibility/`: M18K-specific depth-file feasibility checks; no physical-unit calibration was established.
- `demo/app.py`: previously user-confirmed Gradio inference demo around the WB-only M18K checkpoint. It is a working UI prototype and regression fixture, not the general detector.

## New project implementation boundaries

The production application should separate dataset adapters, model adapters, inference providers, temporal tracking, growth analytics, persistence and UI. New adapters should retain the original source category IDs/labels and create an explicit mapping to the project schema. Do not copy third-party code into this directory until the source licence has been checked and its attribution/terms are retained.
