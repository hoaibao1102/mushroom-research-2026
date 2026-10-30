from search_extract import *
dois=['10.1109/fet68771.2026.11601212','10.14569/ijacsa.2024.0150454','10.1109/icsses64899.2025.11009558','10.1109/icaiset66439.2026.11542036','10.57180/ngmd7490']
items=[('paper_'+str(i+1)+'_crossref','https://api.crossref.org/works/'+d) for i,d in enumerate(dois)]
items += [('paper1_ieee','https://ieeexplore.ieee.org/document/11601212/'),('paper2_publisher','https://thesai.org/Publications/ViewPaper?Volume=15&Issue=4&Code=IJACSA&SerialNo=54'),('c01_v2_public_api','https://data.mendeley.com/public-api/datasets/jrbx34k77g/versions/2/files'),('c01_v1_public_api','https://data.mendeley.com/public-api/datasets/jrbx34k77g/versions/1/files')]
for item in items:
 r=fetch(item)
 with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps(r)+'\n')
 subprocess.run(['python',CITE,'--ledger',str(LEDGER),'add',r['url'],'--title',r['name']],capture_output=True)
 print(json.dumps(r))
extract()
for p in (ROOT/'sources').glob('paper*_crossref.json'):
 x=json.loads(p.read_text())['message']; print('\n',p.name,json.dumps({k:x.get(k) for k in ['title','author','published','container-title','abstract','reference','link','resource']},ensure_ascii=True))
for p in (ROOT/'sources').glob('*public_api.json'):print(p.name,p.read_text()[:10000])
for p in (ROOT/'sources').glob('paper*.txt'):print(p.name,p.read_text(encoding='utf-8')[:20000])
