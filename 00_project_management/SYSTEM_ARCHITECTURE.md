# System architecture — Colab training, local inference

## 1. Runtime topology

```text
PUBLIC DATASETS + REVIEWED FIELD IMAGES
                  |
                  v
        DATA INGESTION / QC
   image IDs, labels, timestamps,
   grow-unit mapping, dataset manifest
                  |
          +-------+--------+
          |                |
          v                v
   GOOGLE COLAB        LOCAL DATA STORE
   GPU TRAINING        images + SQLite
   validation          metadata + review queue
   checkpoints                |
          |                   v
          |           LOCAL INFERENCE API
          |          model adapter / preprocessing
          |          AMD provider -> CPU fallback
          |                   |
          +---- model package |
                    |         v
                    |    DETECTION / SEGMENTATION
                    |         |
                    |         v
                    |    TEMPORAL TRACKER
                    |         |
                    |         v
                    |    GROWTH / MATURITY ANALYTICS
                    |         |
                    +----> MODEL REGISTRY
                              |
                              v
                        LOCAL DASHBOARD
                        history / charts / export
```

The app must not depend on a live Colab session. Colab is an offline training environment that exports a versioned model package to local storage.

## 2. Logical components

### Data ingestion

- Dataset adapters for COCO, YOLO and source-specific annotation formats.
- Stable image IDs and checksums; preserve original image paths and metadata.
- Normalize annotations into a project-level record while retaining the source category and source annotation ID.
- Keep source-specific label maps; map a label to generic `mushroom` only when the source annotation actually identifies a mushroom.

### Model layer

- Common inference contract: input image + metadata → zero or more detections containing class, confidence, bounding box and optional mask.
- Existing YOLOv8n-seg workflow is the first reusable implementation path because training, evaluation and a Gradio inference demo already exist in this repository.
- The current M18K WB-only checkpoint is a regression/demo artifact for its original domain, not the multi-species production checkpoint.
- MushR Detectron2 Mask R-CNN and Charisis MMDetection/Mask R-CNN are research implementations to inspect/adapt; they are not required to be forced into the first deployment.
- Model architecture and input resolution remain provisional until the prepared datasets and local inference resource tests are available.

### Runtime provider interface

- `AMD_GPU`: first acceleration target; test ONNX export and ONNX Runtime DirectML compatibility on the RX 5500 XT and actual Windows driver stack.
- `CPU`: required fallback and reference implementation.
- `NVIDIA_GPU`: future provider using the same model adapter contract; not required for the first release.
- Startup diagnostics must report the selected provider and fallback reason. A failed GPU probe must not prevent the app from starting in CPU mode.

### Tracking

- Track clusters at the cluster level, not individual fruit bodies by default.
- Use mask overlap, bounding geometry, appearance and sequence metadata to associate detections between captures.
- Keep an explicit unmatched/missed-track state and allow reappearance after temporary occlusion.
- Record events such as new, matched, temporarily missing, reappeared, harvested/removed and manually corrected.
- Tracking decisions must be reviewable; no deletion of old cluster history when a cluster disappears.

### Growth and environment analytics

- Compute pixel area, mask dimensions, relative change and growth trajectory per track.
- Convert pixel measurements to physical units only when camera geometry or a known-size reference is configured and validated.
- Join timestamped environmental data by grow unit/batch and a documented time window.
- Use species- and cultivation-specific maturity labels only when source mapping is defined.

### Persistence and user interface

- SQLite for the first local deployment; keep database access behind a repository layer so a server database can be added later.
- Store image metadata, predictions, tracks, growth measurements, environmental samples, review decisions and model versions.
- Dashboard views: overview by batch/grow unit, daily image review, individual track history, growth charts, environment comparison and export.

## 3. Training-to-inference model package

Every exported model package should contain:

- model weights (`.pt`, `.onnx` or model-native format);
- architecture/configuration and label map;
- preprocessing/postprocessing configuration;
- source dataset manifest and version;
- training parameters and package versions;
- validation and regression-test report;
- SHA-256 checkpoint hash;
- runtime compatibility note and known limitations.

## 4. Model update lifecycle

`deployed model → collect predictions → human review → versioned dataset → Colab candidate training → regression evaluation → model promotion or rejection`.

Promotion is explicit and reversible. The currently deployed model remains available until the candidate passes. Pseudo-labels are never silently accepted as ground truth.

## 5. Deployment constraints

The initial target is the user's i3-10105 / RX 5500 XT 8 GB / 12 GB RAM desktop. Default to single-image inference, configurable image size and lazy model loading. Test peak VRAM/RAM, latency, cold start and long-run stability before selecting the production model. The AMD path is not considered complete until measured on the target machine.
