# WP-01: C02 vs Excluded DS-02 Identity and Overlap Review

**Review Objective:** Verify whether Candidate C02 (*MushR: Annotated Dataset of Oyster Mushrooms*) is identical to, derived from, or overlapping with the excluded dataset DS-02 (*Annotated Oyster Mushroom Images*, Mendeley `hf55tkx489`).  
**Auditor:** Dataset Provenance Auditor  
**Date:** 2026-10-23  
**Final Classification:** `CONFIRMED_DISTINCT`  

---

## 1. Provenance Comparison Matrix

| Provenance Dimension | Excluded DS-02 (`hf55tkx489`) | Candidate C02 (`etcelab` MushR) | Comparative Finding |
|---|---|---|---|
| **Dataset Title** | *Annotated Oyster Mushroom Images* | *MushR: Annotated Dataset of Oyster Mushrooms* | Different titles |
| **Persistent Identifier** | DOI: `10.17632/hf55tkx489.1` | Kaggle: `etcelab/mushr-annotated-dataset-oyster-mushrooms` (Paper DOI: `10.3390/agriculture13081533`) | Completely distinct identifiers and hosting platforms |
| **Hosting Platform** | Mendeley Data | Kaggle (ETCE-LAB) | Independent hosting |
| **Authors / Contributors** | Sonay Duman; Abdullah Elewi; Abdulsalam Hajhamed; Rasheed Khankan; Amina Souag; Asma Ahmed | Anant Sujatanagarjuna; Shohreh Kia; Dominique Fabio Briechle; Benjamin Leiding | **Zero author overlap.** |
| **Research Institution** | Mersin University & Toros University, Turkey | Institute for Software and Systems Engineering, TU Clausthal, Germany | **Completely different academic institutions.** |
| **Geographic Location** | Mersin, Turkey | Clausthal-Zellerfeld, Lower Saxony, Germany | **Different countries and cultivation facilities.** |
| **Publication Date** | 15 July 2024 | Paper: 1 August 2023; Kaggle: 20 November 2024 | Independent timeline |
| **Cultivation System** | Traditional shelf cultivation in room over 2 cycles | Custom reusable plastic buckets (MushR pods) in 2 grow tents | Different cultivation containers and environments |
| **Imaging System** | Custom sensor-camera rig; 555 raw images | 6 Raspberry Pi HQ cameras (120° wide-angle); 34,400 raw scene images; 3,011 filtered images | Distinct camera hardware and image quantities |
| **Target Classes** | Small, Medium, Large, Overdue | Pinning, Not-Ready, Ready, Overdue | Distinct developmental taxonomy |
| **License** | CC BY 4.0 | CC BY-SA 4.0 | Independent licensing |

---

## 2. Overlap & Derivative Analysis

1. **Institutional and Geographic Independence:**  
   The primary source documentation establishes beyond doubt that DS-02 was gathered in Turkey by a Turkish research team, whereas C02 was gathered in Germany by a German research team at TU Clausthal as part of the EU Horizon 2020 VEDLIoT project.
2. **Physical Apparatus Differences:**  
   C02 specifically developed and photographed proprietary "mushroom pods" (white plastic buckets with 3.5 cm drilled holes), which are prominently visible in the C02 imagery. DS-02 imagery consists of standard mushroom shelf cultivation.
3. **Exclusion Enforcement:**  
   No data files, archives, labels, or checkpoints from DS-02 were imported, accessed, or reused in this verification. DS-02 remains recorded in `EXCLUDED_DATASETS.csv` as `EXCLUDED`.

---

## 3. Scientific Conclusion

**Classification:** `CONFIRMED_DISTINCT`  
Candidate C02 is an entirely independent research project and dataset. There is zero evidence of shared images, shared authors, or shared physical provenance with the abandoned DS-02 dataset. Re-evaluating C02 presents zero risk of inadvertently resurrecting or importing DS-02 data.
