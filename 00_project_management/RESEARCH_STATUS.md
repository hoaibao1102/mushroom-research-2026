# Research status — 9 November 2026

| Work | Status | Latest record |
|---|---|---|
| M18K V2 EDA and YOLOv8n-seg tests | Complete | [Days 1–2](../09_results/README.md) |
| Prediction review and mask-area analysis | Complete | [Day 3 reports](../09_results/README.md) |
| Full-test area evaluation, Otsu baseline and inference demo | Complete | [Day 4 reports](../09_results/README.md) |
| Dense-scene NMS comparison | Preliminary | Eight selected images only; full 450-image test pending |
| RGB-D area feasibility | Checked | Depth scale/intrinsics/alignment unverified; no mm² result |
| WB-only Gradio demo | Working | Colab run confirmed by user |
| Charisis cluster tracking notebook | Prepared; not run | Real Zenodo data and Colab smoke run pending |
| MushR maturity notebook | Prepared; not run | Kaggle image join and Colab smoke run pending |
| Dataset QC and source permissions | Open | See current task board |

## Next

1. Run the Charisis smoke test and verify its sequence/image mapping.
2. Run the MushR smoke test and verify the GitHub annotation-to-Kaggle image join.
3. Review the Kaggle image dataset terms before redistribution.
4. Recheck NMS IoU 0.50 on all 450 M18K V2 test images.
