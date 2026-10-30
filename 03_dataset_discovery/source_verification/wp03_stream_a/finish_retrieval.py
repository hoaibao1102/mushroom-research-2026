from discover import *
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self): super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
  if t in ['p','h1','h2','h3','tr','li']:self.parts.append('\n')
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
p=Text();p.feed((BASE/'paper_shiitake.txt').read_text(encoding='utf-8'));text=' '.join(p.parts);(BASE/'paper_shiitake_fulltext.txt').write_text(text,encoding='utf-8')
for l in text.splitlines():
 if any(w in l.lower() for w in ['203735','split','images','accuracy','map','yolo','limitation','future','class','dataset','gpu']):print(l[:2500])
for u,n in [('https://api.elsevier.com/content/article/PII:S2352340926006335?httpAccept=text/xml','paper_rgbd_xml'),('https://www.sciencedirect.com/science/article/pii/S2352340926006335','paper_rgbd_correct'),('https://mdpi-res.com/d_attachment/sensors/sensors-26-01935/article_deploy/sensors-26-01935.xml','paper_rdguidenet_xml')]:
 t=fetch(u,n);print(n,len(t))
