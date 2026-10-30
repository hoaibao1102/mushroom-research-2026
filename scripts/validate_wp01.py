"""Validate WP-01 Source Verification deliverables and scientific integrity.
Standard library only. Never download payloads or execute model training.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAYLOAD_EXTENSIONS = {
    '.jpg','.jpeg','.png','.bmp','.tif','.tiff','.webp','.gif',
    '.mp4','.avi','.mov','.npy','.npz','.parquet','.h5','.hdf5',
    '.tfrecord','.pt','.pth','.ckpt','.onnx','.safetensors','.weights',
    '.pkl','.pickle','.zip','.rar','.7z','.tar','.gz','.tgz','.bz2','.xz','.bin','.gguf'
}

ALLOWED_EVIDENCE_STATUSES = {
    'VERIFIED_FROM_PRIMARY_SOURCE',
    'REPORTED_BY_SOURCE_NOT_AUDITED',
    'INFERRED',
    'UNVERIFIED',
    'CONTRADICTED'
}

WP01_REQUIRED_FILES = [
    '03_dataset_discovery/source_verification/C01_SOURCE_VERIFICATION.md',
    '04_dataset_candidates/C01_substrate_contamination/reports/WP-01_C01_FEASIBILITY.md',
    '03_dataset_discovery/source_verification/C02_SOURCE_VERIFICATION.md',
    '04_dataset_candidates/C02_mushr_harvest_readiness/reports/WP-01_C02_FEASIBILITY.md',
    '03_dataset_discovery/source_verification/C02_VS_DS02_IDENTITY_CHECK.md',
    '03_dataset_discovery/dataset_comparisons/WP-01_CANDIDATE_COMPARISON.md',
    '03_dataset_discovery/source_verification/WP-01_EVIDENCE_REGISTRY.csv',
    '03_dataset_discovery/source_verification/WP-01_UNRESOLVED_QUESTIONS.md',
    'setup_reports/WP-01_SOURCE_VERIFICATION_REPORT.md'
]


def validate_wp01(root=ROOT):
    results = []
    def check(condition, message):
        results.append((bool(condition), message))

    # 1. Required Files
    for rel_path in WP01_REQUIRED_FILES:
        target = root / rel_path
        check(target.is_file() and target.stat().st_size > 0, f"Nonempty WP-01 deliverable: {rel_path}")

    # 2. Evidence Registry Validation
    ev_path = root / '03_dataset_discovery/source_verification/WP-01_EVIDENCE_REGISTRY.csv'
    expected_ev_headers = [
        'claim_id', 'claim_text', 'candidate_id', 'source_title',
        'source_url_or_doi', 'source_type', 'source_publication_update_date',
        'access_date', 'source_location', 'evidence_status', 'confidence', 'verification_notes'
    ]
    try:
        with ev_path.open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            headers = [h.strip('\ufeff') for h in reader.fieldnames]
            check(headers == expected_ev_headers, "WP-01 Evidence Registry header matches schema")
            claims = list(reader)
            check(len(claims) >= 50, f"Evidence registry has comprehensive claim coverage (found {len(claims)} claims)")
            invalid_statuses = [c.get('evidence_status') for c in claims if c.get('evidence_status') not in ALLOWED_EVIDENCE_STATUSES]
            check(len(invalid_statuses) == 0, f"All claim evidence_status in allowed vocabulary (invalid: {invalid_statuses})")
            empty_claims = [c.get('claim_id') for c in claims if not c.get('claim_text') or not c.get('source_url_or_doi')]
            check(len(empty_claims) == 0, f"All claims have non-empty text and source pointers (empty: {empty_claims})")
    except Exception as exc:
        check(False, f"Evidence registry unreadable: {exc}")

    # 3. Candidate Registry
    cand_path = root / '03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv'
    try:
        with cand_path.open(encoding='utf-8', newline='') as f:
            cands = list(csv.DictReader(f))
            c_dict = {c['candidate_id']: c for c in cands}
            check({'C01', 'C02'}.issubset(c_dict.keys()), "Candidates C01 and C02 registered")
            check(c_dict['C01']['verification_status'] == 'SOURCE_VERIFIED_METADATA_ONLY', "C01 marked SOURCE_VERIFIED_METADATA_ONLY")
            check(c_dict['C02']['verification_status'] == 'SOURCE_VERIFIED_METADATA_AND_CODE', "C02 marked SOURCE_VERIFIED_METADATA_AND_CODE")
            check(c_dict['C01']['qc_status'] == 'NOT_VERIFIED' and c_dict['C02']['qc_status'] == 'NOT_VERIFIED', "Candidate QC remains NOT_VERIFIED")
            check(c_dict['C01']['decision'] == 'PENDING' and c_dict['C02']['decision'] == 'PENDING', "Candidate selection decision remains PENDING")
    except Exception as exc:
        check(False, f"Candidate registry check failed: {exc}")

    # 4. Paper Registry
    paper_path = root / '02_literature_review/PAPER_REGISTRY.csv'
    try:
        with paper_path.open(encoding='utf-8', newline='') as f:
            papers = list(csv.DictReader(f))
            p_dict = {p['paper_id']: p for p in papers}
            check('P001' in p_dict, "Primary MushR paper P001 registered")
            check(p_dict['P001']['doi'] == '10.3390/agriculture13081533', "P001 DOI matches 10.3390/agriculture13081533")
            check(p_dict['P001']['verification_status'] == 'FULL_TEXT_REVIEWED', "P001 verification_status is FULL_TEXT_REVIEWED")
            check('P002' in p_dict, "Related C01 paper P002 (Bacanto 2026) registered")
    except Exception as exc:
        check(False, f"Paper registry check failed: {exc}")

    # 5. Exclusion Registry
    excl_path = root / '03_dataset_discovery/excluded_datasets/EXCLUDED_DATASETS.csv'
    try:
        with excl_path.open(encoding='utf-8', newline='') as f:
            excls = list(csv.DictReader(f))
            check(any(e['source_identifier'] == 'hf55tkx489' and e['exclusion_status'] == 'EXCLUDED' for e in excls), "DS-02 hf55tkx489 remains EXCLUDED")
            check(len(excls) == 1, "Only confirmed DS-02 exclusion in registry")
    except Exception as exc:
        check(False, f"Exclusion registry check failed: {exc}")

    # 6. Project State & Gates
    try:
        state_path = root / '00_project_management/project_state.json'
        state = json.loads(state_path.read_text(encoding='utf-8'))
        check(state['current_phase'].startswith('PHASE 0'), "Phase 0 preserved")
        check(state['current_work_package'] == 'WP-01', "Current work package is WP-01")
        check(state['dataset_selected'] is False, "dataset_selected remains False")
        check(state['training_authorized'] is False, "training_authorized remains False")
        check(state['current_gate'] == 'G0', "current_gate is G0")
        check(all(v == 'NEEDS_MORE_EVIDENCE' for v in state['gates'].values()), "All G0–G6 gates remain NEEDS_MORE_EVIDENCE")
        check(state['candidate_g0_recommendations']['C01'] == 'NEEDS_MORE_EVIDENCE', "C01 G0 recommendation is NEEDS_MORE_EVIDENCE")
        check(state['candidate_g0_recommendations']['C02'] == 'NEEDS_MORE_EVIDENCE', "C02 G0 recommendation is NEEDS_MORE_EVIDENCE")
    except Exception as exc:
        check(False, f"Project state check failed: {exc}")

    # 7. Payload & Storage Audit (Ensuring zero data/weights downloaded)
    payloads = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if '.git' in rel.parts or '__pycache__' in rel.parts:
            continue
        if path.is_file() and path.suffix.lower() in PAYLOAD_EXTENSIONS:
            payloads.append(rel.as_posix())
    check(len(payloads) == 0, f"Zero dataset/media/checkpoint payloads in workspace (found: {payloads})")

    storage_dirs = [
        root / '04_dataset_candidates/C01_substrate_contamination/raw',
        root / '04_dataset_candidates/C02_mushr_harvest_readiness/raw',
        root / '08_experiments/runs',
        root / '08_experiments/checkpoints',
        root / '11_field_validation/external_test_data'
    ]
    for sdir in storage_dirs:
        non_gitkeep = [p.name for p in sdir.rglob('*') if p.is_file() and p.name != '.gitkeep']
        check(len(non_gitkeep) == 0, f"Payload storage {sdir.name} is empty (found: {non_gitkeep})")

    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='Workspace root')
    args = parser.parse_args()
    results = validate_wp01(args.root.resolve())
    failures = sum(not passed for passed, _ in results)
    for passed, message in results:
        print(('PASS' if passed else 'FAIL') + ' | ' + message)
    print(f"\nWP-01 validation: {len(results)-failures} PASS / {failures} FAIL")
    return 1 if failures else 0

if __name__ == '__main__':
    sys.exit(main())
