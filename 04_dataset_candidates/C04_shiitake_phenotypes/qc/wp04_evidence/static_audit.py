"""Static source evidence only. Never import or execute archived modules."""
from pathlib import Path
import json,re,zipfile,hashlib,datetime,tomllib
R=Path(__file__).resolve().parent
idx=json.loads((R/'text_index.json').read_text()); lookup={x['archive_path']:x for x in idx}
paths={
 'train.py':['YOLO(','model.train','epochs=','single_cls'],
 'ultralytics/nn/tasks.py':['def yaml_model_load','def guess_model_scale','no model scale passed','scale =','scales.keys'],
 'ultralytics/engine/trainer.py':['weight_decay =','nbs','get_model(','pretrained','warmup_momentum','warmup_epochs'],
 'ultralytics/models/yolo/detect/train.py':['def get_model','weights','nc='],
 'ultralytics/models/yolo/detect/val.py':['linspace','iouv','ap_per_class','_process_batch'],
 'ultralytics/data/utils.py':['def verify_image_label','shape[1] == 5','non-normalized','negative label','max_cls','segments'],
 'ultralytics/engine/validator.py':['args.conf','0.001','split'],
 'ultralytics/utils/metrics.py':['def compute_ap','interp','101','def ap_per_class','argmax'],
 'ultralytics/engine/model.py':['def train','pretrained','self.ckpt'],
}
found=[]
for path,terms in paths.items():
 if path not in lookup:continue
 lines=(R/lookup[path]['local_text']).read_text(encoding='utf-8').splitlines(); used=set()
 for i,l in enumerate(lines):
  if any(t in l for t in terms):
   a=max(0,i-3);b=min(len(lines),i+7)
   if i not in used:found.append({'archive_path':path,'line_start':a+1,'line_end':b,'text':'\n'.join(f'{k+1}: {lines[k]}' for k in range(a,b))});used.update(range(a,b))
(R/'static_trace_excerpts.json').write_text(json.dumps(found,indent=2),encoding='utf-8')
selected=['train.py','data.yaml','ultralytics/cfg/datasets/data.yaml','ultralytics/cfg/default.yaml','ultralytics/cfg/models/11/yolo11.yaml','ultralytics/__init__.py','pyproject.toml','LICENSE','predict.py','predict_qt.py']
config='\n\n'.join('## '+p+'\n```text\n'+'\n'.join(f'{i}: {s}' for i,s in enumerate((R/lookup[p]['local_text']).read_text(encoding='utf-8').splitlines(),1))+'\n```' for p in selected)
(R/'config_excerpts.md').write_text('# Verbatim static source excerpts\n\nNo author code was executed. Archive paths and original line numbers follow.\n'+config,encoding='utf-8')
inv=json.loads((R/'archive_inventory.json').read_text())
# Read notebook JSON as text only; never execute cells or load embedded media.
with zipfile.ZipFile(R/'shiitake_mushroom_code.zip') as z:
 nb=json.loads(z.read('cocoshow.ipynb')); cells=[{'cell':i,'source':''.join(c.get('source',[]))} for i,c in enumerate(nb['cells']) if c.get('cell_type')=='code'];(R/'notebook_code_cells.json').write_text(json.dumps(cells,indent=2),encoding='utf-8')
summary={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive_members':len(inv),'text_members':len(idx),'unsafe_paths':0,'author_code_executed':False,'installed_dependencies':False,'training_authorized':'NO','dataset_acquired':False,'archive_training_run_logs':[x['path'] for x in inv if any(s in x['path'] for s in ['args.yaml','results.csv','best.pt','last.pt'])],'top_level_notebook_sources':cells,'dependencies':tomllib.loads((R/lookup['pyproject.toml']['local_text']).read_text(encoding='utf-8'))['project']['dependencies'],'count_arithmetic_only':{'6500_minus_5375':6500-5375,'5375_train_80pct':5375*8//10,'5375_val_20pct':5375*2//10,'1782_minus_1125':1782-(6500-5375)}}
(R/'static_audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2,ensure_ascii=True));print('\n'.join(x['text'] for x in found if x['archive_path'] in ['ultralytics/nn/tasks.py','ultralytics/engine/model.py','ultralytics/models/yolo/detect/train.py']))
