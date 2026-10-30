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
