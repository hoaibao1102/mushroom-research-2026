# Research status — 10 November 2026

| Work | Status | Latest record |
|---|---|---|
| M18K V2 EDA and YOLOv8n-seg tests | Complete | [Days 1–2](../09_results/README.md) |
| Prediction review and mask-area analysis | Complete | [Day 3 reports](../09_results/README.md) |
| Full-test area evaluation, Otsu baseline and inference demo | Complete | [Day 4 reports](../09_results/README.md) |
| Dense-scene NMS comparison | Preliminary | Eight selected images only; full 450-image test pending |
| RGB-D area feasibility | Checked | Depth scale/intrinsics/alignment unverified; no mm² result |
| WB-only Gradio demo | Working | Colab run confirmed by user |
| Charisis cluster-tracking notebook | Prepared; real-data run not evidenced in this archive | See [Day 7 report](../09_results/reports/Day7_Notebook_Preparation_2026-11-09.md) |
| MushR maturity notebook | Prepared; real-data run not evidenced in this archive | See [Day 7 report](../09_results/reports/Day7_Notebook_Preparation_2026-11-09.md) |
| Local application prototype | Implemented; initial user run reported working overall | [Day 8 report](../09_results/reports/Day8_Local_Application_Prototype_2026-11-10.md) |
| Application model inference / AMD runtime | Not verified by this archive | No trained checkpoint in the bundled app snapshot; DirectML unavailable in validation environment |
| Dataset QC and source permissions | Open | See [current task board](TASK_BOARD.md) |

## Research-side next steps

1. Verify the real Charisis and MushR dataset schemas, image joins and source permissions against the actual data used for training.
2. Keep model-quality claims tied to full, held-out evaluations rather than smoke runs.
3. Recheck NMS IoU 0.50 on all 450 M18K V2 test images.
4. Resolve M18K V2 annotation/duplicate flags and RGB-D calibration gaps where those results remain in use.
5. Record the separate application repository URL on the root README when it is available; keep ongoing product development outside this research repo.
