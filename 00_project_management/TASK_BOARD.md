# Research task board — 10 November 2026

| Task | Status | Next action |
|---|---|---|
| Day 8 local application prototype | Implemented; 7/7 unit tests pass | Keep this repo as the research record; app development moves to a separate repository |
| Application repository link | Pending | Add the app repo URL to the root README when available |
| Charisis cluster-tracking workflow | Prepared in Day 7 notes; run evidence not present in this archive | Verify the actual Zenodo sequence/image mapping and retain executed results |
| MushR maturity workflow | Prepared in Day 7 notes; run evidence not present in this archive | Verify the COCO-to-Kaggle image join and retain executed results |
| Kaggle raw-image terms | Open | Check license/usage terms separately from the GitHub code license |
| NMS IoU 0.50 comparison | Preliminary | Evaluate on all 450 M18K V2 test images |
| M18K V2 annotation/duplicate flags | Open | Resolve the original Day 3 findings |
| RGB-D physical-area measurement | Blocked | Need verified depth scale, intrinsics and RGB-depth alignment |
| Target Windows model inference / AMD runtime | Not verified | Test actual model bundles on the target machine; preserve CPU fallback |

## Notebook run rule

Run smoke mode before full training. Keep each source's classes, split and metrics separate. Send the executed notebook and first full traceback on failure; do not change labels, architecture or split during troubleshooting without recording the change.
