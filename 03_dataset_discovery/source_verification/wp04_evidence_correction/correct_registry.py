"""Offline historical claim-level repair. Run from any cwd; originals read-only."""
from pathlib import Path
import csv,json,hashlib,re,html,collections
HERE=Path(__file__).resolve().parent
# HERE parents: source_verification, 03_dataset_discovery, repository
ROOT=HERE.parents[2]
BASE=ROOT/'03_dataset_discovery/source_verification'
OLD=BASE/'WP-03_SOURCE_EVIDENCE.csv'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def norm(s): return ' '.join(html.unescape(s).split())
rows=list(csv.DictReader(OLD.open(encoding='utf-8-sig',newline='')))
before=sha(OLD)
assert before=='8b467a44a850bd95ba2eaeb4c575d0a1dc8a52f61b53210a5d43957765b1fb2f', 'Historical input differs from audited HEAD 7076719'
claims=(HERE/'claims.txt').read_text(encoding='utf-8').splitlines()
assert len(rows)==len(claims)==202
A=load(BASE/'wp03_stream_a/candidates.json')['candidates']
LA={s['id']:s for s in load(BASE/'wp03_stream_a/source_ledger.json')['sources']}
B=load(BASE/'wp03_stream_b/claim_evidence.json')
LB={s['id']:s for s in load(BASE/'wp03_stream_b/citation_ledger.json')['sources']}
logs={}
for stream in ['a','b']:
 logs[stream]=[json.loads(l) for l in (BASE/f'wp03_stream_{stream}/access_log.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
aflat=[(f'C{int(c["temporary_id"][1:])+2:02}',c,e) for c in A for e in c['evidence']]
assert len(aflat)==156
# Explicit semantic conflict flags, not absence-of-replication flags.
conflicts={11:'99.70% called accuracy here versus 99.66% accuracy and 99.70% weighted score in results.',12:'DenseNet-201 99.98% conflicts with 99.44% in results/discussion.',15:'DenseNet-201 99.98% conflicts with 99.44% in results/discussion.',17:'DenseNet-201 99.98% conflicts with 99.44% in results/discussion.',18:'DenseNet-201 99.98% conflicts with 99.44% in results/discussion.',19:'DenseNet-201 99.98% conflicts with 99.44% in results/discussion.'}
# Structural document observations (not claims that experimental outcomes are true).
sourcefacts={1,3,31,64,66,67,68,69,70,71,72,73,74,76,77,78,80,81,86,96,100,113,114,115,116,117,118,119,120,121,122,136,153,154,155,158,172,173,174,176,187,200,201,202}
proposals={6,61,63,93,126,146,148,171,183}
# Numeric table fragments need model/task/header context explicitly preserved in location.
table_context={164:'Table 4: theta_diff (degrees), synthetic',165:'Table 4: theta_diff (degrees), real 10 images',166:'Table 5: Detection F1/AP/AR then Segmentation F1/AP/AR',167:'Table 5: Detection F1/AP/AR then Segmentation F1/AP/AR',168:'Table 5: Detection F1/AP/AR then Segmentation F1/AP/AR',195:'Table 2: Mask R-CNN/MobileNet-V3, RGB 3 channels; F1/AP/AR',196:'Table 2: Mask R-CNN/ResNet-50, RGB 3 channels; F1/AP/AR',197:'Table 2: Mask R-CNN/ResNet-50, RGB-D 4 channels; F1/AP/AR',198:'Table 2: YOLOv8-M/CSPDarknet, Seg, 1280; F1/AP/AR'}
proof=[]; corrected=[]
for n,(r,claim) in enumerate(zip(rows,claims),1):
 stream='a' if r['stream'].startswith('A') else 'b'; ledger=LA if stream=='a' else LB
 if stream=='a':
  cid,c,e=aflat[n-1]
  assert cid==r['candidate_id'] and norm(e['quote'])==norm(r['verbatim_quote']) and e['locator']==r['source_location']
  sid=e['source_id']; source=ledger[sid]; saved=BASE/'wp03_stream_a'/e['saved_file']; mapref=f'wp03_stream_a/candidates.json:{c["temporary_id"]}.evidence[{c["evidence"].index(e)}]; source_ledger source {sid}'
 else:
  matches=[(i,e) for i,e in enumerate(B) if norm(e['quote'])==norm(r['verbatim_quote']) and e['locator']==r['source_location'] and e['url']==r['source_url']]
  assert matches,(n,r)
  bi,e=matches[0];sid=e['citation_id'];source=ledger[sid];saved=BASE/'wp03_stream_b/sources'/e['locator'].split(':line')[0];mapref=f'wp03_stream_b/claim_evidence.json:[{bi}]; citation_ledger source {sid}'
 url=e.get('url') or e.get('source_url') or source.get('url','')
 assert not r['source_url'] or url==r['source_url']
 raw=saved.read_text(encoding='utf-8-sig') if saved.exists() else ''
 # Search decoded saved JSON strings as well as literal saved text; normalization is whitespace + HTML entity decoding only.
 texts=[raw]
 try:
  obj=json.loads(raw)
  def strings(x):
   if isinstance(x,str):yield x
   elif isinstance(x,dict):
    for v in x.values():yield from strings(v)
   elif isinstance(x,list):
    for v in x:yield from strings(v)
  texts.extend(strings(obj))
 except ValueError:pass
 quote=norm(r['verbatim_quote']); found=any(quote in norm(t) for t in texts)
 # Match a short verbatim span. Prefer sentence overlap with the manually recovered proposition.
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',quote)
 tokens=set(re.findall(r'[a-z0-9]+',claim.lower()))-{'the','a','of','and','in','to','for','authors','report','c03','c04'}
 def score(s):return len(tokens & set(re.findall(r'[a-z0-9]+',s.lower())))
 chosen=max(sentences,key=score) if sentences else quote
 words=chosen.split(); excerpt=' '.join(words[:35])
 assert not found or any(excerpt in norm(t) for t in texts)
 loghits=[x for x in logs[stream] if x.get('url')==url or (x.get('file') and Path(x['file']).name==saved.name)]
 successful=[x for x in loghits if x.get('status')==200]
 uncertainty=[]
 if not found or not url:
  status='UNRESOLVED';uncertainty.append('Historical quotation could not be matched against saved original text, or source provenance is missing. URL intentionally blank.');url=''
 elif n in conflicts:
  status='AUTHOR_REPORTED_RESULT_CONTRADICTED';uncertainty.append(conflicts[n]+' Contradicted means internally inconsistent source claims, not independent experimental falsification.')
 elif n in sourcefacts:status='SOURCE_FACT_VERIFIED_IN_SAVED_TEXT'
 elif n in proposals:status='AUTHOR_PROPOSAL_NOT_VALIDATED'
 else:status='AUTHOR_REPORTED_NOT_REPRODUCED'
 if n not in sourcefacts:uncertainty.append('Saved wording verified only; no empirical replication, payload inspection or external-validity certification.')
 if n in {80,81}:uncertainty.append('Non-article recommendation/navigation contamination in historical extraction; not evidence for candidate.')
 if n in {66,67,113,114,115,116,117,118,119}:uncertainty.append('Bibliographic presence does not prove cited dataset usage or independently verify the cited result.')
 if n in {1,65,157,158,160,172,173,174,176,199,200,201,202}:uncertainty.append('Availability/license/count statements remain version- and scope-dependent; advertised downloads were not fetched.')
 if n in {75,123,124,156}:uncertainty.append('Historical excerpt is truncated; consult saved source context for full object/relationship.')
 if not successful:uncertainty.append('No matching HTTP-200 access-log entry found; provenance relies on original evidence and source ledger.')
 if not uncertainty:uncertainty.append('Verification establishes document content only, not underlying empirical truth.')
 title=source.get('title','')
 if stream=='a' and saved.name=='paper_agronomy_fulltext.txt':title=A[0]['paper']['title']
 if stream=='a' and saved.name=='paper_shiitake_fulltext.txt':title=A[1]['paper']['title']
 if stream=='a' and 'rdguidenet' in saved.name:title='RD-GuideNet: A Depth-Guided Framework for Robust Detection, Segmentation, and Temporal Tracking of White Button Mushrooms'
 location=r['source_location']
 if n in table_context:location+='; '+table_context[n]
 conf='HIGH_DOCUMENT_TRACEABILITY' if found and successful else 'MEDIUM_DOCUMENT_TRACEABILITY' if found else 'LOW_UNRESOLVED'
 out=dict(evidence_id=r['evidence_id'],candidate_id=r['candidate_id'],specific_claim=claim,original_claim=r['claim'],primary_source_url=url,source_title=title,source_location=location,supporting_excerpt=excerpt,verification_status=status,access_date=e.get('access_date',e.get('retrieved_date',source.get('accessed',r['access_date']))),confidence=conf,remaining_uncertainty=' '.join(uncertainty),original_saved_source=saved.relative_to(ROOT).as_posix())
 corrected.append(out)
 proof.append(dict(evidence_id=r['evidence_id'],mapping=mapref,saved_text_quote_verified=found,saved_sha256=sha(saved) if saved.exists() else None,successful_access_log_entries=len(successful),source_id=sid,original_url_blank=not r['source_url'],recovered_url=url,contradicted=n in conflicts,excerpt_words=len(excerpt.split())))
FIELDS='evidence_id,candidate_id,specific_claim,original_claim,primary_source_url,source_title,source_location,supporting_excerpt,verification_status,access_date,confidence,remaining_uncertainty,original_saved_source'.split(',')
# Generic coverage cannot be gamed by appending an ID or quote index.
for c in corrected:
 assert c['specific_claim']!=c['original_claim']
 assert not re.search(r'primary.source excerpt|see locator|quote.index|evidence item|excerpt supporting',c['specific_claim'],re.I)
 assert len(c['specific_claim'].split())>=9
byclaim=collections.defaultdict(list)
for c in corrected:byclaim[norm(c['specific_claim']).lower()].append(c['evidence_id'])
duplicates=[v for v in byclaim.values() if len(v)>1]
# Only genuine duplicated historical evidence may retain a shared semantic proposition.
for ids in duplicates:
 original=[r for r in rows if r['evidence_id'] in ids]
 assert len({(r['candidate_id'],r['source_location'],norm(r['verbatim_quote'])) for r in original})==1,ids
outpath=BASE/'WP-03_EVIDENCE_REGISTRY_CORRECTED.csv'
with outpath.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(corrected)
assert sha(OLD)==before
stats={'historical_rows':len(rows),'corrected_rows':len(corrected),'historical_blank_urls':sum(not r['source_url'] for r in rows),'recovered_previously_blank_urls':sum(not r['source_url'] and bool(c['primary_source_url']) for r,c in zip(rows,corrected)),'corrected_blank_urls':sum(not c['primary_source_url'] for c in corrected),'mapped_rows':len(proof),'quote_verified_rows':sum(x['saved_text_quote_verified'] for x in proof),'unresolved_rows':sum(c['verification_status']=='UNRESOLVED' for c in corrected),'contradicted_rows':len(conflicts),'status_counts':dict(collections.Counter(c['verification_status'] for c in corrected)),'candidate_counts':dict(collections.Counter(c['candidate_id'] for c in corrected)),'duplicate_semantic_claim_groups':duplicates,'generic_claim_rows':0,'max_excerpt_words':max(x['excerpt_words'] for x in proof),'historical_sha256_before':before,'historical_sha256_after':sha(OLD),'corrected_sha256':sha(outpath),'ids_order_and_candidates_preserved':all((r['evidence_id'],r['candidate_id'])==(c['evidence_id'],c['candidate_id']) for r,c in zip(rows,corrected))}
# Read back actual CSV and enforce schema, identity and count.
with outpath.open(encoding='utf-8',newline='') as f:
 reader=csv.DictReader(f); assert reader.fieldnames==FIELDS;back=list(reader)
assert back==corrected and len({c['evidence_id'] for c in back})==202
(HERE/'verification.json').write_text(json.dumps({'method':'Offline ledger-ID and exact historical quote/locator mapping; whitespace/HTML normalization and decoded saved JSON values; manually authored specific propositions; document truth only.','statistics':stats,'row_audit':proof},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=['# WP-03 evidence QC addendum (WP-04 correction)','', '## Scope and invariants','', 'All 202 historical records are retained in original order with their evidence and candidate IDs. The original CSV is untouched. Only the corrected registry, this addendum, and the correction subdirectory are written. No network, dataset payload, image, weight, training, commit or push operations were performed.','', 'Historical SHA-256: `'+before+'`.','', '## Code-derived counts','', '```json',json.dumps(stats,ensure_ascii=False,indent=2),'```','', '## Recovery and classification','', 'Stream A: map C03–C06 to A01–A04, preserve nested evidence order, require candidate/quote/locator equality, then join the nested source_id to source_ledger.json. This recovers missing URLs without inventing them. Stream B: require exact normalized quote, locator and URL equality in claim_evidence.json, then join citation_id to citation_ledger.json. Access logs provide independent HTTP-200 cross-checks; saved originals are linked by their actual repository paths.','', 'Every specific_claim is a manually interpreted proposition, not an ID-prefixed generic excerpt label. The script rejects generic template phrases and duplicate claims unless the original candidate/quote/locator triple is itself identical. Genuine historical duplicates remain visible rather than being fabricated into distinct claims. All original generic claims remain verbatim in original_claim.','', 'SOURCE_FACT_VERIFIED_IN_SAVED_TEXT means a structural/document/advertised-repository fact is present, not that the underlying experiment is true. AUTHOR_REPORTED_NOT_REPRODUCED includes methods, outcomes, interpretations and secondary literature reports; AUTHOR_PROPOSAL_NOT_VALIDATED covers author future-work suggestions (not reviewer evidence). AUTHOR_REPORTED_RESULT_CONTRADICTED identifies explicit within-paper numeric conflicts. UNRESOLVED would require a blank URL when provenance or saved-text support cannot be established. No reviewer-generated performance hypothesis has been upgraded to a source result. Confidence describes document traceability only.','', '## Contradictions and contamination','', 'WP03-E011 conflates ResNet-50 weighted score 99.70% with accuracy, whereas the result text gives 99.66% accuracy. WP03-E012/E015/E017/E018/E019 claim DenseNet-201 accuracy 99.98% despite 99.44% in the results/discussion. These six flags are internal consistency findings, not experimental falsifications. E056 preserves the later discussion value and cross-reference.','', 'E080 and E081 are unrelated web-page recommendation titles. Bibliography rows are identified as citations rather than evidence of dataset use. Captions/headings establish only the content indicated, not new numeric results. SMS3D full-set author-contact restrictions and M18K differing README/paper scope remain explicit, rather than declaring every historical statement false or replacing it with one current count. C03 private-data wording and later Zenodo availability remain version/subset uncertainties, not a fabricated resolved contradiction.','', '## Quote verification and limitations','', 'The full historical quotation is checked against its saved text or decoded JSON string values; matching normalizes only whitespace and HTML entities. Short supporting excerpts are contiguous spans of those checked quotations (at most 35 words). Full original quotations remain in the unchanged historical CSV. Compact quotes may not express every clause of a manually recovered proposition; consult the linked original locator and row audit. For table fragments the corrected locator includes table headers, model/backbone/task/channel context recovered from adjacent saved lines.','', 'No new live retrieval or empirical audit was performed. An HTTP-200 log documents historical retrieval, not current availability. A source statement is not proof of correctness, leakage absence, annotation quality, license compatibility, reproducibility or real-farm transfer. Unique evidence IDs do not imply independent observations.','', '## Reproduction','', '`python 03_dataset_discovery/source_verification/wp04_evidence_correction/correct_registry.py`','', 'Inputs: unchanged historical CSV, claims.txt, both original stream evidence/ledgers/access logs and saved text. Outputs: corrected CSV, this addendum, verification.json (per-row mappings, saved-source hashes, quote checks and counts). The script performs no network calls.']
(ROOT/'03_dataset_discovery/screening_reports/WP-03_EVIDENCE_QC_ADDENDUM.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps(stats,indent=2))
