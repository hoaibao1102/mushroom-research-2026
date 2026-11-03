# Research task board — current as of 2026-11-03

| Work | Status | Evidence / action needed |
| --- | --- | --- |
| Day 1 — V2 EDA and class inventory | DONE | 09_results/reports/M18K_V2_EDA_2026-10-30.md |
| Day 2 — two-class YOLOv8n-seg train/evaluate | DONE (reported run) | 09_results/metrics/Day2_Two_Class_Heldout_Test_2026-11-02.json; checkpoint in team Drive |
| Day 2 — WB-only YOLOv8n-seg train/evaluate | DONE (reported run) | 09_results/metrics/Day2_WB_Only_Heldout_Test_2026-11-02.json; corrected separate WB-only test |
| Day 2 — WB COCO→YOLO conversion / mask area sanity | DONE (submitted) | 07_source_code and 09_results/metrics/wb_* |
| Day 3 — sampled predicted mask area error | DONE for 30 images | 09_results/area_evaluation/mask_area_matches.csv and summary |
| Day 3 — 12-image qualitative error review | DONE for reviewed PNGs | 09_results/reports/Day3_WB_Qualitative_Review_2026-11-03.md |
| Day 3 — manuscript integration | DRAFT UPDATED | 10_research_paper/drafts; final peer review still needed |
| Confirm source V2 legal reuse, official research selection and formal gate approvals | NEEDS HUMAN DECISION | Source/license and approval evidence missing |
| Independently verify two suspected WB GT anomalies | OPEN | Inspect full original COCO category/polygons for 004252/004472 |
| Verify five dHash=0 train/test pairs and scene groups | OPEN | Compare exact SHA-256 + visual RGB, possible same acquisition groups |
| Investigate V2 4,652 vs 4,495 image counts | OPEN | Verify upstream release archive/manifest |
| Physical area (mm²), 3D pose, quality prediction | OUT OF V1 SCOPE | Do not claim complete; depth intrinsics and units unverified |

Remaining tasks are verification and manuscript closure, **not retraining**. Experiment logs are user-supplied results, not re-executed by the repository packager.
