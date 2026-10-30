"""Write blocked C01 evidence outputs, exclusively creating new files."""
from pathlib import Path
import csv,json,datetime,hashlib,subprocess
E=Path(__file__).resolve().parent; C=E.parent.parent; R=C.parent.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert commit=='f50f946b1d5f1bd11407c09b3b210ae0370fbde2'
assert subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()=='research/wp-02-feasibility-audit'
log={'preflight_root':str(R),'branch':'research/wp-02-feasibility-audit','head':commit,'initial_status':'clean (terminal preflight)','wp01_object':'da1688a commit object verified','browser':'Failed before navigation: Chrome real-profile locked; no browser closed or configuration changed','client_bundle':'HTTP 403; no bundle saved','acquisition':'Stopped: exact-v2 file/archive name, size and content type unresolved','download_payload_bytes':0,'timestamp':now}
(E/'execution_summary.json').open('x',encoding='utf8').write(json.dumps(log,indent=2))
checks=[]
for rel in ['source/C01_v2_original.zip','source/C01_v2_metadata.json','raw/example.jpg']:
 p=C/rel
 r=subprocess.run(['git','check-ignore','-v',str(p)],cwd=R,capture_output=True,text=True)
 checks.append({'path':rel,'returncode':r.returncode,'stdout':r.stdout.strip()})
assert checks[0]['returncode']==0 and checks[1]['returncode']==1 and checks[2]['returncode']==0
(E/'ignore_checks.json').open('x').write(json.dumps(checks,indent=2))
fields=['candidate_id','source_url','repository_commit','dataset_version','local_path','bytes','sha256','download_timestamp','content_type','parse_status','status','notes']
with (C/'qc/wp02_c01_download_manifest.csv').open('x',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerow(dict(candidate_id='C01',source_url='https://data.mendeley.com/datasets/jrbx34k77g/2',repository_commit=commit,dataset_version='2',local_path='',bytes='',sha256='',download_timestamp='',content_type='',parse_status='EXACT_V2_ARCHIVE_METADATA_UNRESOLVED',status='NOT_DOWNLOADED',notes='Status row, not an acquired archive; payload bytes transferred=0. Name/size/type unknown. Public file routes blocked or empty.'))
with (C/'qc/image_inventory.csv').open('x',newline='',encoding='utf8') as f:
 csv.writer(f).writerow(['candidate_id','relative_path','class_folder','extension','bytes','mtime_ns','sha256','decode_status','width','height','mode','orientation','exif_datetime','bag_id','session_id','notes'])
stats={'candidate_id':'C01','dataset_doi':'10.17632/jrbx34k77g.2','dataset_version':'2','repository_commit':commit,'audit_timestamp':now,'status':'ACQUISITION_BLOCKED_METADATA_UNCLEAR','selection_status':'PENDING','training_executed':False,'payload_downloaded_bytes':0,'authorization_max_payload_bytes':1610612736,'archive_name':None,'archive_bytes':None,'archive_content_type':None,'archive_sha256':None,'extraction_executed':False,'image_inventory_rows':0,'audited_image_count':None,'class_counts_measured':None,'source_reported_counts':{'total':761,'healthy':299,'single_infected':147,'mixed_infected':315},'source_reported_counts_audited':False,'dimensions':None,'decode_corrupt_count':None,'exact_duplicate_groups':None,'filename_patterns':None,'exif_grouping_clues':None,'perceptual_review':'NOT_PERFORMED','independence':'UNVERIFIED','biological_confirmation':'UNVERIFIED','paper_relationship':'NO_EXACT_DATASET_PAPER_CONFIRMED','gate_recommendation':'NEEDS_MORE_EVIDENCE','blockers':['Exact-v2 archive inventory, size, type and download URL not established','Live public routes returned 404/403 or empty arrays; browser unavailable due profile lock','Independent-unit grouping and biological labels not assessed'],'verification_status':'PENDING_INDEPENDENT_READBACK'}
(C/'qc/wp02_c01_statistics.json').open('x').write(json.dumps(stats,indent=2))
report='''# WP-02 C01 acquisition / QC feasibility audit

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
'''
(C/'reports/WP-02_C01_DATA_FEASIBILITY.md').open('x',encoding='utf8').write(report)
print(json.dumps(stats,indent=2))
