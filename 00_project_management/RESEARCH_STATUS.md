# Research status — 3 November 2026 (Day 3)

| Item | Actual status / evidence |
| --- | --- |
| Day 1: M18K V2 EDA | **DONE** — 4,495 indexed RGB images; 700,589 COCO annotations; depth filename pairing and plots |
| Day 2: YOLO reproduction workflow | **DONE** — two independently trained YOLOv8n-seg configurations (BB+WB and WB-only), both held-out tests recorded; **not** an identical reproduction of published original scores |
| Day 3: 2D mask-area evaluation | **DONE for 30-image sample** — matched mask area MAE=207.4 px², mean relative abs error=8.80% |
| Day 3: qualitative error analysis | **DONE for 12 exported figures** — reviewed report and corrected boundary-count bug |
| Current research-paper draft | **UPDATED** — Markdown and Word under `10_research_paper/drafts/` |
| External exact source/permission approval | **NOT VERIFIED** — do not infer formal approval from experiment completion |
| BB label validation and count discrepancy | **OPEN** — rare category and 4,652 vs 4,495 ambiguity |
| Train/test scene independence | **OPEN** — five zero-distance perceptual dHash pairs, no exact pixel hash or visual paired clearance |
| Apparent GT mask anomalies | **OPEN** — possible issues in test images `004252` and `004472`; requires raw COCO examination |
| Depth calibration / physical area | **NOT DONE** — current areas only in px²; mm²/3D area not supported |
| Original M18K benchmark equivalence | **NOT ESTABLISHED** — original subset/splits/metric differ |
| Formal QC research gates G0/G1/G2 | **NEEDS_MORE_EVIDENCE**, despite completed experiment execution |

See `00_project_management/TASK_BOARD.md` for next actions and `12_reproducibility/manifests/DAY2_DAY3_EVIDENCE.json` for traceability. Historic WP-00 setup reports have not been relabeled as current findings.
