# C05 Subset Reconciliation

## Scope and evidence classes

This is the output of one bounded metadata/source-only pass. No dataset payload, image, archive, model or annotation file was downloaded.

- `FACT`: directly verified metadata identity or visible record property.
- `AUTHOR_REPORTED`: stated by the dataset record or primary method paper; payload not independently audited.
- `INFERENCE`: bounded interpretation, explicitly not treated as fact.
- `NOT_VERIFIED`: evidence required but absent from the inspected sources.

## Source ledger

| Source | Role | Relevant evidence |
|---|---|---|
| Mendeley dataset `10.17632/8n6nr43gk3.1` | Release record | 129 mosaics; RGB/depth/COCO description; `YYYYMMDD_cycleXX`; 10-minute cycle; CC BY 4.0. |
| DataCite record for `10.17632/8n6nr43gk3.1` | DOI identity | Title, creators, publisher, year and versioned DOI identity. |
| Method paper `10.3390/s26061935` | Experimental methods | 128 tracking mosaics; 12 benchmark RGB images; patches; instance totals; YOLO parameters; two beds and one collection cycle. |
| Data-description paper `10.1016/j.dib.2026.113085` | Dataset description | Dataset/release context; no inspected manifest closed the subset gaps. |

## Count reconciliation

| Count | Evidence class | Meaning supported by source | Relationship to other counts |
|---:|---|---|---|
| 129 | AUTHOR_REPORTED | Total stitched RGB-depth mosaics in the public release description. | Canonical file inventory and relation to the paper's 128 were not available. |
| 128 | AUTHOR_REPORTED | Stitched mosaics used as inputs for segmentation/tracking in the method paper; 298 trajectories were manually inspected across these frames. | The excluded/additional release mosaic is not identified. |
| 12 | AUTHOR_REPORTED | RGB mosaics used for the YOLO segmentation benchmark; each 615 × 988 before patching. | Exact filenames and membership in the 128/129 sets are not published in the inspected text. |
| 4361 | AUTHOR_REPORTED | Manually polygon-annotated mushroom instances across the 12 benchmark images. | This is an instance count, not an image or independent-sample count. |
| 3445 | AUTHOR_REPORTED | Instances reported as used for training. | No image/patch membership manifest found. |
| 916 | AUTHOR_REPORTED | Instances reported as used for testing. | No image/patch membership manifest found. |

Arithmetic consistency of 3445 + 916 = 4361 does not establish that the split was performed at image, patch, instance, time or bed level.

## Questions and decisions

### 1. Why 129 versus 128 versus 12?

- **AUTHOR_REPORTED:** 129 is the release count, 128 is the method's temporal analysis count, and 12 is the YOLO benchmark image count.
- **NOT_VERIFIED:** why one release mosaic is absent from the method-paper count.
- **NOT_VERIFIED:** whether release versioning, failed processing, deliberate exclusion or a counting convention caused the difference.
- **INFERENCE:** 12 was drawn from the acquisition described in the paper because Section 2.4 points back to Section 2.1 preprocessing. This does not identify membership.

No unreported explanation is accepted.

### 2. Can the 12 benchmark images be identified?

**No, not from the public metadata and primary text inspected in this pass.** The paper provides dimensions, patch dimensions and aggregate annotation totals but no 12-filename list. The release metadata provides a general filename convention, not benchmark membership.

Status: `NOT_VERIFIED`.

### 3. Can train/test image and patch membership be reconstructed leakage-free?

**No.** The inspected sources do not provide:

- the 12 parent filenames;
- a parent-image train/test assignment;
- patch coordinates or patch filenames;
- patch-to-parent relationships;
- edge/overlap/empty-patch handling;
- an instance-to-image split ledger.

The reported 3445/916 instance counts cannot be safely converted into a split. Generating one now would be a new protocol, not reproduction, and is prohibited by this audit.

Status: `NOT_VERIFIED`; leakage-safe reconstruction unavailable.

### 4. Are COCO masks provided for all 129?

- **AUTHOR_REPORTED:** the release includes pixel-level cap annotations in COCO format and reproduction notes mention `_annotations.coco.json`.
- **NOT_VERIFIED:** that every RGB mosaic among all 129 appears in the COCO `images` table and has corresponding annotation coverage.
- **NOT_VERIFIED:** whether annotation coverage is full-release, 128-frame, 12-image or another subset.

A global dataset-description sentence is not a per-file coverage audit.

### 5. Do time/bed identifiers support forward-time or bed-aware evaluation?

- **FACT:** public reproduction notes document names in `YYYYMMDD_cycleXX` form and define cycles as 10-minute intervals.
- **AUTHOR_REPORTED:** acquisition used two beds, one growth cycle and four collection dates.
- **INFERENCE:** lexical date/cycle ordering may support temporal ordering after the file inventory is verified.
- **NOT_VERIFIED:** explicit bed ID in filenames, COCO records or a manifest.
- **NOT_VERIFIED:** independence of repeated mushroom instances across frames.

Forward-time evaluation is conceptually possible but not currently reconstructable as a historical benchmark. Bed-aware evaluation is blocked by absent record-level bed membership; two beds would also yield a fragile estimate.

## Leakage analysis

The acquisition is a repeated time series of the same cultivation beds. Therefore:

1. adjacent mosaics can contain the same physical mushrooms;
2. patches from one mosaic share scene and acquisition context;
3. patches from neighboring times can be near-duplicates in content;
4. an instance-level random split can distribute observations of the same mushrooms across train and test;
5. an ungrouped patch split can distribute one parent mosaic across train and test.

Consequently, neither mosaic counts nor annotated instance counts represent independent biological samples. A valid future protocol must preserve parent and temporal provenance before any split, but this audit does not generate that split.

## Baseline reconstruction fields

| Field | Evidence | Status |
|---|---|---|
| Models | YOLOv8-seg and YOLO11-seg | AUTHOR_REPORTED |
| Initialization | Pretrained weights | AUTHOR_REPORTED; checkpoint identity unspecified |
| Original image | 615 × 988 | AUTHOR_REPORTED |
| Patch size | 256 × 128 | AUTHOR_REPORTED |
| Network input | 256 × 256 | AUTHOR_REPORTED |
| Optimizer | Adam | AUTHOR_REPORTED |
| Learning rate | 0.01 | AUTHOR_REPORTED |
| Batch | 32 | AUTHOR_REPORTED |
| Initial epochs | 50 | AUTHOR_REPORTED |
| Additional epochs | YOLOv8: 30; YOLO11: 20 | AUTHOR_REPORTED |
| Exact model sizes | Not stated in inspected text | NOT_VERIFIED |
| Ultralytics/package versions | Not stated | NOT_VERIFIED |
| Seeds/determinism | Not stated | NOT_VERIFIED |
| Augmentation/config YAML | Not recovered | NOT_VERIFIED |
| 12-image manifest | Not recovered | NOT_VERIFIED |
| Image/patch split manifest | Not recovered | NOT_VERIFIED |
| Released `best.pt` files | Table names a weight file generically; availability/identity not verified | NOT_VERIFIED |

## Reconciliation conclusion

The count discrepancy is **described but not resolved**. The evidence supports three distinct scopes but not their exact set membership. C05 therefore fails the subset/provenance gate required for `GO_FOR_DEEP_QC` in this work package.

- Subset reconciliation: `INCOMPLETE`
- 12-image identity: `NOT_VERIFIED`
- Leakage-safe historical split: `NOT_RECONSTRUCTABLE_FROM_INSPECTED_METADATA`
- All-129 mask coverage: `NOT_VERIFIED`
- Forward-time key: `PARTIALLY_SUPPORTED_BY_DATE_CYCLE_NAMING`
- Bed-aware key: `NOT_VERIFIED`
