"""Repository-level checks for historical evidence and Day 6 system specification."""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkspaceTests(unittest.TestCase):
    def test_validator_accepts_updated_workspace(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_workspace.py")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + "\n" + result.stderr)

    def test_historical_baseline_is_not_misrepresented_as_general(self):
        state = json.loads((ROOT / "00_project_management/project_state.json").read_text(encoding="utf-8"))
        self.assertTrue(state["dataset_eda_executed"])
        self.assertTrue(state["baseline_reproduced"])
        self.assertFalse(state["exact_original_benchmark_reproduced"])
        self.assertEqual(state["day3_area_sample_images"], 30)
        self.assertIsNone(state["working_candidate_id"])
        self.assertEqual(state["legacy_experiment_candidate_id"], "C03")
        self.assertFalse(state["dataset_selected"])

    def test_day2_and_day4_experiment_registry_entries(self):
        with (ROOT / "08_experiments/experiment_registry.csv").open(newline="", encoding="utf-8-sig") as stream:
            ids = {row["experiment_id"] for row in csv.DictReader(stream)}
        self.assertTrue({
            "EXP-M18K-V2-2CLASS-20261102",
            "EXP-M18K-V2-WB-20261102",
            "EXP-M18K-V2-DAY4-AREA-20261104",
            "EXP-M18K-V2-DAY4-OTSU-20261104",
            "EXP-M18K-V2-DAY4-DEMO-20261104",
        }.issubset(ids))

    def test_day4_and_day5_boundaries_are_preserved(self):
        state = json.loads((ROOT / "00_project_management/project_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["day4_area_full_test_images"], 450)
        self.assertEqual(state["day4_area_matched_gt_instances"], 68794)
        self.assertFalse(state["day4_dataset_qc_cleared"])
        self.assertFalse(state["demo_video_completed"])
        self.assertTrue(state["presentation_completed"])
        self.assertEqual(state["day5_dense_counting_sample_images"], 8)
        self.assertFalse(state["day5_dense_full_test_validated"])
        self.assertFalse(state["day5_rgbd_calibration_verified"])
        self.assertFalse(state["day5_rgbd_physical_area_mm2_computed"])
        self.assertTrue(state["day5_gradio_demo_user_confirmed_working"])

    def test_day6_increment0_system_scope(self):
        state = json.loads((ROOT / "00_project_management/project_state.json").read_text(encoding="utf-8"))
        self.assertTrue(state["increment_0_completed"])
        self.assertTrue(state["day6_source_audit_completed"])
        self.assertFalse(state["model_architecture_selected"])
        self.assertFalse(state["amd_runtime_verified"])
        self.assertFalse(state["user_uploads_required_for_increment_1"])
        requirements = (ROOT / "00_project_management/SYSTEM_REQUIREMENTS.md").read_text(encoding="utf-8").lower()
        self.assertIn("cluster", requirements)
        self.assertIn("human review", requirements)
        architecture = (ROOT / "00_project_management/SYSTEM_ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertIn("Colab", architecture)
        self.assertIn("CPU", architecture)
        self.assertIn("AMD", architecture)

    def test_day6_source_registry_and_candidate_roles(self):
        with (ROOT / "03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv").open(newline="", encoding="utf-8-sig") as stream:
            rows = {row["candidate_id"]: row for row in csv.DictReader(stream)}
        self.assertTrue({"C02", "C03", "C04", "C05", "C06", "C07", "C08"}.issubset(rows))
        self.assertEqual(rows["C04"]["decision"], "PRIMARY_TRACKING_SOURCE_TO_VALIDATE")
        self.assertEqual(rows["C03"]["decision"], "SUPPORTING_REFERENCE_ONLY")
        with (ROOT / "08_experiments/experiment_registry.csv").open(newline="", encoding="utf-8-sig") as stream:
            ids = {row["experiment_id"] for row in csv.DictReader(stream)}
        self.assertIn("WP06-INCREMENT0-20261108", ids)

    def test_explicit_dataset_exclusion_remains_enforced(self):
        with (ROOT / "03_dataset_discovery/excluded_datasets/EXCLUDED_DATASETS.csv").open(newline="", encoding="utf-8-sig") as stream:
            exclusions = list(csv.DictReader(stream))
        self.assertTrue(any(row["source_identifier"] == "hf55tkx489" and row["exclusion_status"] == "EXCLUDED" for row in exclusions))
        with (ROOT / "03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv").open(newline="", encoding="utf-8-sig") as stream:
            candidates = {row["candidate_id"]: row for row in csv.DictReader(stream)}
        self.assertEqual(candidates["C05"]["decision"], "EXCLUDED_BY_PRIOR_USER_INSTRUCTION")
        self.assertEqual(candidates["C05"]["qc_status"], "NOT_PERMITTED_UNDER_D001")

    def test_dataset_inspector_handles_small_coco_fixture(self):
        inspector = ROOT / "07_source_code/data/inspect_dataset.py"
        with tempfile.TemporaryDirectory() as temp:
            data_root = Path(temp) / "dataset"
            image_dir = data_root / "images"
            annotation_dir = data_root / "annotations"
            image_dir.mkdir(parents=True)
            annotation_dir.mkdir(parents=True)
            (image_dir / "one.jpg").write_bytes(b"fixture-image-placeholder")
            coco = {
                "images": [{"id": 1, "file_name": "images/one.jpg", "width": 100, "height": 80}],
                "annotations": [{
                    "id": 10, "image_id": 1, "category_id": 3,
                    "bbox": [2, 3, 10, 12], "segmentation": [[2, 3, 12, 3, 12, 15, 2, 15]],
                }],
                "categories": [{"id": 3, "name": "mushroom"}],
            }
            (annotation_dir / "instances.json").write_text(json.dumps(coco), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(inspector), "--root", str(data_root), "--dimension-sample", "0"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["summary"]["image_count"], 1)
            self.assertEqual(len(report["coco_annotations"]), 1)
            coco_report = report["coco_annotations"][0]
            self.assertEqual(coco_report["images"], 1)
            self.assertEqual(coco_report["annotations"], 1)
            self.assertEqual(coco_report["checks"]["missing_image_files_count"], 0)
            self.assertEqual(coco_report["checks"]["invalid_bbox_count"], 0)

    def test_validator_rejects_missing_eda(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "repo"
            shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            (destination / "09_results/reports/M18K_V2_EDA_2026-10-30.md").unlink()
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_workspace.py"), "--root", str(destination)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL | Day 1 EDA evidence", result.stdout)


if __name__ == "__main__":
    unittest.main()
