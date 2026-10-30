"""Header-validated RAR extraction and image-only QC; never execute bundled code."""
from pathlib import Path,PurePosixPath,PureWindowsPath
import json,csv,hashlib,subprocess,collections,stat,sys,time
import rarfile
from PIL import Image
import PIL,imagehash
C=Path('D:/Capstone/mushroom-research-2026/04_dataset_candidates/C03_agaricus_disease'); E=C/'qc/wp04_evidence'; Q=C/'qc'; f=json.loads((E/'live_record.json').read_bytes())['files'][0]; archive=C/'source'/f['key']
assert archive.stat().st_size==f['size'] and 'md5:'+hashlib.md5(archive.read_bytes()).hexdigest()==f['checksum']
out=C/'source/extracted'; assert not out.exists()
r=rarfile.RarFile(archive); members=[]; seen=set(); total=0
for m in r.infolist():
    n=m.filename.replace('\\','/'); p=PurePosixPath(n); win=PureWindowsPath(n)
    assert not p.is_absolute() and not win.is_absolute() and not win.drive and '..' not in p.parts
    assert all(':' not in x and not x.endswith((' ','.')) and x.split('.')[0].upper() not in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]} for x in p.parts)
    assert not m.is_symlink() and not getattr(m,'file_redir',None) and not m.needs_password()
    key=n.rstrip('/').casefold(); assert key not in seen; seen.add(key)
    total+=m.file_size; assert total<=3000000000
    members.append({'path':n,'size':m.file_size,'is_dir':m.isdir(),'crc':m.CRC})
(Q/'archive_members.json').write_text(json.dumps({'expanded_limit_bytes':3000000000,'declared_expanded_bytes':total,'members':members},indent=2))
# Parent path ignored by existing glob rules for payload extensions; no ignore files changed.
out.mkdir()
cmd=['C:/Windows/System32/tar.exe','-x','-k','-f',str(archive),'-C',str(out)]
p=subprocess.run(cmd,capture_output=True,text=True)
(E/'extraction_log.json').write_text(json.dumps({'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'tool':'Windows bsdtar 3.8.9 libarchive 3.8.9','policy':'Complete header validation; reject traversal/absolute/drive paths, links, encryption, case-fold duplicates, Windows special names; max 3GB; new empty directory; -k no overwrite; no bundled code executed'},indent=2)); assert p.returncode==0
actual={x.relative_to(out).as_posix():x for x in out.rglob('*') if x.is_file()}
expected={m['path']:m['size'] for m in members if not m['is_dir']}
assert set(actual)==set(expected) and all(actual[n].stat().st_size==s for n,s in expected.items())
rows=[]; exact=collections.defaultdict(list); dhashes=[]
for n,p in sorted(actual.items()):
    b=p.read_bytes(); h=hashlib.sha256(b).hexdigest(); exact[h].append(n)
    row={'path':n,'bytes':len(b),'sha256':h,'mtime_ns':p.stat().st_mtime_ns,'extension':p.suffix.lower(),'status':'NON_IMAGE_OR_UNSUPPORTED'}
    try:
        with Image.open(p) as im:
            row.update(format=im.format,width=im.width,height=im.height,mode=im.mode,channels=len(im.getbands()),exif_orientation=im.getexif().get(274),exif_keys=[str(k) for k in im.getexif().keys()]); im.verify()
        with Image.open(p) as im:
            im.load(); row['dhash64']=str(imagehash.dhash(im)); dhashes.append((n,int(row['dhash64'],16)))
        row['status']='DECODE_OK'
    except Exception as ex: row['error']=repr(ex)
    rows.append(row)
    if len(rows)%1000==0: print('decoded',len(rows),flush=True)
(Q/'inventory.json').write_text(json.dumps(rows,indent=2))
groups=[{'sha256':h,'paths':paths} for h,paths in exact.items() if len(paths)>1]
candidates=[]
for i,(a,h) in enumerate(dhashes):
    for b,k in dhashes[i+1:]:
        dist=(h^k).bit_count()
        if dist<=4: candidates.append({'a':a,'b':b,'hamming_distance':dist,'status':'UNVERIFIED_PERCEPTUAL_CANDIDATE'})
(Q/'duplicates.json').write_text(json.dumps({'sha256_duplicate_groups':groups,'perceptual_method':'ImageHash dhash 64-bit grayscale resize; all pairs Hamming <=4; screening threshold not calibrated, not identity or specimen evidence','perceptual_candidates':candidates},indent=2))
summary={'physical_files':len(rows),'image_decode_ok':sum(r['status']=='DECODE_OK' for r in rows),'other_or_error':sum(r['status']!='DECODE_OK' for r in rows),'expanded_bytes':sum(r['bytes'] for r in rows),'extensions':dict(collections.Counter(r['extension'] for r in rows)),'by_parent':dict(collections.Counter(str(PurePosixPath(r['path']).parent) for r in rows)),'dimensions':dict(collections.Counter(f"{r.get('width')}x{r.get('height')}" for r in rows)),'modes':dict(collections.Counter(r.get('mode','UNKNOWN') for r in rows)),'sha256_duplicate_groups':len(groups),'sha256_duplicate_files':sum(len(g['paths']) for g in groups),'perceptual_candidates':len(candidates),'pillow_version':PIL.__version__,'python_version':sys.version}
(Q/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
