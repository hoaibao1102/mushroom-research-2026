from pathlib import Path
import json,csv,hashlib,datetime,collections
R=Path('D:/Capstone/mushroom-research-2026'); C=R/'04_dataset_candidates/C03_agaricus_disease'; Q=C/'qc'; E=Q/'wp04_evidence'
s=json.loads((Q/'summary.json').read_text()); d=json.loads((E/'live_record.json').read_bytes()); f=d['files'][0]; rows=json.loads((Q/'inventory.json').read_text()); dup=json.loads((Q/'duplicates.json').read_text())
with (C/'acquisition_manifest.csv').open(newline='',encoding='utf-8') as inp: acq=list(csv.DictReader(inp))[0]
# Filename indices are clues only; no specimen joins asserted.
clues={}
for light in ['white','uv','mix']:
 selected=[r for r in rows if r['illumination_folder']==light]
 clues[light]={'examples':[r['path'].split('/')[-1] for r in selected[:5]],'distinct_filenames':len({r['path'].split('/')[-1] for r in selected}),'exif_keys':dict(collections.Counter(k for r in selected for k in r.get('exif_keys',[])))}
(E/'grouping_clues.json').write_text(json.dumps({'status':'UNVERIFIED','notes':'Per-light/class folder and ordinal file names are not specimen IDs. No authoritative train/validation/test split or specimen/farm/session mapping bundled: all extracted members are JPEGs. Cross-light pairing by ordinal unsupported.','lights':clues},indent=2))
classrows=[]
for code,label,paper in [('hl','Healthy',731),('bb','Bacterial Blotch',576),('db','Dry Bubble',665),('kw','Cobweb (provisional kw mapping)',664),('wb','Wet Bubble',559)]:
 vals=[sum(v for k,v in s['by_light_class'].items() if k.startswith(light+'/') and k.endswith('_'+code)) for light in ['white','uv','mix']]
 classrows.append(f'| {label} | {paper} | {vals[0]} | {vals[1]} | {vals[2]} |')
text=f'''# C03 deep source verification — WP04

- Decision: **NEW_PROTOCOL_REQUIRED** (reviewer assessment, not a paper fact).
- Acquisition: **ACQUIRED_CHECKSUM_VERIFIED**; exact record only. Technical integrity QC complete; scientific dataset-selection/G1 gate **BLOCKED** pending biological grouping, label provenance and approved evaluation protocol. **Training authorization: NO**.
- Reviewer: Hermes automated source/QC audit. Retrieval UTC: {acq['retrieved_utc']}. Branch `research/wp-04-deep-verification`, starting HEAD `7076719a2ee61a4922068d6326b8261be716af14` verified before writes.
- Scope: only C03 source verification, unchanged authorized archive, safe extraction and image QC. No final dataset, research-gap declaration, training, model implementation, alternative record/version, DS02 transfer, commit or push. Shared registries/state and `.gitignore` not edited. All prior originals preserved.

## 1. Live exact-record identity and lawful access

Primary live source: https://zenodo.org/api/records/20260929 (landing https://zenodo.org/records/20260929). Independent DOI metadata: https://api.datacite.org/dois/10.5281/zenodo.20260929. Preserved responses: `04_dataset_candidates/C03_agaricus_disease/qc/wp04_evidence/live_record.json`, headers JSON and `datacite_exact.json`.

| Field | Directly observed metadata |
|---|---|
| Exact DOI | `10.5281/zenodo.20260929` |
| Title | {d['metadata']['title']} |
| Publisher | Zenodo (confirmed DataCite) |
| Published / created / modified | {d['metadata']['publication_date']} / {d['created']} / {d['modified']} |
| Version | Explicit version label absent/null; version index 0, is_last true in this snapshot; record revision {d['revision']}. Concept `20260928` is metadata only, not downloaded. |
| Structured creator | ALBAYRAK, ÜMIT; Selçuk University; ORCID 0000-0002-7942-7191 |
| Structured contributors | GÖLCÜK, ADEM (Researcher), ORCID 0000-0002-6734-5906; AKTAS, SINAN (Researcher), ORCID 0000-0003-1657-5901 |
| Access / license | Open / CC-BY-4.0; DataCite gives https://creativecommons.org/licenses/by/4.0/legalcode |
| Exact file | `{f['key']}` |
| Files / compressed bytes | 1 / {f['size']} decimal bytes; below hard limit 500000000 |
| Publisher checksum | `{f['checksum']}` |
| Measured MD5 | `{acq['md5']}` — match |
| Measured SHA-256 | `{acq['sha256']}` |
| Measured bytes | {acq['actual_size_bytes']} — match |

Structured creator/contributor metadata is not the six-person narrative citation: the description lists Albayrak, Golcuk, Aktas, Coruh, Tasdemir and Baykan. Both are retained without silently replacing one with the other. Description's suggested dataset citation title also differs from structured title. Article six-author metadata is preserved in `paper_review.json`.

Rights decision: explicit later author-associated open CC-BY-4.0 deposit, also confirmed by DOI registration, permits this bounded acquisition/QC with attribution and license notice; retain attribution to deposited creator/contributors and related paper on any permitted reuse, indicate derived QC changes. CC-BY permits reuse/adaptation subject to attribution; it does not establish privacy consent, diagnostic validity or rights in every depicted object. Paper's Data Availability statement says data were not public because of privacy/confidentiality (local full text line 120); later release is a temporal access difference, not proof the paper statement was false or every privacy issue is resolved. Preserve and escalate that uncertainty before publication/redistribution. No bulk payload is tracked.

Archive ignore gate was checked **before transfer**: existing `.gitignore:62:*.rar`, captured in `ignore_check.txt`; no ignore edit. JPEGs are already globally ignored. Initial connection reset after 1048576 bytes; preserved that prefix, resumed same exact URL with checked HTTP 206 Content-Range, no restart/version substitution. Final size and publisher MD5 passed. Range progress/errors retained in `resume_log.json`; no >500MB archive transfer occurred. `acquisition_manifest.csv` records the actual completed result.

## 2. Safe extraction and measured inventory

Extractor: Windows `C:/Windows/System32/tar.exe`, **bsdtar/libarchive 3.8.9**, `-x -k` into a newly created empty `source/extracted/`. Python rarfile 4.5 inspected the complete header list first. Rejected absolute/drive/traversal paths, symlinks/redirections, encrypted entries, case-fold duplicate names and Windows special names. Declared expansion ceiling **3000000000 bytes**; actual expanded file bytes **{s['expanded_bytes']}**. No overwrite permitted; extracted tree reconciled to headers by paths and sizes. No bundled code executed. All {s['physical_files']} physical extracted files are JPEGs, distinct from the single original RAR. Header listing also contains 19 directories (including wrapper). Exact header list: `qc/archive_members.json`; extraction command/result: `qc/wp04_evidence/extraction_log.json`.

Measured image QC (Pillow {s['pillow']}, verify followed by independent reopen/full load):
- Images successfully decoded: **{s['image_decode_ok']}**; decode errors: **{len(s['decode_errors'])}**; non-image files: **{len(s['non_images'])}**.
- Dimensions: `{json.dumps(s['dimensions'])}`; color modes/channels: `{json.dumps(s['modes'])}` (channel count retained per image).
- EXIF keys observed: `{json.dumps(s['exif_keys'])}`; source orientation tags retained per-image; no silent rotation/recompression or repair applied.
- SHA-256 computed on every original extracted file; exact duplicate groups: **{s['sha256_duplicate_groups']}**, files participating: **{s['sha256_duplicate_files']}**.
- Perceptual screening: **{s['perceptual_candidates']} pairs**, all-pairs ImageHash 4.3.2 64-bit dHash Hamming distance <=4. Threshold is heuristic/uncalibrated, not a confirmed duplicate or biological identity rule; candidates require image-level human review. Cross-class/light edges retained, not removed.

Inventory `qc/inventory.json` (plus checkpoint JSONL) includes relative paths, bytes, mtime_ns, extension, SHA-256, decoding result, dimensions, modes/channels, EXIF and dHash. `qc/duplicates.json` includes exact groups and perceptual candidates. No files excluded/deleted/quarantined. These are image-integrity checks, **not disease-label validation**; no human pathologist adjudication or calibrated near-duplicate review was performed.

## 3. Paper–deposit reconciliation: white subset matches counts, not historical identity

Primary paper: **Classification and Analysis of Agaricus bisporus Diseases with Pre-Trained Deep Learning Models**, DOI https://doi.org/10.3390/agronomy15010226, Agronomy 15(1), 226, MDPI, 2025. Local publisher XML-derived full text reviewed: `03_dataset_discovery/source_verification/wp03_stream_a/paper_agronomy_fulltext.txt`; source hashes and literal line passages retained in `qc/wp04_evidence/paper_review.json`. Source XML `paper_xml_alternate.txt` remains unchanged. Zenodo explicitly marks `isSupplementTo` this DOI and says it was used in the publication: **author-linked dataset**, not independently demonstrated byte-for-byte paper-era release.

| Class | Paper white (section 2.2) | Measured white | Measured UV | Measured mix |
|---|---:|---:|---:|---:|
{chr(10).join(classrows)}
| Total | 3195 | {s['by_light']['white']} | {s['by_light']['uv']} | {s['by_light']['mix']} |

The `kw` class-folder mapping to Cobweb is a **provisional inference** from the declared five categories, counts and remaining class; no separate label dictionary is bundled. Do not silently rename source folders. All deposited JPEGs total {s['image_decode_ok']}, not 3195; only the white subfolder reproduces paper per-class counts. Matching counts are evidence of compatibility, not pixel/source identity. Released sizes/preprocessing and light variants may differ from historical inputs. No author paper-era hash/split manifest was supplied.

**Paper-reported protocol:** sections 2.1–2.4 describe Turkey farm collection over 12 months, custom controlled portable imaging box, smartphone, matte black background, multiple angles and disease stages. Expert mycologists/manual annotation and specialist-panel cross-check are reported (lines 51, 56). This supports expert-guided visual diagnosis provenance only; laboratory culture/PCR/pathogen confirmation is **UNVERIFIED**, not established by the reviewed Methods. Multiple views/stages do not establish how many repeated physical specimens exist or which images share them.

**Preprocessing (section 2.5, line 58):** architecture-dependent resizing (typically 224×224), preserving aspect ratio, intensity normalization [0,1], background cleaning, no synthetic augmentation. Exact resize/pad/crop policy and background-cleaning implementation are not specified enough for exact recreation. Released JPEG dimensions are measured above, not assumed raw camera originals.

**Training configuration (section 2.6):** batch 11, SGD momentum 0.9, learning rate 0.001, 8 epochs, no early stopping; MATLAB R2023b plus Python 3.9 workflow. Section 2.7 explicitly uses 80% train / 20% validation, validation for tuning and reporting, **no separate test**. No released split membership/seed/specimen grouping or historical preprocessing/checkpoint bytes are present in this all-JPEG archive. No training code or checkpoints were acquired or executed.

**Reported baselines:** 20 pretrained CNN architectures. Table 2: ResNet-50 accuracy 99.66%, precision 99.67%, recall 99.64%, F1 99.65%, AUC 99.99%, AP 99.79%, weighted overall score 99.70%; DarkNet-53 overall 99.51%; DenseNet-201 overall 99.50%; MobileNet-v2 overall 98.47%; EfficientNet-b0 overall 95.20% and accuracy 94.52%. These are author-reported validation results, **not held-out test evidence**, and none were rerun here. Overall score is weighted precision .2 + recall .3 + F1 .3 + AUC .1 + AP .1 (section 2.8), not accuracy. Preserve internal inconsistencies: section 3 says VGG-16 was excluded for overfitting, then says it did not overfit and Table 2 reports it; abstract/intro sometimes conflate overall score with accuracy, and related-work prose claims DenseNet-201 99.98% versus Table 2 99.44%. Do not choose a convenient conflicting number as a target.

## 4. Grouping, leakage and readiness

Observed grouping clues: illumination directory (`white`, `uv`, `mix`), class directory and ordinal filenames (examples in `grouping_clues.json`). Archive contains only JPEGs: **no specimen/bag/batch/farm/session identifier manifest, label adjudication record, README, split manifest, code or checkpoint file**. File timestamps/ordinal similarity are not validated specimen identities. Cross-light pairings and repeated-specimen counts remain **UNVERIFIED**. dHash/byte matches, if any, establish image relationships only, not biological independence.

No train/validation/test split was created. Before scientific use: obtain authoritative specimen/farm/session IDs and cross-light pairing, establish grouping across views/stages, review exact/perceptual candidates without treating them as disease truth, confirm `kw` semantics and diagnosis validation, clarify historical preprocessing and split membership, and approve an independent-group protocol with a genuinely separate held-out evaluation cohort. Any new split/preprocessing makes a **new protocol**, not exact reproduction of the paper's 80/20 validation reuse.

Decision alternatives considered: EXACT_REPRODUCTION_FEASIBLE rejected (missing historical image hashes, preprocessing implementation and splits/seeds); PARTIAL_REPRODUCTION_FEASIBLE could describe a later authorized method-level approximation on the count-compatible white subset, but does not close independent-unit/label gates. INSUFFICIENT_EVIDENCE is too broad for metadata, access and image integrity, which were measured. Overall decision **NEW_PROTOCOL_REQUIRED**, with G1 blocked until unresolved scientific issues are addressed. No final candidate selection follows from acquisition success.

Farm white/grey oyster versus Agaricus cross-species transfer: **UNVERIFIED**. Controlled Turkey Agaricus photographs are not evidence of performance on Vietnamese oyster farms, uncontrolled light, new devices or new sites. No cross-species/domain generalization claim is authorized.

## 5. Evidence, reproducibility and limitations

All supporting C03 outputs are under `04_dataset_candidates/C03_agaricus_disease/`: `acquisition_manifest.csv`; unchanged ignored RAR and `source/extracted/`; `qc/archive_members.json`, `inventory.json`, `inventory.jsonl`, `summary.json`, `duplicates.json`; scripts/logs/metadata/source review/grouping/verification under `qc/wp04_evidence/`. Acquisition and resume scripts use Python standard library. QC environment in scratch: Python 3.12.13 with pillow 13.0.0, rarfile 4.5, ImageHash 4.3.2, numpy 2.5.4, scipy 1.18.1, pywavelets 1.10.0. libarchive-c 5.3 installed but not used: DLL unavailable; Windows bsdtar used instead. Initial dependency DNS failure recovered on retry. First monolithic QC exceeded tool timeout after safe extraction, before a persistent inventory; `qc_existing.py` restarted QC on the untouched extracted tree with incremental JSONL checkpoints. No source overwrite or repair occurred.

Verification script: `qc/wp04_evidence/verify.py`, readback result `verification.json`. Scope is exact file/hash/mtime/count reconciliation, duplicate-edge-distance checks and payload ignore coverage, **not biological or diagnostic scientific verification**. This report is the only authored shared discovery report; no shared state/registry/ignore changes. Remaining blockers are diagnosis laboratory provenance, repeated specimen/farm linkage, historical data/split/preprocessing identity, human perceptual/label review, privacy/redistribution clarification and transfer validity. Training remains unauthorized.
'''
(R/'03_dataset_discovery/source_verification/C03_DEEP_SOURCE_VERIFICATION.md').write_text(text,encoding='utf-8')
print('report written',len(text))
