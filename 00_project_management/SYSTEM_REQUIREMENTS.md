# System requirements — Day 6 baseline

## 1. Functional requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| FR-01 | Import images from local folders or an application upload, preserving original files | Import test with supported JPG/PNG and reproducible image IDs |
| FR-02 | Record capture time, camera/station, cultivation unit (column/tray/rack), batch and optional species | Metadata validation rejects missing required association fields or records explicit unknowns |
| FR-03 | Detect mushrooms in general cultivation scenes | Held-out qualitative and quantitative evaluation on more than one mushroom type |
| FR-04 | Produce instance masks when the selected model supports them | Visual overlays and mask integrity tests |
| FR-05 | Associate clusters across daily captures from the same configured view | Stable IDs on a labelled or manually reviewed multi-date sequence; track events logged |
| FR-06 | Handle missed detections, temporary occlusion, reappearance and harvest/removal events | Synthetic and real-sequence tests; no silent deletion of historical tracks |
| FR-07 | Calculate per-instance pixel area, bounding dimensions and relative change | Unit-tested calculations with synthetic masks and stored image-space units |
| FR-08 | Aggregate growth curves and counts by cultivation unit and batch | Query and chart tests using known fixture data |
| FR-09 | Store environmental observations and associate them with a cultivation unit/batch and time | Import test for timestamped temperature/humidity records |
| FR-10 | Allow optional maturity/stage prediction with source-specific class mapping | Unknown/unsupported class mappings remain explicit; no forced cross-species label equivalence |
| FR-11 | Queue uncertain detections for human review and store user-corrected annotations | Review state and accepted/rejected labels are persisted |
| FR-12 | Create a versioned training dataset and run retraining in Colab | Dataset manifest, config, model checkpoint and training log linked by version |
| FR-13 | Evaluate a candidate model against a fixed regression set before deployment | Promotion report shows no unreviewed regression and records the chosen thresholds |
| FR-14 | Run the deployed application locally without an active Colab runtime | Offline inference/application smoke test after model and dependencies are installed |
| FR-15 | Export records and reports | CSV export and annotated-image export tests |

## 2. Non-functional requirements

- **Local-first:** application database, image archive and inference run on the local machine; network access is needed only for optional external acquisition or updates.
- **Resource-aware:** stream images from disk, use configurable image size and one-at-a-time inference by default, and avoid keeping several large models resident simultaneously.
- **Runtime modularity:** model loading and tensor execution are behind a provider interface. AMD acceleration is prioritized; CPU remains supported; NVIDIA is a future provider.
- **Reproducible training:** store source dataset versions, annotation-map version, train/validation groups, random seed, package versions, model configuration and checkpoint hash.
- **Safe model updates:** no automatic deployment from pseudo-labels. Human-reviewed samples and regression tests are mandatory.
- **Traceability:** each prediction records model version, input image, processing time, confidence and inference configuration.
- **Maintainability:** separate data ingestion, model inference, tracking, analytics, persistence and user interface.

## 3. Input data contract

Each captured image should be associated with:

- `image_id` — unique immutable image key;
- `captured_at` — capture timestamp with timezone or documented local timezone;
- `camera_id` — fixed camera or view identifier;
- `grow_unit_id` — column, shelf, tray, rack or equivalent physical cultivation unit;
- `batch_id` — production/cultivation batch;
- `species` — optional known species; otherwise `unknown`;
- `image_path` and source checksum;
- optional `environment_sample_id` or timestamp-linked environmental values.

A tracking sequence is keyed by at least `(camera_id, grow_unit_id, batch_id)`. Track IDs are scoped to a sequence namespace; they are not assumed globally transferable between cameras or different physical grow units.

## 4. Measurement contract

- Base area is reported in `px²`; width/height are in `px`.
- Relative growth compares measurements for the same track under comparable image geometry.
- Physical units (`mm`, `cm`, `mm²`) are disabled until calibration/reference evidence is recorded.
- Growth rate records include the time interval and method; a one-day difference must not be presented as a biological rate without the elapsed-time metadata.
- Harvest/removal and camera movement are explicit events, not inferred as zero growth.

## 5. Learning and update policy

1. Archive new daily images and the model predictions that generated them.
2. Prioritize low-confidence, high-disagreement, novel-appearance and manually selected cases for annotation.
3. Treat model-generated labels as drafts only.
4. Add human-reviewed examples to a versioned dataset.
5. Train a candidate model in Colab and preserve the previous deployed model.
6. Evaluate candidate on a fixed regression set plus the new target data.
7. Promote only when acceptance rules pass; otherwise keep the previous checkpoint and record the failure.
