# Day 2 — Reproduction of YOLOv8 detection and instance segmentation on M18K V2

**Date of recorded experiments:** 2026-11-02  
**Outcome:** Both pretrained YOLOv8n-seg configurations were trained for 10 epochs, saved and evaluated on the 450-image held-out **test** split. This is a reproduction of the **method/workflow on M18K V2**, not an exact numerical replication of Zakeri et al.'s original benchmark.

## Dataset and experiments

| Dataset | Train | Validation | Test | Total instances |
| --- | ---: | ---: | ---: | ---: |
| M18K V2 indexed images | 3,596 | 449 | 450 | 700,589 (BB: 858; WB: 699,731) |

Both models: YOLOv8n-seg, RGB input at 640, batch 8, 10 epochs, seed 42, AdamW, lr0=0.0001, Tesla T4. No RGB-D input was used for model training. A separate WB-only label conversion retained all images; six invalid WB train polygons were excluded, leaving 699,725 valid WB polygons.

| Test metric | Two-class, **overall mean of BB and WB** | Two-class, **WB class only** | WB-only (WB class) |
| --- | ---: | ---: | ---: |
| Test images | 450 | 450 | 450 |
| Test GT instances | 70,289 | 70,192 | 70,192 |
| Box AP@50 | 0.5066 | 0.992 | 0.9921 |
| Box AP@50:95 | 0.4313 | 0.849 | 0.8399 |
| Mask AP@50 | 0.4995 | 0.989 | 0.9906 |
| Mask AP@50:95 | 0.3963 | 0.787 | 0.7974 |
| Mask recall | 0.481 (class mean) | 0.962 | 0.9631 |

**BB class from the two-class experiment:** 97 GT test instances; BB mask AP@50=0.0095, mask AP@50:95=0.00571 and recall≈0. This affects the **macro-averaged** two-class score severely; it is not a WB segmentation failure. BB comprises only 0.122% of original annotations. Class imbalance is a plausible cause, not a proven isolated cause.

**Original paper reference:** Zakeri et al. (2025), Table 2, YOLOv8-N segmentation AP=0.712 at 640; AP=0.846 at 1280. The paper used a different main dataset subset (2,000 images) and train/val/test protocol, and metric equivalence is not established. **Do not claim to outperform the paper or to have reproduced its numerical benchmark.**

## Evidence and reproduction notes

- Two-class completed run/test summary: `12_reproducibility/logs/two_class_train_and_test_log_summary.txt` (structured excerpt from user-supplied console log).
- WB-only corrected test: `12_reproducibility/logs/WB_only_corrected_heldout_test_log_summary.txt` (user-supplied separate test run).
- Machine-readable metrics: `09_results/metrics/Day2_*_Heldout_Test_2026-11-02.json`.
- WB dataset validation: `09_results/metrics/wb_conversion_summary.json`, `wb_rebuild_verification.json` and Day 2 dataset report.
- Ultralytics 8.4.198, Python 3.13.16, PyTorch 2.11.0+cu130, Tesla T4 for the reported test runs.
- **Notebook caveat:** `Day2_WB_Only_Training_and_Day3_Error_Analysis.ipynb` contains an earlier test cell that accidentally evaluates two-class labels; its saved result is *not* used here. The corrected separate WB-only test metrics above are authoritative for this study.
- Checkpoints and the large WB labels ZIP remain on Drive; they are not included in Git or this archive.

## Conclusion

The team completed the Day 2 reproduction milestone: operational dataset preparation, successful training of both YOLOv8n-seg configurations and held-out test evaluation. The limitations regarding BB imbalance, non-identical original benchmark, and split leakage carry forward to Day 3.
