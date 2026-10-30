"""WP02 metadata-only acquisition; never downloads image/model assets."""
import pathlib,json,urllib.request,datetime,hashlib,csv,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[2]; E=ROOT/'qc/wp02_evidence'; M=ROOT/'dataset_metadata'
M.mkdir(parents=True,exist_ok=True)
def fetch(url,p):
    if p.exists(): raise FileExistsError(p)
    ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'WP02-C02-metadata-audit'}),timeout=90) as r:
        b=r.read(40_000_001); ct=r.headers.get('Content-Type'); status=r.status
    if len(b)>40_000_000: raise ValueError('metadata cap exceeded')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    rec=dict(source_url=url,local_path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),download_timestamp=ts,content_type=ct,status=str(status))
    with (E/'access_log.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(rec)+'\n')
    return b,rec
repo='https://api.github.com/repos/ETCE-LAB/mushr-mask-r-cnn'
b,_=fetch(repo+'/commits/HEAD',E/'current_commit.json'); sha=json.loads(b)['sha']
b,_=fetch(repo+'/git/trees/'+sha+'?recursive=1',E/'current_tree.json')
rows=[]
for name,version in [('MushR_Dataset_V1.1_2023_04_04-COCO.json','V1.1_2023_04_04'),('MushR_Dataset_2023_06_29_TEST-COCO.json','2023_06_29_TEST')]:
    b,r=fetch('https://raw.githubusercontent.com/ETCE-LAB/mushr-mask-r-cnn/'+sha+'/'+name,M/name)
    d=json.loads(b);r.update(candidate_id='C02',repository_commit=sha,dataset_version=version,parse_status='valid JSON object' if isinstance(d,dict) else 'unexpected root',notes='Unchanged author bytes; no repair/remapping')
    rows.append(r)
with (ROOT/'qc/wp02_c02_download_manifest.csv').open('x',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames='candidate_id,source_url,repository_commit,dataset_version,local_path,bytes,sha256,download_timestamp,content_type,parse_status,status,notes'.split(','));w.writeheader();w.writerows(rows)
for name in ['README.md','train_net.py','train.sh','continue_training.sh','eval.sh','train_2023_04_04/config.yaml','eval_2023_04_20/config.yaml','eval_2023_07_19_new/config.yaml','inference.py','predictor.py']:
    fetch('https://raw.githubusercontent.com/ETCE-LAB/mushr-mask-r-cnn/'+sha+'/'+name,E/'author_code'/name)
base='https://www.kaggle.com/api/v1/datasets/list/etcelab/mushr-annotated-dataset-oyster-mushrooms'
files=[]; token=None; pages=0; seen=set()
try:
    while True:
        url=base+'?pageSize=200'+('&pageToken='+urllib.parse.quote(token,safe='') if token else '')
        b,_=fetch(url,E/f'kaggle_page_{pages+1:03}.json');d=json.loads(b);pages+=1
        fs=d.get('datasetFiles',d.get('files',[]));files.extend(fs)
        token=d.get('nextPageToken');print('Kaggle',pages,len(fs),bool(token),flush=True)
        if not token:break
        if token in seen:raise ValueError('repeated pagination token')
        seen.add(token)
    if not files:raise ValueError('empty Kaggle inventory')
    inv={'mode':'fresh_paginated_API','access_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':pages,'pagination_complete':True,'files':files}
except Exception as exc:
    old=ROOT.parents[1]/'03_dataset_discovery/source_verification/wp01_c02_code_evidence'
    inv={'mode':'WP01 dated fallback','error':repr(exc),'summary':json.loads((old/'kaggle_inventory_summary.json').read_text()),'files':json.loads((old/'kaggle_files_aggregated.json').read_text())}
(E/'kaggle_inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
print('COMMIT',sha,'manifest',[(r['local_path'],r['bytes']) for r in rows])
