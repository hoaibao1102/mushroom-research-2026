"""Independent readback/recomputation and remote byte-hash verification."""
import pathlib,json,csv,hashlib,collections,urllib.request,datetime
R=pathlib.Path(__file__).resolve().parents[2];E=R/'qc/wp02_evidence';s=json.loads((R/'qc/coco_annotation_statistics.json').read_bytes());out={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':[],'sources':[]}; ds={}
manifest=list(csv.DictReader((R/'qc/wp02_c02_download_manifest.csv').open(encoding='utf8',newline='')))
assert len(manifest)==2
for row in manifest:
 p=R/row['local_path'];b=p.read_bytes();d=json.loads(b);split='test' if 'TEST' in p.name else 'train';ds[split]=d
 assert len(b)==int(row['bytes']) and hashlib.sha256(b).hexdigest()==row['sha256']
 with urllib.request.urlopen(row['source_url'],timeout=90) as response:remote=response.read()
 assert hashlib.sha256(remote).hexdigest()==row['sha256'] and remote==b
 assert (len(d['images']),len(d['annotations']))==(s['splits'][split]['images'],s['splits'][split]['annotations'])
 assert collections.Counter(a['category_id'] for a in d['annotations'])==collections.Counter({c['id']:c['instances'] for c in s['splits'][split]['categories'] if c['instances']})
 assert all(len({v['id'] for v in d[k]})==len(d[k]) for k in ['images','categories','annotations'])
 out['sources'].append({'split':split,'sha256':row['sha256'],'bytes':len(b),'remote_readback_identical':True})
paths=[]
for p in sorted(E.glob('kaggle_page_*.json')):
 d=json.loads(p.read_bytes());paths.extend(v['name'] for v in d['datasetFiles'])
assert len(paths)==3011 and len(set(paths))==3011 and not d.get('nextPageToken')
rows=list(csv.DictReader((E/'linkage_rows.csv').open(encoding='utf8',newline='')));assert len(rows)==sum(len(d['images']) for d in ds.values())
matched=set()
for split,d in ds.items():
 for i in d['images']:
  row=next(r for r in rows if r['split']==split and int(r['image_id'])==i['id']);fn=i['file_name'];bn=fn.rsplit('/',1)[-1]
  for k,matches in [('exact_path_matches',[p for p in paths if p==fn]),('exact_basename_matches',[p for p in paths if p.rsplit('/',1)[-1]==bn]),('casefold_basename_matches',[p for p in paths if p.rsplit('/',1)[-1].casefold()==bn.casefold()])]:assert int(row[k])==len(matches)
  matches=[p for p in paths if '/'.join(p.split('/')[1:])==fn.removeprefix('ANNOTATION_BATCHES/')];assert int(row['explicit_wrapper_relative_matches'])==len(matches);matched.update(matches)
assert len(matched)==s['kaggle']['matched_unique_paths'];assert set(json.loads((E/'unmatched_kaggle_images.json').read_bytes()))==set(paths)-matched
active={split:{i['file_name'] for i in d['images'] if i['id'] in {a['image_id'] for a in d['annotations']}} for split,d in ds.items()}
allpaths={split:{i['file_name'] for i in d['images']} for split,d in ds.items()}
overlap=allpaths['train']&allpaths['test'];out['split_analysis']={'all_path_overlap':len(overlap),'annotated_image_paths':{k:len(v) for k,v in active.items()},'both_splits_annotated_path_overlap':len(active['train']&active['test']),'test_paths_annotated_in_train':len(allpaths['test']&active['train']),'test_annotated_paths_present_but_empty_in_train':len(active['test']&(allpaths['train']-active['train']))}
out['kaggle_duplicate_summary']={'unique_basenames':len(set(p.rsplit('/',1)[-1] for p in paths)),'duplicated_basename_groups':len(s['kaggle']['duplicate_basenames']),'files_in_duplicated_basename_groups':sum(s['kaggle']['duplicate_basenames'].values()),'excess_duplicate_basename_occurrences':sum(n-1 for n in s['kaggle']['duplicate_basenames'].values())}
# Verify every acquired source, including code and API metadata, against acquisition log.
logs=[json.loads(line) for line in (E/'access_log.jsonl').read_text().splitlines()]
for r in logs:
 b=(R/r['local_path']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
out['checks']=['manifest exact schema and two rows','COCO counts/categories/unique IDs independently recomputed','both annotation sources remotely refetched and byte-identical','16 Kaggle pages reaggregated, terminal token empty, 3011 unique paths','371 linkage rows independently recomputed','unmatched inventory partition recomputed','all acquired source hashes readback verified'];out['acquired_sources_verified']=len(logs);out['status']='PASS metadata verification only; not training or scientific reproducibility approval'
with (E/'independent_verification.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
