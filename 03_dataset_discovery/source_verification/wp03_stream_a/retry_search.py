from discover import *
urls=[('https://mdpi-res.com/d_attachment/agronomy/agronomy-15-00226/article_deploy/agronomy-15-00226.xml','paper_xml_alternate'),('https://api.figshare.com/v2/articles?order=published_date&order_direction=desc&page_size=10','figshare_healthcheck')]
for u,n in urls:
 t=fetch(u,n);print(n,len(t))
for i,q in enumerate(['"RGB-D Time-Series Dataset of White Button Mushroom Growth"','"Phenotypic image dataset of naturally grown shiitake mushrooms"','"Liadi" "mycelium"']):
 t=fetch('https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':q,'rows':3}),'retry_crossref_'+str(i))
 if t:
  for a in json.loads(t)['message']['items']: print(i,a.get('DOI'),a.get('title'))
