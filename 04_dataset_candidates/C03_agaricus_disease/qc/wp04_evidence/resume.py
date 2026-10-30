"""Resume exact archive with checked ranges, never substitute content."""
from pathlib import Path
import urllib.request,json,hashlib,csv,time,datetime
C=Path('D:/Capstone/mushroom-research-2026/04_dataset_candidates/C03_agaricus_disease'); E=C/'qc/wp04_evidence'; d=json.loads((E/'live_record.json').read_bytes()); f=d['files'][0]; p=C/'source'/f['key']; size=f['size']; log=[]
assert size<=500000000
for attempt in range(150):
    start=p.stat().st_size
    if start==size: break
    end=min(start+4*1024*1024-1,size-1)
    try:
        req=urllib.request.Request(f['links']['self'],headers={'Range':f'bytes={start}-{end}','User-Agent':'Research-QC/1.0'})
        with urllib.request.urlopen(req,timeout=90) as r:
            assert r.status==206 and r.headers.get('Content-Range')==f'bytes {start}-{end}/{size}', (r.status,dict(r.headers))
            b=r.read(end-start+2); assert len(b)==end-start+1
        with p.open('ab') as out: out.write(b)
        log.append({'start':start,'end':end,'status':'APPENDED_VALIDATED_RANGE'}); print(p.stat().st_size,flush=True)
    except Exception as ex:
        log.append({'start':start,'end':end,'error':repr(ex)}); time.sleep(1)
    (E/'resume_log.json').write_text(json.dumps(log,indent=2))
b=p.read_bytes(); md5=hashlib.md5(b).hexdigest(); sha=hashlib.sha256(b).hexdigest(); ok=len(b)==size and 'md5:'+md5==f['checksum']
with (C/'acquisition_manifest.csv').open(newline='',encoding='utf-8') as inp: rows=list(csv.DictReader(inp))
rows[0].update(status='ACQUIRED_CHECKSUM_VERIFIED' if ok else 'BLOCKED_INCOMPLETE',actual_size_bytes=len(b),sha256=sha,md5=md5,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
with (C/'acquisition_manifest.csv').open('w',newline='',encoding='utf-8') as out:
    w=csv.DictWriter(out,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
print(json.dumps(rows[0],indent=2)); assert ok
