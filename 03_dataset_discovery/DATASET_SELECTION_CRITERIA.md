# Dataset selection criteria — general mushroom monitoring

The first release needs a useful combination of whole-scene mushroom recognition, optional instance masks, repeated-view imagery for cluster tracking, and enough metadata to group results by camera, cultivation unit, batch and date. No single candidate is assumed to satisfy every task.

## Required evidence by task

| System task | Required dataset evidence | Current candidates / role |
|---|---|---|
| General mushroom recognition | Full-scene images with reliable mushroom/non-mushroom labels across more than one useful species | MushR and Charisis for oyster scenes; M18K as button-mushroom supporting data; target-site images later needed for domain fit |
| Instance segmentation | Full-scene masks or polygons with image-to-annotation correspondence | MushR COCO; Charisis masks; M18K annotations as a supporting format/model workflow |
| Cluster tracking and growth | Ordered repeated captures from the same camera/view, stable grow-unit or experiment identifiers, and preferably reviewed temporal IDs | Charisis as primary temporal source; MushR hourly capture series; inspect M18K growth subset as a separate supporting source |
| Maturity/developmental stage | Explicit class definitions, stage examples and source/species information | MushR oyster maturity classes; Wang seven-stage concepts; target-site stage definitions may be required |
| Species breadth | Representative examples from multiple cultivated species | Optional six-species image collection for image-level classification/robustness; target-scene examples remain necessary |
| Environmental analysis | Timestamped sensor readings linkable to a cultivation unit/batch | Site-provided sensor exports; define a source-agnostic schema |
| Depth/3D extension | Aligned RGB-depth pairs with verified scale, intrinsics and calibration | M18K RGB-D as optional; MushroomSegDepth only after code licence and dataset availability are resolved |

## Selection and split principles

- Select and combine sources by role; do not force a single dataset to solve every task.
- Inspect real archive contents and annotation semantics before training.
- Preserve source-specific labels and category IDs. Do not merge maturity taxonomies across species without a documented mapping and human review.
- Split by independent time-lapse experiment, sequence, camera capture, cultivation cycle, tray or batch wherever such IDs exist. Adjacent frames/crops from one scene must not leak across train/validation/test.
- Distinguish full-scene frames from cropped objects. Crop counts are not independent scene counts.
- A dataset that contains only object crops or image-level species labels cannot validate whole-scene cluster tracking.
- Dataset licences and code licences are checked separately. Unknown terms block redistribution, not necessarily private exploratory inspection.
- “Available on request” is not a public download and is not required for the first system build.
- Excluded source identifiers listed in `excluded_datasets/EXCLUDED_DATASETS.csv` are not candidates for retrieval, import or analysis.

## Current selection status

No single production dataset has been selected. Increment 1 should first validate small samples from Charisis and MushR, then inspect M18K's growth-monitoring subset only if it contributes a distinct need. Model architecture selection remains pending annotation-schema and local-runtime evidence.
