"""Validate clean WP-00 infrastructure, never download or train. Python stdlib only."""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_EXTENSIONS = {'.jpg','.jpeg','.png','.bmp','.tif','.tiff','.webp','.gif','.mp4','.avi','.mov','.npy','.npz','.parquet','.h5','.hdf5','.tfrecord','.pt','.pth','.ckpt','.onnx','.safetensors','.weights','.pkl','.pickle','.zip','.rar','.7z','.tar','.gz','.tgz','.bz2','.xz','.bin','.gguf'}


def validate(root):
    results = []
    def check(condition, message):
        results.append((bool(condition), message))
    requirement_path = root / '12_reproducibility/manifests/workspace_requirements.json'
    try:
        spec = json.loads(requirement_path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return [(False, f'Requirements manifest unreadable: {exc}')]
    for directory in spec['directories']:
        check((root / directory).is_dir(), 'Directory: ' + directory)
    for filename in spec['files']:
        path = root / filename
        check(path.is_file() and path.stat().st_size > 0, 'Nonempty file: ' + filename)
    registries = {}
    for filename, expected in spec['csv_headers'].items():
        try:
            with (root / filename).open(encoding='utf-8', newline='') as stream:
                reader = csv.DictReader(stream, strict=True)
                rows = list(reader)
                check(reader.fieldnames == expected, 'CSV header: ' + filename)
                check(all(None not in row and all(v is not None for v in row.values()) for row in rows), 'CSV row widths: ' + filename)
                registries[filename] = rows
        except (OSError, UnicodeError, csv.Error) as exc:
            check(False, f'CSV unreadable: {filename}: {exc}')
    candidates = registries.get('03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv', [])
    ids = [r.get('candidate_id') for r in candidates]
    check({'C01','C02'}.issubset(ids) and len(ids) == len(set(ids)), 'Unique C01 and C02 records exist')
    check(all(r.get('verification_status') == 'PENDING_VERIFICATION' and r.get('dataset_paper_link_status') == 'NOT_VERIFIED' and all(r.get(k) == 'NOT_VERIFIED' for k in ('qc_status','baseline_status','gap_status')) and r.get('decision') == 'PENDING' for r in candidates), 'Candidate claims remain unverified/unselected')
    exclusions = registries.get('03_dataset_discovery/excluded_datasets/EXCLUDED_DATASETS.csv', [])
    check(any(r.get('source_identifier') == 'hf55tkx489' and r.get('exclusion_status') == 'EXCLUDED' and 'DS-02' in r.get('exclusion_reason','') for r in exclusions), 'DS-02 hf55tkx489 explicitly excluded')
    check(len(exclusions) == 1, 'Only user-confirmed exclusion initialized')
    check(not registries.get('08_experiments/experiment_registry.csv', []), 'No fictional experiments')
    check(not registries.get('02_literature_review/RESEARCH_GAP_MATRIX.csv', []), 'No invented research gaps')
    papers = registries.get('02_literature_review/PAPER_REGISTRY.csv', [])
    check(len(papers) == 1 and papers[0].get('paper_url') == 'https://www.mdpi.com/2077-0472/13/8/1533' and all(not papers[0].get(k) for k in ('title','authors','year','doi')) and papers[0].get('relationship_status') == 'NOT_VERIFIED', 'Only supplied unverified paper source; no invented metadata')
    try:
        state = json.loads((root / '00_project_management/project_state.json').read_text(encoding='utf-8'))
        check(state['current_phase'].startswith('PHASE 0') and state['current_work_package'] == 'WP-00', 'Phase 0 / WP-00 preserved')
        check(all(state[k] is False for k in ['dataset_selected','paper_selected','research_gap_validated','baseline_reproduced','training_authorized','external_validation_started']) and state['selected_candidate_id'] is None, 'No selection/training/scientific completion authorized')
        check(state['current_gate'] == 'G0' and state['gates'] == {f'G{i}':'NEEDS_MORE_EVIDENCE' for i in range(7)}, 'All G0–G6 unpassed')
        check(state['next_work_package'] == 'WP-01: Candidate Dataset & Paper Source Verification', 'Next package is WP-01; not started')
        status = (root / '00_project_management/RESEARCH_STATUS.md').read_text(encoding='utf-8')
        check(all(f'{label}: NO' in status for label in ['Dataset selected','Paper selected','Research gap validated','Baseline reproduced','Training authorized','External validation started']) and state['created_at'] in status, 'Human-readable status matches initialization metadata/date')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        check(False, f'State metadata invalid: {exc}')
    payloads = []
    forbidden_links = []
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if '.git' in relative.parts or '__pycache__' in relative.parts:
            continue
        if path.is_symlink() or path.is_junction():
            forbidden_links.append(relative.as_posix())
        if path.is_file() and path.suffix.lower() in PAYLOAD_EXTENSIONS:
            payloads.append(relative.as_posix())
    check(not forbidden_links, 'No symlinks/junctions importing external artifacts: ' + repr(forbidden_links))
    check(not payloads, 'No dataset/media/archive/model payloads anywhere: ' + repr(payloads))
    # Empty storage checks also catch labels, text or extensionless payloads.
    storage = list((root / '04_dataset_candidates').glob('*/raw')) + list((root / '04_dataset_candidates').glob('*/processed')) + list((root / '04_dataset_candidates').glob('*/derived'))
    storage += [root / p for p in ['08_experiments/runs','08_experiments/checkpoints','11_field_validation/external_test_data']]
    for directory in storage:
        extra = [p.relative_to(root).as_posix() for p in directory.rglob('*') if p.is_file() and p.name != '.gitkeep']
        check(not extra, 'Empty WP-00 payload storage: ' + directory.relative_to(root).as_posix() + ' ' + repr(extra))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='Workspace root (also supports isolated regression fixtures)')
    args = parser.parse_args()
    results = validate(args.root.resolve())
    for passed, message in results:
        print(('PASS' if passed else 'FAIL') + ' | ' + message)
    failures = sum(not passed for passed, _ in results)
    print(f'\nWP-00 validation: {len(results)-failures} PASS / {failures} FAIL')
    return 1 if failures else 0

if __name__ == '__main__':
    raise SystemExit(main())
