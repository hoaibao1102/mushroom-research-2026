# M18K V2 dataset QC protocol — updated 2026-10-30

This protocol applies to candidate C03 while preserving the shared group's QC gates. The notebook has executed **initial** steps, not full QC.

1. **Provenance and license:** record exact V2 source, archive hash, access date, licensing and reproducible extraction. **Pending human verification.**
2. **Inventory and schema:** enumerate split RGB/depth files and stream COCO JSON; record category ID-name mapping; flag malformed/missing fields. **Initial audit executed:** 4,495 images, 700,589 annotations, 6 nonpositive boxes.
3. **Visual annotation audit:** stratify by BB/WB, size, density, split and depth quality; have a reviewer inspect at least a predeclared sample and record disagreements. **Pending.**
4. **RGB-D consistency:** verify filename pairing, image/depth dimensions, finite/valid depth values, camera calibration and units. **Filename matches verified; geometry not fully verified.**
5. **Independent units and leakage:** record scene/tray/batch/time where available; check exact hashes, perceptual similarity and grouped splits, not just filename equality. **Pending.**
6. **Reconcile counts:** compare 4,495 COCO records against release documentation's 4,652 count, and document any difference. **Pending.**
7. **Training input export:** log polygon conversion losses and validate visualized YOLO labels on train and validation before training; keep test untouched.
8. **Archive evidence:** publish lightweight source manifests, QC exception table and reviewer decision; keep all raw payloads and checkpoints outside Git.

**Gate G1 remains NEEDS_MORE_EVIDENCE** until critical conditions are addressed. Null or missing evidence is never a pass.
