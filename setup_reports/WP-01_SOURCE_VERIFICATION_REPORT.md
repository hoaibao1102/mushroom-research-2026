# WP-01 Setup and Verification Report: Candidate Dataset & Paper Source Verification

## A. Executive Summary

- **Work Package:** WP-01 (Candidate Dataset & Paper Source Verification)
- **Execution Date:** 2026-10-23
- **Repository Path:** `D:\Capstone\mushroom-research-2026`
- **Branch:** `research/wp-01-source-verification` (Starting commit: `478560ed9d3cf412b725a2866edeea77744f7040`)
- **Overall Status:** **PASS** (Source Verification Complete; All Claims Traceable; Infrastructure Protected)
- **Dataset Selection Decision:** **PENDING HUMAN REVIEW** (No dataset selected; no training authorized)
- **Principal Findings:**
  1. **Candidate C01 (Mendeley `10.17632/jrbx34k77g.2`):** Source identity, authors (Abdullah Mazumdar et al.), version 2 (published 2025-06-30), and CC BY 4.0 license are verified. Reported image count is 761 across 3 classes. However, no published paper uses this exact dataset; biological ground truth is unconfirmed; and bag-level grouping metadata is missing.
  2. **Candidate C02 (MushR Kaggle / MDPI):** Full text of the peer-reviewed paper (*Agriculture* 2023, 13, 1533) was retrieved and reviewed. C02 is formally linked to the author project and GitHub code repositories. Kaggle v1 (updated 2024-11-20) contains 3,011 JPGs under CC BY-SA 4.0. Code uses Detectron2 Mask R-CNN. Discrepancies exist: code registers 4 classes while paper evaluates 3; Kaggle API index does not show the COCO annotation JSON file; and dependencies are unpinned.
  3. **DS-02 Exclusion Verification:** Rigorous provenance audit confirms C02 is **`CONFIRMED_DISTINCT`** from the abandoned DS-02 dataset (`hf55tkx489`). C02 originates from TU Clausthal, Germany, whereas DS-02 originates from Mersin, Turkey, with zero shared authors, hardware, or data.
  4. **Gate G0 Recommendations:** Both C01 and C02 receive a recommendation of **`NEEDS_MORE_EVIDENCE`** (Conditional Hold). Neither candidate is ready for immediate training.

---

## B. Verification Results

### Candidate C01 (Mushroom Disease Dataset)
- Title: *Mushroom Disease Dataset (Healthy, Single Infected & Mixed Infected)*
- Platform: Mendeley Data
- DOI: `10.17632/jrbx34k77g.2`
- Authors: Abdullah Mazumdar, Jubayer Ahmed Bhuiyan Shawon, Sumon Debnath, Md Abdullah
- Publication Date: 2025-06-30 (v2); 2025-06-16 (v1)
- License: CC BY 4.0
- Source-Reported Counts: 761 total (299 healthy, 147 single-infected, 315 mixed-infected)
- Data Quality & Provenance Status: Data payloads were not downloaded. Lab confirmation and bag-level groupings are unverified.

### Candidate C02 (MushR Annotated Dataset of Oyster Mushrooms)
- Title: *MushR: Annotated Dataset of Oyster Mushrooms*
- Platform: Kaggle (`etcelab/mushr-annotated-dataset-oyster-mushrooms`)
- Publisher: `etcelab` (ETCE-LAB, TU Clausthal)
- Kaggle Version & Date: Version 1, updated 2024-11-20T11:14:14.987Z
- License: CC BY-SA 4.0 (Dataset); GPL-3.0 / AGPL-3.0 (Code)
- File Organization: 3,011 JPG files in `Filtered_2.A` (1096), `Filtered_2.B` (1159), `Filtered_2.C` (756); 7.35 GiB uncompressed.
- Pinned Code Commits:
  - `ETCE-LAB/MushR`: `b22cf285402b816bbd477d83ca63c5c0265d0483`
  - `ETCE-LAB/mushr-mask-r-cnn`: `e8a0493b193c15c5f6129d89d7f14d89e84a8868`

---

## C. Paper Verification

### Paper P001 (MushR Paper)
- Title: *MushR: A Smart, Automated, and Scalable Indoor Harvesting System for Gourmet Mushrooms*
- Authors: Anant Sujatanagarjuna; Shohreh Kia; Dominique Fabio Briechle; Benjamin Leiding
- Publication: *Agriculture* 2023, 13, 1533 (Published 1 August 2023)
- DOI: `10.3390/agriculture13081533`
- License: CC BY 4.0 (MDPI Open Access)
- Metrics Clarification:
  - Final training accuracy reported as **91.72%** (not test accuracy).
  - Held-out test set COCO AP: Bbox AP = **61.88%**, Segmentation AP = **49.33%**.
  - Small object segmentation AP is notably low at **9.01%**.
- Link to Dataset: Appendix A links GitHub and raw dataset slug. The author's main project README explicitly links the annotated Kaggle slug.

### C01 Related Literature
- No paper cites DOI `10.17632/jrbx34k77g.2`.
- Found direct same-task prior work: Bacanto et al. (IEEE 2026, DOI: `10.1109/FET68771.2026.11601212`), studying mushroom fruiting bag contamination (healthy, green mold, black mold; 86.9% accuracy). Classified as `SAME_TASK_DIFFERENT_DATASET`.

---

## D. DS-02 Exclusion Review

- **Status:** **`CONFIRMED_DISTINCT`**
- **Evidence:** C02 was gathered in Clausthal-Zellerfeld, Germany at TU Clausthal using 6 Raspberry Pi cameras and reusable buckets. DS-02 (`hf55tkx489`) was collected in Mersin, Turkey by Mersin/Toros University researchers using standard cultivation beds. Zero author, institutional, geographic, or apparatus overlap exists.
- **Safety Confirmation:** Zero DS-02 data files, images, or previous checkpoints were accessed or imported.

---

## E. Reproduction Feasibility

- **C01 Feasibility:** Simple classification pipeline (<1 hour compute). However, reproducing an existing scientific benchmark is impossible because no published baseline exists. Severe leakage risk without bag IDs.
- **C02 Feasibility:** Detectron2 Mask R-CNN baseline exists, but reproduction is impeded by unpinned dependencies, hardcoded file paths in author scripts, and a class count discrepancy (4 classes registered in code vs 3 evaluated in paper).

---

## F. Candidate Comparison Summary

| Dimension | C01 (Substrate Contamination) | C02 (MushR Harvest Readiness) |
|---|---|---|
| Published Paper | None | Peer-reviewed MDPI Agriculture (2023) |
| Baseline Model | None | Detectron2 Mask R-CNN (AP 61.88/49.33) |
| License | CC BY 4.0 | CC BY-SA 4.0 (Data) / GPL-3.0 (Code) |
| Engineering Complexity | Low (standard CNN) | High (Instance segmentation + DBSCAN) |
| Leakage Risk | Severe (no bag IDs) | High (hourly fixed-camera correlation) |
| Recommendation | NEEDS_MORE_EVIDENCE | NEEDS_MORE_EVIDENCE |

---

## G. Gate G0 Recommendations

- **C01 Recommendation:** `NEEDS_MORE_EVIDENCE` (Conditional Hold)  
  *Justification:* Source verified, but lacks published baseline, biological confirmation, and split/bag metadata.
- **C02 Recommendation:** `NEEDS_MORE_EVIDENCE` (Conditional Hold)  
  *Justification:* Source and paper verified, but annotation JSON access on Kaggle, class mismatches, and software environment pinning remain unresolved.
- **Overall Research Gates:** All gates G0–G6 remain unpassed (`NEEDS_MORE_EVIDENCE`). No training authorized.

---

## H. Unresolved Questions (Summary)

1. *C02:* Exact location and schema of COCO annotation JSON files on Kaggle.
2. *C02:* Resolution of 4-class code vs 3-class paper evaluation.
3. *C01:* Availability of cultivation bag identifiers or timestamp metadata to prevent split leakage.
4. *C01:* Method of pathogen identification (visual vs laboratory).

---

## I. Validation Results

1. **Evidence Registry Compilation:** 65 primary claims successfully extracted and validated into `03_dataset_discovery/source_verification/WP-01_EVIDENCE_REGISTRY.csv`.
2. **Registry Schema Checks:** All CSV files parsed strictly with standard-library `csv.DictReader`; row widths and schemas confirmed.
3. **Clean Storage Check:** Confirmed 0 bytes of dataset payloads, archives, weights, or checkpoints in the workspace.
4. **Git Status:** Working tree clean on branch `research/wp-01-source-verification`. No unauthorized commits or merges performed.

---

## J. Next Work Package: WP-02 Recommendation

**Recommended Next Work Package:**  
`WP-02: Targeted Annotation & Metadata Auditing (Pre-Selection Phase)`  
- **Scope:**  
  1. Perform targeted inspection of C02 Kaggle annotation files without downloading full image payloads.
  2. Inquire or inspect C01 metadata headers for bag grouping identifiers.
  3. Prepare containerized or virtualenv pre-flight checks for Detectron2 dependencies.
  4. Submit final comparison to project stakeholders for formal candidate selection.
- **Strict Limitation:** Do not start WP-02 without explicit authorization.
