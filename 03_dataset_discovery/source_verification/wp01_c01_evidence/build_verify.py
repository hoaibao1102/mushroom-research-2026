from retrieve import *
import csv,hashlib
from html import unescape
S=ROOT/'sources'
def load(n):return json.loads((S/n).read_text(encoding='utf-8'))
# Extract a publisher-hosted abstract embedded in metadata, not a search snippet.
s=(S/'paper1_ieee_alternative.html').read_text(encoding='utf-8')
a=unescape(re.search(r'<meta property="og:description" content="(.*?)"',s,re.S).group(1))
(S/'paper1_publisher_abstract.txt').write_text(a,encoding='utf-8')
for n in ['c01_v2','c01_v1']:
 t=(S/(n+'_embedded_state.txt')).read_text(encoding='utf-8');state=json.JSONDecoder().raw_decode(t.split('window.INITIAL_STATE = ',1)[1])[0]
 (S/(n+'_snapshot.json')).write_text(json.dumps(state['dataset']['snapshot'],indent=2,ensure_ascii=False),encoding='utf-8')
fields='claim_id,claim_text,candidate_id,source_title,source_url_or_doi,source_type,source_publication_update_date,access_date,source_location,evidence_status,confidence,verification_notes'.split(',')
rows=[]
def claim(text,source='c01_v2',loc='Description',status='REPORTED_BY_SOURCE_NOT_AUDITED',notes='',candidate='C01',confidence='HIGH',date='2025-06-30'):
 urls={'c01_v2':'https://data.mendeley.com/datasets/jrbx34k77g/2','c01_v1':'https://data.mendeley.com/datasets/jrbx34k77g/1','versions':'https://data.mendeley.com/public-api/datasets/jrbx34k77g/versions','datacite':'https://api.datacite.org/dois/10.17632/jrbx34k77g.2','paper1':'https://ieeexplore.ieee.org/abstract/document/11601212','paper2':'https://thesai.org/Publications/ViewPaper?Volume=15&Issue=4&Code=IJACSA&SerialNo=54','ds02':'https://api.datacite.org/dois/10.17632/hf55tkx489.1','search':'https://api.openalex.org/works?search=%22jrbx34k77g%22&per-page=20'}
 rows.append(dict(zip(fields,[f'WP01-{len(rows)+1:03}',text,candidate,source,urls[source],'PRIMARY_REPOSITORY_METADATA' if source.startswith('c01') or source in ['versions','datacite','ds02'] else 'PUBLISHER_ABSTRACT' if source.startswith('paper') else 'SEARCH_INDEX',date,'2026-10-23',loc,status,confidence,notes or 'Public metadata/text only; no payload audit.'])))
claim('C01 v2 title: Mushroom Disease Dataset (Healthy, Single Infected & Mixed Infected); DOI 10.17632/jrbx34k77g.2.',loc='Title / DOI',status='VERIFIED_FROM_PRIMARY_SOURCE')
claim('C01 v2 contributors: Abdullah Mazumdar; Jubayer Ahmed Bhuiyan Shawon; Sumon Debnath; Md Abdullah.',loc='Contributors',status='VERIFIED_FROM_PRIMARY_SOURCE')
claim('C01 v2 published 30 June 2025.',loc='Published',status='VERIFIED_FROM_PRIMARY_SOURCE')
claim('Repository and DOI registry declare CC BY 4.0.',source='datacite',loc='data.attributes.rightsList',status='VERIFIED_FROM_PRIMARY_SOURCE',notes='Declaration verified, underlying third-party rights not audited.')
claim('761 total images: 299 healthy, 147 single-infected, 315 mixed-infected.',notes='Source-reported counts only; no enumeration or independent audit.')
claim('Cultivation bags photographed at Mushroom Development Institute, Savar, Dhaka, Bangladesh.')
claim('Source associates infected images with green mold, black mold or both.')
claim('Mixed-infected means multiple pathogens or overlapping infection patterns, typically both molds.',notes='Does not establish laboratory-confirmed co-infection for each image.')
claim('iPhone 11 Pro Max captured HEIC; later converted to JPG.')
claim('Biological confirmation, organism identities and expert adjudication protocol are unresolved.',status='UNVERIFIED',notes='Not specified in retrieved Description; no payload/assay inspected.')
claim('Bag/session/batch IDs and repeated-view linkage remain unresolved.',status='UNVERIFIED',notes='No manifest retrieved; do not assume images are independent bags.')
claim('Predefined train/validation/test split and group-disjoint evaluation are unresolved.',status='UNVERIFIED',notes='No split protocol in retrieved metadata.')
claim('Folders, literal labels, filenames, file sizes, checksums and per-file counts are unresolved.',status='UNVERIFIED',loc='Files heading; embedded state filesLoading=true; access log',notes='Empty/loading HTML state and unsuccessful metadata endpoints do not establish no files.')
claim('Public version list contains available v1 (2025-06-16) and v2 (2025-06-30).',source='versions',loc='JSON array entries',status='VERIFIED_FROM_PRIMARY_SOURCE')
claim('v1 title is Mushroom Disease Dataset (Healthy, Black Mold & Green Mold).',source='c01_v1',loc='Title',status='VERIFIED_FROM_PRIMARY_SOURCE',date='2025-06-16')
claim('v1 reports 680 images: 299 healthy, 72 single-infected, 309 mixed-infected.',source='c01_v1',date='2025-06-16')
claim('v1 title mold names do not match the healthy/single/mixed wording in its own description.',source='c01_v1',loc='Title versus Description',status='VERIFIED_FROM_PRIMARY_SOURCE',date='2025-06-16',notes='Observed metadata semantic mismatch, not proof of erroneous per-file labels.')
claim('v1-to-v2 file additions, replacements and label changes are unknown.',status='UNVERIFIED',notes='Metadata count changes cannot establish a file-level diff.')
claim('C01 source describes a candidate bag-image classification task, not confirmed object detection.',status='INFERRED',confidence='MODERATE',notes='Reviewer interpretation of class description; annotations not inspected.')
claim('No exact-C01-DOI citing paper or reuse was confirmed in the bounded search.',source='search',loc='search_openalex_exact.json meta.count=0; exact_crossref_retry.json; access_search_log.jsonl',status='UNVERIFIED',date='2026-10-23',confidence='MODERATE',notes='Search outcome only, not proof of absence or novelty; noisy web results and incomplete indexing.')
claim('2026 Bacanto et al. paper abstract describes healthy/green-mold/black-mold fruiting bags collected in Laguna using iPhone 15 and expert validation.',source='paper1',loc='HTML meta[property=og:description]; paper1_publisher_abstract.txt',date='2026-04-22',candidate='RELATED-01')
claim('2026 Bacanto et al. abstract reports ResNet-18+CBAM and GLCM features, ANN, 100 epochs and 86.9% accuracy.',source='paper1',loc='HTML meta[property=og:description]',date='2026-04-22',candidate='RELATED-01',notes='Abstract only; not independently reproduced; split and dataset size unknown.')
claim('Bacanto et al. is same-task different-dataset prior work, not confirmed C01 reuse.',source='paper1',loc='Abstract collection place/device versus C01 Description',status='INFERRED',date='2026-04-22',candidate='RELATED-01',notes='Explicit Laguna/iPhone 15 account differs from Savar/iPhone 11 Pro Max; no C01 reference in deposited Crossref references.')
claim('2024 Ujir et al. abstract reports 1400 images from two Pleurotus ostreatus strains over 14 days, HSV and CNN approaches.',source='paper2',date='2024',loc='Abstract',candidate='RELATED-02')
claim('Ujir et al. abstract reports 92.15% growth and 97.81% contamination prediction average accuracy.',source='paper2',date='2024',loc='Abstract',candidate='RELATED-02',notes='Author-reported abstract metrics; not transferable to C01.')
claim('DS02 is Annotated Oyster Mushroom Images, issued 2024-07-15, CC BY 4.0.',source='ds02',date='2024-07-15',loc='data.attributes titles/dates/rightsList',candidate='DS02_EXCLUDED',status='VERIFIED_FROM_PRIMARY_SOURCE')
claim('DS02 reports 555 raw camera images, about 8000 mushroom-labeled and over 8000 maturity-labeled images, sensor data and two cultivation cycles in Mersin.',source='ds02',date='2024-07-15',loc='data.attributes.descriptions',candidate='DS02_EXCLUDED',notes='Metadata comparison only; exclusion unchanged, no DS02 payload imported.')
claim('G0 remains conditional/hold and training is not authorized pending provenance, label and grouping evidence.',status='INFERRED',loc='findings.md Scope and decision',confidence='HIGH',notes='Reviewer recommendation; no dataset acceptance or training performed.')
titles={'c01_v2':'Mushroom Disease Dataset (Healthy, Single Infected & Mixed Infected), version 2','c01_v1':'Mushroom Disease Dataset (Healthy, Black Mold & Green Mold), version 1','versions':'Mendeley Data C01 public version history','datacite':'DataCite registration: 10.17632/jrbx34k77g.2','paper1':'Hybrid Feature Engineering and Artificial Neural Network for Mushroom Fruiting Bag Contamination Classification','paper2':'Automating Mushroom Culture Classification: A Machine Learning Approach','ds02':'Annotated Oyster Mushroom Images: DataCite registration','search':'OpenAlex exact dataset-stem search'}
for row in rows:row['source_title']=titles[row['source_title']]
with (ROOT/'claims.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
papers=[]
for i in range(1,6):
 x=load(f'paper_{i}_crossref.json')['message']; d=x['DOI'];papers.append({'paper_id':f'RELATED-{i:02}','doi':d,'title':x['title'][0],'authors':'; '.join(' '.join([a.get('given',''),a.get('family','')]).strip() for a in x['author']),'publication_date':'-'.join(map(str,x['published']['date-parts'][0])),'venue':'; '.join(x.get('container-title',[])),'review_scope':'ABSTRACT_ONLY' if i<3 else 'METADATA_ONLY','task_relevance':'SAME_TASK_BAG_CONTAMINATION' if i==1 else 'RELATED_CULTURE_CONTAMINATION' if i==2 else 'UNRESOLVED_DISEASE_LEAD','c01_relationship':'SAME_TASK_DIFFERENT_DATASET' if i==1 else 'RELATED_DOMAIN_DIFFERENT_DATASET' if i==2 else 'UNCERTAIN','evidence_path':f'sources/paper_{i}_crossref.json','notes':'Primary publisher abstract recovered' if i<3 else 'No methods/metrics extracted'})
x=load('chapter2026_crossref.json')['message'];papers.append({'paper_id':'RELATED-06','doi':x['DOI'],'title':x['title'][0],'authors':'; '.join(' '.join([a.get('given',''),a.get('family','')]).strip() for a in x.get('author',[])) or 'AUTHORS_NOT_RETRIEVED','publication_date':'-'.join(map(str,x['published']['date-parts'][0])),'venue':'; '.join(x.get('container-title',[])),'review_scope':'INDEX_ABSTRACT_ONLY','task_relevance':'RELATED_CULTURE_CONTAMINATION','c01_relationship':'UNCERTAIN','evidence_path':'sources/chapter2026_crossref.json; sources/openalex_bags.json','notes':'Same title/results as 2024 paper; not independent confirmation'})
with (ROOT/'related_papers.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=papers[0].keys());w.writeheader();w.writerows(papers)
# Attach exact evidence for every cited source, using retrieved text/JSON.
quotes={1:('c01_v2.txt','The dataset comprises a total of 761 high-resolution images, including 299 healthy samples, 147 single-infected samples, and 315 mixed-infected samples.'),2:('c01_v1.txt','The dataset comprises a total of 680 high-resolution images, including 299 healthy samples, 72 single-infected ones, and 309 mixed-infected images.'),3:('excluded_ds02_v1.txt','Annotated Oyster Mushroom Images'),4:('c01_datacite_v2.json','Creative Commons Attribution 4.0 International'),5:('c01_datacite_v1.json','Mushroom Disease Dataset'),6:('c01_versions_api.json','2025-06-30'),9:('search_crossref_exact_doi.json','title 17632'),10:('search_bing_exact_doi.txt','TikTok'),12:('search_bing_exact_stem.txt','Kiến Tường'),19:('search_openalex_exact.json','"count": 0'),20:('c01_files_metadata.json','[]'),22:('c01_files_no_folder.json','"error":400'),23:('google_exact.txt','Google Search'),24:('google_related.txt','Google Search'),25:('openalex_bags.json','Automating Mushroom Culture Classification'),26:('crossref_bags_retry.json','Hybrid Feature Engineering'),27:('paper_1_crossref.json','Hybrid Feature Engineering'),28:('paper_2_crossref.json','Automating Mushroom Culture Classification'),29:('paper_3_crossref.json','Automated Disease Detection'),30:('paper_4_crossref.json','IoT-Based Automated Mushroom House'),31:('paper_5_crossref.json','Mushroom Disease Detection'),32:('paper1_ieee.txt',"we need to verify that you're not a robot"),33:('paper2_publisher.txt','We evaluated a dataset of 1400 images from two strains of Pleurotus ostreatus mycelium samples over a period of 14 days.'),36:('paper1_publisher_abstract.txt','a dataset comprising healthy, green mold, black mold fruiting bags was collected from mushroom farms in Laguna.'),39:('chapter2026_crossref.json','AUTOMATING MUSHROOM CULTURE CLASSIFICATION'),40:('exact_crossref_retry.json','"total-results":0'),8:('ds02_datacite.json','Annotated Oyster Mushroom Images')}
for i,(file,q) in quotes.items():
 if i in [6,9,19,20,22,40]:
  obj=load(file)
  if i==9:obj=obj['message']['items'][0]['title']
  pretty=json.dumps(obj,indent=2,ensure_ascii=False)
  if i==20:continue
  file=file.replace('.json','_pretty.txt');(S/file).write_text(pretty,encoding='utf-8');q=pretty
 if i==10:q='TikTok - Make Your Day'
 if i==12:q='Bến xe Miền Tây'
 if i in [23,24]:q='Nếu bạn gặp vấn đề khi truy cập vào Google Tìm kiếm'
 r=subprocess.run(['python',CITE,'--ledger',str(LEDGER),'quote',str(i),'--text',q,'--from',str(S/file)],capture_output=True,text=True)
 if r.returncode:print('QUOTE FAILED',i,r.stdout,r.stderr)
subprocess.run(['python',CITE,'--ledger',str(LEDGER),'render','--replace-in',str(ROOT/'findings.md'),'--style','evidence'],check=True)
r=subprocess.run(['python',CITE,'--ledger',str(LEDGER),'verify',str(ROOT/'findings.md'),'--evidence'],capture_output=True,text=True)
(ROOT/'citation_verification.txt').write_text(r.stdout+r.stderr,encoding='utf-8');print(r.stdout,r.stderr)
allowed={'VERIFIED_FROM_PRIMARY_SOURCE','REPORTED_BY_SOURCE_NOT_AUDITED','INFERRED','UNVERIFIED','CONTRADICTED'}
assert all(x['evidence_status'] in allowed and all(x[k] for k in fields) for x in rows)
assert all(re.fullmatch(r'10\.\d{4,9}/\S+',x['doi']) for x in papers)
assert r.returncode==0
manifest=[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(S.iterdir()) if p.is_file()]
(ROOT/'source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
result={'scope':'structural/vocabulary/citation-provenance; NOT independent scientific audit','result':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'claim_rows':len(rows),'related_paper_rows':len(papers),'saved_source_files':len(manifest),'required_claim_columns':fields,'all_statuses_valid':True,'citation_evidence_verification':r.returncode==0,'dataset_payloads_downloaded':False,'training_run':False,'g0_recommendation':'CONDITIONAL_HOLD','training_authorization':'NOT_AUTHORIZED','shared_registries_or_git_modified':False}
(ROOT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
