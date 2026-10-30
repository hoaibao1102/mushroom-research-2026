# C03 Final Provenance Status

**As of:** 2026-10-30

**Status:** `ESSENTIAL_PROVENANCE_PENDING_AUTHOR_CLARIFICATION`

**Training authorized:** `NO`

| Question | Available evidence | Status | Closure requirement |
|---|---|---|---|
| Dataset identity | Zenodo record 20260929; archive/inventory hashes measured [Z] | `ESTABLISHED_FOR_RELEASED_PAYLOAD` | None for release identity |
| Historical paper equivalence | White class counts exactly match paper | `COUNT_COMPATIBLE_ONLY` | Historical file manifest/checksums or author confirmation |
| Biological repetition | WP-04B AI screen suggests repeated-looking and different specimens [B] | `NOT_VERIFIED` | Authoritative image-to-specimen mapping |
| Ordinal filenames | Equal ordinal failed as a reliable visual key [B] | `REJECTED_AS_GROUPING_KEY` | Do not use as identity |
| Specimen/session/farm/batch IDs | Not present in audited release | `MISSING` | Author-provided mapping with field definitions |
| Historical split/seeds | Paper reports 80/20 only [P] | `MISSING` | Original train/validation manifests and seeds |
| `kw → Cobweb` | Count/ontology compatibility; no direct token definition | `PROVISIONAL` | Data dictionary or explicit author confirmation |
| Diagnosis provenance | Expert mycologist annotation reported [P] | `AUTHOR_REPORTED_EXPERT_VISUAL` | Clarify whether laboratory confirmation exists |
| Contact route | Corresponding-author email in primary XML [P] | `VERIFIED_FROM_SAVED_PRIMARY_SOURCE` | Human sends inquiry |
| Inquiry response | Draft prepared | `DRAFT_NOT_SENT` | Actual send date and response evidence |

No specimen IDs have been inferred or created. AI screening, filename ordinals, image scores, and visible similarity are not authoritative biological identities.

## Bounded resolution plan

1. Human completes sender identity and sends `C03_AUTHOR_INQUIRY.md`.
2. Record the actual date in `C03_CORRESPONDENCE_TRACKER.csv`.
3. Preserve any response/attachments with permission and hashes.
4. Audit coverage, definitions, missing rows, class consistency, and cross-light relationships.
5. Reassess the estimand matrix on 2026-11-06.

If essential evidence remains unavailable, record separately:

- `AUTHOR_RESPONSE_NOT_RECEIVED` or the actual response state; and
- `REQUIRED_EVIDENCE_UNAVAILABLE`.

Neither means the author rejected the request. Do not start another unrestricted image-matching cycle.

## Sources

- **[P]** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226; saved XML contact locator `front/article-meta/author-notes/corresp`.
- **[Z]** Zenodo record https://zenodo.org/records/20260929 and C03 WP-04 inventory.
- **[B]** `03_dataset_discovery/source_verification/C03_SPECIMEN_GROUPING_AUDIT.md` and `C03_LABEL_SEMANTICS_AUDIT.md`.
