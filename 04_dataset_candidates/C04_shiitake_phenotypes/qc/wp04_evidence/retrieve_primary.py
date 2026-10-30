"""WP04 C04 bounded primary retrieval. Never fetch dataset/image assets."""
import urllib.request, json, hashlib, datetime, concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCES={
'zenodo_record.json':'https://zenodo.org/api/records/20373531',
'zenodo_versions.json':'https://zenodo.org/api/records/20373531/versions',
'zenodo_latest.json':'https://zenodo.org/api/records/20373531/versions/latest',
'publisher.html':'https://www.nature.com/articles/s41597-026-07754-7',
'datacite.json':'https://api.datacite.org/dois/10.5281/zenodo.20373531'}
def fetch(item):
 name,url=item; row={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research source verification)'})
  with urllib.request.urlopen(req,timeout=65) as r:
   b=r.read(12_000_001); assert len(b)<=12_000_000,'metadata size guard'; row.update(status=r.status,final_url=r.url,headers=dict(r.headers),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()); (ROOT/name).write_bytes(b)
 except Exception as e: row['error']=str(e)
 return row
if __name__=='__main__':
 rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(fetch,SOURCES.items()))
 (ROOT/'primary_access_log.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 print(json.dumps([{k:v for k,v in x.items() if k!='headers'} for x in rows],indent=2))
