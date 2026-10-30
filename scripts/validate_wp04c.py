"""Validate WP-04C decision artifacts without contacting authors or reading raw images."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = [
    "setup_reports/WP-04C_DECISION_REPORT.md",
    "02_literature_review/author_correspondence/C03_AUTHOR_INQUIRY.md",
    "02_literature_review/author_correspondence/C03_CORRESPONDENCE_TRACKER.csv",
    "03_dataset_discovery/source_verification/C03_FINAL_PROVENANCE_STATUS.md",
    "05_research_protocols/C03_ESTIMAND_FEASIBILITY_MATRIX.md",
    "02_literature_review/research_gap_analysis/C03_GAP_DECISION.md",
    "03_dataset_discovery/screening_reports/C03_GO_NO_GO_RECOMMENDATION.md",
]
RECEIPT = ROOT / "setup_reports/WP-04C_VALIDATION.json"
EXPECTED_WP04B = "3f45000f0bf2299d9eb7ecf7376dbc1592af1e57"
CONTACT = "ugur.coruh@erdogan.edu.tr"
SOURCE_XML = ROOT / "03_dataset_discovery/source_verification/wp03_stream_a/paper_xml_alternate.txt"
ALLOWED_PREFIXES = (
    "setup_reports/WP-04C_",
    "02_literature_review/author_correspondence/",
    "02_literature_review/research_gap_analysis/C03_GAP_DECISION.md",
    "03_dataset_discovery/source_verification/C03_FINAL_PROVENANCE_STATUS.md",
    "05_research_protocols/C03_ESTIMAND_FEASIBILITY_MATRIX.md",
    "03_dataset_discovery/screening_reports/C03_GO_NO_GO_RECOMMENDATION.md",
    "scripts/validate_wp04c.py",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def run() -> dict:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: object = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    paths = [ROOT / p for p in OUTPUTS]
    check("seven_non_validation_outputs_exist", all(p.is_file() and p.stat().st_size > 300 for p in paths), OUTPUTS)

    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/research/wp-04b-c03-readiness")
    check("wp04b_checkpoint_at_expected_sha", head == EXPECTED_WP04B, head)
    check("wp04b_remote_tracking_matches", remote == EXPECTED_WP04B, remote)
    check("wp04c_branch", git("branch", "--show-current") == "research/wp-04c-final-decision")

    xml = SOURCE_XML.read_text(encoding="utf-8")
    check("verified_contact_in_primary_xml", f"<email>{CONTACT}</email>" in xml and 'ref-type="corresp"' in xml)

    inquiry = (ROOT / OUTPUTS[1]).read_text(encoding="utf-8")
    check("inquiry_not_sent", "DRAFT_NOT_SENT" in inquiry and "NOT_SENT" in inquiry)
    check("inquiry_has_verified_recipient", f"To: {CONTACT}" in inquiry)
    numbered = re.findall(r"(?m)^([1-7])\. ", inquiry)
    check("inquiry_has_seven_questions", numbered == list("1234567"), numbered)
    check("inquiry_requests_non_sensitive_metadata", "do not need sensitive farm names" in inquiry)

    with (ROOT / OUTPUTS[2]).open(encoding="utf-8-sig", newline="") as handle:
        tracker = list(csv.DictReader(handle))
    required = {"contact_source", "contact_date", "questions", "response_status", "evidence_received", "remaining_blockers"}
    check("tracker_schema_and_seven_rows", len(tracker) == 7 and required.issubset(tracker[0]), len(tracker))
    check("tracker_has_no_fabricated_contact_or_response", all(not r["contact_date"] and r["response_status"] == "DRAFT_NOT_SENT" and r["evidence_received"] == "NONE" for r in tracker))

    matrix = (ROOT / OUTPUTS[4]).read_text(encoding="utf-8")
    check("four_estimands_separated", all(token in matrix for token in ("A. Image-level", "B. Performance under changing illumination", "C. Previously unseen biological specimens", "D. Unseen farms")))
    check("no_a_b_to_c_d_overclaim", "A estimates performance on released files only" in matrix and "Neither A nor B proves D" in matrix)

    combined = "\n".join(p.read_text(encoding="utf-8") for p in paths if p.suffix == ".md")
    check("decision_scope_is_explicit", "CONDITIONAL_GO" in combined and "NO_GO_FOR_PRIMARY_GENERALIZATION" in combined and "GO` — not recommended" in combined)
    check("gates_not_promoted", all(token in combined for token in ("Dataset selected: `NO`", "Training authorized: `NO`", "Research gap validated: `NO`")))
    check("deadline_and_no_rejection_claim", "2026-11-06" in combined and "does not mean rejection" in combined)
    check("no_training_or_split_claim", "No split created; no model trained" in matrix and "NOT_AUTHORIZED" in combined)

    status_raw = subprocess.run(["git", "status", "--porcelain=v1", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    changed = [entry.decode("utf-8", errors="replace")[3:] for entry in status_raw.split(b"\0") if entry]
    unauthorized = [p for p in changed if not p.startswith(ALLOWED_PREFIXES)]
    check("git_changes_only_wp04c_authorized_paths", not unauthorized, unauthorized)
    forbidden_ext = {".pt", ".pth", ".ckpt", ".onnx", ".safetensors", ".zip", ".rar", ".7z"}
    check("no_new_model_or_archive", not [p for p in changed if Path(p).suffix.lower() in forbidden_ext])
    check("no_ds02_path", not [p for p in changed if "ds-02" in p.lower() or "hf55tkx489" in p.lower()])
    check("no_experiment_or_split_outputs", not [p for p in changed if p.startswith(("08_experiments/", "06_selected_research/")) or "split" in Path(p).name.lower()])

    tracked_diff = git("diff", "--name-only")
    check("previous_tracked_reports_unchanged", not tracked_diff, tracked_diff)

    artifacts = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)} for p in paths]
    artifacts.append({"path": SOURCE_XML.relative_to(ROOT).as_posix(), "bytes": SOURCE_XML.stat().st_size, "sha256": digest(SOURCE_XML), "role": "primary_contact_source"})
    artifacts.append({"path": "scripts/validate_wp04c.py", "bytes": Path(__file__).stat().st_size, "sha256": digest(Path(__file__))})

    passed = all(c["passed"] for c in checks)
    return {
        "work_package": "WP-04C",
        "validator": "phase-specific structural and internal-consistency verifier",
        "status": "PASS" if passed else "FAIL",
        "python": sys.version,
        "checks": checks,
        "artifacts": artifacts,
        "authorization": {
            "dataset_selected": "NO",
            "training_authorized": "NO",
            "research_gap_validated": "NO",
            "final_topic_selected": "NO",
            "author_inquiry_sent": "NO",
            "wp04c_committed_or_pushed": "NO",
        },
        "non_execution": {
            "model_training": "NOT_RUN",
            "split_creation": "NOT_RUN",
            "ds02_import": "NOT_RUN",
            "dataset_modification": "NOT_RUN",
            "background_monitoring": "NOT_SCHEDULED",
        },
        "scientific_note": "PASS validates artifact consistency and gate wording; it does not resolve biological provenance, labels, novelty, or author response.",
    }


def main() -> int:
    result = run()
    RECEIPT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    for item in result["checks"]:
        print(("PASS" if item["passed"] else "FAIL"), "|", item["name"], "|", item["detail"])
    print("WP-04C validation:", result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
