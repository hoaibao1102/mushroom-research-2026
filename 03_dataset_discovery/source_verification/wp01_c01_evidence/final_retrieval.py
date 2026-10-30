from search_extract import *
items=[('paper1_ieee_alternative','https://ieeexplore.ieee.org/abstract/document/11601212'),('paper1_repository_search','https://api.openalex.org/works/https://doi.org/10.1109/fet68771.2026.11601212'),('paper5_publisher','https://www.thelight-explorer.com/mushroom-disease-detection-and-classification-with-decision-support/'),('chapter2026_crossref','https://api.crossref.org/works/10.58532/nbennurngcdb1p1c2'),('exact_crossref_retry','https://api.crossref.org/works?'+urlencode({'query':'jrbx34k77g','rows':20})),('c01_files_api_alt','https://data.mendeley.com/api/datasets-v2/datasets/jrbx34k77g/versions/2/files'),('c01_folders_api_alt','https://data.mendeley.com/public-api/datasets/jrbx34k77g/folders?version=2')]
for item in items:
 r=fetch(item)
 with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps(r)+'\n')
 subprocess.run(['python',CITE,'--ledger',str(LEDGER),'add',r['url'],'--title',r['name']],capture_output=True);print(json.dumps(r))
extract()
r={'access_timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'name':'browser_c01_metadata_attempt','url':'https://data.mendeley.com/datasets/jrbx34k77g/2','status':'FAILED','error':'Browser profile locked; no browser closed or profile modified. urllib primary retrieval successful.'}
with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps(r)+'\n')
for n in ['paper5_publisher','c01_files_api_alt','c01_folders_api_alt']:
 for p in (ROOT/'sources').glob(n+'.*'):
  if p.suffix in ['.txt','.json']:print(p.name,p.read_text(encoding='utf-8')[:14000])
