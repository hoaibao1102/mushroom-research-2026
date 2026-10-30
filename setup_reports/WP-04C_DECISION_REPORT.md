# WP-04C — C03 Final Provenance Resolution & GO/NO-GO

**Decision preparation:** 2026-10-30

**Decision deadline:** 2026-11-06

**Branch:** `research/wp-04c-final-decision`

**Dataset selected:** `NO`

**Training authorized:** `NO`

**Research gap validated:** `NO`

## 1. Executive decision

C03 receives **`CONDITIONAL_GO` only for the bounded author-clarification step**. Under current evidence, the recommendation for claims about unseen biological specimens, unseen farms, or independent illumination robustness is **`NO_GO_FOR_PRIMARY_GENERALIZATION`**.

A narrow image-file-level benchmark could be defined transparently, but it would estimate performance on withheld released files—not biological generalization—and is not currently a sufficiently strong primary capstone contribution. No split or training is authorized.

## 2. WP-04B preservation

WP-04B was reviewed, committed, pushed, and read back successfully:

- Commit: `3f45000f0bf2299d9eb7ecf7376dbc1592af1e57`
- Message: `docs(research): complete WP-04B scientific readiness`
- Remote branch: `origin/research/wp-04b-c03-readiness`
- Commit contents: 19 reviewed project files
- Forbidden payloads in commit: none

The checkpoint excludes raw images, RAR/ZIP archives, model weights, publisher full-text captures, and C04 static source copies. WP-04C outputs remain uncommitted and unpushed.

## 3. Author contact and inquiry

The corresponding-author address **`ugur.coruh@erdogan.edu.tr`** is present in the saved primary-paper XML at `front/article-meta/author-notes/corresp[@id="c1-agronomy-15-00226"]/email`.[P]

An English inquiry covering specimen repetition, specimen mapping, acquisition metadata, historical split/seeds, `kw` semantics, exact white-set equivalence, and diagnosis provenance has been prepared. Status: **`DRAFT_NOT_SENT`**. Sender details and contact date remain blank for human completion. No response or rejection is claimed.

## 4. Provenance findings

- The Zenodo record and local 9,403-image payload identity are established.[Z]
- Exact equivalence of the released 3,195 White images to the historical paper corpus is only count-compatible, not pixel/manifests verified.
- No authoritative specimen, session, farm, date, or batch mapping is available.
- The 120-pair WP-04B judgments are AI screening only; no human-confirmed biological identity exists.[B]
- Equal filename ordinals are not reliable grouping keys.
- `kw → Cobweb` remains provisional.
- The paper reports expert mycologist annotation, but laboratory confirmation was not established in reviewed Methods.[P]

## 5. Estimand decision

| Scope | Current decision |
|---|---|
| A. Withheld released image files | Narrow descriptive estimand is conceptually possible, but dependence remains uncontrolled and no protocol/split is approved. |
| B. Changing illumination | Not identified as a same-specimen illumination effect; pairing and specimen-disjoint groups are missing. |
| C. Previously unseen biological specimens | `NOT_DEFENSIBLE_CURRENTLY`. |
| D. Unseen farms/cultivation sessions | `NOT_DEFENSIBLE_CURRENTLY`. |

A or B must not be presented as evidence for C or D.

## 6. Research-gap decision

Existing bounded evidence already covers White-light CNN classification, multi-illumination collection, color-space approaches, domain shift, and group/leakage-aware evaluation methods.[L] The absence of an independent test in the original paper is not itself novelty.

The unresolved issue is a **data/evidence gap**: the current release lacks authoritative dependencies needed to identify biological or farm-level generalization. No literature-gap or novelty claim is validated.

## 7. Deadline rule

A human may send the prepared inquiry immediately after completing sender details. At the 2026-11-06 review:

1. record whether the inquiry was actually sent;
2. record whether a response arrived;
3. separately assess whether the required evidence was supplied and resolves the blockers.

No response means only “response not received”; it does not mean rejection. If essential grouping and label evidence remains unavailable, retain `NO_GO_FOR_PRIMARY_GENERALIZATION` and evaluate a dataset with authoritative grouping and independent evaluation support.

## 8. Authorization state

- Model training: `NOT_AUTHORIZED`
- Split creation: `NOT_AUTHORIZED`
- Final topic selection: `NOT_AUTHORIZED`
- Dataset selection: `PENDING`
- Research gap: `UNVALIDATED`
- WP-04C commit/push: `NOT_PERFORMED`

## Sources and evidence boundaries

- **[P] Primary paper:** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226. Saved full-text XML: `03_dataset_discovery/source_verification/wp03_stream_a/paper_xml_alternate.txt`; contact locator: `front/article-meta/author-notes/corresp`; Methods locators cover dataset, annotation, preprocessing, and 80/20 validation.
- **[Z] Primary dataset:** https://zenodo.org/records/20260929; local identity/inventory evidence in `03_dataset_discovery/source_verification/C03_DEEP_SOURCE_VERIFICATION.md` and `04_dataset_candidates/C03_agaricus_disease/qc/image_inventory.csv`.
- **[B] Project audit:** `C03_SPECIMEN_GROUPING_AUDIT.md`, `C03_LABEL_SEMANTICS_AUDIT.md`, and candidate-local WP-04B review artifacts. These are audit evidence, not primary biological ground truth.
- **[L] Bounded literature evidence:** `C03_GAP_PRESCREEN.md` and candidate-local `literature_registry.csv`; no unrestricted literature search was performed in WP-04C.
