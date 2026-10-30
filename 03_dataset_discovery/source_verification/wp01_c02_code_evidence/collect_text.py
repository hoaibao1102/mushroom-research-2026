import json,urllib.parse
from collect_sources import BASE,fetch
for repo in ['MushR','mushr-mask-r-cnn']:
    sha=json.loads((BASE/repo/'commit.json').read_text())['sha']
    tree=json.loads((BASE/repo/'tree.json').read_text())
    for o in tree['tree']:
        p=o['path']
        if o['type']=='blob' and o.get('size',0)<100000 and (p.lower().endswith(('.py','.sh','.yaml','.yml','.md','.conf')) or p=='LICENSE'):
            fetch('https://raw.githubusercontent.com/ETCE-LAB/'+repo+'/'+sha+'/'+urllib.parse.quote(p),repo+'/text/'+p,100000)
# Kaggle file listing pagination: file metadata only, never file content.
page=json.loads((BASE/'kaggle_files.json').read_text()); pages=[page]; tokens=set()
while page.get('nextPageToken') or page.get('nextPageTokenNullable'):
    token=page.get('nextPageToken') or page.get('nextPageTokenNullable')
    if token in tokens: raise RuntimeError('Repeated pagination token')
    tokens.add(token)
    url='https://www.kaggle.com/api/v1/datasets/list/etcelab/mushr-annotated-dataset-oyster-mushrooms?pageToken='+urllib.parse.quote(token,safe='')+'&pageSize=1000'
    raw=fetch(url,f'kaggle_files_page_{len(pages)+1:03d}.json')
    if not raw:break
    page=json.loads(raw);pages.append(page)
    if len(pages)>100:raise RuntimeError('Unexpected page count')
files=[f for p in pages for f in p.get('datasetFiles',p.get('files',[]))]
(BASE/'kaggle_files_aggregated.json').write_text(json.dumps({'pages':len(pages),'pagination_complete':not bool(page.get('nextPageToken') or page.get('nextPageTokenNullable')),'files':files},indent=2),encoding='utf-8')
print('KAGGLE',len(pages),len(files));print((BASE/'kaggle_view.json').read_text());print('FILE FIRST',files[:2])
