"""Fetch C01 exact-v2 public metadata only; refuse overwrites."""
import urllib.request, json, datetime, pathlib
BASE=pathlib.Path(__file__).resolve().parent
urls={"mendeley_v2":"https://data.mendeley.com/public-api/datasets/jrbx34k77g/versions/2", "mendeley_files":"https://data.mendeley.com/public-api/datasets/jrbx34k77g/versions/2/files", "datacite_v2":"https://api.datacite.org/dois/10.17632/jrbx34k77g.2", "landing_v2":"https://data.mendeley.com/datasets/jrbx34k77g/2"}
results=[]
for name,url in urls.items():
    row={"url":url,"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"C01-research-metadata-audit/1.0"}),timeout=60) as r:
            data=r.read(8*1024*1024+1)
            if len(data)>8*1024*1024: raise ValueError('metadata limit exceeded')
            row.update(status=r.status,content_type=r.headers.get('Content-Type'),bytes=len(data),resolved_url=r.url)
            p=BASE/(name+'.txt'); p.open('xb').write(data)
            print(name, data[:18000].decode('utf8',errors='replace'))
    except Exception as e: row['error']=str(e);print(name,str(e))
    results.append(row)
(BASE/'metadata_requests.json').open('x',encoding='utf8').write(json.dumps(results,indent=2))
