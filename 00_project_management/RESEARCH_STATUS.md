# Project status — 8 November 2026 (Day 6)

## Current goal

Build a general mushroom growth-monitoring application for fixed horizontal camera views of clusters growing from cultivation columns, bags, racks or trays. The system will recognize and optionally segment mushrooms, track clusters across repeated daily captures, measure relative growth, associate site-provided environmental records and compare cultivation units/batches. Training runs in Google Colab; the complete inference and monitoring application runs locally.

## Day 6 — Increment 0: requirements, source audit and system specification

**Status: complete.**

- Translated the project brief into operating-scene, functional, measurement, deployment and model-update requirements.
- Defined the image metadata contract around capture time, camera/view, grow unit and batch.
- Audited public code and data sources for Charisis, MushR, M18K, Wang and MushroomSegDepth; documented their distinct roles, access limitations and license checks.
- Recorded source exclusions in the exclusion registry and kept them out of the active acquisition plan.
- Defined the local-first runtime: Colab training/export; local inference, tracking, storage and dashboard; AMD acceleration as the first target and CPU as a required fallback.
- Kept the production model architecture provisional until real annotations and local runtime behavior have been tested.
- Preserved the Day 1–5 M18K experiments as domain-specific engineering evidence; they are not multi-species performance claims.
- Repository validation passed (189 checks), all 9 unit tests passed, and Python compile checks passed.
- No new dataset archive was downloaded, no upstream model code was executed and no model was trained in Day 6.

## Reusable work from Days 1–5

| Work | Evidence | Current use and limitation |
|---|---|---|
| M18K V2 EDA | `09_results/reports/M18K_V2_EDA_2026-10-30.md` | Reuse data inspection and COCO-loader patterns; dataset is button-mushroom-specific |
| YOLOv8n-seg training/evaluation | `09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md` | Reuse training, export and evaluation workflow; existing weights are not general-mushroom weights |
| Area and qualitative analysis | Day 3 reports, CSV and JSON outputs | Reuse mask-area calculations and error-review procedures; retain px² scope |
| Full-test area, Otsu and inference MVP | Day 4 reports, notebooks and outputs | Reuse image-space measurements, baseline comparison and local inference application patterns |
| NMS and RGB-D feasibility | Day 5 report and scripts | NMS result remains an eight-image pilot; depth remains uncalibrated |
| Gradio app | `07_source_code/demo/app.py` | UI prototype and regression fixture for the historical WB-only model |

Historical M18K results apply only to their recorded white-button/baby-bella datasets and splits. They do not establish cross-species or target-farm performance.

## Source roles and readiness

| Source | Status | Intended role |
|---|---|---|
| Charisis 2025 + Zenodo 15041243 | Public dataset record identified; archive/schema/sequence checks pending | Primary temporal cluster-tracking source |
| MushR 2023 code + annotations/raw images | Public model repository and annotation files identified; archive, image matching, release weights and dataset terms pending | Reusable instance-segmentation and maturity pipeline |
| M18K V2 and growth-monitoring subset | Public source; earlier analysis/model work retained | Supporting data and software baseline; not the general target-domain dataset |
| Wang 2025 | Paper available; its dataset is stated to be available on request | Seven-stage concepts and architecture findings; no exact training reproduction required |
| MushroomSegDepth 2026 | Public code; data access/licence not confirmed | Optional depth extension only |
| Six-species image collection | Public listing identified; schema and license need review | Optional species-breadth supplement; not temporal tracking data |

## Gate status

| Gate | Status | Exit requirement |
|---|---|---|
| G0 — Increment 0 | **Complete** | Target scope, system requirements, source roles and architecture documented |
| G1 — Data integration | Pending | Sample archives retrieved; schemas, class maps, sequence metadata and file integrity validated |
| G2 — Model prototype | Pending | Candidate model trained in Colab and evaluated on held-out groups |
| G3 — Tracking/measurement | Pending | Multi-date sequence tests with grow-unit-scoped identities and measurement checks |
| G4 — Local runtime | Pending | CPU fallback and AMD inference tested on target desktop |
| G5 — Application | Pending | Local storage, API and dashboard integrated |
| G6 — Field validation | Pending | Target-scene captures and operating protocol evaluated |

## Next work package: WP-07 / Increment 1

1. Retrieve Charisis Zenodo metadata and a small sample; inspect sequence IDs, timestamp fields and segmentation schema.
2. Retrieve the MushR model repository, annotation JSONs and release metadata; verify the matching raw-image paths and dataset terms before acquiring images.
3. Inventory the M18K growth-monitoring subset as optional supporting material; keep the existing WB checkpoint isolated as a domain-specific regression artifact.
4. Build source-specific dataset adapters, annotation validation, sequence metadata preservation and visual mask checks.
5. Produce a source/sample manifest with retrieval date, exact version and SHA-256 hashes.

**User input required now:** none. Any Kaggle credential, if required, is entered privately in the user's own Colab Secrets and never sent in chat.
