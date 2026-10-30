from html.parser import HTMLParser
from pathlib import Path
import re,json,hashlib,datetime,csv
R=Path(__file__).resolve().parent
repo=R.parents[3]
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t in ('p','h1','h2','h3','h4','tr','section'):self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
  if t in ('p','h1','h2','h3','h4','tr'):self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
p=P();p.feed((R/'publisher.html').read_text(encoding='utf-8'));text='\n'.join(re.sub(r'\s+',' ',s).strip() for s in ''.join(p.out).splitlines() if s.strip());(R/'publisher_text.txt').write_text(text,encoding='utf-8')
prior=repo/'03_dataset_discovery/source_verification/wp03_stream_a'
rows=[]
for name in ['zenodo_20373531.txt','paper_shiitake_fulltext.txt','source_ledger.json','access_log.jsonl','candidates.json']:
 q=prior/name
 rows.append({'path':q.relative_to(repo).as_posix(),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
(R/'wp03_input_hashes.json').write_text(json.dumps(rows,indent=2))
excerpts=[]
for i,line in enumerate(text.splitlines(),1):
 if any(k.lower() in line.lower() for k in ['1,782','5,375','6,500','43,752','experimental setup','Creative Commons','Code availability','YOLOv8n','independent','epochs','Algorithm 1','Table 1','Table 2','Table 3']):excerpts.append({'line':i,'text':line})
(R/'primary_excerpts.json').write_text(json.dumps(excerpts,indent=2,ensure_ascii=False),encoding='utf-8')
partial=R/'shiitake_mushroom_code.zip'
if partial.exists() and partial.stat().st_size!=5724836:partial.rename(R/'shiitake_mushroom_code.zip.partial')
print(json.dumps(excerpts,indent=2,ensure_ascii=True))
