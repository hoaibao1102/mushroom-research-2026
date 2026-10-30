from pathlib import Path
import json,hashlib,collections,re,math
S=Path('C:/Users/MSI PC/AppData/Local/hermes/cache/scratch');p=S/'c05_annotations.coco.json';assert hashlib.sha256(p.read_bytes()).hexdigest()=='58c3ca4d862883d927c495a5357d49a294d5411f0bc816fef5c0eabe72c20ea9'
j=json.loads(p.read_bytes());im=j['images'];an=j['annotations'];cats=j['categories'];rgb=json.loads((S/'c05_bd1a2893-adbe-439e-a449-a294cca108a3.json').read_bytes());exports=json.loads((S/'c05_4d0b0637-572e-405e-8a5a-dfd6ab58d56e.json').read_bytes());ids={x['id']:x for x in im};ci={x['id'] for x in cats};errors=collections.Counter();examples={};counts=collections.Counter(x['image_id'] for x in an)
def err(k,x):errors[k]+=1;examples.setdefault(k,[]);examples[k]= (examples[k]+[x['id']])[:10]
for x in an:
 for k in ['id','image_id','category_id','bbox','area','segmentation','iscrowd']:
  if k not in x:err('missing_'+k,x)
 if x['image_id'] not in ids:err('orphan_image',x);continue
 if x['category_id'] not in ci:err('orphan_category',x)
 b=x.get('bbox',[]);q=ids[x['image_id']]
 if len(b)!=4 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in b):err('invalid_bbox',x)
 elif b[2]<=0 or b[3]<=0:err('nonpositive_bbox',x)
 elif b[0]<0 or b[1]<0 or b[0]+b[2]>q['width']+.01 or b[1]+b[3]>q['height']+.01:err('bbox_outside',x)
 seg=x.get('segmentation');
 if not seg:err('empty_segmentation',x)
 elif isinstance(seg,list):
  if any(len(z)<6 or len(z)%2 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in z) for z in seg):err('invalid_polygon',x)
 if x.get('area',0)<=0:err('nonpositive_area',x)
links=[]
for x in im:
 m=re.fullmatch(r'(\d{6})_cycle(\d+)_RGB_png\.rf\.[a-f0-9]+\.jpg',x['file_name']);parent=f'{m[1]}_cycle{m[2]}_RGB.png' if m else None
 links.append({'image_id':x['id'],'coco_file':x['file_name'],'parent_png':parent,'annotations':counts[x['id']],'date':m[1] if m else None,'cycle':int(m[2]) if m else None})
rnames={x['filename'] for x in rgb};enames={x['filename'] for x in exports if x['filename'].endswith('.jpg')};parents=[x['parent_png'] for x in links]
qc={'images':len(im),'annotations':len(an),'categories':cats,'instances_by_category':dict(collections.Counter(x['category_id'] for x in an)),'annotated_images':sum(counts[x['id']]>0 for x in im),'empty_images':[x['id'] for x in im if not counts[x['id']]],'duplicate_image_ids':len(im)-len(ids),'duplicate_annotation_ids':len(an)-len({x['id'] for x in an}),'duplicate_category_ids':len(cats)-len(ci),'duplicate_filenames':len(im)-len({x['file_name'] for x in im}),'image_keys':sorted(set().union(*(x.keys() for x in im))),'annotation_keys':sorted(set().union(*(x.keys() for x in an))),'dimensions':dict(collections.Counter(f"{x['width']}x{x['height']}" for x in im)),'errors':dict(errors),'error_examples':examples,'RGB_inventory':len(rgb),'export_JPG_inventory':len(enames),'parent_unique':len(set(parents)),'missing_parent_png':sorted(set(parents)-rnames),'unmatched_RGB':sorted(rnames-set(parents)),'missing_export_JPG':sorted({x['file_name'] for x in im}-enames),'dates':dict(collections.Counter(x['date'] for x in links)),'cycle_ranges':{d:[min(x['cycle'] for x in links if x['date']==d),max(x['cycle'] for x in links if x['date']==d)] for d in {x['date'] for x in links}},'links':links,'pixel_equivalence':'NOT_TESTED','biological_independence':'NOT_ESTABLISHED'}
(S/'c05_qc.json').write_text(json.dumps(qc,indent=2));print(json.dumps({k:v for k,v in qc.items() if k!='links'},indent=2));print('example',im[0],an[0]);print('info',j.get('info'))
