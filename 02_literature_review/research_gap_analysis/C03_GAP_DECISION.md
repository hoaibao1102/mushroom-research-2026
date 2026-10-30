# C03 Research Gap Decision

## Decision question

> Can illumination-robust disease classification be evaluated reliably using the currently released C03 data?

**Answer:** Not as unseen-specimen or unseen-farm generalization with the currently available evidence.

## Evidence classification

### Author-stated scope and limitations

- The 2025 paper evaluates 3,195 White-light images using pretrained CNNs and an 80/20 train/validation design.[P]
- The paper reports no independent test set and identifies broader geographic/environmental robustness as future work.[P]
- Dataset sources describe multiple illumination conditions.[Z]

### Demonstrated audit weaknesses

- Equal filename ordinal is not a reliable specimen-grouping key.[B]
- The release does not contain authoritative specimen/session/farm mappings.[B,Z]
- Validation in the historical paper was used for tuning/evaluation; exact historical reproduction artifacts are unavailable.[P,B]

These facts do not prove that historical leakage occurred; they show that independence cannot be verified.

### Hypotheses, not findings

- Illumination shift may reduce classification performance.
- Group-aware evaluation may differ from random image-level evaluation.
- Multi-light training may improve unseen-light robustness.

None of these hypotheses was tested in WP-04C.

### Approaches already represented in bounded prior work

The reviewed evidence already includes White-light CNN classification, multi-illumination acquisition, A. bisporus color-space analysis, domain adaptation, identity-aware splitting, and leakage-aware agricultural evaluation.[L] Therefore, adding a new backbone, an independent test set, or standard augmentation is not automatically novel.

## Gap classification

- `DATA_GAP`: specimen/session/farm membership is missing.
- `EVIDENCE_GAP`: label semantics and historical equivalence remain unresolved.
- `LITERATURE_GAP`: **not validated**.
- Scientific novelty: **unverified**.

## Contribution decision

The release can support provenance/reproducibility research and potentially a narrowly disclosed image-file-level benchmark. It does not currently support a defensible primary claim of biological illumination robustness or unseen-farm generalization.

Recommendation: `CONDITIONAL_GO` only for bounded author clarification until 2026-11-06. If closure fails, use `NO_GO_FOR_PRIMARY_GENERALIZATION` and assess another dataset rather than inventing identities or launching additional unrestricted matching.

## Sources

- **[P]** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226.
- **[Z]** https://zenodo.org/records/20260929.
- **[B]** WP-04B C03 specimen, label, and reproduction audits.
- **[L]** `C03_GAP_PRESCREEN.md` and candidate-local `literature_registry.csv`; bounded coverage only.