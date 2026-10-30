from discover import *
import xml.etree.ElementTree as ET
urls=[('https://data.mendeley.com/datasets/8n6nr43gk3/1','rgbd_landing.html'),('https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13030075/fullTextXML','rdguidenet.xml'),('https://api.crossref.org/works/10.3390/s26061935','rdguidenet_metadata.json'),('https://api.crossref.org/works?query.title=SMS3D&filter=from-pub-date:2025-04-02&rows=15','sms3d_later_retry.json'),('https://api.crossref.org/works?query.title=M18K&filter=from-pub-date:2025-05-21&rows=15','m18k_later_retry.json')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(lambda p:fetch(*p),urls):print(r)
p=ROOT/'sources'/'rdguidenet.xml'
if p.exists(): (ROOT/'sources'/'rdguidenet.txt').write_text('\n'.join(' '.join(x.itertext()) for x in ET.parse(p).iter() if x.tag in ['article-title','p','title','table','license']),encoding='utf8')
for n in ['sms3d','m18k']:
 d=json.loads((ROOT/'sources'/f'{n}_tree.json').read_text());print(n,[(x['path'],x.get('size')) for x in d['tree'] if x['path'].lower().endswith(('.py','.md','.txt','license','.yaml','.yml'))])
for n in ['sms3d_later_retry','m18k_later_retry']:
 p=ROOT/'sources'/f'{n}.json'
 if p.exists():print(n,[(x.get('title'),x.get('DOI')) for x in json.loads(p.read_text())['message']['items']])
