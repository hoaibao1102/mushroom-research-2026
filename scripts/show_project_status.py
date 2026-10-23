"""Display current metadata and candidate states; no hardcoded success claims."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    try:
        state = json.loads((ROOT / '00_project_management/project_state.json').read_text(encoding='utf-8'))
        with (ROOT / '03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv').open(encoding='utf-8', newline='') as stream:
            candidates = list(csv.DictReader(stream, strict=True))
        print('Project: ' + state['project_name'])
        print('Phase: ' + state['current_phase'])
        print('Current work package: ' + state['current_work_package'])
        print('Current gate: ' + state['current_gate'] + ' / ' + state['gates'][state['current_gate']])
        print('Dataset selected: ' + ('YES' if state['dataset_selected'] else 'NO'))
        print('Selected candidate: ' + str(state['selected_candidate_id']))
        print('Training authorized: ' + ('YES' if state['training_authorized'] else 'NO'))
        for row in candidates:
            print(f"{row['candidate_id']}: verification={row['verification_status']}; QC={row['qc_status']}; baseline={row['baseline_status']}; gap={row['gap_status']}; decision={row['decision']}")
        print('Next work package: ' + state['next_work_package'])
        return 0
    except (OSError, ValueError, csv.Error, KeyError, TypeError) as exc:
        print('FAIL | Cannot read project status: ' + str(exc))
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
