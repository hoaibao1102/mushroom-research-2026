"""WP04 exact-record acquisition only; no alternative versions or training."""
from pathlib import Path
import urllib.request,json,hashlib,csv,datetime,subprocess
ROOT=Path('D:/Capstone/mushroom-research-2026'); C=ROOT/'04_dataset_candidates/C03_agaricus_disease'; E=C/'qc/wp04_evidence'
E.mkdir(parents=True,exist_ok=True)
def get(url):
    with urllib.request.urlopen(url,timeout=90) as r: return r.read(),dict(r.headers)
b,h=get('https://zenodo.org/api/records/20260929'); d=json.loads(b)
(E/'live_record.json').write_bytes(b)
(E/'live_record_headers.json').write_text(json.dumps({'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'headers':h},indent=2))
assert d['id']==20260929 and d['doi']=='10.5281/zenodo.20260929'
assert d['metadata']['license']['id']=='cc-by-4.0' and d['metadata']['access_right']=='open'
assert any(x['identifier']=='10.3390/agronomy15010226' for x in d['metadata']['related_identifiers'])
assert len(d['files'])==1
f=d['files'][0]; assert f['size']<=500000000 and f['key'].endswith('.rar') and '/' not in f['key'] and '\\' not in f['key']
p=C/'source'/f['key']; ignored=subprocess.run(['git','check-ignore','-v',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
assert ignored.returncode==0
(E/'ignore_check.txt').write_text(ignored.stdout)
row={'record':str(d['id']),'doi':d['doi'],'license':'CC-BY-4.0','filename':f['key'],'url':f['links']['self'],'publisher_size_bytes':f['size'],'publisher_checksum':f['checksum'],'status':'PENDING','actual_size_bytes':'','sha256':'','md5':'','retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
def manifest():
    with (C/'acquisition_manifest.csv').open('w',newline='',encoding='utf-8') as out:
        w=csv.DictWriter(out,fieldnames=list(row)); w.writeheader(); w.writerow(row)
manifest()
try:
    p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists()
    req=urllib.request.Request(f['links']['self'],headers={'User-Agent':'Research-QC/1.0'})
    with urllib.request.urlopen(req,timeout=120) as r, p.open('xb') as out:
        length=r.headers.get('Content-Length'); assert length is None or int(length)==f['size']
        total=0; sha=hashlib.sha256(); md5=hashlib.md5()
        while True:
            block=r.read(min(1048576,f['size']-total+1))
            if not block: break
            total+=len(block); assert total<=f['size'] and total<=500000000
            out.write(block); sha.update(block); md5.update(block)
    row.update(actual_size_bytes=total,sha256=sha.hexdigest(),md5=md5.hexdigest())
    assert total==f['size'] and 'md5:'+md5.hexdigest()==f['checksum']
    row['status']='ACQUIRED_CHECKSUM_VERIFIED'
except Exception as ex:
    row['status']='BLOCKED: '+repr(ex); raise
finally: manifest()
print(json.dumps(row,indent=2))
