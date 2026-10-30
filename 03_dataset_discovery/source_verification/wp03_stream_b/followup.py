from discover import *
import xml.etree.ElementTree as ET
p=ROOT/'sources'/'rgbd_fulltext.xml'; tree=ET.parse(p)
print('references',[(x.attrib,' '.join(x.itertext())) for x in tree.iter() if x.tag=='ref'])
urls=[('https://data.mendeley.com/public-api/datasets/8n6nr43gk3/versions/1','rgbd_dataset.json'),('https://api.github.com/repos/abdollahzakeri/sms3d/git/trees/main?recursive=1','sms3d_tree.json'),('https://api.github.com/repos/abdollahzakeri/m18k/git/trees/main?recursive=1','m18k_tree.json')]
for i,q in enumerate(['SMS3D domain adaptation mushroom','M18K depth mushroom detection','RD-GuideNet white button mushrooms']):
 urls.append(('https://api.crossref.org/works?'+urllib.parse.urlencode({'query':q,'filter':'from-pub-date:2025-04-01','rows':8}),f'later_search_{i}.json'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(lambda p:fetch(*p),urls): print(r)
for i in range(3):
 p=ROOT/'sources'/f'later_search_{i}.json'
 if p.exists(): print(i,[(x.get('title'),x.get('DOI')) for x in json.loads(p.read_text())['message']['items']])
