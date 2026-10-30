# WP-02 pre-selection dataset feasibility audit

## A. Executive Summary
Overall status: **PARTIAL / CONDITIONAL**. Authorized audit performed; C01 acquisition BLOCKED and C02 independent-holdout reproduction BLOCKED. These are actual findings, not fabricated completion. Timestamp: 2026-10-30T11:22:18.968369+07:00.
Repository: D:\Capstone\mushroom-research-2026. Branch research/wp-02-feasibility-audit, starting HEAD f50f946b1d5f1bd11407c09b3b210ae0370fbde2. Preflight clean; WP01 safely tracked in da1688a; initial validator38/38 and tests9/9 passed. Historical clean-tree wording was false at the time, later Git checkpoint resolves present preservation only.

## B. C01 Audit
Exact-v2 identity/license metadata accessible. File endpoints returned blocked/not-found/ambiguous empty responses; locked browser profile prevented fallback. No authoritative archive name/size/type/URL was established within authorized1.5GiB bound. No archive/images downloaded or extracted. Header-only image_inventory.csv correctly represents no inspected files, **not an empty dataset**. Reported761 images remain unaudited. Decode, dimensions, labels, EXIF grouping and exact/perceptual duplicate checks BLOCKED/NOT_VERIFIED. Source reported counts299/147/315 do not become measured statistics. NO_EXACT_DATASET_PAPER_CONFIRMED is bounded search scope, not proof no paper exists.

## C. C02 Audit
Pinned author commit e8a0493b193c15c5f6129d89d7f14d89e84a8868. Downloaded unchanged training JSON7337338bytes and test JSON1064392bytes; exact SHA256/source URLs/time are in WP-02_DOWNLOAD_MANIFEST.csv. No Kaggle image payloads or weights acquired.

| Partition | Image records | Annotated image records | Empty image records | Instances | Pinning(id1) | Not-Ready(id2) | Ready(id3) | Overdue(id4) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 330 | 172 | 158 | 2759 | 0 | 723 | 1344 | 692 |
| test | 41 | 24 | 17 | 541 | 0 | 251 | 198 | 92 |

Four categories declared; only three populated. Populated counts exactly match paper Table2. No automatic class deletion/remapping. No within-split duplicate IDs, orphan image/category references or invalid polygon/bbox structures detected by static checks. Shoelace-vs-declared area diagnostic exceeds max(1pixel²,1%) for21train/14test annotations; this is a diagnostic, not automatic proof corrupt labels. Actual images were not decoded;3040x4056 is declared metadata.

Fresh complete Kaggle metadata16pages/3011unique paths. Literal path matches0. Every one of371partition entries has ambiguous basename candidates. Explicit comparison-only wrapper rule resolves all371entries to330unique Kaggle paths;2681Kaggle paths unmatched under that rule. This does not prove pixel identity or completeness. All41test paths occur in train; all541test annotation contents match train after replacing image_id with filename and ignoring annotation id. Parent independently re-read JSON and recomputed this finding. Split-local ID collisions alone are not the basis of this conclusion.

Source timestamp patterns are filename-derived/timezone-unverified; biological specimen/camera/cycle linkage unverified. No image/perceptual duplication audit. Static author code still has hardcoded roots, unpinned Detectron2/PyTorch, saved80-class config vs4declared classes, shell/YAML/paper hyperparameter and checkpoint/output lineage conflicts. No installation/runtime/training performed.

## D. Risk Assessment
Main risks: unsupported sample independence, overlapping advertised split metadata, unresolved empty-image semantics, biological label validity, file-level image integrity and historical training cohort. Old training-time forecasts are UNVERIFIED engineering estimates. Provenance conclusion: PROVENANCE_DISTINCT_IMAGE_OVERLAP_NOT_TESTED. No DS02 assets acquired; no new DS02 requests. Existing public landing metadata is historical evidence, not dataset payload.

## E. Candidate Comparison
See WP-02_FEASIBILITY_COMPARISON.md13criteria. C01 may be simpler engineering but cannot currently be audited at payload level. C02 source/annotations are accessible and numerically consistent with paper counts, yet independent-holdout reproduction is not established. Neither is automatically selected; no numeric scores assigned to unknown criteria, no novelty claimed.

## F. G0 / G1 Recommendations
C01:G0 NEEDS_MORE_EVIDENCE; G1 NEEDS_MORE_EVIDENCE.
C02:G0 GO recommendation for source identity/access only, pending human ratification; G1 NEEDS_MORE_EVIDENCE, with NO-GO for current author JSON pair as evidence of independent heldout evaluation.
No canonical gate is marked passed. G2–G6 unpassed, dataset_selected=false, training_authorized=false unchanged. Source identity and QC/reproducibility are separate gates.

## G. Remaining Blockers
1. Obtain authoritative C01 v2 archive metadata before any further download.
2. Establish C02 effective original cohort/split/checkpoint lineage and seek author clarification of full test-in-train metadata.
3. Human decision on category policy, empty images and any new grouped split; do not silently repair source.
4. Future authorized image integrity/pixel-label/grouping checks; physical independence still unknown.
5. Reproducible environment and literature/gap investigation only after source/data feasibility decisions.

## H. Next Work Package
Recommend **Additional dataset QC**, narrowly scoped to these blockers and separately authorized. If resolution effort is unjustified, pursue further candidate discovery instead. Neither next package executed. No commit/push/merge, model selection, weights, training or final dataset selection performed.

## I. Validation evidence
See setup_reports/WP-02_validation.json for actual commands, exit codes and structural/source-hash verification. Candidate-level checks are in each qc/wp02_evidence/ folder. Original WP00/WP01 validators are preserved, not weakened; expected phase-contract failures must be distinguished from data defects. Validation PASS means artifact consistency, not scientific gate acceptance. The report's quantitative statements were recomputed from source files rather than inferred from delegated summaries.
