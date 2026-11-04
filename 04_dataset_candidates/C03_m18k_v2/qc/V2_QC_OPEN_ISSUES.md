# M18K V2 QC — findings and unresolved issues

| Check | Status | Evidence / qualification |
| --- | --- | --- |
| COCO streaming read | DONE IN NOTEBOOK | 700,589 polygon instances across three JSON files |
| RGB file paths found | DONE IN NOTEBOOK | No unresolved RGB paths reported |
| Depth filename matches | DONE IN NOTEBOOK | 4,495/4,495 matched; no alignment/units guarantee |
| Category mapping | DONE IN NOTEBOOK | ID 1 BB, ID 2 WB, ID 0 background/unmapped |
| Non-positive bounding boxes | FLAGGED | 6 records; repair/exclusion decision pending |
| Missing segmentation field | BASIC SCHEMA ONLY | No missing polygon format reported; not manual shape validity |
| BB class integrity | NEEDS HUMAN REVIEW | 858 BB vs 699,731 WB; stratified visual/source review |
| Exact image hashes | NOT RUN | SHA-256 audit disabled for Colab Drive performance |
| Near duplicates / same scene across splits | NOT RUN | Filename disjointness is insufficient |
| 4,652 vs 4,495 release count | UNRESOLVED | Review archive list vs annotated RGB entries |
| Depth pixel units, intrinsics, RGB alignment | UNVERIFIED | Sample depth plots alone insufficient |
| Dataset license | UNVERIFIED | Review upstream terms and attribution obligations |

**Do not mark dataset QC G1 as GO** until critical checks are reviewed and recorded. Count discrepancies should be investigated, not silently removed from the summary.


## Day 3 follow-up (3 November 2026)

- Khang's 12-image spot-check surfaced five train/test pairs with identical 64-bit perceptual dHash values. This is a **near-duplicate candidate screen**, not a proof of identical content or split leakage. Require exact SHA-256 comparisons, side-by-side RGB and group/acquisition review. See `09_results/wb_error_analysis/similarity_spotcheck.csv`.
- Raw WB overlay figures for test images `004252.png` and `004472.png` appear to include non-mushroom scene regions; annotation/renderer interpretation **NOT VERIFIED**. Inspect original COCO polygon coordinates and categories before declaring GT defects.
- The Day 3 area analysis measured 30 images and cannot clear full-image-content QC or establish physical calibration.

## Day 4 follow-up (4 November 2026)

The submitted `09_results/dataset_qc/day4_submitted/` zip includes new SHA-256 checks and a reviewer `VERIFIED_GOOD` label on `004252.png` and `004472.png`, but **does not clear earlier open flags**. Its five compared train/test filenames differ from the original Day 3 five dHash-equal candidate pairs; one test SHA hash reports `FILE_NOT_FOUND`. No scene-group independence has been established. The images marked good still merit original COCO polygon inspection because other area/segmentation overlays appear suspicious. The submitted report is preserved without accepting its broad conclusion. See `09_results/reports/Day4_QC_Interpretation_2026-11-04.md`.

Day 4 full-test area errors are measured relative to available COCO masks. If annotations are questionable, those metrics must be interpreted accordingly; no new claim of verified physical area or guaranteed leakage-free performance is made.
