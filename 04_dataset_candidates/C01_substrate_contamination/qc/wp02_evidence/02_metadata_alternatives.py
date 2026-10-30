import urllib.request,json,pathlib,datetime
B=pathlib.Path(__file__).resolve().parent
urls={'files_query':'https://data.mendeley.com/public-api/datasets/jrbx34k77g/files?version=2','folders_query':'https://data.mendeley.com/public-api/datasets/jrbx34k77g/folders?version=2','files_api_alt':'https://data.mendeley.com/api/datasets-v2/datasets/jrbx34k77g/versions/2/files','snapshot_query':'https://data.mendeley.com/public-api/datasets/jrbx34k77g?version=2'}
rows=[]
for name,url in urls.items():
 r={'url':url,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=60) as h:
   data=h.read(8*1024*1024+1)
   assert len(data)<=8*1024*1024
   r.update(status=h.status,content_type=h.headers.get('Content-Type'),bytes=len(data)); (B/(name+'.txt')).open('xb').write(data);print(name,data.decode('utf8')[:20000])
 except Exception as e:r['error']=str(e);print(name,str(e))
 rows.append(r)
(B/'alternative_requests.json').open('x').write(json.dumps(rows,indent=2))
