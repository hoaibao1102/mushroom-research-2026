"""Validate Team 10 repo structure and Day 1–3 result consistency; not dataset QC."""
import argparse, csv, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def validate(root):
    checks=[]
    def check(cond,msg): checks.append((bool(cond),msg))
    req=json.loads((root/'12_reproducibility/manifests/workspace_requirements.json').read_text(encoding='utf8'))
    for d in req['directories']: check((root/d).is_dir(),'Directory: '+d)
    for f in req['files']: check((root/f).is_file(),'Required file: '+f)
    for f,fields in req['csv_headers'].items():
        try:
            with (root/f).open(newline='',encoding='utf-8-sig') as src:
                reader=csv.DictReader(src,strict=True); rows=list(reader)
                check(reader.fieldnames==fields,'CSV header: '+f)
                check(all(None not in r and all(v is not None for v in r.values()) for r in rows),'CSV row widths: '+f)
        except (OSError,UnicodeError,csv.Error) as exc:check(False,'CSV unreadable '+f+': '+str(exc))
    with (root/'03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv').open(newline='',encoding='utf-8') as f:
        ids=[r['candidate_id'] for r in csv.DictReader(f)]
    check(all(x in ids for x in ('C01','C02','C03')) and len(set(ids))==len(ids),'C01/C02/C03 candidates unique')
    state=json.loads((root/'00_project_management/project_state.json').read_text(encoding='utf-8'))
    check(state.get('working_candidate_id')=='C03','M18K V2 working candidate')
    check(state.get('dataset_eda_executed') is True,'Day 1 EDA recorded')
    check(state.get('baseline_reproduced') is True and state.get('exact_original_benchmark_reproduced') is False,'Day 2 reproduction on V2, not exact paper numerical benchmark')
    check(state.get('day3_area_sample_images')==30 and state.get('day3_qualitative_sample_images')==12,'Day 3 sample sizes recorded')
    check(state.get('dataset_selected') is False,'No invented official dataset selection approval')
    check((root/'09_results/reports/M18K_V2_EDA_2026-10-30.md').is_file(),'Day 1 EDA evidence')
    check((root/'09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md').is_file(),'Day 2 test report')
    check((root/'09_results/reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md').is_file(),'Day 3 sample report')
    try:
        a=json.loads((root/'09_results/metrics/Day2_Two_Class_Heldout_Test_2026-11-02.json').read_text())
        b=json.loads((root/'09_results/metrics/Day2_WB_Only_Heldout_Test_2026-11-02.json').read_text())
        area=json.loads((root/'09_results/area_evaluation/mask_area_summary.json').read_text())
        check(a['test_images']==b['test_images']==450 and a['test_instances_total']==70289 and b['test_instances_WB']==70192,'Day 2 test counts agree with source')
        check(abs(a['all']['mask_map50_95']-0.396273)<1e-6 and abs(b['mask_map50_95']-0.7973628392154766)<1e-8,'Day 2 mask metrics match supplied evidence')
        check(area['sample_size_images']==30 and area['matched']==4900 and area['unmatched_predictions']==246 and area['unmatched_gt']==70,'Day 3 area counts consistent')
        with (root/'09_results/wb_error_analysis/Khang_error_observations_REVIEWED.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        check(len(rows)==12 and sum(int(r['missed_instances_iou50']) for r in rows)==42 and sum(int(r['extra_instances_iou50']) for r in rows)==94,'Day 3 qualitative sample counts consistent')
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:check(False,'Metrics validation failed: '+str(exc))
    figures=list((root/'10_research_paper/figures').glob('Day3_*.png'))
    check(len(figures)==16,'16 original Day 3 figures are available (12 prediction, 4 area)')
    excluded_ext={'.jpg','.jpeg','.png','.webp','.bmp','.npy','.npz','.pt','.pth','.ckpt','.onnx','.zst','.zip','.7z','.tar','.sqlite','.db'}
    eda_images={'m18k_v2_composition.png','m18k_v2_rgb_depth_pairing.png','m18k_v2_rgb_depth_examples.png','m18k_v2_segmentation_examples.png'}
    unexpected=[]
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if '.git' in rel.parts or '__pycache__' in rel.parts:continue
        if p.is_symlink():unexpected.append('SYMLINK:'+rel.as_posix())
        elif p.is_file() and p.suffix.lower() in excluded_ext:
            if rel.parent==Path('09_results/visualizations') and p.name in eda_images:continue
            if rel.parent==Path('10_research_paper/figures') and p.name.startswith('Day3_') and p.suffix.lower()=='.png':continue
            unexpected.append(rel.as_posix())
    check(not unexpected,'No unapproved heavy/model/raw payloads: '+str(unexpected[:10]))
    return checks

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT);args=parser.parse_args()
    try:checks=validate(args.root.resolve())
    except Exception as exc:print('FAIL | Validator exception: '+str(exc));return 1
    for ok,msg in checks:print(('PASS' if ok else 'FAIL')+' | '+msg)
    fails=sum(not ok for ok,_ in checks)
    print('\nWorkspace validation:',len(checks)-fails,'PASS /',fails,'FAIL')
    return bool(fails)
if __name__=='__main__':sys.exit(main())
