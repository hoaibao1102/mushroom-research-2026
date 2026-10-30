# WP-01: Candidate C02 Source Verification Dossier

**Candidate ID:** C02  
**Candidate Working Name:** MushR Oyster Mushroom Harvest Readiness  
**Target Dataset:** Kaggle `etcelab/mushr-annotated-dataset-oyster-mushrooms`  
**Associated Paper:** Sujatanagarjuna et al., *Agriculture* 2023, 13, 1533 (DOI: `10.3390/agriculture13081533`)  
**Associated Code Repositories:**  
- System Repo: `https://github.com/ETCE-LAB/MushR` (Commit: `b22cf285402b816bbd477d83ca63c5c0265d0483`)  
- Model Repo: `https://github.com/ETCE-LAB/mushr-mask-r-cnn` (Commit: `e8a0493b193c15c5f6129d89d7f14d89e84a8868`)  
**Evaluation Date:** 2026-10-23  
**Review Status:** COMPLETED (Full-Text Paper, Repository Code, and Kaggle Metadata Audited)  
**Gate G0 Recommendation:** NEEDS_MORE_EVIDENCE (Conditional Hold)  

---

## 1. Task B1 — Dataset Identity & Kaggle Inventory

Primary metadata verification was performed using Kaggle's public web and dataset APIs across all 16 pages of metadata. No image payloads or model weights were downloaded.

| Property | Primary Source Value | Verification Status | Source Reference |
|---|---|---|---|
| **Kaggle Dataset Name** | *MushR: Annotated Dataset of Oyster Mushrooms* | VERIFIED_FROM_PRIMARY_SOURCE | Kaggle API view |
| **Kaggle Publisher** | `etcelab` (ETCE-LAB, TU Clausthal, Germany) | VERIFIED_FROM_PRIMARY_SOURCE | Kaggle API view |
| **Kaggle Version & Date** | Version 1; updated `2024-11-20T11:14:14.987Z` | VERIFIED_FROM_PRIMARY_SOURCE | Kaggle API view |
| **Kaggle License** | Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0) | VERIFIED_FROM_PRIMARY_SOURCE | Kaggle API view |
| **Image Count on Kaggle** | 3,011 JPG images (7,898,278,464 uncompressed bytes) | VERIFIED_FROM_PRIMARY_SOURCE | Fully paginated Kaggle file list (16 pages) |
| **Directory Organization** | 3 subdirectories: `Filtered_2.A` (1096), `Filtered_2.B` (1159), `Filtered_2.C` (756) | VERIFIED_FROM_PRIMARY_SOURCE | Kaggle file list aggregation |
| **Annotation Payload** | Top-level COCO annotation JSON files (`.json`) are **NOT listed** in Kaggle file API | UNVERIFIED / DISCREPANCY | Kaggle file inventory |

---

## 2. Task B2 — Paper Relationship Verification

The peer-reviewed paper *MushR: A Smart, Automated, and Scalable Indoor Harvesting System for Gourmet Mushrooms* (Agriculture 2023, 13, 1533) was retrieved from the official MDPI content repository and reviewed in full text (16 pages).

### Direct Paper–Dataset Linkages:
1. **Appendix A (Data Availability Statement):**
   - Explicitly links GitHub repository `https://github.com/ETCE-LAB/MushR`
   - Explicitly links AI model repository `https://github.com/ETCE-LAB/mushr-mask-r-cnn`
   - Cites raw dataset slug: `https://www.kaggle.com/datasets/etcelab/mushr-project-raw-image-dataset-oyster-mushrooms`
2. **Author System README Linkage:**
   - In `ETCE-LAB/MushR/README.md`, the authors explicitly provide the hyperlink: `[Images annotated for Mask R CNN](https://www.kaggle.com/datasets/etcelab/mushr-annotated-dataset-oyster-mushrooms)`.
   - This formally closes the provenance chain linking the 2023 paper to the candidate Kaggle dataset slug.
3. **Temporal Gap & Versioning:**
   - The paper was published on **1 August 2023**.
   - The Kaggle annotated dataset version 1 was updated on **20 November 2024** (15 months later).
   - Byte-level equivalence between the 2023 paper training data and the 2024 Kaggle upload is `UNVERIFIED`.

### Paper-Reported Evaluation Metrics:
- **Training Accuracy:** **91.72%** (Reported on Figure 5 as final iteration training accuracy; **not** test accuracy).
- **Held-Out Test Set Metrics (COCO AP):**
  - Bounding Box AP: **61.88%** (AP50: 71.02%, AP75: 67.92%, APsmall: 20.79%, APmed: 69.79%, APlarge: 87.21%)
  - Segmentation Mask AP: **49.33%** (AP50: 70.64%, AP75: 60.81%, APsmall: 9.01%, APmed: 54.80%, APlarge: 80.22%)
- **Instance Counts in Paper (Table 2):**
  - Train: 2,759 instances (723 Not-Ready, 1,344 Ready, 692 Overdue)
  - Test: 541 instances (251 Not-Ready, 198 Ready, 92 Overdue)
  - *Critical Note:* These are **annotated object instances**, not image counts.

---

## 3. Task B3 — Code Availability & Static Inspection

The author GitHub repositories were statically inspected via GitHub API trees and raw file inspection. No large assets or model checkpoints were cloned.

- **System Repository (`ETCE-LAB/MushR` @ `b22cf28`):**
  - License: GNU Affero General Public License v3.0 (AGPL-3.0-or-later).
  - Contains digital twin schema (Neo4j), Raspberry Pi growth tent controller scripts, and hardware diagrams.
- **Model Repository (`ETCE-LAB/mushr-mask-r-cnn` @ `e8a0493`):**
  - License: GNU General Public License v3.0 (GPL-3.0-or-later).
  - Core implementation: Meta Detectron2 framework with Mask R-CNN ResNet-50-FPN.
  - Weight release: GitHub release `p1` contains `mushr-mask-r-cnn-release.tar.gz` (417,443,840 bytes, unverified weights).
  - Code inspection discrepancies:
    1. **Class Definition Mismatch:** In `train_net.py` (lines 178–181), classes are registered as:
       `MetadataCatalog.get("MushR_Dataset_V1.1").thing_classes = ["Pinning", "Not-Ready", "Ready", "Overdue"]` (4 classes). In contrast, the paper only evaluates 3 classes (`Not-Ready`, `Ready`, `Overdue`).
    2. **Hardcoded User Paths:** Scripts contain hardcoded paths such as `/home/sho/Desktop/MushR_coco_annotations_train.json`.
    3. **Hyperparameter Mismatch:** Config default sets `SOLVER.MAX_ITER = 10000`, while the paper reports 40,000 iterations.
    4. **COCO Class Count Parameter:** In the config, `ROI_HEADS.NUM_CLASSES` remains set to 80 (COCO default) in several places rather than being overridden to 3 or 4.

---

## 4. Gate G0 Evaluation & Recommendation

**Recommendation for C02:** `NEEDS_MORE_EVIDENCE` (Conditional Hold)

**Rationale:**  
The source identity, peer-reviewed paper (2023), author project affiliation, and code repositories are verified. However, the exact availability of the COCO annotation JSON files on Kaggle, the 4-class (code) vs 3-class (paper) discrepancy, and the unpinned Detectron2 runtime environment require resolution before authorizing data acquisition or baseline reproduction.
