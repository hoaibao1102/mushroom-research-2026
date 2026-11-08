# Training and local inference guide

## Current deployment model

The project uses Google Colab for model training and heavier experiments. The production monitoring application runs locally after a versioned checkpoint/configuration package is exported. A running Colab session is not required for inference, tracking, database access or the dashboard.

## Colab responsibilities

- Download public datasets or copy selected, versioned datasets from Drive.
- Run dataset validation and visual inspection before model training.
- Train candidate models using Colab GPU.
- Save checkpoints, model configurations, label maps, preprocessing settings, dataset manifests and training logs.
- Run held-out and fixed regression evaluations.
- Export a package with a SHA-256 checkpoint hash and runtime compatibility notes.

Do not embed API tokens in notebooks or repository files. If Kaggle authentication is needed, store the token in the user's own Colab Secrets and read it at runtime.

## Local responsibilities

- Store source images, app database and outputs locally.
- Load one production model at a time by default.
- Run image inference, temporal tracking, growth calculations and dashboard queries locally.
- Prioritize AMD GPU execution via a compatible ONNX Runtime execution provider such as DirectML, subject to a real model export/compatibility test on the RX 5500 XT.
- Keep CPU inference as a required fallback. NVIDIA/CUDA support is a future provider.
- Report the actual provider and fallback reason at startup; never claim GPU acceleration if the model silently executes on CPU.

## Model package contents

Every exported model version should contain:

- model weights and architecture/config;
- generic and source-specific label maps;
- image preprocessing and prediction post-processing settings;
- dataset version and split manifest;
- training config, random seed and package version snapshot;
- validation and regression report;
- checkpoint SHA-256;
- export format and known local-runtime constraints.

## Model-update procedure

`daily images → inference archive → uncertainty/sample review → human-corrected labels → versioned training data → Colab training → regression check → explicit model promotion or rollback`.

Model-generated labels are drafts, not ground truth. Maintain the previously deployed model until the candidate passes.

## Historical M18K V2 execution record (Days 1–5)

The paths below are preserved as evidence for prior M18K experiments and are not the data layout for every future source.

- Previous M18K V2 Drive path: `/content/drive/MyDrive/M18K_Reproduction/M18K_V2_data/M18KV2/` with `train/`, `valid/`, `test/` folders and RGB/depth/COCO annotation files.
- Day 2 YOLOv8n-seg training used 3,596 train / 449 validation / 450 test images, RGB 640, 10 epochs, batch 8, seed 42 and a Colab Tesla T4.
- The two-class and WB-only checkpoints are external in the team's Drive; they are not included in this repository.
- The WB-only area and Gradio demos require the WB checkpoint and source RGB/COCO data. The original WB training notebook has a legacy test cell pointing to a two-class YAML; use the corrected WB-only evaluation records, not that old cell.
- Day 5 NMS comparison covered eight selected dense test images only. Full-test validation is pending.
- M18K depth scale/intrinsics and exact RGB-depth alignment remain unverified; physical mm² measurements were not produced.

The previous M18K evaluation and QC limitations remain recorded under `09_results/` and `04_dataset_candidates/C03_m18k_v2/`.
