#!/usr/bin/env python3
"""Validate the source-only repository, Day 1–6 records and evidence consistency.

This checks repository metadata and local utility/evidence files. It does not
validate downloaded datasets, model accuracy, Colab execution or GPU support.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream, strict=True))


def validate(root: Path) -> list[tuple[bool, str]]:
    checks: list[tuple[bool, str]] = []

    def check(condition: bool, message: str) -> None:
        checks.append((bool(condition), message))

    req_path = root / "12_reproducibility/manifests/workspace_requirements.json"
    req = _read_json(req_path)
    for directory in req["directories"]:
        check((root / directory).is_dir(), f"Directory: {directory}")
    for file_path in req["files"]:
        check((root / file_path).is_file(), f"Required file: {file_path}")

    # Source-only packages can omit prior course documents, selected figures and
    # large per-instance exports; these remain optional and are never treated as
    # missing source code.
    for file_path in req.get("optional_files", []):
        exists = (root / file_path).is_file()
        check(True, f"Optional artifact {'included' if exists else 'not bundled'}: {file_path}")
    for pattern, expected_count in req.get("optional_globs", {}).items():
        matches = list(root.glob(pattern))
        condition = not matches or len(matches) == expected_count
        check(condition, f"Optional generated files: {pattern} ({len(matches)} present; {expected_count} when bundled)")

    for relative_path, expected_header in req["csv_headers"].items():
        path = root / relative_path
        try:
            with path.open(newline="", encoding="utf-8-sig") as source:
                reader = csv.DictReader(source, strict=True)
                rows = list(reader)
                check(reader.fieldnames == expected_header, f"CSV header: {relative_path}")
                check(
                    all(None not in row and all(value is not None for value in row.values()) for row in rows),
                    f"CSV row widths: {relative_path}",
                )
        except (OSError, UnicodeError, csv.Error) as exc:
            check(False, f"CSV unreadable {relative_path}: {exc}")

    candidates = _read_csv(root / "03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv")
    candidate_ids = [row["candidate_id"] for row in candidates]
    by_candidate = {row["candidate_id"]: row for row in candidates}
    check(
        all(item in by_candidate for item in ("C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08"))
        and len(set(candidate_ids)) == len(candidate_ids),
        "Candidate IDs C01–C08 are present and unique",
    )
    check(
        by_candidate["C04"]["decision"] == "PRIMARY_TRACKING_SOURCE_TO_VALIDATE",
        "Charisis candidate is identified as the primary tracking source to validate",
    )
    check(
        by_candidate["C03"]["decision"] == "SUPPORTING_REFERENCE_ONLY",
        "M18K is retained as a supporting/historical source, not the production selection",
    )

    # Enforce the previously recorded explicit dataset exclusion.
    excluded = _read_csv(root / "03_dataset_discovery/excluded_datasets/EXCLUDED_DATASETS.csv")
    exclusion = next((row for row in excluded if row["source_identifier"] == "hf55tkx489"), None)
    p005 = next((row for row in _read_csv(root / "02_literature_review/PAPER_REGISTRY.csv") if row["paper_id"] == "P005"), None)
    check(exclusion is not None and exclusion["exclusion_status"] == "EXCLUDED", "D001 dataset exclusion is preserved")
    check(
        by_candidate["C05"]["decision"] == "EXCLUDED_BY_PRIOR_USER_INSTRUCTION"
        and by_candidate["C05"]["qc_status"] == "NOT_PERMITTED_UNDER_D001",
        "Excluded candidate cannot enter dataset QC/acquisition",
    )
    check(
        p005 is not None and p005["relationship_status"] == "BIBLIOGRAPHIC_EXCLUSION_RECORD_ONLY",
        "Excluded source is retained as bibliographic identity only",
    )

    state = _read_json(root / "00_project_management/project_state.json")
    check(
        state.get("working_candidate_id") is None and state.get("legacy_experiment_candidate_id") == "C03",
        "No single production dataset is selected; M18K remains a historical supporting baseline",
    )
    check(
        state.get("increment_0_completed") is True
        and state.get("day6_source_audit_completed") is True
        and state.get("day6_target_requirements_documented") is True
        and state.get("day6_system_architecture_documented") is True,
        "Day 6 Increment 0 requirements/source audit and architecture are recorded",
    )
    check(
        state.get("training_environment") == "Google Colab GPU; export versioned model packages.",
        "Colab training/export strategy is recorded",
    )
    check(
        "AMD" in state.get("inference_environment", "") and "CPU" in state.get("inference_environment", ""),
        "AMD-first local inference and CPU fallback are recorded",
    )
    check(state.get("model_architecture_selected") is False, "Production model remains provisional pending data/runtime checks")
    check(state.get("dataset_selected") is False and state.get("training_authorized") is False, "No unearned dataset selection or training approval")
    check(state.get("amd_runtime_verified") is False, "AMD inference is not claimed before target-machine testing")
    check(
        (root / "00_project_management/SYSTEM_REQUIREMENTS.md").is_file()
        and (root / "00_project_management/SYSTEM_ARCHITECTURE.md").is_file(),
        "System requirements and architecture are available",
    )
    check(
        (root / "03_dataset_discovery/SOURCE_DATA_AUDIT_DAY6.md").is_file()
        and (root / "03_dataset_discovery/SOURCE_CODE_REGISTRY.csv").is_file(),
        "Day 6 source and code registries are available",
    )

    # Days 1–5 are retained as historical evidence. These checks deliberately
    # preserve their original species and experiment scope.
    check(state.get("dataset_eda_executed") is True, "Day 1 EDA recorded")
    check(
        state.get("baseline_reproduced") is True and state.get("exact_original_benchmark_reproduced") is False,
        "Day 2 method workflow reproduced on V2; exact paper benchmark not claimed",
    )
    check(
        state.get("day3_area_sample_images") == 30 and state.get("day3_qualitative_sample_images") == 12,
        "Day 3 sample sizes recorded",
    )
    check((root / "09_results/reports/M18K_V2_EDA_2026-10-30.md").is_file(), "Day 1 EDA evidence")
    check((root / "09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md").is_file(), "Day 2 test report")
    check((root / "09_results/reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md").is_file(), "Day 3 sample report")

    try:
        two_class = _read_json(root / "09_results/metrics/Day2_Two_Class_Heldout_Test_2026-11-02.json")
        wb_only = _read_json(root / "09_results/metrics/Day2_WB_Only_Heldout_Test_2026-11-02.json")
        area = _read_json(root / "09_results/area_evaluation/mask_area_summary.json")
        check(
            two_class["test_images"] == wb_only["test_images"] == 450
            and two_class["test_instances_total"] == 70289
            and wb_only["test_instances_WB"] == 70192,
            "Day 2 test counts agree with recorded evidence",
        )
        check(
            abs(two_class["all"]["mask_map50_95"] - 0.396273) < 1e-6
            and abs(wb_only["mask_map50_95"] - 0.7973628392154766) < 1e-8,
            "Day 2 mask metrics match recorded evidence",
        )
        check(
            area["sample_size_images"] == 30
            and area["matched"] == 4900
            and area["unmatched_predictions"] == 246
            and area["unmatched_gt"] == 70,
            "Day 3 area counts are internally consistent",
        )
        rows = _read_csv(root / "09_results/wb_error_analysis/Khang_error_observations_REVIEWED.csv")
        check(
            len(rows) == 12
            and sum(int(row["missed_instances_iou50"]) for row in rows) == 42
            and sum(int(row["extra_instances_iou50"]) for row in rows) == 94,
            "Day 3 qualitative sample counts are internally consistent",
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, csv.Error) as exc:
        check(False, f"Day 1–3 metrics validation failed: {exc}")

    try:
        area4 = _read_json(root / "09_results/area_evaluation/day4_full_test/area_metrics.json")
        overall = area4["overall"]
        check(
            area4["sample"]["images_evaluated"] == 450
            and overall["gt_reference"] == 70192
            and overall["matched"] == 68794,
            "Day 4 full-test WB area sample and matched counts",
        )
        check(
            overall["unmatched_predictions"] == 3388
            and overall["unmatched_gt"] == 1398
            and abs(overall["mae_px2"] - 211.41426577899236) < 1e-5,
            "Day 4 area exclusions and error match recorded metrics",
        )
        demo = _read_json(root / "09_results/inference_demo/Day4_WB_Demo_Summary.json")
        check(demo["test_images_sampled"] == 10 and demo["predicted_wb_instances"] == 1551, "Day 4 inference MVP summary")
        otsu_rows = _read_csv(root / "09_results/otsu_baseline/method_summary_from_notebook.csv")
        otsu = {row["method"]: row for row in otsu_rows}
        check(
            abs(float(otsu["Otsu_full"]["mean_union_IoU"]) - 0.8662) < 0.0001
            and abs(float(otsu["YOLO_WB_only"]["mean_union_IoU"]) - 0.9201) < 0.0001,
            "Day 4 Otsu/YOLO foreground-IoU summaries",
        )
        check(
            (root / "08_experiments/notebooks/Day4_WB_Only_Final_Inference_Executed.ipynb").is_file()
            and (root / "08_experiments/notebooks/Day4_Otsu_Baseline_Ablation_Executed.ipynb").is_file(),
            "Day 4 executed notebooks available",
        )
        check((root / "08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb").is_file(), "Day 5 Gradio launcher notebook available")
        check((root / "07_source_code/demo/app.py").is_file(), "Day 5 Gradio app source available")

        dense = _read_csv(root / "09_results/dense_counting/day5_nms/comparison.csv")
        check(
            len(dense) == 8
            and abs(sum(float(row["baseline_abs_error"]) for row in dense) / 8 - 3.375) < 1e-9
            and abs(sum(float(row["modified_abs_error"]) for row in dense) / 8 - 1.875) < 1e-9,
            "Day 5 dense-scene counting MAE matches the eight-image CSV",
        )
        check(
            sum(float(row["modified_abs_error"]) < float(row["baseline_abs_error"]) for row in dense) == 6
            and sum(float(row["modified_abs_error"]) > float(row["baseline_abs_error"]) for row in dense) == 2,
            "Day 5 per-image NMS outcomes: six improved, two worsened",
        )
        selected = _read_csv(root / "09_results/dense_counting/day5_nms/selected_images.csv")
        check(
            len(selected) == 8 and all(row["visual_confirmation"] == "PENDING" for row in selected),
            "Day 5 dense-image selection remains flagged for visual confirmation",
        )
        depth = _read_json(root / "09_results/rgbd_feasibility/day5/depth_inspection.json")
        valid_depth = depth["depth_validity_in_wb_masks"]
        check(
            valid_depth["images"] == 30
            and valid_depth["instances"] == 4970
            and valid_depth["instances_valid_lt_50pct"] == 301
            and valid_depth["instances_zero_valid"] == 132,
            "Day 5 RGB-D feasibility sample and valid-depth counts",
        )
        extra = _read_json(root / "09_results/rgbd_feasibility/day5/extra_checks_summary.json")
        check(
            extra["test_depth_files"] == 450 and extra["dtype_counts"] == {"float32": 340, "uint16": 110},
            "Day 5 test depth dtype inventory",
        )
        check(
            depth["calibration_verified"] is False
            and (root / "09_results/rgbd_feasibility/day5/findings.md").is_file(),
            "Day 5 RGB-D report keeps physical calibration unverified",
        )
        check(
            state.get("day5_dense_full_test_validated") is False
            and state.get("day5_rgbd_physical_area_mm2_computed") is False,
            "Day 5 limitations recorded without full-test or mm2 claims",
        )
        check(
            state.get("day5_gradio_demo_user_confirmed_working") is True
            and state.get("presentation_completed") is True
            and state.get("demo_video_completed") is False,
            "Day 5 demo, slides and video status recorded",
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, csv.Error) as exc:
        check(False, f"Day 4–5 evidence validation failed: {exc}")

    # Historical binary deliverables and large generated exports are optional in
    # this source-only package. If selected figures are bundled, the set is complete.
    figure_matches = list((root / "10_research_paper/figures").glob("Day3_*.png"))
    check(not figure_matches or len(figure_matches) == 16, "Optional Day 3 figure set is complete when bundled")

    # Prevent large raw data/checkpoints from accidentally entering the source ZIP.
    excluded_extensions = {
        ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".npy", ".npz", ".pt", ".pth",
        ".ckpt", ".onnx", ".zst", ".zip", ".7z", ".tar", ".sqlite", ".db",
    }
    allowed_pngs = {
        "m18k_v2_composition.png", "m18k_v2_rgb_depth_pairing.png",
        "m18k_v2_rgb_depth_examples.png", "m18k_v2_segmentation_examples.png",
    }
    unexpected: list[str] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.is_symlink():
            unexpected.append("SYMLINK:" + relative.as_posix())
        elif path.is_file() and path.suffix.lower() in excluded_extensions:
            if relative.parent == Path("09_results/visualizations") and path.name in allowed_pngs:
                continue
            if relative.parent == Path("10_research_paper/figures") and path.name.startswith("Day3_") and path.suffix.lower() == ".png":
                continue
            if path.suffix.lower() == ".png" and path.stat().st_size <= 3 * 1024 * 1024:
                if relative.parts[:2] in {
                    ("09_results", "area_evaluation"), ("09_results", "dataset_qc"),
                    ("09_results", "otsu_baseline"), ("09_results", "inference_demo"),
                    ("09_results", "dense_counting"), ("09_results", "rgbd_feasibility"),
                }:
                    continue
            unexpected.append(relative.as_posix())
    check(not unexpected, "No unapproved heavy/model/raw payloads: " + str(unexpected[:10]))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        checks = validate(args.root.resolve())
    except Exception as exc:  # malformed workspace metadata should fail clearly
        print(f"FAIL | Validator exception: {exc}")
        return 1
    for passed, message in checks:
        print(("PASS" if passed else "FAIL") + " | " + message)
    failures = sum(not passed for passed, _ in checks)
    print(f"\nWorkspace validation: {len(checks) - failures} PASS / {failures} FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
