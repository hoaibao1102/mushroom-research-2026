# Research task board — 9 November 2026

| Task | Status | Next action |
|---|---|---|
| Charisis cluster-tracking notebook | Prepared | Run smoke mode in Colab; verify Zenodo files and sequence IDs |
| MushR maturity notebook | Prepared | Run smoke mode; verify all COCO image paths against Kaggle files |
| Kaggle raw-image terms | Open | Check license/usage terms separately from the GitHub code license |
| NMS IoU 0.50 comparison | Preliminary | Evaluate on all 450 M18K V2 test images |
| M18K V2 annotation/duplicate flags | Open | Resolve the original Day 3 findings |
| RGB-D physical-area measurement | Blocked | Need verified depth scale, intrinsics and RGB-depth alignment |
| Course report update | Open | Add Day 5 NMS and RGB-D findings if required |
| Demo video | Open | Record the working WB-only Gradio app |

## Notebook run rule

Run smoke mode before full training. Send the executed notebook and first full traceback on failure. Do not change labels, architecture or split during troubleshooting.
