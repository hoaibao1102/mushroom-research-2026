"""Metadata and small text-only primary source retrieval. No assets/training."""
import urllib.request, urllib.error, json, pathlib, datetime, hashlib
BASE=pathlib.Path(__file__).parent
LOG=BASE/'access_log.jsonl'
def fetch(url, dest, cap=2_000_000):
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    record={'access_utc':now,'url':url,'destination':dest}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'WP01-C02-primary-source-audit','Accept':'application/vnd.github+json' if 'api.github.com' in url else 'application/json,text/html;q=0.9,*/*;q=0.1'})
        with urllib.request.urlopen(req,timeout=60) as r:
            data=r.read(cap+1); record.update(status=r.status,content_type=r.headers.get('Content-Type'),final_url=r.url)
        if len(data)>cap: raise ValueError('Response exceeds metadata/text cap')
        p=BASE/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        record.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        return data
    except Exception as e:
        record['error']=str(e); print('ERROR',url,str(e)); return None
    finally:
        with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps(record)+'\n')
if __name__=='__main__':
    for repo in ['MushR','mushr-mask-r-cnn']:
        raw=fetch('https://api.github.com/repos/ETCE-LAB/'+repo,repo+'/repo.json')
        if not raw:continue
        meta=json.loads(raw); branch=meta['default_branch']
        commit=json.loads(fetch(f'https://api.github.com/repos/ETCE-LAB/{repo}/commits/{branch}',repo+'/commit.json'))
        sha=commit['sha']; print(repo,sha)
        tree=json.loads(fetch(f'https://api.github.com/repos/ETCE-LAB/{repo}/git/trees/{sha}?recursive=1',repo+'/tree.json'))
        for obj in tree.get('tree',[]):
            if obj['type']=='blob': print(repo,obj['path'],obj.get('size'))
    for name,url in [('kaggle_view','https://www.kaggle.com/api/v1/datasets/view/etcelab/mushr-annotated-dataset-oyster-mushrooms'),('kaggle_list','https://www.kaggle.com/api/v1/datasets/list?search=mushr'),('kaggle_files','https://www.kaggle.com/api/v1/datasets/list/etcelab/mushr-annotated-dataset-oyster-mushrooms'),('kaggle_page','https://www.kaggle.com/datasets/etcelab/mushr-annotated-dataset-oyster-mushrooms')]:
        data=fetch(url,name+'.json' if name!='kaggle_page' else name+'.html')
        if data: print(name,len(data),data[:120])
