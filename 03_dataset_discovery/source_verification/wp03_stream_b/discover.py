import urllib.request, urllib.parse, json, pathlib, datetime, concurrent.futures
ROOT=pathlib.Path(__file__).parent
(ROOT/'sources').mkdir(exist_ok=True)
def fetch(url,name):
    t=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'WP03 academic metadata verification/1.0'})
        with urllib.request.urlopen(req,timeout=60) as r:
            b=r.read(); status=r.status; final=r.url
        (ROOT/'sources'/name).write_bytes(b)
        rec={'url':url,'retrieved_utc':t,'status':status,'final_url':final,'file':'sources/'+name,'bytes':len(b)}
    except Exception as e: rec={'url':url,'retrieved_utc':t,'error':str(e)}
    with (ROOT/'access_log.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(rec)+'\n')
    return rec
if __name__=='__main__':
    qs=['mushroom dataset quality detection','mushroom harvest maturity image dataset','mushroom dataset Scientific Data','mushroom defect classification dataset']
    def run(p):
        i,q=p; u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query':q,'filter':'from-pub-date:2024-01-01,until-pub-date:2026-12-31','rows':25})
        rec=fetch(u,f'search_{i}.json')
        if 'file' in rec:
            d=json.loads((ROOT/rec['file']).read_text(encoding='utf8'))
            return [(x.get('title'),x.get('DOI')) for x in d['message']['items']]
        return rec
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for q,rows in zip(qs,ex.map(run,enumerate(qs))): print(q,json.dumps(rows,ensure_ascii=True))
