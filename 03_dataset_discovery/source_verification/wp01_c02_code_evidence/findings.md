# WP-01 C02: author code and Kaggle metadata audit

## Scope and decision boundary
Primary-source static audit only. No research selection, implementation, model execution, training, scientific-result verification, image/archive/weight download or annotation payload retrieval. Source snapshots are evidence, not an installed implementation. No login or credentials used. No shared registry/state/git edits made.

## Pinned source revisions
- MushR: `b22cf285402b816bbd477d83ca63c5c0265d0483`; commit time 2025-01-19T20:00:29Z; full untruncated tree saved.
- mushr-mask-r-cnn: `e8a0493b193c15c5f6129d89d7f14d89e84a8868`; commit time 2023-07-19T16:43:00Z; full untruncated tree saved.

## Main outcomes
- Code declares **four** classes including Pinning, not only the three expected maturity names; actual COCO categories remain uninspected.
- Kaggle version 1 public listing is fully enumerated: **3,011 JPG files and no annotation JSON**. Listing bytes equal dataset metadata bytes. Calling this a verified annotation package would overstate available evidence.
- Licensing differs: system AGPL-3.0, model GPL-3.0, dataset-host CC BY-SA 4.0; some source files have third-party notices. These are observed notices, not a legal opinion or full third-party license-clearance audit.
- Detectron2/PyTorch-based implementation is identifiable but environment/version compatibility is **unverified**. No dependency install or runtime check was performed; any current Detectron2 compatibility statement would be an estimate.
- Shell scripts and saved YAMLs disagree; local paths, missing referenced folders, 80-vs-four class settings and unspecified runtime versions prevent claiming turnkey reproducibility from this static audit.

## Dependencies / environment
See `static_imports.json` for all source imports and `module_headers.json` for each retrieved Python/shell header. Model code directly imports Detectron2, torch, OpenCV (`cv2`), NumPy, tqdm and scikit-learn; stdlib and local predictor/flush_predictor imports are also recorded. Hardware system code uses Raspberry Pi/GPIO/I2C and Adafruit interfaces; it is not the detector training runtime. Complete pinned repository trees expose no requirements/environment/lock/build container manifests. README links latest Detectron2 installation guidance without pinning Python, torch, CUDA or Detectron2. No compatibility certification is possible here.

## Annotated-dataset provenance chain and version limit
The pinned system README explicitly labels the exact annotated Kaggle slug as “Images annotated for Mask R CNN” and separately links the exact `ETCE-LAB/mushr-mask-r-cnn` implementation. Its adjacent “Complete Un-Annotated RAW Images” link points to the distinct raw-image Kaggle slug. Claim C02-CODE-001 reproduces the annotated/code link lines exactly; the complete README is preserved. The annotated Kaggle description points back to the system repository and states: “This repository contains the annotated files that we used to train the model.” These author/host statements establish an explicit project-to-annotated-host relationship, not proof that annotation JSON is currently included (the complete file metadata inventory shows only JPG entries).

**Dataset version is not historically pinned by this chain.** The README URL has no version suffix. Kaggle currently reports version 1, created in November 2024, after the 2023 paper/code. This audit records the access-time version metadata; it does not establish which historical bytes, annotations or release were used for the paper. No dataset content hashes were computed because payload download was prohibited. Saved access-log SHA-256 values identify retrieved metadata responses only. Do not equate the current hosted image count with paper training/test instance counts.

## Split and data limitations
Train and test JSON filenames are explicit, but payloads were deliberately not fetched. No annotation-level counts, per-class counts, validation split, split ratio, seed-governed partition generator, camera/time/group independence or leakage audit is claimed. Kaggle directories alone do not establish any of those. Metadata inventory and source category declarations are different evidence layers.

## Primary-source claims and exact excerpts
### C02-CODE-001
The system repository links both the annotated Kaggle dataset and the separate Mask R-CNN implementation.[1] https://github.com/ETCE-LAB/MushR/blob/b22cf285402b816bbd477d83ca63c5c0265d0483/README.md

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: MushR Dataset links
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
  - [Images annotated for Mask R CNN](https://www.kaggle.com/datasets/etcelab/mushr-annotated-dataset-oyster-mushrooms)
  - [MushR Mask R CNN](https://github.com/ETCE-LAB/mushr-mask-r-cnn)
```

### C02-CODE-002
MushR repository-level LICENSE is GNU AGPL v3; individual source headers must also be respected.[2] https://github.com/ETCE-LAB/MushR/blob/b22cf285402b816bbd477d83ca63c5c0265d0483/LICENSE

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: LICENSE opening
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
GNU AFFERO GENERAL PUBLIC LICENSE
```

### C02-CODE-003
MushR application module header explicitly grants AGPL version 3 or later.[3] https://github.com/ETCE-LAB/MushR/blob/b22cf285402b816bbd477d83ca63c5c0265d0483/automated-image-capture/mushrimager.py

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: lines 3-6
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
```

### C02-CODE-004
Arducam camera module has its own three-clause BSD-style redistribution notice, not an AGPL-only header.[4] https://github.com/ETCE-LAB/MushR/blob/b22cf285402b816bbd477d83ca63c5c0265d0483/automated-image-capture/arducam_multicamera.py

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: lines 3-15
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
#      * Neither the name of the copyright holder nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
```

### C02-CODE-005
Mask R-CNN repository-level license is GPL v3, distinct from system repository AGPL and Kaggle CC BY-SA.[5] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/LICENSE

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: LICENSE opening
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
GNU GENERAL PUBLIC LICENSE
```

### C02-CODE-006
Model modules contain GPL-3.0-or-later headers; train_net.py, inference.py and predictor.py also retain Facebook copyright notices.[6] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train_net.py

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: lines 1-17
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
# Copyright (c) Facebook, Inc. and its affiliates.

#  Copyright (C) 2022, 2023 Anant Sujatanagarjuna

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
```

### C02-CODE-007
README delegates dependency installation to Detectron2 official latest instructions; no pinned runtime environment is supplied in the complete repository tree.[7] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/README.md

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: Dependencies
- Notes: Complete tree.json checked: no requirements file, environment.yml, pyproject.toml, setup.py or Dockerfile; no Detectron2/PyTorch/CUDA/Python pin located. Compatibility with a current environment is UNVERIFIED; no install or execution attempted.

Exact excerpt:
```text
To run inference, please follow the official instructions to [install
detectron2](https://detectron2.readthedocs.io/en/latest/tutorials/install.html).
```

### C02-CODE-008
Code uses Detectron2 DefaultTrainer and COCO instance registration and evaluation.[6] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train_net.py

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: lines 40-58,80-81,101
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
        evaluator_list.append(COCOEvaluator(dataset_name, output_dir=output_folder))
```

### C02-CODE-009
README designates separate COCO JSON files for training and testing; annotation payloads and actual image membership were not audited.[7] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/README.md

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: Annotations
- Notes: Tree metadata confirms JSON blobs of 7,337,338 and 1,064,392 bytes; neither downloaded. Counts, category IDs, annotation validity, leakage and split proportions remain unknown.

Exact excerpt:
```text
1. Train: [MushR_Dataset_V1.1_2023_04_04-COCO.json](MushR_Dataset_V1.1_2023_04_04-COCO.json)
2. Test: [MushR_Dataset_2023_06_29_TEST-COCO.json](MushR_Dataset_2023_06_29_TEST-COCO.json)
```

### C02-CODE-010
Training entry point explicitly declares FOUR classes: Pinning, Not-Ready, Ready, Overdue; assuming exactly the three requested maturity classes is contradicted by this source declaration.[6] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train_net.py

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: lines 175-188
- Notes: This is a code metadata declaration, not validation of annotation category contents. No three-class remapping protocol found in the training entry point.

Exact excerpt:
```text
    MetadataCatalog.get("MushR_Dataset_V1.1").thing_classes = ["Pinning",
                                                                "Not-Ready",
                                                                "Ready",
                                                                "Overdue"]
```

### C02-CODE-011
Both COCO registrations hardcode image root /home/sho/Desktop; portable reproduction needs path adaptation.[6] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train_net.py

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: lines 175-184
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
    register_coco_instances("MushR_Dataset_V1.1", {},
                            "MushR_Dataset_V1.1_2023_04_04-COCO.json",
                            "/home/sho/Desktop")
```

### C02-CODE-012
train.sh requests one GPU, upstream Mask R-CNN R50-FPN 3x config, crop enabled, 40,000 iterations, batch 8 and learning rate 0.0001.[8] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train.sh

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: full script
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
last_checkpoint=$(cat train_2023_04_20/last_checkpoint)

./train_net.py --num-gpus 1 \
               --config-file ~/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml \
	       INPUT.CROP.ENABLED True \
               DATASETS.TRAIN \(\"MushR_Dataset_V1.1\",\) \
               SOLVER.MAX_ITER 40000 \
               SOLVER.IMS_PER_BATCH 8 \
               DATASETS.TEST \(\"MushR_Dataset_2023_06_29_TEST\",\) \
               SOLVER.BASE_LR 0.0001 \
               OUTPUT_DIR "train_2023_06_29_03/" \

```

### C02-CODE-013
continue_training.sh differs: one million iterations, checkpoint period 1,000, batch 8 and learning rate 0.001, with a local checkpoint path.[9] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/continue_training.sh

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: full script
- Notes: Script does not pass --resume despite its name; actual optimizer/scheduler continuation semantics were not executed or verified.

Exact excerpt:
```text
last_checkpoint=$(cat train_2023_04_04/last_checkpoint)

./train_net.py --num-gpus 1 \
               --config-file train_2023_04_04/config.yaml \
	       MODEL.WEIGHTS "train_2023_04_04/$last_checkpoint" \
	       INPUT.CROP.ENABLED True \
               DATASETS.TRAIN \(\"MushR_Dataset_V1.1\",\) \
               SOLVER.MAX_ITER 1000000 \
               SOLVER.CHECKPOINT_PERIOD 1000 \
               SOLVER.IMS_PER_BATCH 8 \
               DATASETS.TEST \(\"MushR_Dataset_2023_06_29_TEST\",\) \
               SOLVER.BASE_LR 0.001 \
               OUTPUT_DIR "train_2023_06_29_04/" \

```

### C02-CODE-014
Saved training YAML differs from shell overrides: crop false, batch 2, LR 0.00025, empty test list, seed -1, and ROI_HEADS.NUM_CLASSES 80 rather than declared four.[10] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train_2023_04_04/config.yaml

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: INPUT.CROP,DATASETS,MODEL.ROI_HEADS,SOLVER,SEED
- Notes: All saved YAMLs retain ROI_HEADS.NUM_CLASSES 80. Current train.sh does not override NUM_CLASSES. This is a static configuration mismatch, not a demonstrated runtime failure or result invalidity.

Exact excerpt:
```text
    NUM_CLASSES: 80
```

### C02-CODE-015
Saved training configuration describes CUDA Mask R-CNN with ResNet-50/FPN, polygon masks, BGR input, horizontal flip, train shortest-edge choices 640..800 and max edge 1333.[10] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train_2023_04_04/config.yaml

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: MODEL, INPUT
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
  MASK_FORMAT: polygon
```

### C02-CODE-016
eval.sh uses --eval-only and the named test COCO dataset; COCOEvaluator is the selected evaluation path.[11] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/eval.sh

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: full script
- Notes: No metrics reproduced, and result/log/prediction payloads not fetched. Saved July eval YAML references train_old/model_final.pth, unlike eval.sh checkpoint construction.

Exact excerpt:
```text
last_checkpoint=$(cat train_2023_04_04/last_checkpoint)

./train_net.py --num-gpus 1 \
	       --eval-only \
	       --config-file "train_2023_04_04/config.yaml" \
	       MODEL.WEIGHTS "train_2023_04_04/$last_checkpoint"\
               DATASETS.TEST \(\"MushR_Dataset_2023_06_29_TEST\",\) \
               OUTPUT_DIR "eval_2023_07_19_new" \

```

### C02-CODE-017
README evaluation-result link points to eval_2023_07_19, whereas the pinned tree contains eval_2023_07_19_new; inference scripts reference absent train_2023_04_20 directory.[7] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/README.md

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: Evaluation
- Notes: Verified against complete pinned tree.json and saved inference shell scripts. No attempt to repair or run author code.

Exact excerpt:
```text
Our evaluation results of the trained model are given in [eval_2023_07_19](eval_2023_07_19).
```

### C02-KAGGLE-001
Kaggle public metadata reports version 1, CC BY-SA 4.0, last updated 2024-11-20T11:14:14.987Z and total size 7,898,278,464 bytes.[12] https://www.kaggle.com/api/v1/datasets/view/etcelab/mushr-annotated-dataset-oyster-mushrooms

- Status: VERIFIED_FROM_PRIMARY_SOURCE; confidence: HIGH.
- Location: currentVersionNumber,licenseName,lastUpdated,totalBytes
- Notes: Static primary-source audit only; no execution of source code.

Exact excerpt:
```text
"licenseName":"CC BY-SA 4.0"
```

### C02-KAGGLE-002
Kaggle description reports 34,400 images accumulated over ten months; this is a raw collection claim, not the annotated-host file count.[12] https://www.kaggle.com/api/v1/datasets/view/etcelab/mushr-annotated-dataset-oyster-mushrooms

- Status: REPORTED_BY_SOURCE_NOT_AUDITED; confidence: HIGH.
- Location: description
- Notes: No raw-image dataset or image contents downloaded. The annotated dataset listing contains 3,011 JPG entries, not 34,400.

Exact excerpt:
```text
We captured and accumulated 34,400 images over ten months to ensure a comprehensive dataset.
```

### C02-KAGGLE-003
Complete 16-page metadata inventory contains 3,011 unique JPG paths, no annotation JSON, totaling 7,898,278,464 bytes; top-level counts Filtered_2.A=1096, Filtered_2.B=1159, Filtered_2.C=756.[13] https://www.kaggle.com/api/v1/datasets/list/etcelab/mushr-annotated-dataset-oyster-mushrooms

Computed from primary API metadata, not image or annotation content. The listing has no explicit train/test path split. Folder names A/B/C cannot establish maturity classes or independence.

```json
{
  "access_utc": "2026-10-23T09:55:30.012442+00:00",
  "pages": 16,
  "pagination_complete": true,
  "listed_files": 3011,
  "unique_paths": 3011,
  "total_bytes": 7898278464,
  "extension_counts": {
    ".jpg": 3011
  },
  "top_level_counts": {
    "Filtered_2.A": 1096,
    "Filtered_2.B": 1159,
    "Filtered_2.C": 756
  },
  "non_image_files": []
}
```

### Published model asset metadata
Release metadata only; no weight/archive fetched.[14] https://api.github.com/repos/ETCE-LAB/mushr-mask-r-cnn/releases

```json
[
  {
    "tag": "p1",
    "prerelease": true,
    "published_at": "2023-07-19T21:20:47Z",
    "name": "mushr-mask-r-cnn-release.tar.gz",
    "size": 417443840,
    "url": "https://github.com/ETCE-LAB/mushr-mask-r-cnn/releases/download/p1/mushr-mask-r-cnn-release.tar.gz"
  }
]
```
Archive contents, weight architecture, trained category mapping and checkpoint/config match are UNVERIFIED.

## Sources

[1] https://github.com/ETCE-LAB/MushR/blob/b22cf285402b816bbd477d83ca63c5c0265d0483/README.md — MushR/README.md
[2] https://github.com/ETCE-LAB/MushR/blob/b22cf285402b816bbd477d83ca63c5c0265d0483/LICENSE — MushR/LICENSE
[3] https://github.com/ETCE-LAB/MushR/blob/b22cf285402b816bbd477d83ca63c5c0265d0483/automated-image-capture/mushrimager.py — MushR/automated-image-capture/mushrimager.py
[4] https://github.com/ETCE-LAB/MushR/blob/b22cf285402b816bbd477d83ca63c5c0265d0483/automated-image-capture/arducam_multicamera.py — MushR/automated-image-capture/arducam_multicamera.py
[5] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/LICENSE — mushr-mask-r-cnn/LICENSE
[6] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train_net.py — mushr-mask-r-cnn/train_net.py
[7] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/README.md — mushr-mask-r-cnn/README.md
[8] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train.sh — mushr-mask-r-cnn/train.sh
[9] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/continue_training.sh — mushr-mask-r-cnn/continue_training.sh
[10] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/train_2023_04_04/config.yaml — mushr-mask-r-cnn/train_2023_04_04/config.yaml
[11] https://github.com/ETCE-LAB/mushr-mask-r-cnn/blob/e8a0493b193c15c5f6129d89d7f14d89e84a8868/eval.sh — mushr-mask-r-cnn/eval.sh
[12] https://www.kaggle.com/api/v1/datasets/view/etcelab/mushr-annotated-dataset-oyster-mushrooms — Kaggle MushR annotated dataset metadata
[13] https://www.kaggle.com/api/v1/datasets/list/etcelab/mushr-annotated-dataset-oyster-mushrooms — Kaggle complete paginated file metadata
[14] https://api.github.com/repos/ETCE-LAB/mushr-mask-r-cnn/releases — Author model release metadata
