"""Static COCO and path audit. No imports/execution of author code."""
import json,pathlib,collections as C,math,csv,hashlib,re,datetime
R=pathlib.Path(__file__).resolve().parents[2]; E=R/'qc/wp02_evidence'
def dump(p,d):
    with p.open('x',encoding='utf8') as f:json.dump(d,f,indent=2)
def counter(x):return dict(C.Counter(x))
def dup(x):return {str(k):v for k,v in C.Counter(x).items() if v>1}
def numeric(x):return isinstance(x,(float,int)) and not isinstance(x,bool) and math.isfinite(x)
datasets={s:json.loads((R/'dataset_metadata'/n).read_bytes()) for s,n in [('train','MushR_Dataset_V1.1_2023_04_04-COCO.json'),('test','MushR_Dataset_2023_06_29_TEST-COCO.json')]}
stats={}; issues=[]; patterns=[]
for split,d in datasets.items():
    im={i['id']:i for i in d['images']}; cats={c['id']:c['name'] for c in d['categories']}; counts=C.Counter(a['category_id'] for a in d['annotations']); flags=C.Counter(); segtypes=C.Counter(); areas=[]; boxrat=[]; polyareas=[]
    def issue(kind,aid,detail=''):
        flags[kind]+=1; issues.append(dict(split=split,kind=kind,id=aid,detail=detail))
    for group in ['images','annotations','categories']:
        for k,v in dup([a.get('id') for a in d[group]]).items():issue('duplicate_'+group+'_id',k,str(v))
    for i in d['images']:
        if not all(isinstance(i.get(k),int) and i[k]>0 for k in ['width','height']):issue('invalid_dimensions',i['id'])
        fn=i['file_name']; m=re.fullmatch(r'(\d{8})_(\d{6})\.jpg',pathlib.PurePosixPath(fn).name,re.I)
        dt=None
        if m:
            try:dt=datetime.datetime.strptime(''.join(m.groups()),'%Y%m%d%H%M%S').isoformat()
            except ValueError:issue('invalid_filename_datetime',i['id'])
        patterns.append(dict(split=split,image_id=i['id'],file_name=fn,filename_datetime_no_timezone=dt,camera_or_group_path=str(pathlib.PurePosixPath(fn).parent),date_captured=i.get('date_captured')))
    for a in d['annotations']:
        aid=a['id']; image=im.get(a.get('image_id'))
        if image is None:issue('orphan_image_ref',aid)
        if a.get('category_id') not in cats:issue('orphan_category_ref',aid)
        if a.get('iscrowd') not in (0,1):issue('invalid_iscrowd',aid)
        if 'is_crowd' in a and a['is_crowd']!=a.get('iscrowd'):issue('crowd_alias_disagreement',aid)
        area=a.get('area'); b=a.get('bbox'); seg=a.get('segmentation'); validbox=isinstance(b,list) and len(b)==4 and all(numeric(v) for v in b)
        if not validbox:issue('invalid_bbox',aid)
        else:
            x,y,w,h=b
            if w<=0 or h<=0:issue('nonpositive_bbox',aid)
            if image and (x<0 or y<0 or x+w>image['width']+1e-6 or y+h>image['height']+1e-6):issue('bbox_outside_image',aid)
        if not numeric(area) or area<=0:issue('invalid_area',aid)
        else:
            areas.append(area)
            if validbox and b[2]*b[3]>0:
                boxrat.append(area/(b[2]*b[3]))
                if area>b[2]*b[3]+1:issue('area_exceeds_bbox',aid)
        if isinstance(seg,list):
            segtypes['polygons']+=1; total=0; xs=[];ys=[]
            if not seg:issue('empty_segmentation',aid)
            for p in seg:
                if not isinstance(p,list) or len(p)<6 or len(p)%2 or not all(numeric(v) for v in p):issue('invalid_polygon',aid);continue
                xx=p[::2]; yy=p[1::2];xs+=xx;ys+=yy
                pa=abs(sum(xx[j]*yy[(j+1)%len(xx)]-xx[(j+1)%len(xx)]*yy[j] for j in range(len(xx))))/2;total+=pa
                if pa<=0:issue('zero_shoelace_polygon',aid)
                if image and any(x<0 or y<0 or x>image['width'] or y>image['height'] for x,y in zip(xx,yy)):issue('polygon_outside_image',aid)
            if xs and validbox and any(abs(v-z)>0.11 for v,z in zip([min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)],b)):issue('bbox_polygon_extent_difference_gt_0.11px',aid)
            if numeric(area):
                delta=area-total;polyareas.append(abs(delta))
                if abs(delta)>max(1,area*0.01):issue('area_shoelace_difference_gt_1pct_or_1px',aid,str(delta))
        elif isinstance(seg,dict):
            segtypes['RLE']+=1
            if not isinstance(seg.get('counts'),(list,str)) or not isinstance(seg.get('size'),list) or len(seg['size'])!=2:issue('invalid_RLE_structure',aid)
            elif image and seg['size']!=[image['height'],image['width']]:issue('RLE_dimension_mismatch',aid)
        else:segtypes['invalid']+=1;issue('invalid_segmentation_type',aid)
        attr=a.get('attributes',{}).get('FruitingState')
        if attr is not None and attr!=cats.get(a.get('category_id')):issue('attribute_class_disagreement',aid,str(attr))
    used=set(a['image_id'] for a in d['annotations'])
    stats[split]=dict(images=len(d['images']),annotations=len(d['annotations']),categories=[dict(id=k,name=v,instances=counts[k]) for k,v in cats.items()],unique_ids={k:len(set(x['id'] for x in d[k])) for k in ['images','annotations','categories']},duplicate_filenames=dup([x['file_name'] for x in d['images']]),dimensions=counter(f"{x['width']}x{x['height']}" for x in d['images']),images_without_annotations=len(set(im)-used),segmentation_types=dict(segtypes),iscrowd=counter(str(a.get('iscrowd')) for a in d['annotations']),issues=dict(flags),area_range=[min(areas),max(areas)],max_abs_polygon_shoelace_area_difference=max(polyareas,default=None),date_captured=counter(str(i.get('date_captured')) for i in d['images']))
inv=json.loads((E/'kaggle_inventory.json').read_text()); files=inv['files']; paths=[f['name'] for f in files]; exact=C.defaultdict(list);base=C.defaultdict(list);fold=C.defaultdict(list); suffix=C.defaultdict(list)
for p in paths:
    exact[p].append(p);base[pathlib.PurePosixPath(p).name].append(p);fold[pathlib.PurePosixPath(p).name.casefold()].append(p)
    parts=p.split('/'); suffix['/'.join(parts[1:]) if len(parts)>1 and parts[0]==parts[1] else p].append(p)
rows=[]; matched=set(); linkage={}
for split,d in datasets.items():
    for i in d['images']:
        p=i['file_name']; bn=pathlib.PurePosixPath(p).name; relative=p.removeprefix('ANNOTATION_BATCHES/'); e=exact[p]; b=base[bn];cf=fold[bn.casefold()];s=suffix[relative]
        if len(s)==1:matched.add(s[0])
        rows.append(dict(split=split,image_id=i['id'],annotation_path=p,exact_path_matches=len(e),exact_basename_matches=len(b),casefold_basename_matches=len(cf),explicit_wrapper_relative_matches=len(s),matched_paths=' | '.join(cf),explicit_relative_paths=' | '.join(s)))
    rs=[r for r in rows if r['split']==split]
    linkage[split]={k:dict(unique=sum(r[k]==1 for r in rs),missing=sum(r[k]==0 for r in rs),ambiguous=sum(r[k]>1 for r in rs)) for k in ['exact_path_matches','exact_basename_matches','casefold_basename_matches','explicit_wrapper_relative_matches']}
with (E/'linkage_rows.csv').open('x',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
dump(E/'annotation_issues.json',issues);dump(E/'filename_timestamp_patterns.json',patterns)
unmatched=[p for p in paths if p not in matched]; dump(E/'unmatched_kaggle_images.json',unmatched)
def overlap(key,transform=lambda x:x):
    return sorted(set(transform(i[key]) for i in datasets['train']['images'])&set(transform(i[key]) for i in datasets['test']['images']))
overlaps={'image_ids':overlap('id'),'annotation_ids':sorted(set(a['id'] for a in datasets['train']['annotations'])&set(a['id'] for a in datasets['test']['annotations'])),'exact_paths':overlap('file_name'),'basenames':overlap('file_name',lambda p:pathlib.PurePosixPath(p).name),'casefold_basenames':overlap('file_name',lambda p:pathlib.PurePosixPath(p).name.casefold())}
dump(E/'split_overlaps.json',overlaps)
pattern_summary={}
for s in datasets:
    pp=[p for p in patterns if p['split']==s];dates=[p['filename_datetime_no_timezone'] for p in pp if p['filename_datetime_no_timezone']]
    pattern_summary[s]={'parsed_filename_datetimes':len(dates),'range':[min(dates),max(dates)],'group_paths':counter(p['camera_or_group_path'] for p in pp)}
summary=dict(repository_commit=json.loads((E/'current_commit.json').read_text())['sha'],scope='Metadata/static only; no image decoding, training, author-code execution or repair',splits=stats,kaggle=dict(mode=inv['mode'],access_utc=inv.get('access_utc'),pages=inv.get('pages'),pagination_complete=inv.get('pagination_complete'),files=len(paths),unique_paths=len(set(paths)),duplicate_paths=dup(paths),duplicate_basenames=dup([pathlib.PurePosixPath(p).name for p in paths]),duplicate_casefold_basenames=dup([pathlib.PurePosixPath(p).name.casefold() for p in paths]),matched_unique_paths=len(matched),unmatched_images=len(unmatched),linkage=linkage),overlap_counts={k:len(v) for k,v in overlaps.items()},timestamp_patterns=pattern_summary)
dump(R/'qc/coco_annotation_statistics.json',summary)
# Line-addressed static excerpts, retaining complete originals separately.
excerpts={}
for p in (E/'author_code').rglob('*'):
    if p.is_file():excerpts[p.relative_to(E/'author_code').as_posix()]=[f'{n}: {line}' for n,line in enumerate(p.read_text().splitlines(),1) if any(k in line for k in ['NUM_CLASSES','WEIGHTS:','MASK_ON','MAX_ITER','BASE_LR','IMS_PER_BATCH','MushR','OUTPUT_DIR','register_coco_instances','thing_classes','/home/sho','config-file','last_checkpoint','INPUT.CROP','install','detectron2'])]
dump(E/'static_code_excerpts.json',excerpts)
print(json.dumps(summary,indent=2));print('STATIC',json.dumps(excerpts,indent=2))
