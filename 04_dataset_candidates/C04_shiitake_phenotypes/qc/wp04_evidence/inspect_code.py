"""Download ONLY metadata-listed small code ZIP; statically inspect text, never execute author code."""
from pathlib import Path, PurePosixPath
import json, urllib.request, hashlib, datetime, zipfile, io, csv, re
R=Path(__file__).resolve().parent
j=json.loads((R/'zenodo_record.json').read_text())
assert j['id']==20373531 and j['doi']=='10.5281/zenodo.20373531'
assert j['metadata']['license']['id']=='cc-by-4.0'
f=next(x for x in j['files'] if x['key']=='shiitake_mushroom_code.zip')
assert f['size']==5724836 and f['checksum']=='md5:42aa41b73d6410e76e5c27438a9a2b15'
u=f['links']['self']; assert u=='https://zenodo.org/api/records/20373531/files/shiitake_mushroom_code.zip/content'
t=datetime.datetime.now(datetime.timezone.utc).isoformat()
if (R/f['key']).exists():
 b=(R/f['key']).read_bytes(); status=206; final=json.loads((R/'curl_recovery_log.json').read_text())['url']
else:
 with urllib.request.urlopen(u,timeout=90) as h:
  b=h.read(6_000_001); status=h.status; final=h.url
assert len(b)==f['size'] and 'md5:'+hashlib.md5(b).hexdigest()==f['checksum']
(R/f['key']).write_bytes(b)
log={'url':u,'final_url':final,'retrieved_utc':t,'status':status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest(),'license_basis':'record-level CC-BY-4.0; embedded upstream notices inspected separately','executed_author_code':False}
(R/'code_acquisition.json').write_text(json.dumps(log,indent=2))
inv=[]; texts=[]
with zipfile.ZipFile(io.BytesIO(b)) as z:
 assert sum(x.file_size for x in z.infolist())<100_000_000
 for x in z.infolist():
  p=PurePosixPath(x.filename); safe=not p.is_absolute() and '..' not in p.parts and not (x.external_attr>>16 & 0o170000)==0o120000
  assert safe, x.filename
  inv.append({'path':x.filename,'bytes':x.file_size,'compressed':x.compress_size,'crc32':f'{x.CRC:08x}'})
  # Do not extract archive paths or decode any image, model weight or binary.
  if not x.is_dir() and (p.suffix.lower() in {'.py','.yaml','.yml','.toml','.md','.txt','.cfg','.json','.sh','.bat'} or p.name.lower().startswith(('license','readme','requirements'))):
   if x.file_size<=2_000_000:
    data=z.read(x); text=data.decode('utf-8',errors='replace'); name=f'{len(texts):04d}_{p.name}.txt'; (R/'static_text').mkdir(exist_ok=True); (R/'static_text'/name).write_text(text,encoding='utf-8'); texts.append({'archive_path':x.filename,'local_text':'static_text/'+name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
(R/'archive_inventory.json').write_text(json.dumps(inv,indent=2)); (R/'text_index.json').write_text(json.dumps(texts,indent=2))
print(json.dumps(log,indent=2)); print('ARCHIVE MEMBERS',len(inv),'TEXT MEMBERS',len(texts)); print('\n'.join(str(x) for x in inv))
