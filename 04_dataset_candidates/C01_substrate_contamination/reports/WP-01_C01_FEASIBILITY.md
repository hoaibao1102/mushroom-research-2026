# WP-01 Candidate Assessment: C01 Substrate Contamination Feasibility

**Candidate:** C01 — Mushroom Disease Dataset (Healthy, Single Infected & Mixed Infected)  
**Repository:** Mendeley Data `10.17632/jrbx34k77g.2`  
**Review Date:** 2026-10-23  

---

## 1. Technical & Computational Feasibility

| Dimension | Engineering Assessment | Confidence | Evidence / Notes |
|---|---|---|---|
| **Task Formulation** | 3-class single-label image classification (Healthy vs Single-Infected vs Mixed-Infected) | High | Standard computer vision classification pipeline |
| **Model Architectures** | Lightweight CNNs: ResNet-18, MobileNetV3, EfficientNet-B0; Vision Transformers: ViT-Tiny | High | Standard torchvision models |
| **Compute Requirements** | < 1 GPU-hour on NVIDIA T4 / RTX 3060; ~10-20 MB model checkpoint | High | 761 small images (reported total) |
| **Cloud Execution** | Fully compatible with Google Colab (free tier), Kaggle Kernels, or local workstation | High | Minimal memory footprint (< 2 GB VRAM) |
| **Dependencies** | Python 3.10+, PyTorch 2.x, Torchvision, Scikit-Learn | High | Highly stable standard ecosystem |

---

## 2. Scientific & Methodological Feasibility

| Dimension | Scientific Assessment | Risk Level | Details |
|---|---|---|---|
| **Baseline Availability** | **NONE.** No published paper uses this exact dataset. | HIGH | An original baseline must be established; cannot reproduce an author-published result. |
| **Ground Truth Validity** | Unverified visual assessment. No lab culturing or PCR. | HIGH | High probability of label noise; biological pathogens cannot be definitively identified from exterior bag photos alone. |
| **Leakage Vulnerability** | Critical risk of identical bag specimen leakage across splits. | SEVERE | Without bag IDs, random splitting would violate independence. |
| **Class Balance** | Reported: 299 Healthy (39.3%), 147 Single (19.3%), 315 Mixed (41.4%). | MODERATE | Single-infected class is underrepresented by 50% relative to mixed. |
| **Evaluation Metrics** | Macro-F1, Balanced Accuracy, Per-class Precision/Recall. | LOW | Standard multi-class classification metrics apply directly. |

---

## 3. Real-World Oyster Mushroom Farm Viability

- **Farm Workflow Relevance:** Substrate contamination is the leading cause of crop failure and economic loss in oyster mushroom production. Early removal of infected bags prevents airborne spore dispersion (*Trichoderma* green mold).
- **Practical Deployment Obstacles:**
  - In commercial grow rooms, bags are stacked closely on shelves. Single-angle smartphone photos do not capture the back or base of bags.
  - Workers typically inspect bags physically by touch and smell in addition to sight.
  - Non-ML heuristic alternative: Standard sanitation protocols and scheduled visual inspections by farm staff may render complex multi-class ML unnecessary unless automation (e.g., automated shelving cameras) is used.

---

## 4. Overall Feasibility Conclusion

From a purely computational standpoint, C01 is exceptionally easy to implement. However, scientifically, it is **severely blocked** by the absence of bag identifiers (guaranteed data leakage if randomly split) and lack of biological confirmation. It cannot serve as a reproducible baseline because no published baseline exists.
