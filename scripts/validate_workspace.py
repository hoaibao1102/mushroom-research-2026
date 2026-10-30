"""Validate Team 10 repository structure and research evidence consistency; NOT dataset QC."""
import argparse, csv, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def validate(root):
    results=[]
    def check(ok,msg):results.append((bool(ok),msg))
    req=json.loads((root/'12_reproducibility/manifests/workspace_requirements.json').read_text(encoding='utf8'))
    for d in req['directories']:check((root/d).is_dir(),'Directory: '+d)
    for f in req['files']:check((root/f).is_file(),'Required file: '+f)
    for f,header in req['csv_headers'].items():
        try:
            with (root/f).open(encoding='utf8',newline='') as stream:
                reader=csv.DictReader(stream,strict=True); rows=list(reader)
                check(reader.fieldnames==header,'CSV header: '+f)
                check(all(None not in row and all(v is not None for v in row.values()) for row in rows),'CSV row widths: '+f)
        except (OSError,UnicodeError,csv.Error) as exc:check(False,'CSV unreadable: '+f+' '+str(exc))
    with (root/'03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv').open(encoding='utf8',newline='') as f:
        candidates=list(csv.DictReader(f))
    ids=[r['candidate_id'] for r in candidates]
    check(all(x in ids for x in ['C01','C02','C03']) and len(ids)==len(set(ids)),'Unique C01/C02/C03 candidates')
    check((root/'04_dataset_candidates/C03_m18k_v2/README.md').is_file(),'C03 candidate description')
    state=json.loads((root/'00_project_management/project_state.json').read_text(encoding='utf8'))
    check(state.get('working_candidate_id')=='C03','Working candidate is C03')
    check(not state.get('baseline_reproduced',True),'No unsupported reproduction claim')
    check((root/'09_results/reports/M18K_V2_EDA_2026-10-30.md').is_file(),'EDA report available')
    check((root/'04_dataset_candidates/C03_m18k_v2/analysis/M18K_V2_Research_EDA_Executed_2026-10-30.ipynb').is_file(),'Executed notebook available')
    allowed_images={'09_results/visualizations/m18k_v2_composition.png', '09_results/visualizations/m18k_v2_rgb_depth_pairing.png', '09_results/visualizations/m18k_v2_rgb_depth_examples.png', '09_results/visualizations/m18k_v2_segmentation_examples.png'}
    payload_ext={'.jpg','.jpeg','.png','.webp','.bmp','.npy','.npz','.pt','.pth','.ckpt','.onnx','.zst','.zip','.7z','.tar','.sqlite','.db'}
    unexpected=[]
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if '.git' in rel.parts or '__pycache__' in rel.parts:continue
        if p.is_symlink():unexpected.append('SYMLINK:'+rel.as_posix())
        elif p.is_file() and p.suffix.lower() in payload_ext and rel.as_posix() not in allowed_images:
            unexpected.append(rel.as_posix())
    check(not unexpected,'No unexpected raw/model payloads: '+str(unexpected[:10]))
    return results

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=ROOT)
    root=parser.parse_args().root.resolve()
    try:checks=validate(root)
    except Exception as exc:
        print('FAIL | Validation exception:',exc);return 1
    for ok,description in checks:print(('PASS' if ok else 'FAIL')+' | '+description)
    failed=sum(not ok for ok,_ in checks)
    print(f'\nWorkspace validation: {len(checks)-failed} PASS / {failed} FAIL')
    return 1 if failed else 0
if __name__=='__main__':sys.exit(main())
