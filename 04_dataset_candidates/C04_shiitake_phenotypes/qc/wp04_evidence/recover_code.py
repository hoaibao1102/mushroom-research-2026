"""Bounded range recovery of verified code-only asset; no dataset URL."""
from pathlib import Path
import urllib.request, concurrent.futures, hashlib, json, datetime
R=Path(__file__).resolve().parent
U='https://zenodo.org/records/20373531/files/shiitake_mushroom_code.zip'
N=5724836
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
def part(i):
 a=i*262144;b=min(N,a+262144)-1
 for attempt in range(3):
  try:
   req=urllib.request.Request(U+f'?part={i}',headers={'Range':f'bytes={a}-{b}','User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=35) as r:
    data=r.read(N+1)
    if r.status==200 and len(data)==N:return i,data,True
    assert r.status==206 and len(data)==b-a+1,(r.status,len(data))
    return i,data,False
  except Exception as e:
   if attempt==2:return i,str(e),None
rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=8).map(part,range((N+262143)//262144)))
log={'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':U,'attempt':'parallel bounded ranges after urllib timeout and curl reset','parts':[{'i':i,'bytes':len(b) if isinstance(b,bytes) else 0,'full':full,'error':b if isinstance(b,str) else None} for i,b,full in rows]}
full=next((b for i,b,f in rows if f is True),None)
if full is None and all(f is False for i,b,f in rows):full=b''.join(b for i,b,f in sorted(rows))
if full:
 assert len(full)==N and hashlib.md5(full).hexdigest()=='42aa41b73d6410e76e5c27438a9a2b15'
 (R/'shiitake_mushroom_code.zip').write_bytes(full);log.update(success=True,sha256=hashlib.sha256(full).hexdigest(),bytes=len(full))
else:log['success']=False
(R/'code_recovery_log.json').write_text(json.dumps(log,indent=2));print(json.dumps(log,indent=2))
