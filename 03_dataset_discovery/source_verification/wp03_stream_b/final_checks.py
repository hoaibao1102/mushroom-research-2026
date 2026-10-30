from discover import *
import re,html
for n in ['sms3d','m18k']:
 d=json.loads((ROOT/'sources'/f'{n}_repo.json').read_text());print(n,'license',d['license'],'commit',json.loads((ROOT/'sources'/f'{n}_commit.json').read_text())[0]['sha'])
 fetch(f'https://raw.githubusercontent.com/abdollahzakeri/{n}/main/LICENSE',f'{n}_LICENSE.txt')
for n in ['sms3d','m18k']:
 p=ROOT/'sources'/f'{n}.pdf';b=p.read_bytes();print(n,'pdf_signature',b[:5],'eof',b.rstrip().endswith(b'%%EOF'))
p=(ROOT/'sources'/'rgbd_landing.html').read_text(); d=json.loads(re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',p,re.S).group(1));(ROOT/'sources'/'rgbd_dataset_metadata.json').write_text(json.dumps(d,indent=2),encoding='utf8')
print('rd dates',json.loads((ROOT/'sources'/'rdguidenet_metadata.json').read_text())['message']['published'])
print('RD statements')
for i,line in enumerate((ROOT/'sources'/'rdguidenet.txt').read_text().splitlines()):
 if any(w in line.lower() for w in ['training','github','availability','129','80%','70%','split','limitation']):print(i+1,line[:4000])
