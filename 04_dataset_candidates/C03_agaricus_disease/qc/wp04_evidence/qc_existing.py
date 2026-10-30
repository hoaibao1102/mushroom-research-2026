"""QC existing safe extraction; checkpoint every 250 files; originals untouched."""
from pathlib import Path
import json,hashlib,collections,sys,datetime,itertools
from PIL import Image
import PIL,imagehash
C=Path('D:/Capstone/mushroom-research-2026/04_dataset_candidates/C03_agaricus_disease'); Q=C/'qc'; E=Q/'wp04_evidence'; out=C/'source/extracted'
expected={m['path']:m['size'] for m in json.loads((Q/'archive_members.json').read_text())['members'] if not m['is_dir']}; files={p.relative_to(out).as_posix():p for p in out.rglob('*') if p.is_file()}
assert set(expected)==set(files) and all(files[n].stat().st_size==s for n,s in expected.items())
rows=[]; partial=Q/'inventory.jsonl'; assert not partial.exists()
with partial.open('x',encoding='utf-8') as log:
 for n,p in sorted(files.items()):
    b=p.read_bytes(); h=hashlib.sha256(b).hexdigest(); parts=n.split('/'); row={'path':n,'bytes':len(b),'mtime_ns':p.stat().st_mtime_ns,'extension':p.suffix.lower(),'sha256':h,'illumination_folder':parts[1],'class_folder':parts[2],'status':'NON_IMAGE_OR_UNSUPPORTED'}
    if p.suffix.lower() in {'.jpg','.jpeg','.png','.bmp','.tiff','.tif'}:
     try:
        with Image.open(p) as im:
            row.update(format=im.format,width=im.width,height=im.height,mode=im.mode,channels=len(im.getbands()),exif_orientation=im.getexif().get(274),exif_keys=[str(k) for k in im.getexif().keys()]); im.verify()
        with Image.open(p) as im:
            im.load(); row['dhash64']=str(imagehash.dhash(im))
        row['status']='DECODE_OK'
     except Exception as ex: row['status']='DECODE_ERROR'; row['error']=repr(ex)
    rows.append(row); log.write(json.dumps(row)+'\n')
    if len(rows)%250==0: log.flush(); print('files',len(rows),flush=True)
(Q/'inventory.json').write_text(json.dumps(rows,indent=2))
exact=collections.defaultdict(list); hashes=[]
for row in rows:
 exact[row['sha256']].append(row['path'])
 if row.get('dhash64'): hashes.append((row['path'],int(row['dhash64'],16)))
groups=[{'sha256':h,'paths':p} for h,p in exact.items() if len(p)>1]
candidates=[]
for i,(a,h) in enumerate(hashes):
 for b,k in hashes[i+1:]:
  d=(h^k).bit_count()
  if d<=4: candidates.append({'a':a,'b':b,'hamming_distance':d,'status':'UNVERIFIED_PERCEPTUAL_CANDIDATE'})
(Q/'duplicates.json').write_text(json.dumps({'sha256_duplicate_groups':groups,'perceptual_method':'ImageHash dhash 64-bit, all pairs Hamming <=4; heuristic uncalibrated screening, not confirmed specimen identity','perceptual_candidates':candidates},indent=2))
images=[r for r in rows if r['status']=='DECODE_OK']
summary={'physical_files':len(rows),'image_decode_ok':len(images),'non_images':[r['path'] for r in rows if r['status']=='NON_IMAGE_OR_UNSUPPORTED'],'decode_errors':[r for r in rows if r['status']=='DECODE_ERROR'],'expanded_bytes':sum(r['bytes'] for r in rows),'extensions':dict(collections.Counter(r['extension'] for r in rows)),'by_light_class':dict(collections.Counter(r['illumination_folder']+'/'+r['class_folder'] for r in images)),'by_light':dict(collections.Counter(r['illumination_folder'] for r in images)),'dimensions':dict(collections.Counter(f"{r['width']}x{r['height']}" for r in images)),'modes':dict(collections.Counter(r['mode'] for r in images)),'exif_keys':dict(collections.Counter(k for r in images for k in r['exif_keys'])),'sha256_duplicate_groups':len(groups),'sha256_duplicate_files':sum(len(g['paths']) for g in groups),'perceptual_candidates':len(candidates),'pillow':PIL.__version__,'python':sys.version,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(Q/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
