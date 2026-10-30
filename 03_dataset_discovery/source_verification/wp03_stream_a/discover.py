import urllib.request,urllib.parse,json,pathlib,datetime,concurrent.futures,subprocess
BASE=pathlib.Path(__file__).parent
S='C:/Users/MSI PC/AppData/Local/hermes/skills/research/grounded-citations/scripts/sources.py'
LED=BASE/'source_ledger.json'
def fetch(url,name):
    at=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'WP03-public-metadata-research/1.0'})
        with urllib.request.urlopen(req,timeout=90) as r: text=r.read().decode('utf-8'); status=r.status
        (BASE/(name+'.txt')).write_text(text,encoding='utf-8')
        subprocess.run(['python',S,'--ledger',str(LED),'add',url,'--title',name],capture_output=True)
        rec={'url':url,'accessed_utc':at,'status':status,'file':name+'.txt'}
    except Exception as e: text=''; rec={'url':url,'accessed_utc':at,'error':str(e)}
    with (BASE/'access_log.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(rec)+'\n')
    return text
if __name__=='__main__':
    queries=['titles:mushroom AND (image OR disease OR quality OR growth OR contamination) AND publicationYear:[2024 TO 2026]','mushroom AND image AND publicationYear:[2024 TO 2026] AND client.client-id:bl.mendeley','mushroom AND (image OR dataset) AND publicationYear:[2024 TO 2026] AND (prefix:10.5281 OR prefix:10.6084)','oyster AND image AND publicationYear:[2024 TO 2026]']
    allrecords=[]
    for i,q in enumerate(queries):
        u='https://api.datacite.org/dois?'+urllib.parse.urlencode({'query':q,'page[size]':100})
        t=fetch(u,'search_datacite_'+str(i))
        if t:
            d=json.loads(t); print('QUERY',i,'TOTAL',d.get('meta',{}).get('total')); allrecords+=d.get('data',[])
    unique={x['id']:x for x in allrecords}
    (BASE/'discovery_records.json').write_text(json.dumps(list(unique.values()),indent=2),encoding='utf-8')
    for id,x in unique.items():
        a=x['attributes'];print(id,a.get('publicationYear'),str(a.get('titles')))
