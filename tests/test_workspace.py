"""Tests for M18K Team 10 research repository metadata, not model quality."""
import csv,json,subprocess,sys,tempfile,unittest,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class WorkspaceTests(unittest.TestCase):
    def test_validator_accepts_current_workspace(self):
        run=subprocess.run([sys.executable,str(ROOT/'scripts/validate_workspace.py')],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout+'\n'+run.stderr)
    def test_eda_without_reproduction_claim(self):
        s=json.loads((ROOT/'00_project_management/project_state.json').read_text(encoding='utf8'))
        self.assertTrue(s['dataset_eda_executed'])
        self.assertFalse(s['baseline_reproduced'])
        self.assertEqual(s['working_candidate_id'],'C03')
    def test_c03_candidate_unique(self):
        with (ROOT/'03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv').open(encoding='utf8',newline='') as f:
            rows=list(csv.DictReader(f))
        ids=[r['candidate_id'] for r in rows]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertIn('C03',ids)
    def test_validator_rejects_missing_eda(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst=Path(tmp)/'repo'
            shutil.copytree(ROOT,dst,ignore=shutil.ignore_patterns('.git','__pycache__'))
            (dst/'09_results/reports/M18K_V2_EDA_2026-10-30.md').unlink()
            run=subprocess.run([sys.executable,str(ROOT/'scripts/validate_workspace.py'),'--root',str(dst)],capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertIn('FAIL | EDA report available',run.stdout)
if __name__=='__main__':unittest.main()
