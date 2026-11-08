# Mushroom Growth Monitoring System — Team 10

A local-first computer-vision system for observing mushroom growth in real cultivation environments. The target setup uses fixed horizontal camera views of mushroom clusters growing from columns, bags, racks or trays. The system is designed to recognize mushrooms across more than one species, associate the same visible cluster across daily captures, measure its development, and summarize results by cultivation unit and batch.

## System objectives

1. **Recognize mushrooms:** detect mushrooms in real cultivation scenes and optionally segment their visible boundaries.
2. **Track clusters over time:** associate visible clusters across captures from the same fixed camera and cultivation position.
3. **Measure growth:** retain image-space area and dimensions, cluster counts, growth changes and optional maturity estimates. Physical units require camera calibration or a known reference object.
4. **Compare cultivation units:** organize results by camera, column/tray, batch and date, with optional temperature, humidity and other environmental records.
5. **Improve through reviewed data:** save daily images and model predictions, queue uncertain examples for human review, and train candidate model versions in controlled batches. Promote a new model only after regression checks against a fixed validation set.

## Runtime strategy

- **Training and model experiments:** Google Colab GPU.
- **Production inference and application:** local computer; no running Colab session is required.
- **Primary local acceleration target:** AMD GPU support, investigated through an ONNX-compatible execution provider such as DirectML.
- **Fallback:** CPU inference must remain functional.
- **Future extension:** NVIDIA/CUDA execution-provider support can be added behind the same runtime interface.

AMD acceleration is a target, not yet a verified capability. The exported model graph and the user's RX 5500 XT / driver stack must pass a real inference test before GPU support is described as working.

## Research and implementation foundations

| Source | Reusable contribution | Scope limitation |
|---|---|---|
| Charisis et al. (2025) | Mask-based cluster association, temporal tracking, occlusion/reappearance handling, growth curves and relative sizing | Oyster mushroom time-lapse data and fixed farm setup; adapt the methods to our camera/column identifiers |
| MushR (2023) | Detectron2 Mask R-CNN code, COCO annotations, pretrained-release assets, maturity classes and flush-level grouping | Oyster-specific maturity labels; code is GPL-3.0 and the parent project is AGPL-3.0 |
| Wang et al. (2025) | Seven-stage developmental classification concepts and real-time segmentation architecture | *Pleurotus pulmonarius*; dataset is described as available on request, so exact training reproduction is not required |
| M18K / existing Day 1–5 work | Working YOLOv8n-seg data/training/inference workflow, localizable model interface, area evaluation and Gradio MVP | White-button / baby-bella data; existing WB-only weights are not a general mushroom model |
| MushroomSegDepth (2026) | Optional segmentation plus monocular depth-estimation design | Its 705-pair training dataset is not currently linked as a public download; optional extension only |

See [`03_dataset_discovery/SOURCE_DATA_AUDIT_DAY6.md`](03_dataset_discovery/SOURCE_DATA_AUDIT_DAY6.md) and the source registries for verified access paths, labels, known limitations and license notes.

## Development record

| Day | Work | Reuse in the current system |
|---|---|---|
| Days 1–5 | M18K V2 EDA; two-class and WB-only YOLOv8n-seg experiments; mask-area analysis; NMS pilot; RGB-D feasibility; working WB-only Gradio app | Reuse the data inspection, segmentation, inference, area-measurement, evaluation and UI components as starting points. The saved model is WB-specific and is not presented as a general mushroom detector. |
| **Day 6 — Increment 0** | Target requirements, public source/data audit, system architecture, model/runtime strategy and implementation gates | Establishes the build specification and selects the next data-pipeline work package. |

Earlier M18K V2 metrics remain scoped to their original white-button/baby-bella dataset and evaluation splits. They are not evidence of multi-species field performance.

## Repository guide

- [`00_project_management/`](00_project_management/) — charter, decisions, status, milestones and task board.
- [`01_domain_research/`](01_domain_research/) — cultivation workflow, target scene and open application questions.
- [`02_literature_review/`](02_literature_review/) — paper registry, methods and research gaps.
- [`03_dataset_discovery/`](03_dataset_discovery/) — public source audit and dataset/code registries.
- [`04_dataset_candidates/`](04_dataset_candidates/) — dataset-specific metadata, QC and analysis.
- [`05_research_protocols/`](05_research_protocols/) — data QC, leakage and experiment procedures.
- [`06_selected_research/`](06_selected_research/) — active system scope and reusable methods.
- [`07_source_code/`](07_source_code/) — existing data, evaluation, model and demo code.
- [`08_experiments/`](08_experiments/) and [`09_results/`](09_results/) — experiments and evidence.
- [`12_reproducibility/`](12_reproducibility/) — Colab/local deployment and execution notes.

## Current status — Day 6

**Increment 0 is complete.** The target system and deployment split are documented, public datasets and source repositories are catalogued, and source access, licensing and dataset limitations are identified. No new model has been trained in this increment. The next task is Increment 1: implement and test dataset download, extraction, inventory, annotation validation and visualization in Colab.

Run workspace consistency checks:

```bash
python scripts/validate_workspace.py
python -m unittest discover -s tests -v
```

These checks validate repository metadata and utility code; they do not certify model accuracy, dataset quality or AMD GPU compatibility.

## Data and model storage

Raw datasets, credentials, large annotation archives, model checkpoints and runtime outputs remain outside Git (for example, in Colab storage/Google Drive during training and in a local data directory during inference). Dataset acquisition scripts must record source URL, version, retrieval date and archive hash. Check each upstream dataset's licence separately from its code repository's licence.
