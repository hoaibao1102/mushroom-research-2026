# WP-01: Candidate C01 Source Verification Dossier

**Candidate ID:** C01  
**Candidate Working Name:** Mushroom Substrate Contamination Classification  
**Target Dataset:** Mendeley Data `10.17632/jrbx34k77g.2` (Version 2)  
**Evaluation Date:** 2026-10-23  
**Review Status:** COMPLETED (Metadata & Literature Verification Only)  
**Gate G0 Recommendation:** NEEDS_MORE_EVIDENCE (Conditional Hold)  

---

## 1. Task A1 — Primary Source Identity & Metadata

Primary source verification was conducted using public metadata from Mendeley Data, DataCite registration records, and Crossref APIs. No dataset payloads or images were downloaded.

| Property | Primary Source Value | Verification Status | Evidence Source |
|---|---|---|---|
| **Exact Dataset Title** | *Mushroom Disease Dataset (Healthy, Single Infected & Mixed Infected)* | VERIFIED_FROM_PRIMARY_SOURCE | Mendeley landing page & DataCite API |
| **Publisher / Platform** | Mendeley Data (Elsevier) | VERIFIED_FROM_PRIMARY_SOURCE | Canonical URL / Elsevier platform |
| **Authors / Contributors** | Abdullah Mazumdar; Jubayer Ahmed Bhuiyan Shawon; Sumon Debnath; Md Abdullah | VERIFIED_FROM_PRIMARY_SOURCE | DataCite metadata record |
| **Canonical URL** | `https://data.mendeley.com/datasets/jrbx34k77g/2` | VERIFIED_FROM_PRIMARY_SOURCE | Direct HTTP 200 response |
| **Persistent Identifier** | DOI: `10.17632/jrbx34k77g.2` | VERIFIED_FROM_PRIMARY_SOURCE | DataCite registered DOI |
| **Publication Date** | Version 2: 2025-06-30 (Version 1: 2025-06-16) | VERIFIED_FROM_PRIMARY_SOURCE | Mendeley version metadata |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) | VERIFIED_FROM_PRIMARY_SOURCE | DataCite rights element & landing text |
| **Download Availability** | Public open access (HTTP download available) | VERIFIED_FROM_PRIMARY_SOURCE | Metadata accessibility confirmed |
| **Documented File Types** | Image files (.jpg / .png mentioned in metadata) | REPORTED_BY_SOURCE_NOT_AUDITED | Description text; payload not audited |

### Version History Analysis
- **Version 1 (2025-06-16):** Titled *Mushroom Disease Dataset (Healthy, Black Mold & Green Mold)*. Description reported 680 images: 299 healthy, 72 single-infected, and 309 mixed-infected.
- **Version 2 (2025-06-30):** Title changed to generalize classes to *Healthy, Single Infected & Mixed Infected*. Description updated total count to 761 images.
- **Critical Finding:** The source version history shows a 14-day revision cycle adding 81 images and renaming the dataset from specific fungal molds (Black Mold, Green Mold) to generalized infection categories. Specific file diffs between v1 and v2 were not audited.

---

## 2. Task A2 — Annotation and Data Semantics

| Semantic Dimension | Source Statement | Verification Status | Scientific Risk & Limitations |
|---|---|---|---|
| **Reported Image Counts** | 761 total (299 healthy, 147 single-infected, 315 mixed-infected) | REPORTED_BY_SOURCE_NOT_AUDITED | Not independently audited; payload not downloaded. |
| **Labeling Protocol** | "Visual inspection of mushroom cultivation bags" | UNVERIFIED | No formal scoring rubric or inter-annotator agreement metrics published. |
| **Biological Confirmation** | Description notes: "typically involving both types of mold" | UNVERIFIED | **No laboratory pathogen isolation, culturing, PCR, or microscopy documented.** |
| **Pathogen Taxonomy** | Mentions Green Mold (*Trichoderma* spp.) and Black Mold (*Aspergillus* / *Rhizopus* spp.) | UNVERIFIED / ASSUMED | Fungal species assumed based on visual discoloration only. |
| **Sample Independence** | Not reported in metadata | UNVERIFIED | **High risk of multiple photos per cultivation bag.** No bag IDs or temporal metadata. |
| **Predefined Splits** | None published in metadata | NOT_FOUND | No train/val/test split manifests exist; risk of naive random splitting. |

---

## 3. Task A3 — Related Papers and Literature Verification

A systematic literature search was conducted across Crossref, OpenAlex, IEEE Xplore, and related academic repositories for papers citing DOI `10.17632/jrbx34k77g.2` or utilizing this exact dataset.

### Findings:
1. **Direct Dataset Reuse:**  
   **Zero (0) papers** were found citing `10.17632/jrbx34k77g.2` or referencing this exact Mendeley repository. Given the publication date of 30 June 2025, no peer-reviewed literature currently establishes a verified benchmark on this exact dataset.
2. **Direct Same-Task Prior Work (Different Dataset):**  
   - **Bacanto et al. (2026):** *Hybrid Feature Engineering and Artificial Neural Network for Mushroom Fruiting Bag Contamination Classification*, IEEE, DOI: `10.1109/FET68771.2026.11601212`.
     - *Relevance:* Directly addresses mushroom fruiting bag contamination (healthy, green mold, black mold) using iPhone 15 capture in Laguna, Philippines.
     - *Method:* ResNet-18 + CBAM + GLCM + ANN, achieving 86.9% accuracy.
     - *Classification:* `SAME_TASK_DIFFERENT_DATASET`. Confirms that classifying green/black mold in fruiting bags is an active research topic, but does not use C01.
3. **Related Domain Research:**  
   - **Ujir et al. (2024):** *Automating Mushroom Culture Classification: A Machine Learning Approach*, IJACSA, DOI: `10.14569/IJACSA.2024.0150454`.
     - *Relevance:* Studies *Pleurotus ostreatus* culture contamination classification (1,400 images). `RELATED_DOMAIN_DIFFERENT_DATASET`.

---

## 4. Task A4 — Reproduction Feasibility Assessment

- **Classification Baseline:** Standard CNN baselines (e.g., ResNet-18, MobileNetV3) can be trained with standard PyTorch frameworks with low compute requirements (<1 hour on a free-tier Colab GPU).
- **Critical Methodological Blockers:**
  1. *Lack of Biological Ground Truth:* Visual-only discoloration may conflate non-pathogenic substrate aging/browning with true fungal contamination.
  2. *Data Leakage via Specimen Duplication:* Without bag identifiers, images of the same bag taken from different angles could leak across train and test sets, artificially inflating accuracy.
  3. *Absence of Published Baseline:* Because no published paper uses C01, any implementation would be a de novo baseline rather than a reproduction of prior work.

---

## 5. Gate G0 Evaluation & Recommendation

**Recommendation for C01:** `NEEDS_MORE_EVIDENCE` (Conditional Hold)

**Rationale:**  
The source identity, version (v2), authors, and CC BY 4.0 license are verified from primary metadata. However, the lack of biological confirmation protocols, missing bag-level grouping metadata, and absence of any published baseline paper prevent an unconditional `GO` for dataset selection at this stage.
