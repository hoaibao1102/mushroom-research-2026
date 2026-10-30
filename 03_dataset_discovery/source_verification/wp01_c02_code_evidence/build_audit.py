import json,csv,pathlib,collections,datetime,ast,subprocess
from collect_sources import BASE
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger=BASE/'citation_ledger.json'
S=pathlib.Path('C:/Users/MSI PC/AppData/Local/hermes/skills/research/grounded-citations/scripts/sources.py')
def cite(url,title):
 r=subprocess.run(['python',str(S),'--ledger',str(ledger),'add',url,'--title',title],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr+r.stdout)
 return r.stdout.strip()
claims=[]; sections=[]; sources={}
def add(cid,text,repo,path,loc,quote,status='VERIFIED_FROM_PRIMARY_SOURCE',confidence='HIGH',notes='Static primary-source audit only; no execution of source code.'):
 if repo:
  sha=json.loads((BASE/repo/'commit.json').read_text())['sha'];url=f'https://github.com/ETCE-LAB/{repo}/blob/{sha}/{path}'; date=json.loads((BASE/repo/'commit.json').read_text())['commit']['committer']['date']; title=repo+'/'+path
  raw=(BASE/repo/'text'/path).read_text(encoding='utf-8')
 else:
  url='https://www.kaggle.com/api/v1/datasets/view/etcelab/mushr-annotated-dataset-oyster-mushrooms';date='2024-11-20T11:14:14.987Z';title='Kaggle MushR annotated dataset metadata';raw=(BASE/'kaggle_view.json').read_text()
 if quote and quote not in raw:raise ValueError((cid,'quote not literal'))
 ref=cite(url,title);sources[url]=ref
 claims.append(dict(claim_id=cid,claim_text=text,candidate_id='C02',source_title=title,source_url_or_doi=url,source_type='AUTHOR_CODE' if repo else 'DATASET_HOST_METADATA',source_publication_update_date=date,access_date=NOW,source_location=loc,evidence_status=status,confidence=confidence,verification_notes=notes))
 sections.append(f'### {cid}\n{text}{ref}\n\n- Status: {status}; confidence: {confidence}.\n- Location: {loc}\n- Notes: {notes}\n'+ ('\nExact excerpt:\n```text\n'+quote+'\n```\n' if quote else ''))
add('C02-CODE-001','The system repository links both the annotated Kaggle dataset and the separate Mask R-CNN implementation.','MushR','README.md','MushR Dataset links','  - [Images annotated for Mask R CNN](https://www.kaggle.com/datasets/etcelab/mushr-annotated-dataset-oyster-mushrooms)\n  - [MushR Mask R CNN](https://github.com/ETCE-LAB/mushr-mask-r-cnn)')
add('C02-CODE-002','MushR repository-level LICENSE is GNU AGPL v3; individual source headers must also be respected.','MushR','LICENSE','LICENSE opening','GNU AFFERO GENERAL PUBLIC LICENSE')
add('C02-CODE-003','MushR application module header explicitly grants AGPL version 3 or later.','MushR','automated-image-capture/mushrimager.py','lines 3-6','#  it under the terms of the GNU Affero General Public License as\n#  published by the Free Software Foundation, either version 3 of the\n#  License, or (at your option) any later version.')
add('C02-CODE-004','Arducam camera module has its own three-clause BSD-style redistribution notice, not an AGPL-only header.','MushR','automated-image-capture/arducam_multicamera.py','lines 3-15','#      * Neither the name of the copyright holder nor the\n#        names of its contributors may be used to endorse or promote products\n#        derived from this software without specific prior written permission.')
add('C02-CODE-005','Mask R-CNN repository-level license is GPL v3, distinct from system repository AGPL and Kaggle CC BY-SA.','mushr-mask-r-cnn','LICENSE','LICENSE opening','GNU GENERAL PUBLIC LICENSE')
add('C02-CODE-006','Model modules contain GPL-3.0-or-later headers; train_net.py, inference.py and predictor.py also retain Facebook copyright notices.','mushr-mask-r-cnn','train_net.py','lines 1-17','# Copyright (c) Facebook, Inc. and its affiliates.\n\n#  Copyright (C) 2022, 2023 Anant Sujatanagarjuna\n\n#  This program is free software: you can redistribute it and/or modify\n#  it under the terms of the GNU General Public License as\n#  published by the Free Software Foundation, either version 3 of the\n#  License, or (at your option) any later version.')
add('C02-CODE-007','README delegates dependency installation to Detectron2 official latest instructions; no pinned runtime environment is supplied in the complete repository tree.','mushr-mask-r-cnn','README.md','Dependencies','To run inference, please follow the official instructions to [install\ndetectron2](https://detectron2.readthedocs.io/en/latest/tutorials/install.html).',notes='Complete tree.json checked: no requirements file, environment.yml, pyproject.toml, setup.py or Dockerfile; no Detectron2/PyTorch/CUDA/Python pin located. Compatibility with a current environment is UNVERIFIED; no install or execution attempted.')
add('C02-CODE-008','Code uses Detectron2 DefaultTrainer and COCO instance registration and evaluation.','mushr-mask-r-cnn','train_net.py','lines 40-58,80-81,101','        evaluator_list.append(COCOEvaluator(dataset_name, output_dir=output_folder))')
add('C02-CODE-009','README designates separate COCO JSON files for training and testing; annotation payloads and actual image membership were not audited.','mushr-mask-r-cnn','README.md','Annotations','1. Train: [MushR_Dataset_V1.1_2023_04_04-COCO.json](MushR_Dataset_V1.1_2023_04_04-COCO.json)\n2. Test: [MushR_Dataset_2023_06_29_TEST-COCO.json](MushR_Dataset_2023_06_29_TEST-COCO.json)',notes='Tree metadata confirms JSON blobs of 7,337,338 and 1,064,392 bytes; neither downloaded. Counts, category IDs, annotation validity, leakage and split proportions remain unknown.')
add('C02-CODE-010','Training entry point explicitly declares FOUR classes: Pinning, Not-Ready, Ready, Overdue; assuming exactly the three requested maturity classes is contradicted by this source declaration.','mushr-mask-r-cnn','train_net.py','lines 175-188','    MetadataCatalog.get("MushR_Dataset_V1.1").thing_classes = ["Pinning",\n                                                                "Not-Ready",\n                                                                "Ready",\n                                                                "Overdue"]',notes='This is a code metadata declaration, not validation of annotation category contents. No three-class remapping protocol found in the training entry point.')
add('C02-CODE-011','Both COCO registrations hardcode image root /home/sho/Desktop; portable reproduction needs path adaptation.','mushr-mask-r-cnn','train_net.py','lines 175-184','    register_coco_instances("MushR_Dataset_V1.1", {},\n                            "MushR_Dataset_V1.1_2023_04_04-COCO.json",\n                            "/home/sho/Desktop")')
add('C02-CODE-012','train.sh requests one GPU, upstream Mask R-CNN R50-FPN 3x config, crop enabled, 40,000 iterations, batch 8 and learning rate 0.0001.','mushr-mask-r-cnn','train.sh','full script',(BASE/'mushr-mask-r-cnn/text/train.sh').read_text())
add('C02-CODE-013','continue_training.sh differs: one million iterations, checkpoint period 1,000, batch 8 and learning rate 0.001, with a local checkpoint path.','mushr-mask-r-cnn','continue_training.sh','full script',(BASE/'mushr-mask-r-cnn/text/continue_training.sh').read_text(),notes='Script does not pass --resume despite its name; actual optimizer/scheduler continuation semantics were not executed or verified.')
add('C02-CODE-014','Saved training YAML differs from shell overrides: crop false, batch 2, LR 0.00025, empty test list, seed -1, and ROI_HEADS.NUM_CLASSES 80 rather than declared four.','mushr-mask-r-cnn','train_2023_04_04/config.yaml','INPUT.CROP,DATASETS,MODEL.ROI_HEADS,SOLVER,SEED','    NUM_CLASSES: 80',notes='All saved YAMLs retain ROI_HEADS.NUM_CLASSES 80. Current train.sh does not override NUM_CLASSES. This is a static configuration mismatch, not a demonstrated runtime failure or result invalidity.')
add('C02-CODE-015','Saved training configuration describes CUDA Mask R-CNN with ResNet-50/FPN, polygon masks, BGR input, horizontal flip, train shortest-edge choices 640..800 and max edge 1333.','mushr-mask-r-cnn','train_2023_04_04/config.yaml','MODEL, INPUT','  MASK_FORMAT: polygon')
add('C02-CODE-016','eval.sh uses --eval-only and the named test COCO dataset; COCOEvaluator is the selected evaluation path.','mushr-mask-r-cnn','eval.sh','full script',(BASE/'mushr-mask-r-cnn/text/eval.sh').read_text(),notes='No metrics reproduced, and result/log/prediction payloads not fetched. Saved July eval YAML references train_old/model_final.pth, unlike eval.sh checkpoint construction.')
add('C02-CODE-017','README evaluation-result link points to eval_2023_07_19, whereas the pinned tree contains eval_2023_07_19_new; inference scripts reference absent train_2023_04_20 directory.','mushr-mask-r-cnn','README.md','Evaluation','Our evaluation results of the trained model are given in [eval_2023_07_19](eval_2023_07_19).',notes='Verified against complete pinned tree.json and saved inference shell scripts. No attempt to repair or run author code.')
add('C02-KAGGLE-001','Kaggle public metadata reports version 1, CC BY-SA 4.0, last updated 2024-11-20T11:14:14.987Z and total size 7,898,278,464 bytes.',None,None,'currentVersionNumber,licenseName,lastUpdated,totalBytes','"licenseName":"CC BY-SA 4.0"')
add('C02-KAGGLE-002','Kaggle description reports 34,400 images accumulated over ten months; this is a raw collection claim, not the annotated-host file count.',None,None,'description','We captured and accumulated 34,400 images over ten months to ensure a comprehensive dataset.',status='REPORTED_BY_SOURCE_NOT_AUDITED',notes='No raw-image dataset or image contents downloaded. The annotated dataset listing contains 3,011 JPG entries, not 34,400.')
# File inventory derived solely from completed public metadata pages.
fdata=json.loads((BASE/'kaggle_files_aggregated.json').read_text());fs=fdata['files'];names=[f['name'] for f in fs]
assert fdata['pagination_complete'] and len(names)==len(set(names))
summary={'access_utc':NOW,'pages':fdata['pages'],'pagination_complete':True,'listed_files':len(fs),'unique_paths':len(set(names)),'total_bytes':sum(f['totalBytes'] for f in fs),'extension_counts':dict(collections.Counter(pathlib.Path(n).suffix.lower() for n in names)),'top_level_counts':dict(collections.Counter(n.split('/')[0] for n in names)),'non_image_files':[n for n in names if pathlib.Path(n).suffix.lower() not in ['.jpg','.jpeg','.png']]}
(BASE/'kaggle_inventory_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
url='https://www.kaggle.com/api/v1/datasets/list/etcelab/mushr-annotated-dataset-oyster-mushrooms';ref=cite(url,'Kaggle complete paginated file metadata')
claims.append(dict(claim_id='C02-KAGGLE-003',claim_text='Complete 16-page metadata inventory contains 3,011 unique JPG paths, no annotation JSON, totaling 7,898,278,464 bytes; top-level counts Filtered_2.A=1096, Filtered_2.B=1159, Filtered_2.C=756.',candidate_id='C02',source_title='Kaggle complete paginated file metadata',source_url_or_doi=url,source_type='DATASET_HOST_METADATA',source_publication_update_date='2024-11-20T11:14:14.987Z',access_date=NOW,source_location='kaggle_files.json + kaggle_files_page_002..016.json; kaggle_files_aggregated.json',evidence_status='VERIFIED_FROM_PRIMARY_SOURCE',confidence='HIGH',verification_notes='Names/counts/bytes only; final pagination token empty; sum matches dataset totalBytes exactly. Annotation content, class counts and split membership unknown. No annotation files in exposed listing despite dataset title/description.'))
sections.append('### C02-KAGGLE-003\n'+claims[-1]['claim_text']+ref+'\n\nComputed from primary API metadata, not image or annotation content. The listing has no explicit train/test path split. Folder names A/B/C cannot establish maturity classes or independence.\n\n```json\n'+json.dumps(summary,indent=2)+'\n```\n')
releases=json.loads((BASE/'mushr-mask-r-cnn/releases.json').read_text());weights=[]
for r in releases:
 for a in r['assets']:weights.append({'tag':r['tag_name'],'prerelease':r['prerelease'],'published_at':r['published_at'],'name':a['name'],'size':a['size'],'url':a['browser_download_url']})
(BASE/'published_weight_links.json').write_text(json.dumps(weights,indent=2),encoding='utf-8')
url='https://api.github.com/repos/ETCE-LAB/mushr-mask-r-cnn/releases';ref=cite(url,'Author model release metadata')
sections.append('### Published model asset metadata\nRelease metadata only; no weight/archive fetched.'+ref+'\n\n```json\n'+json.dumps(weights,indent=2)+'\n```\nArchive contents, weight architecture, trained category mapping and checkpoint/config match are UNVERIFIED.\n')
claims.append(dict(claim_id='C02-CODE-018',claim_text='Author release p1 is marked prerelease and publishes mushr-mask-r-cnn-release.tar.gz; metadata and download URL recorded without fetching archive.',candidate_id='C02',source_title='Author model release metadata',source_url_or_doi=url,source_type='AUTHOR_RELEASE_METADATA',source_publication_update_date=releases[0]['published_at'],access_date=NOW,source_location='releases.json assets; published_weight_links.json',evidence_status='VERIFIED_FROM_PRIMARY_SOURCE',confidence='HIGH',verification_notes='No weight contents audited.'))
# Static import and module-header inventories, no project imports/execution.
imports={};headers={}
for repo in ['MushR','mushr-mask-r-cnn']:
 for p in (BASE/repo/'text').rglob('*'):
  if p.is_file() and p.suffix in ['.py','.sh']:
   text=p.read_text(encoding='utf-8');key=str(p.relative_to(BASE));headers[key]='\n'.join(text.splitlines()[:32])
   if p.suffix=='.py':
    imports[key]=[line for line in text.splitlines() if line.startswith(('import ','from '))]
(BASE/'static_imports.json').write_text(json.dumps(imports,indent=2),encoding='utf-8')
(BASE/'module_headers.json').write_text(json.dumps(headers,indent=2),encoding='utf-8')
with (BASE/'claims.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(claims[0]));w.writeheader();w.writerows(claims)
head='''# WP-01 C02: author code and Kaggle metadata audit

## Scope and decision boundary
Primary-source static audit only. No research selection, implementation, model execution, training, scientific-result verification, image/archive/weight download or annotation payload retrieval. Source snapshots are evidence, not an installed implementation. No login or credentials used. No shared registry/state/git edits made.

## Pinned source revisions
'''
for repo in ['MushR','mushr-mask-r-cnn']:
 c=json.loads((BASE/repo/'commit.json').read_text());t=json.loads((BASE/repo/'tree.json').read_text());assert not t.get('truncated')
 head+=f"- {repo}: `{c['sha']}`; commit time {c['commit']['committer']['date']}; full untruncated tree saved.\n"
head+='''
## Main outcomes
- Code declares **four** classes including Pinning, not only the three expected maturity names; actual COCO categories remain uninspected.
- Kaggle version 1 public listing is fully enumerated: **3,011 JPG files and no annotation JSON**. Listing bytes equal dataset metadata bytes. Calling this a verified annotation package would overstate available evidence.
- Licensing differs: system AGPL-3.0, model GPL-3.0, dataset-host CC BY-SA 4.0; some source files have third-party notices. These are observed notices, not a legal opinion or full third-party license-clearance audit.
- Detectron2/PyTorch-based implementation is identifiable but environment/version compatibility is **unverified**. No dependency install or runtime check was performed; any current Detectron2 compatibility statement would be an estimate.
- Shell scripts and saved YAMLs disagree; local paths, missing referenced folders, 80-vs-four class settings and unspecified runtime versions prevent claiming turnkey reproducibility from this static audit.

## Dependencies / environment
See `static_imports.json` for all source imports and `module_headers.json` for each retrieved Python/shell header. Model code directly imports Detectron2, torch, OpenCV (`cv2`), NumPy, tqdm and scikit-learn; stdlib and local predictor/flush_predictor imports are also recorded. Hardware system code uses Raspberry Pi/GPIO/I2C and Adafruit interfaces; it is not the detector training runtime. Complete pinned repository trees expose no requirements/environment/lock/build container manifests. README links latest Detectron2 installation guidance without pinning Python, torch, CUDA or Detectron2. No compatibility certification is possible here.

## Split and data limitations
Train and test JSON filenames are explicit, but payloads were deliberately not fetched. No annotation-level counts, per-class counts, validation split, split ratio, seed-governed partition generator, camera/time/group independence or leakage audit is claimed. Kaggle directories alone do not establish any of those. Metadata inventory and source category declarations are different evidence layers.

## Primary-source claims and exact excerpts
'''
report=head+'\n'.join(sections)
(BASE/'findings.md').write_text(report,encoding='utf-8')
r=subprocess.run(['python',str(S),'--ledger',str(ledger),'render','--cited-in',str(BASE/'findings.md')],capture_output=True,text=True)
if r.returncode:raise RuntimeError(r.stdout+r.stderr)
with (BASE/'findings.md').open('a',encoding='utf-8') as f:f.write('\n'+r.stdout)
r=subprocess.run(['python',str(S),'--ledger',str(ledger),'verify',str(BASE/'findings.md'),'--strict'],capture_output=True,text=True)
(BASE/'citation_verification.txt').write_text(r.stdout+r.stderr,encoding='utf-8')
print('claims',len(claims),'inventory',summary,'weights',weights,'citation verification',r.returncode,r.stdout,r.stderr)
if r.returncode:raise RuntimeError('Citation verification failed')
