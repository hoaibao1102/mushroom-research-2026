# Research task board — M18K

Legend: **DONE (notebook evidence)** = visible in executed notebook; **NEEDS REVIEW** = requires a human or independent check; **PLANNED** = not yet done. Do not interpret PLANNED as authorized or completed.

| Priority | Task | Status | Evidence / remaining action | Responsible |
| --- | --- | --- | --- | --- |
| P0 | Record V2 RGB/depth and annotation file inventory | DONE (notebook evidence) | Executed notebook, inventory outputs | Analyst; reviewer pending |
| P0 | Stream-read all COCO annotation records | DONE (notebook evidence) | 700,589 records; class-ID audit | Analyst; reviewer pending |
| P0 | Generate V2 EDA and example visualizations | DONE (notebook evidence) | `09_results/` figures and report | Analyst; reviewer pending |
| P0 | Determine if BB=858/WB=699,731 reflects correct labels | NEEDS REVIEW | Stratified human review of BB and negative controls; inspect original categories and source | Team/data reviewer |
| P0 | Verify 4,652 release claim vs 4,495 RGB annotation records | NEEDS REVIEW | Compare archive manifest/version and paper/repository release descriptions | Dataset/source reviewer |
| P0 | Verify depth alignment, units, quality | NEEDS REVIEW | Check sensor calibration/intrinsics and sampled arrays, not just stems | Data/3D reviewer |
| P0 | Check train/val/test leakage | NEEDS REVIEW | Full exact hash + near duplicates + growth-scene/acquisition group review | Data reviewer |
| P0 | Confirm C03 as officially selected and clarify dataset license | NEEDS REVIEW | Team lead decision and source/license evidence; update state and decision log | Team lead |
| P1 | Freeze V2 baseline protocol and environment | PLANNED | Split/seed/model/metric definitions, batch budget, Colab environment | Model lead |
| P1 | Train YOLOv8n-seg RGB on V2 | PLANNED | Actual logs, checkpoints and validation metrics; no result yet | Model lead |
| P1 | Evaluate once on held-out test; per-class AP | PLANNED | Test report with rare-class caveat | Evaluator |
| P2 | Paper-compatible benchmark subset and protocol | PLANNED | Reconcile 2,000 vs V2; 70/10/20 vs 80/10/10 | Research lead |
| P2 | RGB vs RGB-D late-fusion comparison | HYPOTHESIS | Predeclare controlled experiment after RGB baseline | Research/model lead |
| P3 | 3D pose estimation feasibility audit | PLANNED | Inspect available 3D labels, calibration and angular-error metric | 3D lead |

Names, approvals and deadlines beyond today's EDA were not supplied, so no assignments are invented.
