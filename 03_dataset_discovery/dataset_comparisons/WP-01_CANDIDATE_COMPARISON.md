# WP-01: Comprehensive Candidate Comparison (C01 vs C02)

**Evaluation Framework:** `03_dataset_discovery/DATASET_SELECTION_CRITERIA.md`  
**Phase:** Phase 0 — Topic & Dataset Selection (WP-01 Evidence Phase)  
**Date:** 2026-10-23  

---

## 1. 14-Criteria Comparative Evaluation

In accordance with project research protocols, criteria are evaluated based strictly on verified primary evidence. Where evidence is incomplete, items are marked `NOT_VERIFIED` rather than receiving artificial numeric scores.

| # | Evaluation Criterion | Candidate C01 (Substrate Contamination) | Candidate C02 (MushR Harvest Readiness) | Evidence Assessment |
|---|---|---|---|---|
| **1** | **Source Reliability** | Mendeley Data (Elsevier); academic contributor team (Bangladesh). | MDPI *Agriculture* (peer-reviewed journal); TU Clausthal (Germany). | C02 is backed by a peer-reviewed publication; C01 is a standalone repository upload. |
| **2** | **Dataset Accessibility** | Open access HTTP on Mendeley; single archive payload. | Open access on Kaggle; 3,011 JPGs accessible via API. Top-level annotation JSON not in API file list. | C01 is easily downloadable; C02 images are accessible, but annotation JSON access needs verification. |
| **3** | **License Clarity** | CC BY 4.0 (Commercial and derivative use permitted with attribution). | CC BY-SA 4.0 for dataset; GPL-3.0 / AGPL-3.0 for code. | C01 has simpler license; C02 has ShareAlike (dataset) and copyleft (code) obligations. |
| **4** | **Annotation Clarity** | Visual inspection folders (Healthy, Single, Mixed). No scoring rubric or biological verification. | Instance polygons (CVAT) for individual mushrooms. Code defines 4 classes; paper reports 3 classes. | C02 has explicit instance masks; C01 has unverified whole-image categorization. |
| **5** | **Paper–Dataset Relationship** | **NONE.** No published paper cites or uses this exact dataset. | **STRONG.** Author project README explicitly links dataset; Appendix A cites raw data. | C02 has a verified direct paper link; C01 has zero verified literature. |
| **6** | **Baseline Availability** | **NONE.** No published baseline exists. | **YES.** Detectron2 Mask R-CNN baseline documented in paper and GitHub. | C02 provides a reproducible benchmark; C01 requires novel baseline construction. |
| **7** | **Reproduction Complexity** | LOW implementation complexity (standard CNN), but no reference baseline to match. | HIGH complexity: Detectron2 C++ dependencies, unpinned environment, hardcoded paths. | C01 is easier to code; C02 is more complex but scientifically grounded. |
| **8** | **Compute Requirements** | Very low (<1 GPU hour on Colab T4). | Low-to-moderate (2-3 GPU hours on Colab T4). | Both fit comfortably within student capstone compute budgets. |
| **9** | **Data Leakage Risk** | **SEVERE.** No bag identifiers; extreme risk of duplicate bag frames crossing splits. | **HIGH.** Hourly capture from 3 fixed cameras in 2 tents; temporal correlation risk across splits. | Both candidates present serious data leakage risks requiring grouped split design. |
| **10** | **Mushroom Domain Relevance** | **HIGH.** Contamination is the #1 financial loss factor in cultivation. | **HIGH.** Harvest timing determines yield quality and labor allocation. | Both address critical real-world oyster mushroom pain points. |
| **11** | **Small-Farm Validation** | High: Any local oyster mushroom farm has contaminated bags to test. | Moderate: Requires mounting multi-camera rigs in grow rooms or manual photo matching. | C01 is simpler for physical field testing; C02 requires more infrastructure. |
| **12** | **Recent Related Research (2024–2026)** | Dataset is 2025; direct same-task prior work published in 2026 (Bacanto et al., IEEE). | Paper published August 2023. Follow-up research exists in automated harvesting. | C01 has very recent peer work (2026); C02 foundational paper is 2023. |
| **13** | **Investigable Limitations** | Overcoming visual label noise, multi-pathogen identification. | Small-object AP degradation (9.0% APsmall), 3 vs 4 class alignment, cluster stability. | C02 offers clear quantitative target metrics to improve; C01 lacks reference metrics. |
| **14** | **Risk of Repeating DS-02** | **ZERO.** Entirely distinct task and domain. | **ZERO.** Confirmed distinct origin (Germany vs Turkey; different authors/hardware). | Neither candidate overlaps with abandoned DS-02. |

---

## 2. Strategic Trade-off Synthesis

- **Candidate C01:**  
  - *Strengths:* Highly practical agricultural problem; modern publication date (2025); simple compute and modeling pipeline.  
  - *Weaknesses:* Scientifically unanchored (no published paper, no reference baseline); unverified biological ground truth (discoloration could be mold or bacteria); severe risk of specimen leakage without bag IDs.  
- **Candidate C02:**  
  - *Strengths:* Formally verified peer-reviewed paper (MDPI 2023); published Detectron2 baseline with clear quantitative metrics (bbox AP 61.88, segm AP 49.33); realistic flush-level agricultural clustering; confirmed distinct from DS-02.  
  - *Weaknesses:* Complex Detectron2 software environment; Kaggle annotation files need pre-flight verification; class definition mismatch between code (4 classes) and paper (3 classes).  

**Conclusion:** Neither candidate can be unconditionally selected today. C02 is significantly more mature scientifically, but requires pre-flight resolution of its annotation payload and software dependencies.
