from discover import *
import time
queries=['SMS3D mushroom','M18k mushroom','mushroom dataset','mushroom quality deep learning']
for i,q in enumerate(queries):
 u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.title':q,'filter':'from-pub-date:2024-01-01','rows':12})
 r=fetch(u,f'title_search_{i}.json')
 if 'file' in r:
  d=json.loads((ROOT/r['file']).read_text(encoding='utf8'))
  print(q,[(x.get('title'),x.get('DOI')) for x in d['message']['items']])
 time.sleep(3)
