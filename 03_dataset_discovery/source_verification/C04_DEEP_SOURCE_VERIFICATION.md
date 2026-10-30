# C04 — WP04 targeted source, code and protocol verification

## Decision and scope

- **Outcome:** live identity/version/license evidence confirmed; small author-listed code archive retrieved, checksum-verified and statically audited. **Exact experimental reproduction is BLOCKED / protocol only partially specified and source-inconsistent.** This is not a training or performance reproduction.
- **Training authorization: NO. Dataset selection: NONE. Human approval: PENDING.** No whole C04 dataset, dataset images, DS02 assets, dependencies, author-code execution, fitting, commits or pushes were performed.
- Repository inspected on `research/wp-04-deep-verification`, HEAD `7076719a2ee61a4922068d6326b8261be716af14`. Scope is this report and candidate-local evidence only.
- Live primary checks began 2026-10-30 05:29:51 UTC; successful code recovery 05:55:14–05:55:22 UTC. Detailed UTC timestamps, original/final URLs, sizes, HTTP results and hashes are in the evidence logs and acquisition manifest.

## Evidence and primary-source identity

Evidence directory: [`../../04_dataset_candidates/C04_shiitake_phenotypes/qc/wp04_evidence/`](../../04_dataset_candidates/C04_shiitake_phenotypes/qc/wp04_evidence/).

| ID | Primary source and saved locator | Direct observation |
|---|---|---|
| S1 | https://zenodo.org/api/records/20373531 ; `zenodo_record.json` | HTTP 200; record 20373531; exact DOI `10.5281/zenodo.20373531`; title **Phenotypic image dataset of naturally grown shiitake mushrooms across multiple varieties and growth stages**; version `1.0`, revision 3, concept record 20373530 / DOI `10.5281/zenodo.20373530`; publication date 2026-05-25. |
| S2 | https://zenodo.org/api/records/20373531/versions and `/versions/latest`; `zenodo_versions.json`, `zenodo_latest.json` | One listed version; latest resolves to exact record 20373531 at this check. This is an observation, not a guarantee against future versions. |
| S3 | https://www.nature.com/articles/s41597-026-07754-7 ; `publisher.html`, `publisher_text.txt` | HTTP 200 full article despite cookie-error query on final URL; DOI `10.1038/s41597-026-07754-7`, Scientific Data 13, 1394 (2026); published 29 June 2026, version of record 07 October 2026. Full-text reviewed. |
| S4 | https://api.datacite.org/dois/10.5281/zenodo.20373531 ; `datacite.json` | Live registration metadata retrieved; supplementary identity evidence, not a substitute for Methods. |
| S5 | https://zenodo.org/records/20373531/files/shiitake_mushroom_code.zip ; `shiitake_mushroom_code.zip` | 5,724,836 bytes, author-listed code-only asset; exact metadata MD5 matched `42aa41b73d6410e76e5c27438a9a2b15`; SHA-256 `e813782a8b746d458f8a7985f34358a2fe7fe5e9d32b17b84f1ba1712725fc89`. |
| S6 | Saved WP03 `wp03_stream_a/paper_shiitake_fulltext.txt`, `zenodo_20373531.txt`, source ledger/access log/candidates | Read as historical primary captures; input hashes retained in `wp03_input_hashes.json`. They contain the same material count and license conflict under investigation. |

Article and Zenodo list the same nine authors: Xinfa Wang, Yongqi Zhu, Huamei Cao, Yafeng Han, Yuxin Tong, Xiujuan Wan, Bihua Chen, Chaohui Zhang and Guang Zhang. Article Data Records, Data availability and Code availability explicitly link the exact version DOI, not merely a similarly titled dataset.

### Access and separate licenses

1. **Dataset record:** S1 `metadata.access_right=open`, `metadata.license.id=cc-by-4.0`. The large file is listed as `shiitake_mushroom_dataset.zip`, 4,110,366,941 bytes, metadata checksum `md5:bf0793493a416257157c521fbb996292`. **NOT DOWNLOADED; checksum not independently validated.** Listed open availability is not a verified full-data transfer.
2. **Article:** S3 Rights and permissions, `publisher_text.txt` line 275, expressly **CC BY-NC-ND 4.0**. This is not CC BY 4.0 and does not transfer the article's restrictions onto every dataset record or authorize sharing adapted article material. The abstract's academic-research wording is descriptive; the explicit record license is recorded separately.
3. **Code:** S1's record-level license is CC BY 4.0, but the archive contains a full `LICENSE` headed GNU Affero General Public License v3, `pyproject.toml` declares AGPL-3.0, and Ultralytics module headers carry AGPL-3.0. **Do not relabel bundled upstream code CC BY merely from the deposition license.** Author-added top-level scripts lack a distinct clear license notice; their exact rights/provenance remain a human/legal clarification item. Record-level metadata and embedded upstream terms are separate layers, not a resolved relicensing chain.
4. Normal urllib API content transfer timed out; curl whole-code transfer timed out/reset, leaving incomplete bytes. Range requests with query parameters returned 403. The canonical no-query file URL accepted curl ranges (206); all parts were length-checked, concatenated and final MD5 validated. `curl_recovery_log.json` is authoritative recovery timing. `code_acquisition.json` records the later local verification time, not an additional remote retrieval. Partial/probe assets are not valid archives and are recorded separately. No dataset URL was fetched.

## Count accounting — unresolved, not normalized

Source locators are S3 Abstract (live text line 38; WP03 line 601), Data collection (65; WP03 700), Data augmentation (78,86; WP03 710,720), Experimental setup (93; WP03 726), Technical Validation (WP03 742).

| Count | Author meaning | Audit status |
|---|---|---|
| 2,600 | Raw photographs collected before screening | PAPER_REPORTED; no raw manifest inspected. |
| 1,782 | Retained original high-resolution images | PAPER_REPORTED; excludes images with unverifiable origins according to Data labeling. |
| 6,500 | Expanded/augmented images; another sentence calls this the expanded training dataset | PAPER_REPORTED; inclusion/exclusion of originals and per-split coverage unresolved. |
| 43,752 | Annotated mushroom **instances** after augmentation, not image count | PAPER_REPORTED; not recomputed from labels. |
| 5,375 | Annotated images divided train/validation 8:2 | PAPER_REPORTED and unreconciled with 6,500. |

Independent arithmetic in `static_audit_summary.json`: 6,500 − 5,375 = **1,125**; an exact 8:2 allocation of 5,375 would be **4,300 train / 1,075 validation**, but these are **derived expectations, not observed split totals**. Do not assign 1,125 images to inference/test without a manifest. It also does not equal the original count (1,782 − 1,125 = 657). No source establishes that these differences are distinct originals, unused augmentations, unlabeled inference images or a reporting error. Code archive has no run `args.yaml`, `results.csv`, `best.pt` or `last.pt` to settle the historical denominator. Dataset not downloaded: no file-level count or population verification is claimed.

## Split, augmentation and independence

- **PAPER_REPORTED:** augmentation uses rotation, vertical flip, brightness, saturation and noise; data expanded from originals, then enhanced images are used for benchmarks. Technical Validation says repeated 8:2 splits and three training iterations/model, reporting averages across validation evaluations. Seeds and actual split memberships are not supplied in the reviewed paper or candidate-specific script.
- **UNRESOLVED:** whether offline augmentation was before or after allocation; whether all derivatives of each original were grouped; parent IDs, raw-to-derived mapping, augmentation seeds/probabilities/ranges and exact split manifests. Narrative ordering and augmentation alone **do not prove leakage**. The risk is unverified derivative/parent overlap and biological dependence, not an established leakage finding.
- **PAPER_REPORTED:** seven production bases, cumulative three-year collection and growth cycles; capture logs/biological tags were used to screen traceability, and EXIF was stripped. This does not provide released sample-level farm/session/cycle/bed/log/specimen IDs or demonstrate farm-disjoint evaluation. Group separation is **NOT_REPORTED as an implemented split rule**, not disproved.
- **PAPER_REPORTED independent inference set:** unlabeled raw images reserved as entirely unseen for qualitative inference. This is not a labeled independent quantitative test. File-level independence remains UNVERIFIED; no sample IDs or group assignments were inspected. All reported quantitative scores are validation scores, not an external held-out-test estimate.
- For a future authorized protocol: freeze verified original-parent and farm/session/cycle grouping first, allocate independent groups before training-only augmentation, preserve original/derived hashes and lineage, keep validation/test unaugmented and sealed, and predeclare class/metric conventions. This is a **reviewer recommendation**, not the authors' verified protocol or authorization to create a split now.

## Actual code/static audit

S5 state: **URL_REPORTED → ARCHIVE_RETRIEVED → CHECKSUM_PINNED → CODE_AUDITED_STATIC**. No author Git commit is pinned; the archived `ultralytics/__init__.py` self-identifies as **8.3.47**, not proof of an exact upstream commit or the historical run environment. All 1,068 ZIP members inventoried, unsafe paths/symlinks rejected and uncompressed-total bounded; 643 text members preserved under synthetic safe filenames with original-path/hash index. Binaries, images and bytecode were not executed or decoded. A notebook's code cells were inspected as JSON/text only. See `archive_inventory.json`, `text_index.json`, `config_excerpts.md`, `static_trace_excerpts.json`, `notebook_code_cells.json`.

### Model, configuration and label findings

| Topic | Paper | Actual archived evidence / assessment |
|---|---|---|
| Core variants | YOLOv8n, YOLOv9t, YOLOv10n, YOLO11n | Root `train.py` has **one** active YOLO11 architecture call. Generic framework model-family configs are not run-specific benchmark scripts. |
| Extra comparisons | Faster R-CNN, RT-DETR, YOLO11s and YOLO11n | Generic RT-DETR framework presence does not reproduce comparison runs. No candidate-specific driver/config/log for all comparisons found. |
| Model construction | No pre-trained weights | `YOLO(model=r'ultralytics/cfg/models/11/yolo11.yaml')`; checkpoint load commented. Model parser defaults absent scale to first `scales` key `n`, so static path supports nano selection. `engine/model.py` passes weights only if `self.ckpt` exists; YAML construction has no checkpoint. Default `pretrained: True` alone is **not** evidence that this script loads pretrained weights. Historical executions remain unverified. |
| Class semantics | Three varieties × four phenotypes | Root `data.yaml` has exactly twelve IDs `0..11`: L00101–L00104, L00201–L00204, L00301–L00304. `single_cls=False`. This is joint variety/phenotype detection, not simply a four-class detector; no class merging authorized. |
| Data paths | images/labels basename pairing | Active root YAML points to machine-specific absolute `E:\software\Pycharm\files\Yolov11 improvements\data\noexif\images\train` and `...\val`; test path is commented. These are not portable published manifests. A different `ultralytics/cfg/datasets/data.yaml` contains unrelated three-class names `Un4047`, `BN207`, `AK58` and YOLOv10 machine paths; root script does **not** select that file. Preserve conflict; do not replace root twelve-class schema with bundled unrelated sample config. |
| Input label format | YOLO `.txt`: cls, normalized center x/y, width/height | `ultralytics/data/utils.py::verify_image_label` statically checks five columns for box labels, coordinate bounds and class range; detection trainer overrides model `nc` from dataset metadata. No C04 actual label contents or counts were inspected. Template model `nc:80` is therefore not evidence of an 80-class C04 run. |
| Epochs | 400 | Root script explicitly **300**, overriding default config `epochs:400`: material reproduction conflict. |
| Optimizer/batch/image | SGD, batch 8; adjusted input resolution unspecified in narrative | Root script SGD, batch 8, **imgsz=640**, workers 6, GPU `0`, `close_mosaic=10`, `resume=False`, `cache=False`. |
| Learning schedule | lr 0.01, decay 0.005, warmup 3, momentum 0.8→0.937 | Defaults: lr0 .01, **weight_decay .0005**, warmup_epochs 3.0, warmup_momentum .8, momentum .937. Script does not override decay. Trainer scales optimizer decay by batch×accumulation/nbs; the literal default differs tenfold and cannot be silently repaired to paper value. |
| Randomness | Repeated splits, three runs/model | Default seed 0, deterministic True; script contains no seed loop or split-generation driver. This does not disprove author runs, but does not reproduce them. |
| Augmentation | Offline expanded pool with listed transforms | Runtime defaults include hsv, mosaic 1.0, flip-left-right .5, rotation 0, flip-up-down 0, plus scale/translate; do not equate these online defaults with the described offline expansion. Root ResizeVOCdatasets.py resizes VOC boxes/images and is not an audited 1,782→6,500 lineage pipeline. |
| Inference entrypoints | Adapted YOLO training/inference scripts claimed | Root `predict.py` imports `unet.Unet` and uses unrelated `ShanghaiGreen` class names; `predict_qt.py` imports GUI modules. Neither is evidence of the paper's YOLO comparison evaluation runner. Missing external dependencies/import targets are static portability concerns, not executed failures. |

### Evaluation and dependency detail

- S3 Evaluation indicators says mAP IoU .5, while Technical Validation reports both AP50 and AP50–95. This wording is not an instruction to set NMS IoU=.5. Archived detector validator constructs `torch.linspace(0.5,0.95,10)`; default `iou:.7` is an **NMS** threshold, `split:val`, `max_det:300`, and confidence unset in YAML resolves to `.001` in validator; default prediction confidence is distinct. `metrics.py` computes AP with interpolated precision/recall; these are framework implementation observations, not run-log verification of historical metric settings.
- Reported YOLO11n validation results in text: P .947, R .929, F1 .938, AP50 .961, AP50–95 .844; Table-3 discussion separately says F1 .936. Preserve this contextual discrepancy, do not average it. No historical scores independently recomputed.
- Dependencies are broad minimum ranges in `pyproject.toml`, not a lockfile/run environment: Python >=3.8, torch >=1.8.0 (Windows excludes 2.4.0), torchvision >=.9.0, numpy >=1.23.0, opencv >=4.6.0, pillow >=7.1.2, pyyaml >=5.3.1, scipy >=1.4.1 and others. Full parsed list is in `static_audit_summary.json`. PyTorch/CUDA/cuDNN/driver/package exact versions and seeds for reported runs remain unknown. No packages installed.

## Required clarification / gate recommendations (reviewer assessment)

**G0 — source/provenance recommendation: CONDITIONAL, PENDING_HUMAN.** Exact primary identity, latest version at check, declared dataset license, separate article license and code artifact are established. Do not promote to unconditional research eligibility: require human review of code licensing layers, intended reuse permissions, count contradiction and biological/task relevance. No dataset is selected.

**G1 — protocol/data acceptance recommendation: HOLD / NOT_READY, PENDING_HUMAN.** Request (1) authoritative image/instance/split count ledger resolving 1,782/6,500/43,752/5,375; (2) original-parent→augmentation manifest and split chronology; (3) farm/session/cycle/log/specimen metadata and independent-inference IDs; (4) exact run configs and seeds for each variant/repetition, 300-versus-400 epochs and .0005-versus-.005 decay explanation; (5) labeled external test or explicit validation-only claim scope; (6) locked runtime/dependency/commit provenance, dedicated inference/eval drivers and any checkpoints/logs necessary for historical reproduction. Future limited data inspection itself needs human authorization; no download approval is implied here.

**Protocol classification:** PARTIALLY_SPECIFIED_WITH_MATERIAL_CONFLICTS; CODE_AVAILABLE_STATIC_AUDITED; EXACT_REPRODUCTION_BLOCKED; INDEPENDENT_QUANTITATIVE_TEST_NOT_ESTABLISHED. Reported validation performance is not a reproduced benchmark and not proof of label quality or leakage-free generalization.

**Farm fit:** available farm has white/grey oyster mushrooms, not shiitake. The C04 joint variety/phenotype ontology cannot be treated as the farm's labels. At most this is a conditional methodological/adjacent-species reference; no direct-transfer or deployment-performance claim is supported.

## Verification scope and retained artifacts

`acquisition_manifest.csv` is metadata/article/code-only, with URLs, timestamps, byte counts, SHA-256 and record MD5 where applicable; upstream dataset entry is metadata-only/not-acquired. `verification.json` checks identity, exact code bytes/checksum, static-artifact consistency, count arithmetic, required output scope and explicit no-training state. PASS means these structural/provenance checks passed, **not** scientific validation or historical reproduction. Network failure logs are retained; a complete recovered code ZIP is not confused with earlier partials. No shared registries, shared state, gitignore, commits or pushes were changed by this task.


## Canonical authorization statement

Training authorization: NO. Dataset selected: NO. Research gap validated: NO. Human scientific approval: PENDING.
