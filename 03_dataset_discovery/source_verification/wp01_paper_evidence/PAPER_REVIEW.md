# MushR primary-paper review

Review scope: **FULL_TEXT_REVIEWED**, all 16 publisher PDF pages. Publisher landing HTML/XML returned HTTP 403; the lawful publisher-hosted PDF was accessible. DOI/title were cross-checked against Crossref. Source excerpts and claim rows are preserved beside this review.[1][2]

## Bibliographic identity

*MushR: A Smart, Automated, and Scalable Indoor Harvesting System for Gourmet Mushrooms*, Anant Sujatanagarjuna, Shohreh Kia, Dominique Fabio Briechle and Benjamin Leiding; Agriculture 13, 1533; published **1 August 2023**; DOI `10.3390/agriculture13081533`. The article is CC BY 4.0. This article license is not a substitute for checking dataset and code licenses.[1][2]

## Dataset and annotation scope

Authors report 34,400 scene images from three camera perspectives in each of two tents, captured simultaneously hourly by six Raspberry Pi HQ cameras over ten months. They distinguish a retained raw corpus from a selected annotated subset. Masks were manually annotated using CVAT for individual fruiting bodies, using visual cues and classes `not-ready`, `ready`, `overdue` (sections 4.1–4.2, PDF pp.7–8). These are **REPORTED_BY_SOURCE_NOT_AUDITED**, not independently counted images or biologically validated labels.[1]

Table 2 reports object instances, **not image counts**: training 723 not-ready, 1,344 ready, 692 overdue (2,759 total); testing 251 not-ready, 198 ready, 92 overdue (541 total). No sample-level split/group manifest was inspected by this paper review. The capture scheme creates a plausible same-scene/specimen/time dependency risk; it does not prove leakage actually occurred.[1]

## Exact paper–dataset relationship boundary

Appendix A (PDF pp.14–15) explicitly links `ETCE-LAB/MushR`, `ETCE-LAB/mushr-mask-r-cnn`, and Kaggle raw dataset slug `etcelab/mushr-project-raw-image-dataset-oyster-mushrooms`. It does **not** explicitly print supplied annotated slug `etcelab/mushr-annotated-dataset-oyster-mushrooms` or identify an annotated Kaggle version. Thus a direct annotated-slug citation cannot be claimed from the paper alone; the author-repository/Kaggle chain must be independently checked.[1]

## Baseline and actual reported evaluation

The paper describes COCO-initialized Detectron2 Mask R-CNN, linking R50-FPN configuration, learning rate 0.00015, batch size 2 and 40,000 iterations. It reports 2.7 GB memory and hardware named “Nvidia GTX 4090”; that source wording is retained rather than silently corrected or validated. These are author reports, not WP-01 execution measurements (section 4.2, p.8).[1]

The **91.72% value is training accuracy**, not held-out test accuracy. Held-out test results are COCO metrics: Table 3 reports bbox AP 61.876 and segmentation AP 49.332; bbox AP50 71.016 and segmentation AP50 70.639. Table 5 defines AP as IoU 0.50:0.05:0.95. These values are source-reported historical results only, not reproduced project results.[1]

Section 4.2 also clusters predicted masks with DBSCAN and combines class mask areas for flush-level harvesting decisions (p.9). Reviewer inference: changing this to whole-image classification would remove object localization and change decision semantics unless a new, explicitly justified task and labeling protocol were defined.[1]

## Author-stated limitations vs reviewer unknowns

Section 6 (pp.12–13) discusses lower AP for not-ready/small objects. Discussion and Limitations names lighting, oyster variations, occlusions, expensive mask annotation and lack of industrial production testing. Section 7 (p.14) suggests broader data/settings and alternative architectures. These are the authors' limitations/future-work statements, **not a validated current research gap**.[1]

Reviewer unknowns: exact current annotated Kaggle version and its relationship to the paper-era release; original train/test image membership and biological/batch/time independence; dataset license; pinned dependency/runtime compatibility; exact evaluation reproducibility and cross-site feasibility. No training, weights, dataset archives, source images or DS-02 artifacts were used in this review.

## Sources

[1] https://mdpi-res.com/d_attachment/agriculture/agriculture-13-01533/article_deploy/agriculture-13-01533.pdf — MushR: A Smart, Automated, and Scalable Indoor Harvesting System for Gourmet Mushrooms
[2] https://api.crossref.org/works/10.3390/agriculture13081533 — Crossref MushR DOI metadata
