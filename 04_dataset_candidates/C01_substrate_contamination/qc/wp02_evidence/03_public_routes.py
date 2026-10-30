import urllib.request,json,pathlib,datetime,re
B=pathlib.Path(__file__).resolve().parent
urls={'files_root':'https://data.mendeley.com/public-api/datasets/jrbx34k77g/files?folder_id=root&version=2','files_version_first':'https://data.mendeley.com/public-api/datasets/jrbx34k77g/files?version=2&folder_id=root','api_files_query':'https://data.mendeley.com/api/datasets-v2/datasets/jrbx34k77g/files?version=2','wayback':'https://archive.org/wayback/available?url=https%3A%2F%2Fdata.mendeley.com%2Fdatasets%2Fjrbx34k77g%2F2'}
rows=[]
for n,u in urls.items():
 r={'url':u,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Accept':'application/json','Referer':'https://data.mendeley.com/datasets/jrbx34k77g/2'}),timeout=45) as h:
   d=h.read(8*1024*1024+1);assert len(d)<=8*1024*1024
   r.update(status=h.status,content_type=h.headers.get('Content-Type'),bytes=len(d));(B/(n+'.txt')).open('xb').write(d);print(n,d.decode('utf8')[:20000])
 except Exception as e:r['error']=str(e);print(n,str(e))
 rows.append(r)
(B/'public_route_requests.json').open('x').write(json.dumps(rows,indent=2))
