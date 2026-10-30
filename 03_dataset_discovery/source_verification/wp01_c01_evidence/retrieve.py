import urllib.request, urllib.error, json, pathlib, datetime, concurrent.futures, re, subprocess
ROOT=pathlib.Path(__file__).parent
(ROOT/'sources').mkdir(exist_ok=True)
LOG=ROOT/'access_search_log.jsonl'
LEDGER=ROOT/'citation_ledger.json'
CITE='C:/Users/MSI PC/AppData/Local/hermes/skills/research/grounded-citations/scripts/sources.py'
def fetch(item):
 name,url=item
 rec={'access_timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'name':name,'url':url,'scope':'public metadata/text only; no dataset payload'}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research metadata verification)','Accept':'application/json,text/html,application/xml;q=0.9,*/*;q=0.5'})
  with urllib.request.urlopen(req,timeout=45) as r:
   data=r.read(5000000);rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(data))
  ext='.json' if 'json' in rec['content_type'] else '.html'
  path=ROOT/'sources'/(name+ext);path.write_bytes(data);rec['saved_path']=str(path)
 except Exception as e:rec.update(status='FAILED',error=str(e))
 return rec
if __name__=='__main__':
 items=[('c01_v2','https://data.mendeley.com/datasets/jrbx34k77g/2'),('c01_v1','https://data.mendeley.com/datasets/jrbx34k77g/1'),('excluded_ds02_v1','https://data.mendeley.com/datasets/hf55tkx489/1'),('c01_datacite_v2','https://api.datacite.org/dois/10.17632/jrbx34k77g.2'),('c01_datacite_v1','https://api.datacite.org/dois/10.17632/jrbx34k77g.1'),('c01_versions_api','https://data.mendeley.com/public-api/datasets/jrbx34k77g/versions'),('c01_api_v2','https://data.mendeley.com/public-api/datasets/jrbx34k77g/versions/2'),('ds02_datacite','https://api.datacite.org/dois/10.17632/hf55tkx489.1')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: results=list(ex.map(fetch,items))
 with LOG.open('a',encoding='utf-8') as f:
  for rec in results:f.write(json.dumps(rec)+'\n')
 for rec in results:
  subprocess.run(['python',CITE,'--ledger',str(LEDGER),'add',rec['url'],'--title',rec['name']],capture_output=True)
  print(json.dumps(rec))
