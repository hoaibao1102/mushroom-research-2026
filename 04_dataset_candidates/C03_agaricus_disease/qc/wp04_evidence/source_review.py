"""Preserve compact primary-source review with literal passages and hashes."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,datetime,urllib.request
R=Path('D:/Capstone/mushroom-research-2026'); A=R/'03_dataset_discovery/source_verification/wp03_stream_a'; E=R/'04_dataset_candidates/C03_agaricus_disease/qc/wp04_evidence'
inputs=['candidates.json','paper_agronomy_fulltext.txt','paper_xml_alternate.txt','crossref_agronomy.txt','zenodo_20260929.txt']
prov=[{'path':str((A/n).relative_to(R)),'bytes':(A/n).stat().st_size,'sha256':hashlib.sha256((A/n).read_bytes()).hexdigest()} for n in inputs]
lines=(A/'paper_agronomy_fulltext.txt').read_text(encoding='utf-8').splitlines()
loc=[8,49,51,53,56,58,60,63,72,78,79,85,107,112,120]
claims=[{'source':prov[1]['path'],'line':i,'text':lines[i-1],'status':'PAPER_REPORTED'} for i in loc]
cross=json.loads((A/'crossref_agronomy.txt').read_bytes())['message']
(E/'paper_review.json').write_text(json.dumps({'reviewer':'Hermes WP04 C03 evidence audit','review_scope':'FULL_TEXT_REVIEWED local publisher XML-derived text and Table 2; primary XML parsed for identity','provenance':prov,'paper_doi':cross['DOI'],'paper_title':cross['title'],'paper_authors':cross['author'],'publisher':cross['publisher'],'published':cross.get('published'),'claims':claims,'assessment':{'diagnosis':'Expert mycologists/manual specialist panel explicitly reported; laboratory isolation/culture/PCR confirmation not established by reviewed Methods. Do not upgrade to lab-confirmed ground truth.','sampling':'Multiple angles/stages and farms are author-reported; specimen IDs, exact repeats and biological independence remain unverified.','access_conflict':'Paper Data Availability states not public due privacy/confidentiality. Later author-deposited Zenodo record explicitly open CC-BY-4.0; lawful limited QC under explicit deposit license, not retrospective proof all privacy concerns resolved.','identity':'Deposit says used in paper but white/UV/mixed description differs from 3195-white-light paper; exact equivalence must be measured.'}},indent=2,ensure_ascii=False),encoding='utf-8')
# Metadata-only independent exact-DOI lookup, no other dataset payloads.
url='https://api.datacite.org/dois/10.5281/zenodo.20260929'
try:
    with urllib.request.urlopen(url,timeout=60) as resp: b=resp.read()
    (E/'datacite_exact.json').write_bytes(b)
    d=json.loads(b)['data']['attributes']; print(json.dumps({k:d.get(k) for k in ['doi','publisher','version','dates','rightsList','creators','contributors','titles']},ensure_ascii=False,indent=2))
except Exception as ex: (E/'datacite_error.txt').write_text(repr(ex))
print('paper_review.json written')
