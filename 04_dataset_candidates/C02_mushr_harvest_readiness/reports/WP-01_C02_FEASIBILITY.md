# WP-01 Candidate Assessment: C02 MushR Harvest Readiness Feasibility

**Candidate:** C02 — MushR Oyster Mushroom Harvest Readiness  
**Target:** Kaggle `etcelab/mushr-annotated-dataset-oyster-mushrooms` / MDPI Agriculture 13(8), 1533  
**Review Date:** 2026-10-23  

---

## 1. Technical & Reproduction Complexity

| Dimension | Technical Assessment | Severity | Evidence / Notes |
|---|---|---|---|
| **Framework** | Facebook Detectron2 (built on PyTorch) | MODERATE-HIGH | Detectron2 requires specific CUDA/C++ compiler extensions; installation frequently breaks on modern Python/PyTorch versions. |
| **Architecture** | Mask R-CNN (ResNet-50-FPN) + DBSCAN post-clustering | HIGH | Requires two-stage pipeline: instance segmentation followed by spatial mask clustering for flush-level harvest decisions. |
| **Dependency Pinning** | **UNPINNED.** No `requirements.txt` or `conda.yaml` provided. | HIGH | Exact PyTorch, torchvision, and Detectron2 commit versions used in 2023 are unrecorded. |
| **Hardcoded Paths** | Hardcoded Linux paths (`/home/sho/Desktop/...`) | LOW-MODERATE | Requires code refactoring to accept relative CLI path arguments. |
| **Compute Budget** | Paper: 40,000 iterations, batch size 2 (~1.1 hours on RTX 4090; 2.7 GB VRAM). | LOW-MODERATE | Can run on Google Colab T4 GPU (~2-3 hours compute time). |
| **Annotation Availability** | Top-level annotation JSON not listed in Kaggle API index. | SEVERE | **If annotation files cannot be obtained, instance segmentation cannot be trained.** |

---

## 2. Scientific Integrity & Data Leakage Assessment

- **Camera Perspective Leakage:** Images were captured from 3 fixed camera angles every hour over 10 months inside 2 growth tents. Sequential hourly images of the same mushrooms will be nearly identical.
- **Split Construction:** The paper reports 2,759 training instances and 541 testing instances. It is critical to verify whether the test set was split by **time / cultivation flush** or by random image assignment. If images from the same camera at consecutive hours crossed splits, test AP would be severely inflated.
- **Task Integrity:** The paper's contribution relies on delineating overlapping caps within a dense flush using instance masks. Simplifying this task to whole-image classification would destroy the ability to identify which specific mushrooms are ready and guide a robotic cutter.

---

## 3. Real-World Oyster Mushroom Farm Viability

- **Agricultural Context:** Oyster mushrooms grow in clusters (flushes). Harvesting individual caps is physically impossible without damaging neighboring caps; the entire cluster must be harvested together. The paper's DBSCAN clustering reflects this biological reality.
- **Automation Feasibility:** The authors prototyped a pneumatic cutting blade and motorized cutter. In a commercial farm, camera lens fogging (humidity > 90% required for oyster mushrooms) and rapid spore deposition are major physical failure modes acknowledged by the authors.

---

## 4. Overall Feasibility Conclusion

C02 represents a scientifically rich and relevant research direction. However, reproduction is **technically demanding** due to Detectron2 environment fragility, potential annotation JSON access issues on Kaggle, and configuration discrepancies. Pre-flight verification of annotation files is mandatory before considering selection.
