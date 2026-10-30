"""Independent filesystem/hash/count reconciliation, not scientific adjudication."""
from pathlib import Path
import json,hashlib,csv,collections,subprocess,datetime
R=Path('D:/Capstone/mushroom-research-2026'); C=R/'04_dataset_candidates/C03_agaricus_disease'; Q=C/'qc'; E=Q/'wp04_evidence'; out=C/'source/extracted'
rows=json.loads((Q/'inventory.json').read_text()); summary=json.loads((Q/'summary.json').read_text()); dup=json.loads((Q/'duplicates.json').read_text()); members=json.loads((Q/'archive_members.json').read_text())
files={p.relative_to(out).as_posix():p for p in out.rglob('*') if p.is_file()}; manifest={r['path']:r for r in rows}; assert len(manifest)==len(rows) and set(files)==set(manifest)
for n,p in files.items():
 r=manifest[n]; s=p.stat(); assert s.st_size==r['bytes'] and s.st_mtime_ns==r['mtime_ns'] and p.suffix.lower()==r['extension']; assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
assert sum(x['bytes'] for x in rows)==summary['expanded_bytes']==members['declared_expanded_bytes']
assert sum(summary['by_light'].values())==summary['image_decode_ok']
exact=collections.defaultdict(list)
for r in rows: exact[r['sha256']].append(r['path'])
assert {k:sorted(v) for k,v in exact.items() if len(v)>1}=={x['sha256']:sorted(x['paths']) for x in dup['sha256_duplicate_groups']}
assert dup['perceptual_candidate_pair_count']==summary['perceptual_candidates']
assert sum(edge[3] for edge in dup['perceptual_bucket_edges'])==summary['perceptual_candidates']
for a,b,d,n in dup['perceptual_bucket_edges']:
 assert (int(a,16)^int(b,16)).bit_count()==d<=4
 na=len(dup['dhash_buckets'][a]); nb=len(dup['dhash_buckets'][b]); assert n==(na*(na-1)//2 if a==b else na*nb)
for h,paths in dup['dhash_buckets'].items():
 assert all(manifest[p]['dhash64']==h for p in paths)
payload=[p for p in C.joinpath('source').rglob('*') if p.is_file()]
ignored_count=0
for start in range(0,len(payload),100):
 batch=payload[start:start+100]
 ignore=subprocess.run(['git','check-ignore',*[p.relative_to(R).as_posix() for p in batch]],text=True,capture_output=True,cwd=R)
 assert ignore.returncode==0 and len(ignore.stdout.splitlines())==len(batch), ignore.stderr
 ignored_count+=len(ignore.stdout.splitlines())
assert ignored_count==len(payload)
report=R/'03_dataset_discovery/source_verification/C03_DEEP_SOURCE_VERIFICATION.md'; assert report.stat().st_size>3000
assert 'NEW_PROTOCOL_REQUIRED' in report.read_text(encoding='utf-8')
result={'status':'PASS','scope':'Independent filesystem/hash/mtime/count/duplicate-edge-distance and ignore reconciliation; not biological identity or scientific peer review','verified_files':len(rows),'payload_files_ignored':len(payload),'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'summary_sha256':hashlib.sha256((Q/'summary.json').read_bytes()).hexdigest(),'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest()}
(E/'verification.json').write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2))
