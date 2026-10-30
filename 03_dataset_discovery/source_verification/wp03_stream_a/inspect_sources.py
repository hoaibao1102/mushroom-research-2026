from discover import *
queries=['mushroom AND publicationYear:[2024 TO 2026] AND prefix:10.17632','mushroom AND (quality OR disease OR contamination OR maturity OR growth) AND publicationYear:[2024 TO 2026]','titles.title:mushroom AND publicationYear:[2024 TO 2026]']
for i,q in enumerate(queries):
 t=fetch('https://api.datacite.org/dois?'+urllib.parse.urlencode({'query':q,'page[size]':100}),'search_extra_'+str(i))
 if t:
  d=json.loads(t);print('QUERY',i,'TOTAL',d.get('meta',{}).get('total'))
  for x in d.get('data',[]):
   a=x['attributes'];print(x['id'],a.get('titles'))
ids=['23322006','20373531','20260929','17688985']
for id in ids:
 t=fetch('https://zenodo.org/api/records/'+id,'zenodo_'+id)
 if t:
  d=json.loads(t); print('ZENODO',id,json.dumps(d.get('metadata'),ensure_ascii=True));print('FILES METADATA',[(x.get('key'),x.get('size')) for x in d.get('files',[])])
t=fetch('https://api.datacite.org/dois/10.17632/bsvbtcc348.1','datacite_bsvbtcc348_1')
if t: print('MYCELIUM',t)
