> **Historical alternative as of 2026-10-30:** Team 10 is currently analyzing C03 M18K V2. This earlier candidate remains in the registry for continuity; it was not selected, independently verified or discarded by a formal new decision.

# C02 — Oyster Mushroom Harvest Readiness

## Identification and source
- Candidate ID: C02
- Dataset URL (user supplied, not retrieved): https://www.kaggle.com/datasets/etcelab/mushr-annotated-dataset-oyster-mushrooms
- Identifier: `etcelab/mushr-annotated-dataset-oyster-mushrooms`
- Version: UNKNOWN
- Candidate status: PENDING_VERIFICATION; selection decision: PENDING.

## Known task definition
SOURCE_CLAIM from WP-00 specification: Recognition of oyster mushroom harvest-readiness states. Expected direction: CV_CLASSIFICATION_OR_DETECTION_NOT_VERIFIED. This is a proposed task, not a verified account of the actual labels.

## Known metadata
Only the supplied source URL, candidate name and identifier are recorded. Dataset payload, number of files, independent units, classes, collection conditions, licensing, authors, image resolutions, annotation format and splits are UNKNOWN. No dataset has been downloaded.

## Literature and unverified information
Possible associated paper supplied by user: https://www.mdpi.com/2077-0472/13/8/1533 . Relationship is NOT_VERIFIED. Title, authors, DOI and metadata have not been checked. C02 is not assumed to be DS-02; exact identity and overlap must be checked separately.

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
