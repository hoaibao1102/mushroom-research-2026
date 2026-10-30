from pathlib import Path
import subprocess,concurrent.futures,json,datetime,hashlib
R=Path(__file__).resolve().parent;N=5724836;U='https://zenodo.org/records/20373531/files/shiitake_mushroom_code.zip'
def get(i):
 a=i*524288;b=min(N,a+524288)-1;p=R/f'code_part_{i:02}.bin'
 r=subprocess.run(['curl','-sS','-L','--fail','--max-time','60','-H',f'Range: bytes={a}-{b}',U,'-o',str(p),'-w','%{http_code}'],capture_output=True,text=True)
 return {'i':i,'a':a,'b':b,'status':r.stdout,'exit':r.returncode,'error':r.stderr,'bytes':p.stat().st_size if p.exists() else 0}
t=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(get,range((N+524287)//524288))); log={'url':U,'started_utc':t,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parts':rows,'success':False}
if all(x['exit']==0 and x['status']=='206' and x['bytes']==x['b']-x['a']+1 for x in rows):
 b=b''.join((R/f"code_part_{x['i']:02}.bin").read_bytes() for x in rows);log['md5']=hashlib.md5(b).hexdigest()
 if len(b)==N and log['md5']=='42aa41b73d6410e76e5c27438a9a2b15':
  (R/'shiitake_mushroom_code.zip').write_bytes(b);log.update(success=True,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
(R/'curl_recovery_log.json').write_text(json.dumps(log,indent=2));print(json.dumps(log,indent=2))
