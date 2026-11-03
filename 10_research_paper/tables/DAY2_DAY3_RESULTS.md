# Results tables for manuscript (2026-11-03)

## Day 2: held-out test, 450 images

| Configuration | GT count | Box AP50 | Box AP50:95 | Mask AP50 | Mask AP50:95 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Two-class overall (macro) | 70,289 | 0.5066 | 0.4313 | 0.4995 | 0.3963 |
| Two-class WB subset | 70,192 | 0.9920 | 0.8490 | 0.9890 | 0.7870 |
| Two-class BB subset | 97 | 0.0213 | 0.0141 | 0.0095 | 0.00571 |
| WB-only | 70,192 | 0.9921 | 0.8399 | 0.9906 | 0.7974 |

**Caution:** two-class overall mAP is a class-macro mean, not instance-weighted. The two-class and single-class models were evaluated against different annotation sets. Original paper AP values (0.712 @ 640, 0.846 @ 1280) are not directly comparable; different dataset, splits, protocols and metric interpretation.

## Day 3: WB-only mask area, 30-image random sample

| GT | Pred | Matched IoU≥0.5 | MAE px² | Mean relative abs error | Median relative abs error |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 4,970 | 5,146 | 4,900 | 207.4 | 8.80% | 7.34% |

**Caution:** errors only over 4,900 matched masks; 70 unmatched GT/246 unmatched predictions reported separately. Area is pixel², not mm².

## Day 3: qualitative sample (12 selected images)

| GT | Pred | Matched IoU≥0.5 | Unmatched GT | Unmatched Pred |
| ---: | ---: | ---: | ---: | ---: |
| 1,303 | 1,355 | 1,261 | 42 | 94 |

These are **sample counts**, not full-test detection precision/recall.
