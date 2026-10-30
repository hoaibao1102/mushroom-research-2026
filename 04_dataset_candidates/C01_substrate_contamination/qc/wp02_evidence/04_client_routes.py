import urllib.request,pathlib,re,json,datetime
B=pathlib.Path(__file__).resolve().parent
u='https://data.mendeley.com/datasets/bundle.js?8814bfd8bfcb6231e2b5'
try:
 with urllib.request.urlopen(u,timeout=60) as h:d=h.read(12*1024*1024+1);assert len(d)<=12*1024*1024
 (B/'public_client_bundle.txt').open('xb').write(d)
 s=d.decode('utf8');hits=[]
 for term in ['/files','/folders','/archive']:
  for m in list(re.finditer(re.escape(term),s))[:30]:hits.append(s[max(0,m.start()-350):m.end()+350])
 (B/'client_route_excerpts.json').open('x').write(json.dumps(hits,indent=2)); print('\n'.join(hits))
except Exception as e:print(type(e).__name__,str(e))
