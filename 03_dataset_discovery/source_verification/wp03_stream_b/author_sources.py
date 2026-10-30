from discover import *
urls=[('https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13452286/fullTextXML','rgbd_fulltext.xml')]
for repo in ['sms3d','m18k']:
 urls.extend([(f'https://api.github.com/repos/abdollahzakeri/{repo}',f'{repo}_repo.json'),(f'https://api.github.com/repos/abdollahzakeri/{repo}/readme',f'{repo}_readme.json'),(f'https://api.github.com/repos/abdollahzakeri/{repo}/commits?per_page=1',f'{repo}_commit.json')])
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for r in ex.map(lambda p:fetch(*p),urls): print(r)
import base64,xml.etree.ElementTree as ET
for repo in ['sms3d','m18k']:
 p=ROOT/'sources'/f'{repo}_readme.json'
 if p.exists(): (ROOT/'sources'/f'{repo}_readme.txt').write_text(base64.b64decode(json.loads(p.read_text())['content']).decode(),encoding='utf8')
p=ROOT/'sources'/'rgbd_fulltext.xml'
if p.exists(): (ROOT/'sources'/'rgbd_fulltext.txt').write_text('\n'.join(' '.join(x.itertext()) for x in ET.parse(p).iter() if x.tag in ['article-title','p','title','table','license']),encoding='utf8')
