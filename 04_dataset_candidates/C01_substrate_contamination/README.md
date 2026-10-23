# C01 — Mushroom Substrate Contamination Classification

## Identification and source
- Candidate ID: C01
- Dataset URL (user supplied, not retrieved): https://data.mendeley.com/datasets/jrbx34k77g/2
- Identifier: `jrbx34k77g/2`
- Version: 2 (URL component supplied by user; not independently verified)
- Candidate status: PENDING_VERIFICATION; selection decision: PENDING.

## Known task definition
SOURCE_CLAIM from WP-00 specification: Classifying healthy and contaminated mushroom substrate bags. Expected direction: IMAGE_CLASSIFICATION. This is a proposed task, not a verified account of the actual labels.

## Known metadata
Only the supplied source URL, candidate name and identifier are recorded. Dataset payload, number of files, independent units, classes, collection conditions, licensing, authors, image resolutions, annotation format and splits are UNKNOWN. No dataset has been downloaded.

## Literature and unverified information
No paper using this exact dataset has been confirmed. Do not infer an association from similar titles or tasks.

## Potential research questions — HYPOTHESIS only
- Is the proposed task operationally meaningful compared with a non-ML workflow?
- Can a reproducible baseline generalize across biological units, batches or acquisition conditions?
- Could a lightweight approach meet a later agreed resource budget without losing meaningful performance?
No gap, improvement or deployment benefit is confirmed.

## Verification requirements
Record dated primary-source evidence for identity, ownership, version, access, license and annotation semantics. Check exclusion registry against exact identifiers and provenance. Document exact paper-dataset relationship or state unresolved. Later authorized QC must establish integrity, independent units, duplicates and grouping before selection/training.

## Current gate status
G0: NEEDS_MORE_EVIDENCE. G1–G6: NEEDS_MORE_EVIDENCE. No gate passed. Training NOT authorized.

## Next actionable steps
WP-01 only after authorization: verify the supplied source, record license/version/access and explicit source claims in `source/`, complete metadata and relationship verification in `dataset_metadata/`, record contradictions and produce a screening report. Do not download in WP-00; later authorized original data belongs in `raw/` (ignored), with checksums in versioned metadata. No DS-02 artifacts may be imported.
