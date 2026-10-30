"""Standard-library regression tests; fixtures never contain research data."""
import subprocess
import sys
import unittest
import csv
import os
import shutil
import tempfile
from pathlib import Path


def clone_workspace(destination):
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns('.git', '__pycache__'))


def validate_fixture(root):
    return subprocess.run([sys.executable, str(ROOT / 'scripts/validate_workspace.py'), '--root', str(root)], capture_output=True, text=True)


def validate_wp01_fixture(root):
    return subprocess.run([sys.executable, str(ROOT / 'scripts/validate_wp01.py'), '--root', str(root)], capture_output=True, text=True)


class RejectionTests(unittest.TestCase):
    def test_missing_protocol_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
            root = Path(tmp) / 'workspace'
            clone_workspace(root)
            (root / '05_research_protocols/DATASET_QC_PROTOCOL.md').unlink()
            result = validate_fixture(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAIL | Nonempty file: 05_research_protocols/DATASET_QC_PROTOCOL.md', result.stdout)

    def test_malformed_csv_header_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
            root = Path(tmp) / 'workspace'
            clone_workspace(root)
            (root / '02_literature_review/PAPER_REGISTRY.csv').write_text('wrong_header\n', encoding='utf-8')
            result = validate_fixture(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAIL | CSV header:', result.stdout)

    def test_missing_exclusion_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
            root = Path(tmp) / 'workspace'
            clone_workspace(root)
            path = root / '03_dataset_discovery/excluded_datasets/EXCLUDED_DATASETS.csv'
            header = path.read_text(encoding='utf-8').splitlines()[0]
            path.write_text(header + '\n', encoding='utf-8')
            result = validate_fixture(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAIL | DS-02 hf55tkx489 explicitly excluded', result.stdout)

    def test_non_payload_text_in_raw_storage_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
            root = Path(tmp) / 'workspace'
            clone_workspace(root)
            (root / '04_dataset_candidates/C01_substrate_contamination/raw/forbidden_marker.txt').write_text('TEST MARKER ONLY: not research data', encoding='utf-8')
            result = validate_fixture(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAIL | Empty WP-00 payload storage:', result.stdout)

    def test_checkpoint_extension_rejected_without_model_content(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
            root = Path(tmp) / 'workspace'
            clone_workspace(root)
            (root / '08_experiments/checkpoints/forbidden_marker.pt').touch()
            result = validate_fixture(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAIL | No dataset/media/archive/model payloads anywhere:', result.stdout)

ROOT = Path(__file__).resolve().parents[1]

class WorkspaceTests(unittest.TestCase):
    def test_wp01_validator_accepts_clean_workspace(self):
        script = ROOT / 'scripts/validate_wp01.py'
        self.assertTrue(script.is_file(), 'WP-01 validator must exist')
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('WP-01 validation: 38 PASS / 0 FAIL', result.stdout)

    def test_wp00_validator_flags_wp01_transition(self):
        """Original WP-00 validator strictly enforces WP-00 state and must flag WP-01 transition."""
        script = ROOT / 'scripts/validate_workspace.py'
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, "WP-00 validator must exit 1 on WP-01 workspace")
        self.assertIn('Candidate claims remain unverified/unselected', result.stdout)
        self.assertIn('Phase 0 / WP-00 preserved', result.stdout)

    def test_wp01_validator_rejects_missing_deliverable(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
            root = Path(tmp) / 'workspace'
            clone_workspace(root)
            (root / '03_dataset_discovery/source_verification/C01_SOURCE_VERIFICATION.md').unlink()
            result = validate_wp01_fixture(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAIL | Nonempty WP-01 deliverable: 03_dataset_discovery/source_verification/C01_SOURCE_VERIFICATION.md', result.stdout)

    def test_wp01_validator_rejects_unauthorized_training(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
            root = Path(tmp) / 'workspace'
            clone_workspace(root)
            state_p = root / '00_project_management/project_state.json'
            import json
            s = json.loads(state_p.read_text(encoding='utf-8'))
            s['training_authorized'] = True
            state_p.write_text(json.dumps(s), encoding='utf-8')
            result = validate_wp01_fixture(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAIL | training_authorized remains False', result.stdout)


if __name__ == '__main__':
    unittest.main()
