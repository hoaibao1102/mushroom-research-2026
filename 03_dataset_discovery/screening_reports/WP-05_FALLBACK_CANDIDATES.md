# WP-05 Fallback Candidates

**Scope:** three existing WP-03 candidates only; no new dataset search or payload download.

## C04 — Shiitake phenotype detection

**Recommendation:** `HOLD`

- `FACT`: exact Zenodo record `10.5281/zenodo.20373531`, exact linked paper `10.1038/s41597-026-07754-7`, dataset metadata CC BY 4.0; full 4.11 GB payload not acquired.
- `AUTHOR_REPORTED`: 1,782 retained originals, 6,500 augmented images, 43,752 instances, 5,375 partition images; twelve variety×phenotype labels; seven production bases.
- `UNVERIFIED`: payload integrity, actual labels, parent→augmentation lineage, sample/farm/cycle groups, quantitative independent test.
- `FACT/CONFLICT`: archived script and paper differ on 300/400 epochs and 0.0005/0.005 weight decay.
- `INFERENCE`: operationally adjacent to oyster cultivation, but shiitake labels cannot be transferred to oyster mushrooms.

**Promotion requirement:** reconcile counts, audit labels/payload, recover parent and acquisition grouping, freeze group-safe split, and resolve protocol/license layers.

## C05 — White-button RGB-D time series

**Recommendation:** `CONDITIONAL_GO` for bounded payload/grouping verification only; `HOLD` for selection/training.

- `FACT`: Mendeley dataset DOI `10.17632/8n6nr43gk3.1`, version 1, CC BY 4.0; exact method-paper link `10.3390/s26061935`.
- `AUTHOR_REPORTED`: 129 paired stitched RGB-D mosaics, 128 tracking mosaics, 12 annotated benchmark mosaics, 4,361 instances, two beds, 10-minute cadence.
- `UNVERIFIED`: payload integrity, exact 129↔128↔12 manifest, parent/time-group split, runnable author implementation.
- `FACT`: repeated observations from the same two beds mean image/patch-random splits cannot support independent biological generalization.
- `INFERENCE`: strongest fallback for a narrowed same-facility temporal segmentation/tracking question, not disease/maturity classification or cross-farm deployment.

**Promotion requirement:** authorized bounded payload QC; canonical RGB-depth-annotation manifest; parent/time grouping; defensible forward-time or bed-aware estimand; adequate support after grouping; pinned baseline or explicitly new reimplementation.

## C08 — M18K detection, pose, and growth

**Recommendation:** `HOLD`

- `FACT`: exact paper relationship to DOI `10.3390/computers14050199`; author repository pinned at `84118f23d92e6e0d6866c60b8b9d3a11e5c6e46a`.
- `AUTHOR_REPORTED`: persistent instance IDs for growth tracking; 70/10/20 split; detection/segmentation/pose baselines.
- `UNVERIFIED/HARD BLOCKER`: dataset asset license; repository code Apache-2.0 and article CC BY 4.0 do not establish data rights.
- `UNRESOLVED`: paper/release counts 2,000/423/4,652 and growth 3,838/2,121; release mapping, scene/bed/sequence grouping, temporal-ID manifest.
- `INFERENCE`: a small RGB detector might be compute-feasible after clearance; full RGB-D/pose/growth scope is too large for fallback screening.

**Promotion requirement:** verify archive license, pin one release, reconcile counts, audit annotations/IDs, and establish scene/sequence/bed-disjoint evaluation.

## Screening decision

No candidate is ready for final selection or training. C05 is the best **next bounded verification direction**, not a selected winner. C04 remains the oyster-adjacent contingency; C08 remains blocked by asset license and release/grouping uncertainty.
