# Active research and implementation scope — Day 6

The project will build a local-first computer-vision application for general mushroom growth monitoring in fixed horizontal camera views of cultivation columns, bags, racks or trays.

## Main workflow

1. Import or capture repeated images with camera/view, capture timestamp, cultivation-unit and batch metadata.
2. Detect mushrooms generally and generate instance masks where these materially improve boundaries and measurements.
3. Associate the same visible cluster across dates within its own camera/grow-unit/batch sequence.
4. Record cluster count, pixel area, bounding dimensions, relative change, growth trajectory and optional maturity estimates.
5. Join site-provided environmental measurements and summarize by cultivation unit and batch.
6. Archive images, predictions and uncertainty signals; require human review before new samples become training labels.
7. Train candidate models in Colab, run fixed regression checks, and export versioned packages for local deployment.

## Research components to reuse

- **Temporal tracking:** Charisis et al. (2025), especially mask-based association, missed-detection handling and relative growth visualization. Adapt track IDs to the target `(camera_id, grow_unit_id, batch_id)` namespace.
- **Instance segmentation and maturity:** MushR (2023), using its public implementation/annotations as a source-specific component. Its oyster maturity classes are not universal labels.
- **Existing engineering baseline:** the repository's executed YOLOv8n-seg workflow, data conversion, mask-area evaluation and Gradio application. The M18K WB-only checkpoint is a regression/demo artifact only.
- **M18K:** supporting data-loader and RGB-D/growth-subset reference, subject to independent schema/QC; it is not the sole system dataset.
- **Developmental-stage concepts:** Wang et al. (2025), as optional guidance for stage mapping. The request-only dataset is not a dependency.
- **Environment:** use records supplied by the target cultivation site in a source-agnostic schema.
- **Depth:** optional extension based on calibrated depth data; not required for the first release.

## Model decision

The production architecture is not frozen. The first implementation should use the strongest reusable code path that fits the actual data annotations and can be exported to the local runtime. YOLOv8-seg is a practical prototype candidate because this repository already has executed training/evaluation code and an inference demo. MushR/Charisis Mask R-CNN is an important alternative. Choose after Increment 1 inspects real annotations and a small Colab prototype is tested through local CPU/AMD inference.

## Scope boundaries

- A working recognition → tracking → measurement → local dashboard pipeline takes priority over exact paper benchmark reproduction.
- No request-only private dataset is required to start.
- No forced equivalence between species-specific maturity taxonomies.
- Physical dimensions are disabled until calibration/reference evidence is validated.
- No automatic promotion from pseudo-labels; reviewed data and regression evaluation are mandatory.

**Current stage:** Increment 0 complete. Next: Increment 1 — data acquisition, annotation-schema inspection and dataset adapters.
