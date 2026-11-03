# Manuscript structure — working draft updated 2026-11-03

The original outline was a planning artifact. An actual **working draft** is now available at `10_research_paper/drafts/M18K_V2_Day3_Research_Draft_2026-11-03.md` (and `.docx`).

1. Introduction — mushroom localization and instance segmentation in dense growing beds.
2. Related work — Zakeri et al. (2025) and YOLOv8 segmentation; avoid invented advances.
3. Data — M18K V2: 4,495 indexed images, 700,589 annotated objects, BB rarity, dataset split and quality limitations.
4. Methods — RGB-only YOLOv8n-seg, two-class and WB-only training, conversion, matched mask-area calculation in px².
5. Experiments — actual 10-epoch settings, held-out test metrics; distinguish training/validation/test and individual class means.
6. Results — Day 2 BB/WB and WB-only performance; Day 3 30-image area error and 12-image qualitative review.
7. Discussion — imbalance, touching caps, boundary errors, suspected annotation issues, unverified leakage, and non-comparability with the original paper.
8. Conclusion — successful workflow reproduction **on V2**, no physical mm² or quality prediction claims.

**Open before submission:** source/license review, raw COCO inspection for 004252/004472, full train/test duplication review, correct academic references, selected figure permissions. This draft is not a finalized submission.
