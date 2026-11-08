# C04 — Charisis oyster mushroom time-lapse dataset

## Source identity

- Paper: [A novel Mask R-CNN-based tracking pipeline for oyster mushroom cluster growth monitoring in time-lapse image datasets](https://doi.org/10.1016/j.compag.2025.110590)
- Dataset: [Zenodo record 15041243](https://zenodo.org/records/15041243)
- Species: *Pleurotus ostreatus*.
- Paper-reported dataset: 6,382 high-resolution images and 37,004 annotated cluster instances from four time-lapse experiments.

## Why it is relevant

The target system needs to associate the same visible mushroom cluster across repeated captures. Charisis directly studies instance segmentation and temporal cluster tracking, including mask-based association and cases where clusters are occluded or temporarily hidden. The paper also describes relative sizing using substrate dimensions as a reference.

The paper's reported results and methods are research findings, not reproduced project results. No standalone author GitHub repository for this paper was verified. The UCD thesis identifies supplementary code in Annex D; its executable completeness remains to be inspected.

## Increment 1 checks — not yet completed

1. Retrieve the Zenodo API record and archive file list; record version, licence, file sizes and SHA-256.
2. Download a small sample rather than the full archive first.
3. Inspect image dimensions, timestamps, experiment/sequence fields, camera/view metadata and class map.
4. Determine whether annotations include persistent ground-truth track IDs. Do not assume that frame-level COCO instance IDs are temporal identities.
5. Visualize masks on the original images and check whether substrate references/camera geometry are available.
6. Design splits by independent experiment/sequence rather than by random adjacent frames.

## Adaptation boundary

This is the primary public tracking foundation, but its oyster-mushroom farm setup does not automatically represent the target vertical-column scene or other species. The implementation will keep track IDs scoped to `(camera_id, grow_unit_id, batch_id)` and use target-scene validation later.

**Status:** public dataset record identified; archive/schema/sequence validation pending. No data is stored in this repository.
