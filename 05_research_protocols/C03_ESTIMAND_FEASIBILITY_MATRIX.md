# C03 Estimand Feasibility Matrix

**Assessment date:** 2026-10-30

**No split created; no model trained.**

| Estimand | Required grouping/evidence | Available evidence | Missing evidence | Main leakage/confounding risk | Defensible now? |
|---|---|---|---|---|---|
| **A. Image-level classification within the released dataset** | Unique file IDs, immutable file-level sampling rule, exact-overlap control, transparent label scope | 9,403 decoded JPEGs; class/light counts; no exact SHA duplicates [Z,B] | Approved sampling/split protocol; biological dependencies; full label certainty | Same specimen/views may cross file partitions; near-dependencies and label noise | **Conditionally definable only as a descriptive source-label file benchmark.** It cannot support new-specimen claims. |
| **B. Performance under changing illumination** | For causal paired-light effect: verified same-specimen pairs; for domain transfer: specimen-disjoint groups and balanced labels | White/UV/Mixed folders and acquisition descriptions [P,Z] | Authoritative pairing, specimen groups, acquisition covariates | Light may be confounded with specimen/session/class; repeated specimens can cross domains | **Not defensible as independent illumination robustness.** Folder-level descriptive comparison may be possible after protocol approval. |
| **C. Previously unseen biological specimens** | Complete specimen IDs covering all views/lights; enough independent specimens per class | Only bounded AI screening, not identity evidence [B] | Authoritative mapping and independent group counts | Same specimen in train/test; fabricated similarity groups | **No. `NOT_DEFENSIBLE_CURRENTLY`.** |
| **D. Unseen farms or cultivation sessions** | Image-to-farm/session/batch/date membership; multiple held-out units with class support | Paper reports multiple farms/visits at aggregate level [P] | Image-level memberships and sufficient independent units | Farm/session/device/background may be confounded with class and light | **No. `NOT_DEFENSIBLE_CURRENTLY`.** |

## Claim boundaries

- A estimates performance on released files only.
- B does not prove C unless specimens are disjoint or paired appropriately.
- Neither A nor B proves D.
- Expert-source-label performance is not laboratory-confirmed disease performance.
- Historical manifests may help reproduce the paper but do not by themselves establish biological independence.

## Acceptance before revising the protocol

1. Mapping covers every included file or gives an explicit exclusion reason.
2. Definitions of specimen/session/farm/batch are supplied.
3. Cross-light relationships and independent group counts are audited.
4. `kw` semantics and diagnosis provenance are clarified.
5. A target population and primary estimand are declared before split generation.
6. A group-aware sealed evaluation protocol receives human approval.

Without these conditions, the primary-generalization protocol remains blocked.

## Sources

- **[P]** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226.
- **[Z]** https://zenodo.org/records/20260929 and measured C03 inventory.
- **[B]** WP-04B specimen and label audits.