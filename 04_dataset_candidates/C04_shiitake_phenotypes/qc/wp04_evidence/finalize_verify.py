from pathlib import Path
import json,csv,hashlib,datetime,subprocess,zipfile
R=Path(__file__).resolve().parent;repo=R.parents[3]; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rows=[]
for x in json.loads((R/'primary_access_log.json').read_text()):
 p=R/x['name'];rows.append({'artifact':p.name,'kind':'ARTICLE' if p.suffix=='.html' else 'METADATA','url':x['url'],'retrieved_utc':x['retrieved_utc'],'status':str(x.get('status','ERROR')),'bytes':p.stat().st_size if p.exists() else 0,'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else '', 'upstream_md5':'','access_scope':'FULL_TEXT' if p.suffix=='.html' else 'METADATA_ONLY'})
j=json.loads((R/'zenodo_record.json').read_text()); rec=json.loads((R/'curl_recovery_log.json').read_text());code=R/'shiitake_mushroom_code.zip'
rows.append({'artifact':code.name,'kind':'CODE_ARCHIVE','url':rec['url'],'retrieved_utc':rec['finished_utc'],'status':'206_RANGE_RECOVERY_VERIFIED','bytes':code.stat().st_size,'sha256':hashlib.sha256(code.read_bytes()).hexdigest(),'upstream_md5':'42aa41b73d6410e76e5c27438a9a2b15','access_scope':'STATIC_TEXT_ONLY_NO_EXECUTION'})
f=next(x for x in j['files'] if x['key']=='shiitake_mushroom_dataset.zip')
rows.append({'artifact':f['key'],'kind':'UPSTREAM_DATASET_LISTING_NOT_ACQUIRED','url':f['links']['self'],'retrieved_utc':rows[0]['retrieved_utc'],'status':'NOT_DOWNLOADED','bytes':0,'sha256':'','upstream_md5':f['checksum'],'access_scope':'METADATA_ONLY_LISTED_BYTES_4110366941'})
# Remove only redundant code-only transfer fragments after full checksum verification.
assert hashlib.md5(code.read_bytes()).hexdigest()=='42aa41b73d6410e76e5c27438a9a2b15'
removed=[]
for p in list(R.glob('code_part_*.bin'))+[R/'code_tail.probe',R/'shiitake_mushroom_code.zip.partial']:
 if p.exists():removed.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});p.unlink()
(R/'transfer_fragments_cleanup.json').write_text(json.dumps({'utc':now,'removed_redundant_code_only_fragments':removed},indent=2))
with (R/'acquisition_manifest.csv').open('w',newline='',encoding='utf-8') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report=repo/'03_dataset_discovery/source_verification/C04_DEEP_SOURCE_VERIFICATION.md';text=report.read_text(encoding='utf-8');idx=json.loads((R/'text_index.json').read_text());summary=json.loads((R/'static_audit_summary.json').read_text())
checks={
'exact_record':j['id']==20373531 and j['doi']=='10.5281/zenodo.20373531',
'live_dataset_license':j['metadata']['license']['id']=='cc-by-4.0',
'article_separate_license':'Attribution-NonCommercial-NoDerivatives 4.0' in (R/'publisher_text.txt').read_text(encoding='utf-8'),
'code_bytes_and_md5':len(code.read_bytes())==5724836 and hashlib.md5(code.read_bytes()).hexdigest()=='42aa41b73d6410e76e5c27438a9a2b15',
'archive_crc_integrity':zipfile.ZipFile(code).testzip() is None,
'archive_inventory_count':len(json.loads((R/'archive_inventory.json').read_text()))==summary['archive_members']==1068,
'all_text_extracts_exist':all((R/x['local_text']).is_file() for x in idx),
'no_training_authorization':summary['training_authorized']=='NO' and 'Training authorization: NO' in text,
'count_conflict_preserved':all(x in text for x in ['1,782','6,500','43,752','5,375','unresolved']),
'no_dataset_acquired':not summary['dataset_acquired'] and not any(p.name==f['key'] for p in R.rglob('*')),
'no_author_code_execution':not summary['author_code_executed'] and not summary['installed_dependencies'],
'pending_human_gates':'G0' in text and 'G1' in text and 'PENDING_HUMAN' in text,
'farm_fit_caveat':'white/grey oyster' in text and 'no direct-transfer' in text,
'report_substantive':len(text)>12000,
}
tracked=subprocess.run(['git','diff','--name-only'],cwd=repo,capture_output=True,text=True).stdout.splitlines()
checks['no_existing_tracked_files_modified']=not tracked
result={'timestamp_utc':now,'scope':'STRUCTURAL_PROVENANCE_STATIC_CONSISTENCY_NOT_SCIENTIFIC_REPRODUCTION','checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL','training_authorized':'NO','dataset_selected':'NONE','human_approval':'PENDING','protocol_classification':'PARTIALLY_SPECIFIED_WITH_MATERIAL_CONFLICTS','report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'acquisition_manifest_sha256':hashlib.sha256((R/'acquisition_manifest.csv').read_bytes()).hexdigest()}
(R/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert all(checks.values())
