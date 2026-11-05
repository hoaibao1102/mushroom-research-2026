# Research status — 5 November 2026 (Day 5)

| Stage | Status | What the evidence says |
|---|---|---|
| Day 1 — M18K V2 EDA | **Done** | 4,495 indexed RGB images and 700,589 original annotations were audited. |
| Day 2 — YOLOv8n-seg reproduction on V2 | **Done** | Two-class and WB-only models have held-out test results. This reproduces the approach on V2, not the exact original paper benchmark. |
| Day 3 — area and prediction review | **Done** | 30-image mask-area analysis and 12-image qualitative review. |
| Day 4 — course MVP experiments | **Done** | Full 450-image WB area evaluation, 10-image inference notebook, scratch Otsu verification and small baseline/ablation. |
| Day 5 — dense-scene counting | **Preliminary result** | NMS IoU 0.70 → 0.50 reduced count MAE from 3.375 to 1.875 on eight selected dense images. Full 450-image validation is still needed. |
| Day 5 — RGB-D feasibility | **Feasibility study complete** | 30 images / 4,970 WB masks inspected. Depth units and intrinsics are not verified; no mm² estimate was made. |
| Day 5 — WB-only Gradio demo | **Working** | User confirmed the Colab app launched, loaded a random test image and ran inference. Checkpoint stays in Drive. |
| Course report and slides | **Prepared** | Word/PDF report and editable presentation are in `10_research_paper/submission/`. They predate the Day 5 member findings. |
| Demo video | **Open** | The live app can be shown; a separate recording has not been made. |
| Dataset QC and permissions | **Open** | Earlier duplicate/annotation concerns and formal source/license approval remain unresolved. |

## Current research questions

1. Does the lower NMS IoU setting improve counting across all 450 test images, or only the selected dense scenes?
2. Can the upstream dataset release provide verified depth units, intrinsics and RGB-depth alignment? If not, physical area needs a separately calibrated data source.
3. Can the course report be updated to include the Day 5 NMS and RGB-D findings before submission?

See `00_project_management/TASK_BOARD.md` for the current follow-up work.
