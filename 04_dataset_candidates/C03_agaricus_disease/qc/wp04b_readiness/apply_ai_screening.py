from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "bounded_similarity_review.csv"

# Blinded, plate-level AI screening. These are not human reviewer verdicts and
# never populate reviewer/adjudication fields or create grouping edges.
SCREENING = {
    1:"DIFFERENT_SPECIMEN",2:"DIFFERENT_SPECIMEN",3:"SAME_VISIBLE_SPECIMEN",4:"UNCERTAIN",5:"DIFFERENT_SPECIMEN",
    6:"DIFFERENT_SPECIMEN",7:"DIFFERENT_SPECIMEN",8:"DIFFERENT_SPECIMEN",9:"LIKELY_SAME_SPECIMEN",10:"SAME_VISIBLE_SPECIMEN",
    11:"LIKELY_SAME_SPECIMEN",12:"DIFFERENT_SPECIMEN",13:"DIFFERENT_SPECIMEN",14:"DIFFERENT_SPECIMEN",15:"DIFFERENT_SPECIMEN",
    16:"SAME_VISIBLE_SPECIMEN",17:"DIFFERENT_SPECIMEN",18:"LIKELY_SAME_SPECIMEN",19:"DIFFERENT_SPECIMEN",20:"DIFFERENT_SPECIMEN",
    21:"DIFFERENT_SPECIMEN",22:"LIKELY_SAME_SPECIMEN",23:"DIFFERENT_SPECIMEN",24:"DIFFERENT_SPECIMEN",25:"DIFFERENT_SPECIMEN",
    26:"LIKELY_SAME_SPECIMEN",27:"DIFFERENT_SPECIMEN",28:"SAME_VISIBLE_SPECIMEN",29:"SAME_VISIBLE_SPECIMEN",30:"LIKELY_SAME_SPECIMEN",
    31:"DIFFERENT_SPECIMEN",32:"LIKELY_SAME_SPECIMEN",33:"SAME_VISIBLE_SPECIMEN",34:"DIFFERENT_SPECIMEN",35:"DIFFERENT_SPECIMEN",
    36:"DIFFERENT_SPECIMEN",37:"LIKELY_SAME_SPECIMEN",38:"DIFFERENT_SPECIMEN",39:"DIFFERENT_SPECIMEN",40:"SAME_VISIBLE_SPECIMEN",
    41:"SAME_VISIBLE_SPECIMEN",42:"LIKELY_SAME_SPECIMEN",43:"LIKELY_SAME_SPECIMEN",44:"UNCERTAIN",45:"LIKELY_SAME_SPECIMEN",
    46:"LIKELY_SAME_SPECIMEN",47:"DIFFERENT_SPECIMEN",48:"DIFFERENT_SPECIMEN",49:"SAME_VISIBLE_SPECIMEN",50:"DIFFERENT_SPECIMEN",
    51:"SAME_VISIBLE_SPECIMEN",52:"SAME_VISIBLE_SPECIMEN",53:"DIFFERENT_SPECIMEN",54:"DIFFERENT_SPECIMEN",55:"DIFFERENT_SPECIMEN",
    56:"LIKELY_SAME_SPECIMEN",57:"DIFFERENT_SPECIMEN",58:"SAME_VISIBLE_SPECIMEN",59:"UNCERTAIN",60:"DIFFERENT_SPECIMEN",
    61:"SAME_VISIBLE_SPECIMEN",62:"LIKELY_SAME_SPECIMEN",63:"SAME_VISIBLE_SPECIMEN",64:"DIFFERENT_SPECIMEN",65:"SAME_VISIBLE_SPECIMEN",
    66:"LIKELY_SAME_SPECIMEN",67:"LIKELY_SAME_SPECIMEN",68:"DIFFERENT_SPECIMEN",69:"SAME_VISIBLE_SPECIMEN",70:"DIFFERENT_SPECIMEN",
    71:"DIFFERENT_SPECIMEN",72:"SAME_VISIBLE_SPECIMEN",73:"LIKELY_SAME_SPECIMEN",74:"DIFFERENT_SPECIMEN",75:"UNCERTAIN",
    76:"DIFFERENT_SPECIMEN",77:"DIFFERENT_SPECIMEN",78:"UNCERTAIN",79:"LIKELY_SAME_SPECIMEN",80:"UNCERTAIN",
    81:"LIKELY_SAME_SPECIMEN",82:"LIKELY_SAME_SPECIMEN",83:"LIKELY_SAME_SPECIMEN",84:"DIFFERENT_SPECIMEN",85:"SAME_VISIBLE_SPECIMEN",
    86:"UNCERTAIN",87:"LIKELY_SAME_SPECIMEN",88:"DIFFERENT_SPECIMEN",89:"DIFFERENT_SPECIMEN",90:"DIFFERENT_SPECIMEN",
    91:"LIKELY_SAME_SPECIMEN",92:"DIFFERENT_SPECIMEN",93:"DIFFERENT_SPECIMEN",94:"DIFFERENT_SPECIMEN",95:"DIFFERENT_SPECIMEN",
    96:"DIFFERENT_SPECIMEN",97:"LIKELY_SAME_SPECIMEN",98:"DIFFERENT_SPECIMEN",99:"UNCERTAIN",100:"DIFFERENT_SPECIMEN",
    101:"DIFFERENT_SPECIMEN",102:"DIFFERENT_SPECIMEN",103:"DIFFERENT_SPECIMEN",104:"DIFFERENT_SPECIMEN",105:"DIFFERENT_SPECIMEN",
    106:"SAME_VISIBLE_SPECIMEN",107:"DIFFERENT_SPECIMEN",108:"DIFFERENT_SPECIMEN",109:"LIKELY_SAME_SPECIMEN",110:"LIKELY_SAME_SPECIMEN",
    111:"DIFFERENT_SPECIMEN",112:"LIKELY_SAME_SPECIMEN",113:"DIFFERENT_SPECIMEN",114:"DIFFERENT_SPECIMEN",115:"DIFFERENT_SPECIMEN",
    116:"UNCERTAIN",117:"DIFFERENT_SPECIMEN",118:"DIFFERENT_SPECIMEN",119:"SAME_VISIBLE_SPECIMEN",120:"LIKELY_SAME_SPECIMEN",
}


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 120 or set(SCREENING) != set(range(1, 121)):
        raise AssertionError("Expected complete 120-pair screening")
    for row in rows:
        order = int(row["review_order"])
        row["ai_screening_verdict"] = SCREENING[order]
        row["ai_screening_status"] = "AI_SCREENING_NOT_HUMAN_ADJUDICATION"
        row["ai_screening_note"] = "Plate-level visible morphology review; does not establish biological identity or create a grouping edge."
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    overall = Counter(row["ai_screening_verdict"] for row in rows)
    by_arm: dict[str, Counter[str]] = defaultdict(Counter)
    by_stratum: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        verdict = row["ai_screening_verdict"]
        by_arm[row["selection_arm"]][verdict] += 1
        key = f"{row['class_code']}:{row['left_light']}-{row['right_light']}"
        by_stratum[key][verdict] += 1
    summary_path = ROOT / "ai_screening_summary.csv"
    with summary_path.open("w", encoding="utf-8-sig", newline="") as handle:
        fields = ["scope", "key", "SAME_VISIBLE_SPECIMEN", "LIKELY_SAME_SPECIMEN", "DIFFERENT_SPECIMEN", "UNCERTAIN", "total"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        def emit(scope: str, key: str, counts: Counter[str]) -> None:
            writer.writerow({"scope":scope,"key":key,**{v:counts[v] for v in ("SAME_VISIBLE_SPECIMEN","LIKELY_SAME_SPECIMEN","DIFFERENT_SPECIMEN","UNCERTAIN")},"total":sum(counts.values())})
        emit("overall", "all", overall)
        for key in sorted(by_arm): emit("selection_arm", key, by_arm[key])
        for key in sorted(by_stratum): emit("stratum", key, by_stratum[key])
    print("overall", dict(overall))
    print("by_arm", {k:dict(v) for k,v in by_arm.items()})


if __name__ == "__main__":
    main()
