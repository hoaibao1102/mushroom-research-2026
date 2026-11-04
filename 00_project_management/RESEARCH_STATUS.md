# Research status — 4 November 2026 (Day 4)

| Stage | Status | Evidence / qualification |
| --- | --- | --- |
| Day 1 — M18K V2 EDA | **DONE** | 4,495 COCO-indexed RGB images, 700,589 original annotations; RGB/depth filename matches |
| Day 2 — YOLOv8n-seg paper-approach reproduction on V2 | **DONE** | Two-class and WB-only checkpoints, both reported held-out test results; **not** an exact original 2025 benchmark reproduction |
| Day 3 — sampled WB mask-area and qualitative review | **DONE** | 30-image matched-mask area evaluation, 12 qualitative prediction figures |
| Day 4 — WB full-test predicted area | **DONE (submitted)** | 450 images, 68,794 matched WB masks, area MAE 211.41 px², mean relative error 8.81%; unmatched detections tracked separately |
| Day 4 — WB-only inference MVP | **DONE (executed notebook)** | 10 test images; 1,551 detected WB instances; masks/counts/px² area and CSV/ZIP export |
| Day 4 — scratch Otsu and classical baseline | **DONE (10-image demo experiment)** | 10/10 agreement with OpenCV, 10-image same-data comparison, two simple ablations; not full-test semantic/instance benchmark |
| Day 4 — English IVP course report | **DRAFT PREPARED** | Editable Word and review PDF; still needs submission metadata, source citation check and final edit |
| Day 4 — dataset QC | **SUBMITTED; ISSUES OPEN** | Tested five different pairs than original Day 3 flags; exact hashes do not clear near-duplicate scene overlap; two GT anomalies unresolved |
| Demo video and 12–15-minute slides | **NOT DONE** | Final course deliverables still pending |
| Four techniques across three course lessons | **NEEDS LESSON MAPPING** | Scratch Otsu, grayscale/Gaussian, morphology and connected components demonstrated; actual chapter mapping not established |
| Formal upstream source/license approval and research gates | **NOT VERIFIED** | Existing G0/G1/G2 status remains needs-more-evidence |
| Physical mm², depth-calibrated or 3D surface area | **NOT IMPLEMENTED** | Current area in px² only |

See `00_project_management/TASK_BOARD.md` and `09_results/reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md`. No retraining was needed on Day 4.
