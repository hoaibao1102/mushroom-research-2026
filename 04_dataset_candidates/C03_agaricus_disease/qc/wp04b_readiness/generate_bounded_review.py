from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[4]
CANDIDATE = ROOT / "04_dataset_candidates" / "C03_agaricus_disease"
SOURCE = CANDIDATE / "source" / "extracted" / "Comprehensive Image Dataset of Agaricus bisporus Diseases Under Controlled Illumination Conditions"
OUT = Path(__file__).resolve().parent
PLATES = OUT / "review_plates"
SEED = 20261030

COUNTS = {
    "hl": {"white": 731, "uv": 728, "mix": 728},
    "bb": {"white": 576, "uv": 568, "mix": 493},
    "db": {"white": 665, "uv": 666, "mix": 632},
    "kw": {"white": 664, "uv": 675, "mix": 666},
    "wb": {"white": 559, "uv": 506, "mix": 546},
}
LIGHT_PAIRS = (("white", "uv"), ("white", "mix"), ("uv", "mix"))
VERDICTS = "SAME_VISIBLE_SPECIMEN|LIKELY_SAME_SPECIMEN|DIFFERENT_SPECIMEN|UNCERTAIN"


def relpath(light: str, cls: str, ordinal: int) -> Path:
    prefix = {"white": "w", "uv": "u", "mix": "m"}[light]
    if cls == "hl":
        folder = f"{prefix}0_hl"
        name = f"{prefix}0hl_{ordinal:04d}.jpg"
    else:
        folder = f"{prefix}1_{cls}"
        name = f"{prefix}_{cls}_{ordinal:04d}.jpg"
    return Path(light) / folder / name


def dhash(gray: np.ndarray) -> int:
    small = cv2.resize(gray, (9, 8), interpolation=cv2.INTER_AREA)
    return sum(int(v) << i for i, v in enumerate((small[:, 1:] > small[:, :-1]).ravel()))


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    den = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / den) if den else 0.0


def image_metrics(left: Path, right: Path) -> dict[str, float | int]:
    a = cv2.imread(str(left), cv2.IMREAD_COLOR)
    b = cv2.imread(str(right), cv2.IMREAD_COLOR)
    if a is None or b is None:
        raise RuntimeError(f"Decode failure: {left} / {right}")
    ga = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    gb = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    hamming = (dhash(ga) ^ dhash(gb)).bit_count()

    def norm_gray(g: np.ndarray) -> np.ndarray:
        g = cv2.resize(g, (128, 128), interpolation=cv2.INTER_AREA).astype(np.float32)
        return (g - g.mean()) / max(float(g.std()), 1e-6)

    na, nb = norm_gray(ga), norm_gray(gb)
    gray_corr = float(np.mean(na * nb))
    ea = cv2.Canny(cv2.resize(ga, (256, 256)), 60, 160).astype(np.float32).ravel()
    eb = cv2.Canny(cv2.resize(gb, (256, 256)), 60, 160).astype(np.float32).ravel()
    edge_cosine = cosine(ea, eb)

    def hsv_hist(img: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [24, 16], [0, 180, 0, 256]).ravel()
        return hist.astype(np.float32)

    hist_cosine = cosine(hsv_hist(a), hsv_hist(b))
    orb = cv2.ORB_create(nfeatures=500)
    ka, da = orb.detectAndCompute(ga, None)
    kb, db = orb.detectAndCompute(gb, None)
    good = []
    inliers = 0
    if da is not None and db is not None and len(da) >= 2 and len(db) >= 2:
        matches = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da, db, k=2)
        good = [m for m, n in matches if m.distance < 0.75 * n.distance]
        if len(good) >= 4:
            src = np.float32([ka[m.queryIdx].pt for m in good])
            dst = np.float32([kb[m.trainIdx].pt for m in good])
            _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
            inliers = int(mask.sum()) if mask is not None else 0
    return {
        "dhash_hamming": hamming,
        "gray_correlation": round(gray_corr, 6),
        "edge_cosine": round(edge_cosine, 6),
        "hsv_hist_cosine": round(hist_cosine, 6),
        "orb_ratio_matches": len(good),
        "orb_homography_inliers": inliers,
    }


def thumb(path: Path, normalized: bool = False) -> Image.Image:
    with Image.open(path) as src:
        img = src.convert("RGB")
    if normalized:
        img = ImageOps.autocontrast(img)
        img = ImageEnhance.Contrast(img).enhance(1.15)
    img.thumbnail((220, 220), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (220, 220), "white")
    canvas.paste(img, ((220 - img.width) // 2, (220 - img.height) // 2))
    return canvas


def plate(rows: list[dict[str, object]], path: Path, stratum: str) -> None:
    width, row_h = 940, 245
    sheet = Image.new("RGB", (width, 48 + row_h * len(rows)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((8, 8), f"C03 bounded review | {stratum} | native L/R + normalized L/R", fill="black", font=font)
    draw.text((8, 25), "Algorithmic review suggestions only; filenames/arm hidden from first-pass reviewer.", fill="black", font=font)
    for i, row in enumerate(rows):
        y = 48 + i * row_h
        left = SOURCE / str(row["left_relative_path"])
        right = SOURCE / str(row["right_relative_path"])
        for x, im in zip((0, 225, 470, 695), (thumb(left), thumb(right), thumb(left, True), thumb(right, True))):
            sheet.paste(im, (x, y + 20))
        draw.text((8, y + 3), f"{row['review_order']:03d} | {row['blinded_pair_id']}", fill="black", font=font)
    sheet.save(path, quality=92)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PLATES.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for cls in ("hl", "bb", "db", "kw", "wb"):
        for left_light, right_light in LIGHT_PAIRS:
            n = min(COUNTS[cls][left_light], COUNTS[cls][right_light])
            q = [1 + math.floor(j * (n - 1) / 7) for j in range(8)]
            tuples = [(q[i], q[i], "EQUAL_ORDINAL") for i in (0, 1, 3, 4, 6, 7)]
            tuples += [(q[2], q[5], "SHIFTED_CONTROL"), (q[5], q[2], "SHIFTED_CONTROL")]
            for idx, (lo, ro, arm) in enumerate(tuples, 1):
                lp, rp = relpath(left_light, cls, lo), relpath(right_light, cls, ro)
                la, ra = SOURCE / lp, SOURCE / rp
                if not la.is_file() or not ra.is_file():
                    raise FileNotFoundError(f"Missing designed pair: {la} / {ra}")
                pair_id = f"{cls}-{left_light}-{right_light}-{idx:02d}"
                rec: dict[str, object] = {
                    "pair_id": pair_id,
                    "blinded_pair_id": hashlib.sha256(pair_id.encode()).hexdigest()[:12],
                    "class_code": cls,
                    "left_light": left_light,
                    "right_light": right_light,
                    "left_ordinal": lo,
                    "right_ordinal": ro,
                    "selection_arm": arm,
                    "selection_rule_version": "C03_BOUNDED_V1",
                    "left_relative_path": lp.as_posix(),
                    "right_relative_path": rp.as_posix(),
                    **image_metrics(la, ra),
                    "reviewer_1_verdict": "",
                    "reviewer_2_verdict": "",
                    "adjudicated_verdict": "",
                    "allowed_verdicts": VERDICTS,
                    "review_notes": "",
                }
                rows.append(rec)
    if len(rows) != 120 or len({r["pair_id"] for r in rows}) != 120:
        raise AssertionError("Expected exactly 120 unique pairs")
    rng = random.Random(SEED)
    rng.shuffle(rows)
    for order, rec in enumerate(rows, 1):
        rec["review_order"] = order
    fields = list(rows[0])
    with (OUT / "bounded_similarity_review.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    index_rows = []
    by_stratum: dict[str, list[dict[str, object]]] = {}
    for rec in rows:
        key = f"{rec['class_code']}-{rec['left_light']}-{rec['right_light']}"
        by_stratum.setdefault(key, []).append(rec)
    for plate_no, key in enumerate(sorted(by_stratum), 1):
        cohort = sorted(by_stratum[key], key=lambda r: int(r["review_order"]))
        plate_path = PLATES / f"plate_{plate_no:02d}_{key}.jpg"
        plate(cohort, plate_path, key)
        for rec in cohort:
            index_rows.append({"plate": plate_path.relative_to(OUT).as_posix(), "review_order": rec["review_order"], "blinded_pair_id": rec["blinded_pair_id"], "pair_id": rec["pair_id"]})
    with (OUT / "image_review_index.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(index_rows[0]))
        writer.writeheader()
        writer.writerows(sorted(index_rows, key=lambda r: int(r["review_order"])))

    manifest = {
        "audit_id": "C03_bounded_cross_illumination_grouping_audit_v1",
        "status": "ALGORITHMIC_SUGGESTIONS_GENERATED_HUMAN_VERDICTS_PENDING",
        "seed": SEED,
        "pair_count": len(rows),
        "strata": len(by_stratum),
        "equal_ordinal_pairs": sum(r["selection_arm"] == "EQUAL_ORDINAL" for r in rows),
        "shifted_controls": sum(r["selection_arm"] == "SHIFTED_CONTROL" for r in rows),
        "biological_independence": "NOT_VERIFIED",
        "hard_warning": "Scores and equal ordinals are review suggestions, not specimen identity. No split or training is authorized.",
        "files": ["bounded_similarity_review.csv", "image_review_index.csv", *[p.name for p in sorted(PLATES.glob("*.jpg"))]],
    }
    (OUT / "bounded_review_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
