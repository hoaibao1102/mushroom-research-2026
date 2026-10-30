from search_extract import *
items=[('c01_folders_metadata','https://data.mendeley.com/public-api/datasets/jrbx34k77g/folders?folder_id=root&version=2'),('c01_files_no_folder','https://data.mendeley.com/public-api/datasets/jrbx34k77g/files?version=2'),('google_exact','https://www.google.com/search?q=%22jrbx34k77g%22'),('google_related','https://www.google.com/search?q=mushroom+bag+contamination+classification+2025+2026'),('openalex_bags','https://api.openalex.org/works?'+urlencode({'search':'mushroom contamination classification','filter':'from_publication_date:2024-01-01,to_publication_date:2026-10-23','per-page':30})),('crossref_bags_retry','https://api.crossref.org/works?'+urlencode({'query.title':'mushroom contamination detection','rows':30,'filter':'from-pub-date:2024-01-01,until-pub-date:2026-10-23'}))]
for item in items:
 r=fetch(item)
 with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps(r)+'\n')
 subprocess.run(['python',CITE,'--ledger',str(LEDGER),'add',r['url'],'--title',r['name']],capture_output=True)
 print(json.dumps(r))
extract()
for name in ['google_exact','google_related']:
 p=ROOT/'sources'/f'{name}.txt'
 if p.exists():print(name,p.read_text(encoding='utf-8')[:18000])
for name in ['c01_folders_metadata','c01_files_no_folder']:
 p=ROOT/'sources'/f'{name}.json'
 if p.exists():print(name,p.read_text()[:16000])
for name in ['openalex_bags','crossref_bags_retry']:
 p=ROOT/'sources'/f'{name}.json'
 if p.exists():
  j=json.loads(p.read_text());rows=j.get('results',j.get('message',{}).get('items',[]))
  for x in rows:print(name,x.get('doi',x.get('DOI')),x.get('title'),x.get('publication_date'),x.get('abstract','')[:1000])
