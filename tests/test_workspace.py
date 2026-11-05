"""Repository-level evidence checks; no fresh model/data audit."""
import csv, json, subprocess, sys, tempfile, unittest, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class WorkspaceTests(unittest.TestCase):
    def test_validator_accepts_updated_workspace(self):
        r=subprocess.run([sys.executable,str(ROOT/'scripts/validate_workspace.py')],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+'\n'+r.stderr)
    def test_three_day_state_without_claiming_original_benchmark(self):
        s=json.loads((ROOT/'00_project_management/project_state.json').read_text())
        self.assertTrue(s['dataset_eda_executed']); self.assertTrue(s['baseline_reproduced'])
        self.assertFalse(s['exact_original_benchmark_reproduced'])
        self.assertEqual(s['day3_area_sample_images'],30)
        self.assertEqual(s['working_candidate_id'],'C03')
        self.assertFalse(s['dataset_selected'])
    def test_exp_registry_has_both_completed_tests(self):
        with (ROOT/'08_experiments/experiment_registry.csv').open(newline='') as f:rows=list(csv.DictReader(f))
        ids={r['experiment_id'] for r in rows}
        self.assertIn('EXP-M18K-V2-2CLASS-20261102',ids)
        self.assertIn('EXP-M18K-V2-WB-20261102',ids)
    def test_day4_mvp_evidence_without_claiming_qc_clearance(self):
        s=json.loads((ROOT/'00_project_management/project_state.json').read_text())
        self.assertEqual(s['day4_area_full_test_images'],450)
        self.assertEqual(s['day4_area_matched_gt_instances'],68794)
        self.assertEqual(s['day4_otsu_evaluation_images'],10)
        self.assertFalse(s['day4_dataset_qc_cleared'])
        self.assertFalse(s['demo_video_completed'])
        self.assertTrue(s['presentation_completed'])
    def test_day4_registry_entries(self):
        with (ROOT/'08_experiments/experiment_registry.csv').open(newline='') as f: ids={row['experiment_id'] for row in csv.DictReader(f)}
        self.assertIn('EXP-M18K-V2-DAY4-AREA-20261104',ids)
        self.assertIn('EXP-M18K-V2-DAY4-OTSU-20261104',ids)
        self.assertIn('EXP-M18K-V2-DAY4-DEMO-20261104',ids)

    def test_day5_evidence_is_recorded_with_appropriate_limits(self):
        s=json.loads((ROOT/'00_project_management/project_state.json').read_text())
        self.assertEqual(s['day5_dense_counting_sample_images'],8)
        self.assertFalse(s['day5_dense_full_test_validated'])
        self.assertFalse(s['day5_rgbd_calibration_verified'])
        self.assertFalse(s['day5_rgbd_physical_area_mm2_computed'])
        self.assertTrue(s['day5_gradio_demo_user_confirmed_working'])
    def test_day5_registry_entries(self):
        with (ROOT/'08_experiments/experiment_registry.csv').open(newline='') as f: ids={r['experiment_id'] for r in csv.DictReader(f)}
        self.assertIn('EXP-M18K-V2-DAY5-DENSE-NMS-20261105',ids)
        self.assertIn('EXP-M18K-V2-DAY5-RGBD-FEASIBILITY-20261105',ids)
    def test_validator_rejects_missing_eda(self):
        with tempfile.TemporaryDirectory() as t:
            dst=Path(t)/'repo';shutil.copytree(ROOT,dst,ignore=shutil.ignore_patterns('.git','__pycache__'))
            (dst/'09_results/reports/M18K_V2_EDA_2026-10-30.md').unlink()
            r=subprocess.run([sys.executable,str(ROOT/'scripts/validate_workspace.py'),'--root',str(dst)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)
            self.assertIn('FAIL | Day 1 EDA evidence',r.stdout)
if __name__=='__main__':unittest.main()
