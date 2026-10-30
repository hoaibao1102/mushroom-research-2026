from discover import *
import xml.etree.ElementTree as ET,re,html
for u,n in [('https://www.nature.com/articles/s41597-026-07754-7','paper_shiitake'),('https://api.crossref.org/works/10.1016/j.dib.2026.113085','crossref_rgbd'),('https://api.crossref.org/works/10.1038/s41597-026-07754-7','crossref_shiitake'),('https://www.sciencedirect.com/science/article/pii/S2352340926007168','paper_rgbd_attempt')]:
 t=fetch(u,n);print(n,len(t))
 if n=='crossref_rgbd' and t: print(t[:12000])
p=BASE/'paper_xml_alternate.txt'
r=ET.fromstring(p.read_text(encoding='utf-8'));text='\n'.join(' '.join(x.itertext()) for x in r.iter() if x.tag in ['p','title','article-title','table','label']);(BASE/'paper_agronomy_fulltext.txt').write_text(text,encoding='utf-8')
for line in text.splitlines():
 if any(w in line.lower() for w in ['3195','split','70%','80%','training','limitation','future','99.70','uv','white light','white-light']):print(line[:2500])
