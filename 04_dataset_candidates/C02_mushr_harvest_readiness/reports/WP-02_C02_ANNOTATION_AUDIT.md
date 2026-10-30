# WP-02 C02 annotation and author-code static audit

## Outcome — recommendations pending human decision

The author annotations are available and internally reference-consistent, but this is **not scientific reproducibility**. Do not approve an independent held-out evaluation or training on these declared splits: every test filename is present in train, and **all 541 test annotations are identical to train annotations after replacing local image IDs by source filenames and omitting annotation IDs**. No files were repaired, filtered, or remapped. No image content, model, training or author script was executed.

## Provenance and correction to WP-01 interpretation

Resolved GitHub `commits/HEAD` on 2026-10-30 UTC to `e8a0493b193c15c5f6129d89d7f14d89e84a8868` (same as WP-01). README lines 11–12 explicitly designate train and test JSON; the claim that author annotations were unavailable/unspecified is incorrect. README lines 16–18 designate the training config directory and train.sh. Original responses, complete pinned source snapshots, UTC acquisition times and SHA-256 are under `../qc/wp02_evidence/`. Both original JSON byte streams are under `../dataset_metadata/`; the two-row `../qc/wp02_c02_download_manifest.csv` contains pinned raw URLs and content types. No images, archives, weights, DS02 requests, dependency installations or training occurred.

| Split / unchanged author JSON | Bytes | SHA-256 |
|---|---:|---|
| Train `MushR_Dataset_V1.1_2023_04_04-COCO.json` | 7337338 | `f2aa01c1ea5042c3b177a3dc7a165ba56f493463b3543f59afe9cc21beace12a` |
| Test `MushR_Dataset_2023_06_29_TEST-COCO.json` | 1064392 | `94e5800f4c39578af2bddf4dbc3900d788e6e0cee815f9ddc72c3c10dcfe808d` |

The API tree and commit record are saved, not inferred from a mutable branch link. Source JSON was independently fetched again from each pinned raw URL and byte equality verified.

## Actual categories and paper comparison

| Original category ID | Original name | Train instances | Test instances |
|---:|---|---:|---:|
| 1 | Pinning | 0 | 0 |
| 2 | Not-Ready | 723 | 251 |
| 3 | Ready | 1344 | 198 |
| 4 | Overdue | 692 | 92 |
| Total | | 2759 | 541 |

Four category definitions, **three populated classes**. This reconciles paper Table 2 with author code's four-name list, without inventing a new label mapping. Paper Table 2 counts match exactly, including per-class counts (saved `03_dataset_discovery/source_verification/wp01_paper_evidence/MushR_publisher_full_text.txt`, lines 345–348). Paper figure labels 1/2/3 are not these source COCO IDs 2/3/4. No silent deletion of Pinning or contiguous-ID conversion is authorized.

## COCO integrity results

| Check | Train | Test |
|---|---:|---:|
| Image entries / unique IDs | 330 / 330 | 41 / 41 |
| Annotation entries / unique IDs | 2759 / 2759 | 541 / 541 |
| Category entries / unique IDs | 4 / 4 | 4 / 4 |
| Images with annotations | 172 | 24 |
| Images without annotations | 158 | 17 |
| Declared dimensions | 330 × 3040×4056 | 41 × 3040×4056 |
| Polygon annotations | 2759 | 541 |
| RLE annotations | 0 | 0 |
| iscrowd=0 | 2759 | 541 |
| Area range (source units, px² implied) | 227–178348 | 227–26488 |
| Polygon shoelace area discrepancy > max(1 px², 1% declared area) | 21 | 14 |

All required arrays exist. Zero within-split duplicate image/annotation/category IDs, orphan image/category references, duplicate file_name strings, invalid/nonfinite/nonpositive dimensions, bbox lengths/values/sizes, out-of-frame bboxes, invalid/nonpositive areas, area greater than bbox area (1 px² tolerance), invalid crowd values or contradictory `is_crowd` aliases. All polygons have even coordinate counts ≥6, finite coordinates, positive shoelace area, and coordinates inside declared image dimensions. Polygon extrema and bbox agree within 0.11 px. FruitingState attributes agree with category names. RLE checks are implemented but not exercised because none exist. Self-intersection, rasterized mask area, overlap-union semantics, pixel alignment, image readability and actual dimensions were **not verified**. Declared dimensions are metadata only.

Declared versus floating-point polygon shoelace areas differ beyond the stated diagnostic threshold in 21 train and 14 test annotations; largest absolute differences across all annotations are 321.9600000001956 and 53.5 px² respectively. This may reflect exporter/rasterization conventions and is not proof of corrupted masks. Exact IDs/differences remain in `annotation_issues.json`; no correction was applied. Empty image entries are not automatically negative examples: completeness must be adjudicated.

## Static author training/configuration audit (no execution)

Complete pinned files are in `../qc/wp02_evidence/author_code/`; line-addressed extracts are in `static_code_excerpts.json`.

- `train_net.py:175–188` registers the exact two JSON files, roots both at absolute `/home/sho/Desktop`, and sets both metadata lists to `[Pinning, Not-Ready, Ready, Overdue]`. Portable image-root/linkage adaptation would require explicit later approval, not an annotation repair here.
- `train_net.py:131–139` merges the supplied config and CLI options then freezes config. It does not explicitly set the ROI class count to 3 or 4.
- README points at `train_2023_04_04/config.yaml`, but `train.sh:4` uses an external `~/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml`, not that saved config. Its external contents/version were not retrieved. `train.sh` requests crop=True, 40000 iterations, batch=8, LR=0.0001, test dataset above, output `train_2023_06_29_03/`. Its first line reads `train_2023_04_20/last_checkpoint` but the value is not used subsequently.
- Saved `train_2023_04_04/config.yaml` has `MODEL.ROI_HEADS.NUM_CLASSES: 80` (line 196), MASK_ON true, ImageNet-pretrained MSRA R-50 weights (line 270), LR=0.00025, batch=2, 40000 iterations, output `train`. Other NUM_CLASSES values belong to other heads; do not conflate them with ROI_HEADS.
- `continue_training.sh` uses the saved config/checkpoint and requests 1000000 iterations, batch=8, LR=0.001, output `train_2023_06_29_04/`. `eval.sh` uses that saved config plus checkpoint and the declared test registration, output `eval_2023_07_19_new`.
- Both saved evaluation configs have ROI_HEADS.NUM_CLASSES=80 (line 200). The July config points to `train_old/model_final.pth`, LR=0.00025, batch=2, 40000 iterations; April points to `train_2023_04_20/model_0009999.pth`, LR=0.00015, batch=2, 400000 iterations and a train registration `MushR_Dataset_V1.1_2023_04_20` not registered in this entry point.
- Thus source files alone do not establish the effective published training run, checkpoint lineage, exact dependency versions, or a coherent class-head configuration. Do not assert runtime failure or correct these discrepancies without execution/approval. README's Detectron2 installation link is not an environment lockfile.

## Split warning and gates

There are 41 colliding image IDs and 541 colliding annotation IDs across split-local namespaces; those collisions alone are not evidence of leakage. More materially: 41/41 exact test paths (and basenames) occur in train; 24 test images carry annotations in both; all 541 test annotations repeat train content ignoring local IDs. The 17 empty test images are empty in train as well. This is directly evidenced metadata overlap, not a pixel duplicate claim and not proof of what the authors actually loaded in a historical run. Treat held-out independence and published evaluation reproducibility as blocked pending human investigation. See the separate image-linkage report.

## Verification and limits

`verify.py` independently reparsed source JSON and statistics, recomputed class/ID counts and all linkage rows, reaggregated all 16 Kaggle pages, read back all 30 acquired-source hashes, and refetched both JSON sources to prove byte identity. It returned PASS for metadata verification only (`independent_verification.json`). `additional_checks.py` verified canonical annotation overlap and casefold exact paths (`additional_checks.json`). Scripts refuse existing evidence targets rather than overwrite them. Gate decisions remain recommendations pending human; source availability is not scientific reproducibility.
