"""Validate WP-04B artifacts without reading or modifying raw images."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REPORTS = [
    "setup_reports/WP-04B_READINESS_REPORT.md",
    "03_dataset_discovery/screening_reports/C03_FINAL_FEASIBILITY_DECISION.md",
    "03_dataset_discovery/source_verification/C03_SPECIMEN_GROUPING_AUDIT.md",
    "03_dataset_discovery/source_verification/C03_LABEL_SEMANTICS_AUDIT.md",
    "02_literature_review/methodology_comparison/C03_PAPER_REPRODUCTION_MATRIX.md",
    "05_research_protocols/C03_PROPOSED_EVALUATION_PROTOCOL.md",
    "02_literature_review/research_gap_analysis/C03_GAP_PRESCREEN.md",
]
LOCAL = ROOT / "04_dataset_candidates/C03_agaricus_disease/qc/wp04b_readiness"
RECEIPT = ROOT / "setup_reports/WP-04B_VALIDATION.json"
VERDICTS = {"SAME_VISIBLE_SPECIMEN", "LIKELY_SAME_SPECIMEN", "DIFFERENT_SPECIMEN", "UNCERTAIN"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run() -> dict:
    checks: list[dict[str, object]] = []
    def check(name: str, passed: bool, detail: object = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    paths = [ROOT / p for p in REPORTS]
    check("required_reports_nonempty", all(p.is_file() and p.stat().st_size > 500 for p in paths), [p.relative_to(ROOT).as_posix() for p in paths])

    review = LOCAL / "bounded_similarity_review.csv"
    with review.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    check("exactly_120_unique_pairs", len(rows) == 120 and len({r["pair_id"] for r in rows}) == 120, len(rows))
    check("exactly_15_strata", len({(r["class_code"], r["left_light"], r["right_light"]) for r in rows}) == 15)
    arms = Counter(r["selection_arm"] for r in rows)
    check("bounded_arms_90_30", arms == {"EQUAL_ORDINAL": 90, "SHIFTED_CONTROL": 30}, dict(arms))
    check("paths_are_c03_relative_jpegs", all(".." not in Path(r[k]).parts and Path(r[k]).suffix.lower() == ".jpg" for r in rows for k in ("left_relative_path", "right_relative_path")))
    check("human_verdicts_blank", all(not r["reviewer_1_verdict"] and not r["reviewer_2_verdict"] and not r["adjudicated_verdict"] for r in rows))
    check("ai_screening_typed_separately", all(r["ai_screening_verdict"] in VERDICTS and r["ai_screening_status"] == "AI_SCREENING_NOT_HUMAN_ADJUDICATION" for r in rows))
    screen = Counter(r["ai_screening_verdict"] for r in rows)
    check("screening_totals", screen == {"DIFFERENT_SPECIMEN": 63, "LIKELY_SAME_SPECIMEN": 28, "SAME_VISIBLE_SPECIMEN": 20, "UNCERTAIN": 9}, dict(screen))

    plates = sorted((LOCAL / "review_plates").glob("*.jpg"))
    plate_ok = len(plates) == 15
    for plate in plates:
        try:
            with Image.open(plate) as image:
                image.verify()
        except Exception:
            plate_ok = False
    check("15_review_plates_decode", plate_ok, len(plates))

    decision = (ROOT / REPORTS[1]).read_text(encoding="utf-8")
    readiness = (ROOT / REPORTS[0]).read_text(encoding="utf-8")
    protocol = (ROOT / REPORTS[5]).read_text(encoding="utf-8")
    check("decision_conditional_go", "`CONDITIONAL_GO`" in decision)
    check("training_not_authorized", "Training authorized: `NO`" in decision and "`TRAINING_NOT_AUTHORIZED`" in protocol)
    check("dataset_selection_pending", "Dataset selected: `NO / PENDING`" in decision and "**Dataset selection:** `PENDING`" in readiness)
    check("research_gap_unvalidated", "Research gap validated: `NO`" in decision and "**Research gap:** `UNVALIDATED`" in readiness)
    check("biological_independence_not_verified", "BIOLOGICAL_INDEPENDENCE_NOT_VERIFIED" in readiness)

    changed = subprocess.run(["git", "status", "--porcelain=v1", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.split(b"\0")
    new_paths = [x.decode("utf-8", errors="replace")[3:] for x in changed if x]
    forbidden_ext = {".pt", ".pth", ".ckpt", ".onnx", ".safetensors", ".zip", ".rar", ".7z"}
    forbidden = [p for p in new_paths if Path(p).suffix.lower() in forbidden_ext]
    check("no_new_model_or_archive_payload", not forbidden, forbidden)
    ds02 = [p for p in new_paths if "ds-02" in p.lower() or "hf55tkx489" in p.lower()]
    check("no_new_ds02_paths", not ds02, ds02)
    experiment_paths = [p for p in new_paths if p.startswith("08_experiments/")]
    check("no_experiment_or_checkpoint_outputs", not experiment_paths, experiment_paths)

    literature = list(csv.DictReader((LOCAL / "literature_registry.csv").open(encoding="utf-8-sig", newline="")))
    check("literature_registry_unique", len(literature) == 10 and len({r["doi_or_record"].lower() for r in literature}) == 10)

    artifact_paths = paths + [review, LOCAL / "image_review_index.csv", LOCAL / "ai_screening_summary.csv", LOCAL / "bounded_review_manifest.json", LOCAL / "literature_registry.csv", LOCAL / "source_metadata_verification.json", LOCAL / "generate_bounded_review.py", LOCAL / "apply_ai_screening.py", ROOT / "scripts/validate_wp04b.py", ROOT / "setup_reports/WP-04B_COMMAND_RECEIPT.json"] + plates
    artifacts = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)} for p in artifact_paths]
    return {
        "work_package": "WP-04B",
        "validator": "phase-specific structural and internal-consistency verifier",
        "python": sys.version,
        "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
        "checks": checks,
        "artifacts": artifacts,
        "prohibited_actions": {"model_training": "NOT_RUN", "split_creation": "NOT_RUN", "ds02_import": "NOT_RUN", "dataset_modification": "NOT_RUN"},
        "scientific_note": "PASS validates artifact consistency; it does not verify biological independence or adjudicate labels.",
    }


def main() -> int:
    result = run()
    RECEIPT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    for item in result["checks"]:
        print(("PASS" if item["passed"] else "FAIL"), "|", item["name"], "|", item["detail"])
    print("WP-04B validation:", result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
