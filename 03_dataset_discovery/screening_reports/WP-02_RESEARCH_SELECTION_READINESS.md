# WP-02 research selection readiness

Dataset selection: PENDING_HUMAN_REVIEW. Training authorization: NO. Research gap validated: NO.

| Candidate | G0 recommendation | G1 recommendation | Reason |
|---|---|---|---|
| C01 | NEEDS_MORE_EVIDENCE | NEEDS_MORE_EVIDENCE | Source/version/license documented but actual v2 payload accessibility unresolved; no image or grouped-split QC |
| C02 | GO for source identity/access only; human ratification pending | NEEDS_MORE_EVIDENCE; current published holdout use NO-GO | Author JSON identity/checksums and platform linkage established; split metadata overlaps, no pixel/biological independence audit |

G0 GO recommendation is limited to source identity; PROVENANCE_DISTINCT_IMAGE_OVERLAP_NOT_TESTED is the exclusion comparison scope. It is not a claim of mathematically zero overlap and does not override the DS-02 exclusion. Existing canonical gate flags are not changed or marked passed. G1–G6 remain unpassed; no source availability result authorizes training.

## Closure requirements
1. C01: authoritative exact-v2 archive names/size/type/download URL within 1.5 GiB; then separately approved integrity, grouping and label audit. Not an assumption that source is empty or permanently inaccessible.
2. C02: author explanation of test-in-train metadata, original loader/cohort/checkpoint lineage; human-reviewed independent-unit split policy, not automatic removal of test images.
3. C02: declared empty records versus intentionally negative images; four category schema with zero Pinning instances; reconcile 80-class config with effective historical model.
4. Both: biological/operational label validity and collection-group independence; no true independent sample count established.
5. Only after data feasibility and human review: literature/gap verification; no confirmed contribution is claimed.

Recommended next work package: **Additional dataset QC**. Do not execute it as part of WP02. Compare effort against a further candidate search if blocker resolution is not practical.
