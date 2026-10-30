import pathlib,json,collections
R=pathlib.Path(__file__).resolve().parents[2];E=R/'qc/wp02_evidence'
a=json.loads((R/'dataset_metadata/MushR_Dataset_V1.1_2023_04_04-COCO.json').read_bytes());b=json.loads((R/'dataset_metadata/MushR_Dataset_2023_06_29_TEST-COCO.json').read_bytes());paths=[x['name'] for x in json.loads((E/'kaggle_inventory.json').read_bytes())['files']]
def canonical(d):
 im={i['id']:i['file_name'] for i in d['images']};o=collections.Counter()
 for x in d['annotations']:
  x=dict(x);x.pop('id');x['image_id']=im[x['image_id']];o[json.dumps(x,sort_keys=True)]+=1
 return o
out={'identical_annotations_ignoring_local_ids':sum((canonical(a)&canonical(b)).values()),'casefold_exact_path_matches':{s:sum(any(p.casefold()==i['file_name'].casefold() for p in paths) for i in d['images']) for s,d in [('train',a),('test',b)]},'all_required_coco_arrays':{s:all(isinstance(d.get(k),list) for k in ['images','annotations','categories']) for s,d in [('train',a),('test',b)]}}
with (E/'additional_checks.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
