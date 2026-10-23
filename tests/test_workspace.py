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
    def test_validator_accepts_clean_workspace(self):
        script = ROOT / 'scripts/validate_workspace.py'
        self.assertTrue(script.is_file(), 'Workspace validator must exist')
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

if __name__ == '__main__':
    unittest.main()
