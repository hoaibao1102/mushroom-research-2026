from discover import *
urls=[('https://api.datacite.org/dois/10.17632/8n6nr43gk3.1','datacite_rgbd'),('https://data.mendeley.com/datasets/8n6nr43gk3/1','mendeley_rgbd'),('https://data.mendeley.com/datasets/bsvbtcc348/1','mendeley_mycelium'),('https://www.mdpi.com/2073-4395/15/1/226','paper_agronomy'),('https://www.mdpi.com/2073-4395/15/1/226/xml','paper_agronomy_xml'),('https://api.crossref.org/works/10.3390/agronomy15010226','crossref_agronomy'),('https://api.figshare.com/v2/articles?resource_doi=10.3390/agronomy15010226','figshare_search_doi')]
for u,n in urls:
 t=fetch(u,n)
 print(n,'OK' if t else 'FAILED')
 if n in ['datacite_rgbd','crossref_agronomy'] and t:
  d=json.loads(t);a=d.get('data',{}).get('attributes',d.get('message',{})); print(json.dumps({k:v for k,v in a.items() if k in ['titles','title','creators','descriptions','relatedIdentifiers','dates','rightsList','version','URL','link','abstract']},ensure_ascii=True))
queries=['"Scanned images of Oyster"','"Pleurotus ostreatus" "Liadi"','"RGB-D Time-Series" mushroom','"Phenotypic image dataset" shiitake']
for i,q in enumerate(queries):
 t=fetch('https://api.crossref.org/works?'+urllib.parse.urlencode({'query':q,'rows':5}),'followup_crossref_'+str(i))
 if t:
  for a in json.loads(t)['message']['items']:print('PAPER',i,a.get('DOI'),a.get('title'))
