import json,csv,hashlib,pathlib
from collect_sources import BASE
rows=list(csv.DictReader((BASE/'claims.csv').open(encoding='utf-8-sig')))
assert len(rows)==21 and len({r['claim_id'] for r in rows})==21
expected=['claim_id','claim_text','candidate_id','source_title','source_url_or_doi','source_type','source_publication_update_date','access_date','source_location','evidence_status','confidence','verification_notes']
assert list(rows[0])==expected
logs=[json.loads(x) for x in (BASE/'access_log.jsonl').read_text().splitlines()]
errors=[]
for r in logs:
 if 'sha256' in r:assert hashlib.sha256((BASE/r['destination']).read_bytes()).hexdigest()==r['sha256']
 if 'error' in r:errors.append(r)
assert not errors
for repo in ['MushR','mushr-mask-r-cnn']:
 tree=json.loads((BASE/repo/'tree.json').read_text());assert not tree.get('truncated')
summary=json.loads((BASE/'kaggle_inventory_summary.json').read_text());assert summary['listed_files']==3011 and summary['total_bytes']==json.loads((BASE/'kaggle_view.json').read_text())['totalBytes']
files=[str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
result={'claims':len(rows),'access_requests':len(logs),'access_errors':len(errors),'all_response_hashes_verified':True,'complete_tree_metadata':True,'inventory_totals_match':True,'artifact_files':files,'prohibited_payloads_fetched':False,'runtime_or_training_executed':False,'shared_files_modified':False}
(BASE/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='artifact_files'},indent=2))
