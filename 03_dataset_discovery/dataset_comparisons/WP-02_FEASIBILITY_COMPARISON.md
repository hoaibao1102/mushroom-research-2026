# WP-02 feasibility comparison

Scope: pre-selection audit only. No numeric rubric scores are assigned: unresolved evidence must not receive a high score or become a fabricated zero. Apply DATASET_SELECTION_CRITERIA.md hard blockers before weighted preferences.

| Criterion | C01 substrate contamination | C02 MushR |
|---|---|---|
| 1 Actual data availability | Metadata accessible; exact-v2 archive inventory/size/URL unresolved; acquisition BLOCKED | Two author COCO JSON acquired; complete fresh Kaggle metadata available; no images acquired |
| 2 Annotation completeness | Literal labels/files NOT_VERIFIED | Four category declarations, three populated; many image records empty; completeness of visual objects NOT_VERIFIED |
| 3 Image–label linkage | NOT_VERIFIED | Literal paths 0 matches; explicit wrapper-relative rule gives unique correspondence for all entries; pixels not checked |
| 4 Integrity | Payload/decode/hash QC BLOCKED | JSON structural checks pass with area diagnostics; image decode/pixel-mask agreement NOT_VERIFIED |
| 5 Independent samples | Bag/session/batch IDs unresolved | Filenames/groups available but not verified biological unit IDs |
| 6 Leakage risk | Cannot defend independent evaluation yet | All test paths and test annotation content occur in train; published split unsuitable as evidence of independent holdout |
| 7 Published method reproduction | NO_EXACT_DATASET_PAPER_CONFIRMED | Published paper/code available, but effective historical cohort/config lineage unresolved |
| 8 Engineering complexity | Classification setup plausibly simpler; estimate only | Instance segmentation plus flush clustering, unpinned dependencies, hardcoded roots and conflicting configs |
| 9 Compute feasibility | Unmeasured; old training-time estimates UNVERIFIED | Unmeasured locally; paper resource figures are source claims, not acceptance benchmarks |
| 10 Recent literature | WP01 bounded 2024–2026 related leads, no new literature search in WP02 | Foundational 2023 paper; recent follow-up coverage remains incomplete |
| 11 Contribution potential | HYPOTHESIS only; biological label and evaluation validity first | HYPOTHESIS only; reproduction repair is not automatically scientific novelty |
| 12 Oyster farm relevance | Proposed visible bag-condition screening; biological/pathogen interpretation unconfirmed | Paper's fruit-body/maturity and flush decision; whole-image classification changes objective |
| 13 Field validation | Consent/site/protocol/labels UNKNOWN | New site/camera domain and operational protocol UNKNOWN; no industrial claim established |

## Recommendation
Neither candidate should be selected automatically. C01: NEEDS_MORE_EVIDENCE because payload access and defensible independence are unresolved. C02: NEEDS_MORE_EVIDENCE overall; NO-GO for treating the current author-designated train/test pair as disjoint held-out evaluation. This does not prove historical misconduct or prohibit all possible uses of the underlying corpus.

Next: **Additional dataset QC**, explicitly authorized and targeted. Resolve authoritative C01 archive metadata; obtain author clarification of C02 cohort/split lineage, class policy and empty-image meaning. A new split or annotation repair requires human protocol approval. If these blockers cannot be resolved within project resources, recommend further candidate discovery rather than defending either dataset. No third candidate is initialized.

## Evidence
- C01 reports/WP-02_C01_DATA_FEASIBILITY.md and qc/wp02_c01_statistics.json.
- C02 reports/WP-02_C02_ANNOTATION_AUDIT.md, reports/WP-02_C02_IMAGE_LINKAGE.md, qc/coco_annotation_statistics.json and row-level qc/wp02_evidence/ artifacts.
- Historical source claims: WP01 registry/paper full text; interpret via WP-01_QC_ADDENDUM.md.
