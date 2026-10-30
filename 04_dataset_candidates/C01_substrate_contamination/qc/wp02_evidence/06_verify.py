"""Independent readback verifier of blocked scope; no raw/source mutations."""
import pathlib,json,csv,hashlib,subprocess,datetime
E=pathlib.Path(__file__).resolve().parent; C=E.parent.parent; R=C.parent.parent
s=json.loads((C/'qc/wp02_c01_statistics.json').read_text())
assert s['payload_downloaded_bytes']==0 and s['audited_image_count'] is None and not s['training_executed']
assert s['archive_sha256'] is None and not s['extraction_executed']
rows=list(csv.DictReader((C/'qc/image_inventory.csv').open(newline='')));assert rows==[]
with (C/'qc/wp02_c01_download_manifest.csv').open(newline='') as f:
 reader=csv.DictReader(f);names=reader.fieldnames;manifest=list(reader)
assert names==['candidate_id','source_url','repository_commit','dataset_version','local_path','bytes','sha256','download_timestamp','content_type','parse_status','status','notes']
assert len(manifest)==1 and manifest[0]['status']=='NOT_DOWNLOADED'
for key in ['local_path','bytes','sha256','download_timestamp','content_type']:assert manifest[0][key]==''
assert manifest[0]['repository_commit']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
for folder in ['source','raw']:
 files=[p.relative_to(C).as_posix() for p in (C/folder).rglob('*') if p.is_file()];assert files==[folder+'/.gitkeep'],files
meta=json.loads((E/'datacite_v2.txt').read_text())['data']['attributes'];assert meta['doi']=='10.17632/jrbx34k77g.2'
assert json.loads((E/'files_root.txt').read_text())==[] and json.loads((E/'files_version_first.txt').read_text())==[]
assert 'NO_EXACT_DATASET_PAPER_CONFIRMED' in (C/'reports/WP-02_C01_DATA_FEASIBILITY.md').read_text(encoding='utf8')
tracked_changes=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines()
assert not any(x.startswith('04_dataset_candidates/C01_substrate_contamination/') for x in tracked_changes)
# Other delegated workers may change shared/other-candidate files concurrently.
assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R,text=True).strip()==''
files=[]
for p in sorted(C.rglob('*')):
 if p.is_file() and (p.parent==E or p.name in ['WP-02_C01_DATA_FEASIBILITY.md','image_inventory.csv','wp02_c01_statistics.json','wp02_c01_download_manifest.csv']):
  files.append({'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()})
v={'status':'PASS_BLOCKED_SCOPE_ONLY','verifier':'06_verify.py independent reparse and filesystem rescan','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inventory_data_rows':len(rows),'download_manifest_status_rows':len(manifest),'source_payload_files':0,'raw_payload_files':0,'c01_tracked_diff_empty':True,'other_worker_tracked_changes':tracked_changes,'staged_diff_empty':True,'files':files}
(E/'verification.json').open('x').write(json.dumps(v,indent=2));print(json.dumps(v,indent=2))
