# WP-02 C01 acquisition / QC feasibility audit

## Outcome
**ACQUISITION_BLOCKED_METADATA_UNCLEAR.** No original archive or images were downloaded; payload transfer is **0 bytes**. No extraction, image QC, split creation, model/weight acquisition, or training occurred. Selection remains PENDING. This is a blocked-scope evidence audit, not G0/G1 approval or scientific novelty assessment.

## Scope and preflight
Authorized root: `D:/Capstone/mushroom-research-2026`; branch `research/wp-02-feasibility-audit`; HEAD `f50f946b1d5f1bd11407c09b3b210ae0370fbde2`; initial working tree clean; WP01 `da1688a` verified as a commit object. User explicitly authorized bounded acquisition/QC; existing protocols still show gate prerequisites unresolved, and no gate is promoted here. Read WP01 C01 assessment/source dossier and screening, QC, leakage and research-gate protocols.

No shared state, registries, shared manifests or `.gitignore` changed. No staging/commit/push. Existing files preserved. No DS02 requests/assets.

## Exact-version source evidence
Target: https://data.mendeley.com/datasets/jrbx34k77g/2 ; DOI `10.17632/jrbx34k77g.2`.

- Live landing page HTTP 200 explicitly identifies snapshot version 2 and exact DOI; its HTML INITIAL_STATE reports CC BY 4.0. Files were a loading placeholder with empty initial client arrays: **not evidence that the dataset has no files**.
- Live DataCite exact DOI HTTP 200 confirms CC BY 4.0 and reports **761 images: 299 healthy, 147 single-infected, 315 mixed-infected**, originally HEIC from iPhone 11 Pro Max, converted to JPG, photographed at Mushroom Development Institute, Savar, Dhaka, Bangladesh. These are source statements, **not measured inventory**. DataCite sizes/formats arrays are empty and contentUrl is null.
- `/public-api/datasets/jrbx34k77g/versions/2` and its `/files` path returned 404.
- Public files/folders query routes, alternate datasets-v2 versioned files route and snapshot query returned 403.
- Two public files routes with `version=2` and `folder_id=root` in alternate query order returned HTTP 200 with `[]`. Without a usable folder tree these do not establish archive absence or completeness.
- Alternate datasets-v2 files query returned 404. Wayback availability lookup returned no snapshot. Public client JS route returned 403.
- Real-browser fallback failed before navigation because Chrome profile was locked; browser was not closed and settings were not changed.

**Original archive names, total size, content type, and exact-v2 download URL remain UNKNOWN.** The authorized maximum is 1.5 GiB (1,610,612,736 bytes). Because size/identity could not be established, acquisition stopped before any payload GET. No substituted archive or version was used.

## Storage and safety
`git check-ignore -v` confirms a prospective lowercase ZIP archive under candidate `source/` is ignored by `*.zip`; a prospective JSON metadata file in the same directory is not ignored. Thus no full source-folder ignore hides metadata. This is a prospective ZIP check only, not proof for an unknown actual filename. `raw/` is already ignored; no ignore edits were made. Original-archive checksum is unavailable because no archive was acquired.

No extraction ran. Before any future extraction, require exact archive metadata and ignore check for its actual filename, stream-enforced cumulative download cap, unchanged original archive hash, and inspected safe extraction with path traversal/absolute/drive/Windows alias checks, symlink/reparse rejection, expanded-byte/member/count/ratio limits and exclusive creation without overwrites, strictly inside candidate raw. Do not run dataset-supplied code.

## QC coverage and interpretation
`qc/image_inventory.csv` is **header-only**. Measured class folders/counts, image dimensions/channels/orientation, full decode corruption, SHA-256 exact duplicates, filename patterns, EXIF/date/bag/session clues and annotation support files are **NOT ASSESSED**, represented by null in statistics rather than fabricated zeros. Empty local inventory is not evidence that source images are missing. Perceptual/visual review was not performed. No images deleted or deduplicated.

No claim of image independence or biological confirmation is made. Missing bag/group metadata would be a leakage risk, not guaranteed leakage. Splits must wait for defensible specimen/batch/session grouping and review. Biological meaning of source classes remains unverified. No exact-dataset paper search was conducted in WP02: inherited relationship is **NO_EXACT_DATASET_PAPER_CONFIRMED**, not “no paper exists.” Prior WP01 GPU-time/VRAM/checkpoint-size assertions are not audited measurements and are not adopted. Three-folder classification is a source-proposed task, potentially manageable only after payload, labels and grouping are assessed; no GPU runtime estimate is supported here.

## Evidence and blockers
All paths below are relative to `04_dataset_candidates/C01_substrate_contamination/`:
- `qc/wp02_evidence/01_metadata.py`, `metadata_requests.json`, `landing_v2.txt`, `datacite_v2.txt`.
- `qc/wp02_evidence/02_metadata_alternatives.py`, `alternative_requests.json`.
- `qc/wp02_evidence/03_public_routes.py`, `public_route_requests.json`, `files_root.txt`, `files_version_first.txt`, `wayback.txt`.
- `qc/wp02_evidence/04_client_routes.py`, `execution_summary.json`, `ignore_checks.json`.
- `qc/wp02_evidence/05_finalize_blocked.py`, `06_verify.py`, `verification.json`.
- `qc/wp02_c01_download_manifest.csv`: one NOT_DOWNLOADED status row; blank path/bytes/hash/time/type mean unavailable, not a downloaded zero-byte archive.
- `qc/wp02_c01_statistics.json` and header-only `qc/image_inventory.csv`.

Next prerequisite: obtain lawful exact-v2 file/folder metadata from the publisher (or an accessible browser session/user-provided authoritative metadata), establishing original archive names, sizes, MIME types and URLs under the cap. Do not infer download availability from landing-page accessibility. Then rerun a separately authorized, safe acquisition/QC continuation; retain current evidence unchanged. G1 and training remain blocked pending integrity/label/grouping evidence and reviewed selection. Independent output/schema/count/checksum readback is recorded in `qc/wp02_evidence/verification.json`; it verifies blocked-scope documentation, not dataset integrity.
