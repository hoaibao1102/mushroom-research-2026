"""Validate WP-05 bounded candidate screening without downloading or training."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = [
    "setup_reports/WP-05_DECISION_SCREENING_REPORT.md",
    "03_dataset_discovery/dataset_comparisons/WP-05_DECISION_MATRIX.md",
    "03_dataset_discovery/screening_reports/WP-05_FALLBACK_CANDIDATES.md",
    "03_dataset_discovery/screening_reports/WP-05_RECOMMENDATION.md",
    "02_literature_review/author_correspondence/C03_FOLLOWUP_CHECKLIST.md",
]
RECEIPT = ROOT / "setup_reports/WP-05_VALIDATION.json"
EXPECTED_WP04C = "69215062f29d0d9bfe3ce194eafb4001097d8138"
ALLOWED = tuple(OUTPUTS) + ("setup_reports/WP-05_VALIDATION.json", "scripts/validate_wp05.py")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


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

    paths = [ROOT / p for p in OUTPUTS]
    check("five_non_validation_outputs_exist", all(p.is_file() and p.stat().st_size > 500 for p in paths), OUTPUTS)
    check("wp05_branch", git("branch", "--show-current") == "research/wp-05-candidate-decision")
    check("wp04c_parent_checkpoint", git("rev-parse", "HEAD") == EXPECTED_WP04C, git("rev-parse", "HEAD"))
    check("wp04c_remote_readback", git("rev-parse", "origin/research/wp-04c-final-decision") == EXPECTED_WP04C)

    report = paths[0].read_text(encoding="utf-8")
    matrix = paths[1].read_text(encoding="utf-8")
    fallback = paths[2].read_text(encoding="utf-8")
    recommendation = paths[3].read_text(encoding="utf-8")
    checklist = paths[4].read_text(encoding="utf-8")
    combined = "\n".join((report, matrix, fallback, recommendation, checklist))

    check("exactly_three_fallbacks", all(f"## {c}" in fallback for c in ("C04", "C05", "C08")) and "## C06" not in fallback and "## C07" not in fallback)
    check("c03_state_preserved", "CONDITIONAL_GO" in combined and "NO_GO_FOR_PRIMARY_GENERALIZATION" in combined)
    check("no_final_selection", "No candidate is ready for selection or training" in report and "No final candidate is selected" in matrix)
    check("gates_remain_no", all(token in report for token in ("**Dataset selected:** `NO`", "**Training authorized:** `NO`", "**Research gap validated:** `NO`")))
    check("c03_inquiry_not_sent", "DRAFT_NOT_SENT" in checklist and "Send manually" in checklist)
    check("deadline_present", "2026-11-06" in combined)
    check("unknowns_not_scored", "Unknown evidence is not assigned a numerical score" in matrix)
    check("candidate_decisions", "C04: shiitake phenotype detection — `HOLD`" in report and "C05: white-button RGB-D time series — `CONDITIONAL_GO`" in report and "C08: M18K detection/pose/growth — `HOLD`" in report)

    registry = (ROOT / "03_dataset_discovery/candidate_registry/WP-03_NEW_CANDIDATES.csv").read_text(encoding="utf-8")
    required_ids = ("10.5281/zenodo.20373531", "10.17632/8n6nr43gk3.1", "10.3390/s26061935", "10.3390/computers14050199")
    check("candidate_identifiers_trace_to_registry", all(i in registry for i in required_ids), required_ids)

    raw = subprocess.run(["git", "status", "--porcelain=v1", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    changed = [entry.decode("utf-8", errors="replace")[3:] for entry in raw.split(b"\0") if entry]
    unauthorized = [p for p in changed if p not in ALLOWED]
    check("only_wp05_paths_changed", not unauthorized, unauthorized)
    forbidden_ext = {".jpg", ".jpeg", ".png", ".zip", ".rar", ".7z", ".pt", ".pth", ".ckpt", ".onnx", ".safetensors"}
    check("no_new_dataset_or_model_payload", not [p for p in changed if Path(p).suffix.lower() in forbidden_ext])
    check("no_ds02_reuse", not [p for p in changed if "ds-02" in p.lower() or "hf55tkx489" in p.lower()])
    check("no_experiment_or_selected_research_outputs", not [p for p in changed if p.startswith(("08_experiments/", "06_selected_research/"))])
    check("tracked_history_unchanged", not git("diff", "--name-only"), git("diff", "--name-only"))

    artifacts = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)} for p in paths]
    artifacts.append({"path": "scripts/validate_wp05.py", "bytes": Path(__file__).stat().st_size, "sha256": sha256(Path(__file__))})
    status = "PASS" if all(c["passed"] for c in checks) else "FAIL"
    return {
        "work_package": "WP-05",
        "validator": "bounded screening structural and internal-consistency verifier",
        "status": status,
        "python": sys.version,
        "checks": checks,
        "artifacts": artifacts,
        "candidate_scope": {"fallback_count": 3, "fallback_ids": ["C04", "C05", "C08"], "new_candidate_search": "NOT_RUN"},
        "authorization": {"dataset_selected": "NO", "training_authorized": "NO", "research_gap_validated": "NO", "final_topic_selected": "NO", "wp05_committed_or_pushed": "NO"},
        "non_execution": {"dataset_download": "NOT_RUN", "model_training": "NOT_RUN", "split_creation": "NOT_RUN", "ds02_reuse": "NOT_RUN", "specimen_id_fabrication": "NOT_RUN"},
        "scientific_note": "PASS validates bounded artifact consistency, not candidate scientific acceptance or reproduced performance.",
    }


def main() -> int:
    result = run()
    RECEIPT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    for item in result["checks"]:
        print(("PASS" if item["passed"] else "FAIL"), "|", item["name"], "|", item["detail"])
    print("WP-05 validation:", result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
