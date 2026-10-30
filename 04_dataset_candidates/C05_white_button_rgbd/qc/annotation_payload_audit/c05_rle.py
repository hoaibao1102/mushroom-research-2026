from pathlib import Path
import json,collections
S=Path('C:/Users/MSI PC/AppData/Local/hermes/cache/scratch');j=json.loads((S/'c05_annotations.coco.json').read_bytes());qc=json.loads((S/'c05_qc.json').read_text());ids={x['id']:x for x in j['images']};issues=collections.Counter();examples={}
def issue(k,a):issues[k]+=1;examples.setdefault(k,[]);examples[k]=(examples[k]+[a['id']])[:20]
def counts(s):
 out=[];p=0
 while p<len(s):
  x=0;k=0
  while True:
   c=ord(s[p])-48;p+=1;x|=(c&31)<<(5*k);k+=1
   if not c&32:
    if c&16:x|=-1<<(5*k)
    break
  if len(out)>2:x+=out[-2]
  out.append(x)
 return out
for a in j['annotations']:
 im=ids[a['image_id']];seg=a['segmentation']
 if not isinstance(seg,dict) or not isinstance(seg.get('counts'),str):issue('not_compressed_RLE',a);continue
 try:r=counts(seg['counts'])
 except Exception:issue('RLE_decode_error',a);continue
 if seg.get('size')!=[im['height'],im['width']]:issue('RLE_size_mismatch',a)
 if min(r)<0 or sum(r)!=im['height']*im['width']:issue('RLE_runs_invalid',a)
 if sum(r[1::2])<=0:issue('RLE_empty_mask',a)
 # area is retained as source metadata; compare without repairing it
 if abs(a['area']-sum(r[1::2]))>0.01:issue('area_differs_from_RLE_mask_pixels',a)
qc['rle_qc']={'algorithm':'COCO compressed run-length integer decoding; verify nonnegative runs, run sum, dimensions and foreground','issues':dict(issues),'examples':examples};qc['segmentation_types']=dict(collections.Counter(type(x['segmentation']).__name__ for x in j['annotations']));qc['extra_name_exact_RGB_matches']=sum(x.get('extra',{}).get('name')==l['parent_png'] for x,l in zip(j['images'],qc['links']));qc['date_captured_values']=sorted(set(x['date_captured'] for x in j['images']));qc['bbox_outside_records']=[a for a in j['annotations'] if a['id'] in [25290,25520]]
(S/'c05_qc.json').write_text(json.dumps(qc,indent=2));print(json.dumps({k:qc[k] for k in ['rle_qc','segmentation_types','extra_name_exact_RGB_matches','date_captured_values','bbox_outside_records']},indent=2)[:8000])
