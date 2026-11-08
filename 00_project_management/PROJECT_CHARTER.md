# Project charter — Mushroom Growth Monitoring System

## Problem and motivation

Mushroom cultivation requires repeated observation of growth, maturity and differences between cultivation conditions. Manual observation makes it difficult to quantify how individual visible clusters change over time or compare growth across cultivation units. The project will develop a computer-vision monitoring system that works with fixed horizontal camera views of mushrooms growing from columns, bags, racks or trays.

## Overall objective

Build a usable local application that can recognize mushrooms across more than one species, associate visible clusters across daily images, calculate growth measurements, organize results by cultivation unit and batch, and incorporate environmental measurements. Use existing research implementations and datasets as starting points and adapt them to the target cultivation scene.

## Active system scope

- **Input:** daily RGB images from fixed or repeatable camera positions, with camera/station ID, capture timestamp, cultivation-unit ID and batch ID. Optional depth and environmental sensor files may be attached.
- **Recognition:** general mushroom detection as the initial target. Instance masks are preferred where they materially improve cluster boundaries and measurements.
- **Tracking:** persistent cluster IDs within a configured camera/cultivation-unit view, including temporary disappearance, occlusion and post-harvest changes.
- **Measurement:** image-space area, bounding-box dimensions, relative size change, cluster count and growth trajectories. Convert to physical dimensions only after a known-size reference or reliable camera calibration is available.
- **Developmental assessment:** maturity/stage is an optional capability. Source-specific labels must be mapped deliberately; species-specific stage schemes must not be treated as interchangeable without review.
- **Cultivation analysis:** group records by camera, column/tray, batch and date; support temperature, humidity and other environmental observations.
- **Incremental model improvement:** retain images and prediction metadata, select uncertain or informative cases for review, add only approved labels to training data, train candidate versions in Colab and promote them only after regression checks.

## Deployment and compute

- Training and heavier model experiments run in Google Colab GPU sessions.
- The complete inference and monitoring application runs locally after model artifacts are exported.
- AMD GPU inference is the primary acceleration target. ONNX Runtime with a compatible DirectML provider is an initial candidate to test; CPU inference is mandatory as a reliable fallback.
- NVIDIA/CUDA support is a future runtime provider, not a requirement for the first working release.
- The user's target desktop is an Intel i3-10105, AMD Radeon RX 5500 XT (8 GB VRAM) and 12 GB system RAM. The model must be evaluated for practical memory consumption on this class of hardware.

## Research foundations

- Charisis et al. (2025): instance segmentation, cluster-level tracking and temporal growth monitoring.
- MushR (2023): Mask R-CNN code/data, maturity assessment and flush-level grouping.
- Environmental data: ingest site-provided temperature, humidity and other readings, linked to the relevant camera, cultivation unit, batch and timestamp.
- Wang et al. (2025): seven developmental stages and real-time segmentation concepts for *Pleurotus pulmonarius*.
- M18K and the existing Day 1–5 work: reusable YOLO segmentation, data conversion, area evaluation and interactive-inference components.
- MushroomSegDepth (2026): optional RGB-only depth estimation concept, subject to data and software availability.

## Non-goals for the first working release

- Exact numerical reproduction of every source paper.
- Guaranteed support for every mushroom species without representative training examples.
- Physical dimensions from uncalibrated pixel/depth values.
- Automatic retraining on unreviewed pseudo-labels.
- Cloud-hosted inference or a permanent Colab dependency.
- Robotic harvesting actuation.

## Success criteria

1. The system imports images with cultivation and timestamp metadata and detects/segments mushrooms.
2. Repeated images from the same view can be linked into persistent cluster histories with auditable track decisions.
3. Per-cluster and per-cultivation-unit growth measurements are stored and visualized over time.
4. Model and dataset versions are traceable; reviewed data can be added for subsequent Colab training.
5. The local application runs without Colab, supports CPU inference, and has a tested AMD acceleration path before that path is called supported.
6. A candidate model update cannot replace the current deployed version without passing a fixed regression check.

## Boundaries and integrity

Keep raw data, large archives, credentials and checkpoints outside Git. Preserve source attribution and comply with each dataset and code license independently. Record uncertainty, maintain source-specific class maps, and do not present earlier white-button metrics as general mushroom performance. Human label review and real-farm validation remain required for deployment claims.
