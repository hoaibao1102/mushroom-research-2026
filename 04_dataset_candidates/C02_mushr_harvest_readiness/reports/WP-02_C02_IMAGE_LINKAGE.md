# WP-02 C02 annotation–image metadata linkage

## Outcome

**Metadata linkage is possible with an explicit wrapper interpretation, but literal paths do not match, every basename lookup is ambiguous, and the advertised test filenames are a subset of train.** Do not treat metadata correspondence as image/pixel integrity, independent evaluation, or scientific reproducibility. Recommendations remain pending human decision. No source names or annotations were changed.

## Complete fresh inventory, not WP-01 fallback

Fresh unauthenticated, metadata-only paginated Kaggle API:
`https://www.kaggle.com/api/v1/datasets/list/etcelab/mushr-annotated-dataset-oyster-mushrooms?pageSize=200`
with successive URL-encoded `pageToken` values. Acquisition completed **2026-10-30T04:15:38.767753+00:00**: 16 pages, first 15 with 200 entries, terminal page 11 entries and no next token; **3011 files / 3011 unique paths**. Raw pages, per-request UTC timestamps, URL, size and SHA-256 are saved in `../qc/wp02_evidence/`. `kaggle_inventory.json` records fresh mode. No dated fallback was needed and no image/archive download was requested. Inventory naming is filename-based, not MIME/pixel validation.

There are zero duplicate full paths; **1161 distinct basenames**, **1069 duplicated basename groups**, **2919 files in those groups**, and **1850 excess duplicate basename occurrences**. Exact and casefold duplicated-basename groups are identical. Complete group counts are retained in `../qc/coco_annotation_statistics.json`.

## Matching rules and exact counts

Each image entry was compared against the full inventory independently; 371 image-entry linkage rows are saved in `linkage_rows.csv` (330 train + 41 test, not 371 unique source paths).

| Rule | Train unique / missing / ambiguous | Test unique / missing / ambiguous |
|---|---|---|
| Literal full path, case-sensitive | 0 / 330 / 0 | 0 / 41 / 0 |
| Literal full path, casefold | 0 / 330 / 0 | 0 / 41 / 0 |
| Exact basename | 0 / 0 / 330 | 0 / 0 / 41 |
| Casefold basename | 0 / 0 / 330 | 0 / 0 / 41 |
| Explicit relative-wrapper interpretation | 330 / 0 / 0 | 41 / 0 / 0 |

The last rule is an **audited correspondence hypothesis**, not a repair: remove the literal leading `ANNOTATION_BATCHES/` from a comparison key only; on the Kaggle side remove just the first of two identical leading components, e.g. `Filtered_2.A/Filtered_2.A/`. Preserve the remaining subgroup and basename. Example:

- Author: `ANNOTATION_BATCHES/Filtered_2.A/0-150-0/20230222_010001.jpg`
- Kaggle: `Filtered_2.A/Filtered_2.A/0-150-0/20230222_010001.jpg`

All 371 entries have one such relative-path match, but the union is only **330 unique Kaggle paths**, because all 41 test paths also occur in train. Consequently **2681 Kaggle image paths are unmatched by either JSON under this explicit rule**. Their complete unchanged inventory names are in `unmatched_kaggle_images.json`. Under literal full-path matching all 3011 inventory paths are unmatched. Under basename-only candidate matching, multiple possible images exist for every annotation image; choosing one would silently destroy subgroup context. Do not equate the unmatched 2681 with missing labels or corruption; these JSON files may represent selected subsets.

## Cross-split overlap and annotation repetition

`split_overlaps.json` enumerates all colliding IDs and filenames:

- 41 image-ID collisions; 541 annotation-ID collisions. These are split-local identifiers and are not sufficient to establish leakage.
- 41 exact full-path overlaps, 41 basename overlaps, 41 casefold basename overlaps. Every test image filename appears in train.
- 172 train image paths and 24 test image paths have annotations; all 24 annotated test image paths are annotated in train. The remaining 17 test paths are present but annotation-empty in train.
- Canonical comparison of complete annotation fields after replacing `image_id` with exact `file_name` and omitting annotation `id` finds **all 541 test annotations identical to train annotations**. This includes class, segmentation, bbox, area, crowd fields and attributes; it is stronger than ID collision alone (`additional_checks.json`).

These published JSONs cannot serve as evidence for disjoint train/test evaluation. This audit establishes overlapping source metadata, not downloaded-image content equality, and cannot prove the effective historical loader/filtering behavior or the authors' actual training cohort. Independent held-out reproducibility should remain blocked pending human investigation; do not silently create a new split.

## Timestamp and camera/group patterns

All filenames in both JSONs parse as `YYYYMMDD_HHMMSS.jpg`. Train filename-derived range: **2022-10-03T13:00:01 to 2023-02-27T15:00:01**; test range: **2022-10-08T10:00:01 to 2023-02-27T15:00:01**. These are **timezone-unverified filename timestamps**, not verified capture times or biological cycle assignments. Every COCO `date_captured` value is numeric 0. Kaggle creationDate is upload metadata, not camera time.

| Source path group below ANNOTATION_BATCHES/ | Train entries | Test entries |
|---|---:|---:|
| Filtered_2.A/0-150-3 | 150 | 0 |
| Filtered_2.A/0-150-0 | 31 | 31 |
| Filtered_2.A/0-9 | 10 | 0 |
| Filtered_2.B/0-119 | 119 | 0 |
| Filtered_2.B/0-9 | 10 | 0 |
| Filtered_2.C/0-9 | 10 | 10 |

The test list is exactly the two source groups shown, both retained in train. A/B/C directory names and subgroup counters are metadata patterns, **not authenticated camera identity, camera synchronization, physical batch, or cycle boundaries**. Complete row-level timestamp/group evidence is in `filename_timestamp_patterns.json`. No pixel/perceptual comparisons, EXIF reads or temporal duplicate inference were authorized.

## Verification and evidence

`verify.py` independently reaggregated all 16 pages, checked the empty terminal pagination token, recomputed every linkage row and the matched/unmatched partition, and read back acquired hashes. Both pinned author JSONs were remotely refetched and proved byte-identical. Results: `independent_verification.json`; canonical annotation and casefold full-path checks: `additional_checks.json`. Counts and detailed duplicate mappings: `../qc/coco_annotation_statistics.json`. Acquisition/static audit scripts, logs, source snapshots and linkage rows are exclusive to `../qc/wp02_evidence/`.

Image bytes, actual dimensions/readability, pixel–mask alignment, near-duplicate images, shared capture episodes, label completeness and the effective training environment remain unverified. No images, Kaggle archives, checkpoints, Detectron2 installation, model execution or training occurred. No shared registry, state file, .gitignore or master manifest was modified; no commit or push was made.
