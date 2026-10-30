from retrieve import *
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlencode,quote
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.out.append(d.strip())
def extract():
 for p in (ROOT/'sources').glob('*.html'):
  t=Text();t.feed(p.read_text(encoding='utf-8'));p.with_suffix('.txt').write_text('\n'.join(t.out),encoding='utf-8')
 for n in ['c01_v2','c01_v1']:
  s=(ROOT/'sources'/f'{n}.html').read_text(encoding='utf-8')
  for m in re.finditer(r'<script[^>]*>(.*?)</script>',s,re.S):
   x=m.group(1)
   if 'INITIAL_STATE' in x or 'files' in x:
    (ROOT/'sources'/f'{n}_embedded_state.txt').write_text(x,encoding='utf-8')
if __name__=='__main__':
 queries=[('exact_doi','"10.17632/jrbx34k77g.2"'),('exact_stem','"jrbx34k77g"'),('related_bags','mushroom substrate bag contamination classification'),('related_mold','mushroom green mold deep learning classification'),('exact_title','"Mushroom Disease Dataset" "Mixed Infected"')]
 items=[]
 for n,q in queries:
  items.append(('search_crossref_'+n,'https://api.crossref.org/works?'+urlencode({'query':q,'rows':12,'filter':'from-pub-date:2024-01-01,until-pub-date:2026-12-31'})))
  items.append(('search_bing_'+n,'https://www.bing.com/search?'+urlencode({'q':q})))
 items += [('search_openalex_exact','https://api.openalex.org/works?'+urlencode({'search':'"jrbx34k77g"','per-page':20})),('c01_files_metadata','https://data.mendeley.com/public-api/datasets/jrbx34k77g/files?folder_id=root&version=2')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(fetch,items))
 with LOG.open('a',encoding='utf-8') as f:
  for r in results:f.write(json.dumps(r)+'\n');print(json.dumps(r))
 for r in results:subprocess.run(['python',CITE,'--ledger',str(LEDGER),'add',r['url'],'--title',r['name']],capture_output=True)
 extract()
 print('VERSIONS',(ROOT/'sources/c01_versions_api.json').read_text())
 print('LANDING TEXT',(ROOT/'sources/c01_v2.txt').read_text(encoding='utf-8'))
