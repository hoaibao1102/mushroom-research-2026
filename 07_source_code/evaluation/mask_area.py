#!/usr/bin/env python3
"""Visible mask area at ORIGINAL image resolution, per instance.

    A_px2 = sum(binary_mask > 0)

Unit: px^2 (pixels squared). Physical calibration (mm^2) is NOT_VERIFIED and not used.
Area is computed from the instance mask, never from the bounding box.

Usage (Colab):
    python mask_area.py --coco-json <.../train/annotations_coco.json> \
        --image-dir <.../train/rgb> --out-csv 09_results/metrics/wb_area_sanity.csv
Also pytest-compatible (test_* functions).
"""
from __future__ import annotations
import argparse, csv, sys
from decimal import Decimal
from pathlib import Path
import numpy as np

WB_KEYS = {"wb", "whitebutton"}


def mask_area_px2(mask) -> int:
    """Area of one instance mask in px^2 = number of pixels with value > 0."""
    a = np.asarray(mask)
    if a.ndim != 2:
        raise ValueError(f"mask must be 2-D (H, W), got shape {a.shape}")
    if a.dtype.kind == "f" and np.isnan(a).any():
        raise ValueError("mask contains NaN")
    return int(np.count_nonzero(a > 0))


def instance_areas_px2(masks) -> list:
    """Per-instance areas for an (N,H,W) array or an iterable of (H,W) masks (no union, no bbox)."""
    return [mask_area_px2(m) for m in masks]


def polygon_to_mask(segmentation, height: int, width: int) -> np.ndarray:
    """Rasterise a COCO polygon segmentation (list of rings) to a (H,W) uint8 mask at original size."""
    try:
        from pycocotools import mask as mu
        return mu.decode(mu.merge(mu.frPyObjects(segmentation, height, width)))
    except ImportError:
        import cv2
        m = np.zeros((height, width), np.uint8)
        for r in segmentation:
            pts = np.round(np.asarray(r, float).reshape(-1, 2)).astype(np.int32)
            cv2.fillPoly(m, [pts], 1)
        return m


# ----------------------------------------------------------------------------- synthetic tests
def _rect(h, w, y0, y1, x0, x1, val=1, dtype=np.uint8):
    m = np.zeros((h, w), dtype)
    m[y0:y1, x0:x1] = val
    return m


def synthetic_cases():
    """(case, mask, expected_area_px2) with analytically known areas."""
    tri = np.tril(np.ones((10, 10), np.uint8))  # staircase: area 55, bbox 100
    two = _rect(50, 50, 0, 5, 0, 5) + _rect(50, 50, 20, 30, 20, 40)  # 25 + 200 disjoint
    return [
        ("empty_mask", np.zeros((64, 64), np.uint8), 0),
        ("single_pixel", _rect(32, 32, 5, 6, 7, 8), 1),
        ("rect_10x20_uint8", _rect(100, 100, 10, 20, 30, 50), 200),
        ("rect_value_255", _rect(100, 100, 10, 20, 30, 50, val=255), 200),
        ("rect_bool", _rect(100, 100, 10, 20, 30, 50, val=True, dtype=bool), 200),
        ("rect_float_0.5", _rect(100, 100, 10, 20, 30, 50, val=0.5, dtype=np.float32), 200),
        ("full_frame_1080x1920", np.ones((1080, 1920), np.uint8), 1080 * 1920),
        ("two_disjoint_components", two, 225),
        ("staircase_not_bbox", tri, 55),
        ("checkerboard_half", (np.indices((40, 40)).sum(0) % 2).astype(np.uint8), 800),
    ]


def test_synthetic_areas():
    for name, m, exp in synthetic_cases():
        assert mask_area_px2(m) == exp, (name, mask_area_px2(m), exp)


def test_per_instance_not_union_not_bbox():
    a = _rect(30, 30, 0, 10, 0, 10)       # 100
    b = _rect(30, 30, 5, 15, 5, 15)       # 100, overlaps a by 25
    assert instance_areas_px2([a, b]) == [100, 100]          # per instance, overlap counted in each
    assert instance_areas_px2(np.stack([a, b])) == [100, 100]
    tri = np.tril(np.ones((10, 10), np.uint8))
    ys, xs = np.nonzero(tri)
    bbox = (ys.max() - ys.min() + 1) * (xs.max() - xs.min() + 1)
    assert bbox == 100 and mask_area_px2(tri) == 55 and mask_area_px2(tri) != bbox


def test_rejects_bad_shapes():
    for bad in (np.zeros((3, 4, 4)), np.zeros(5)):
        try:
            mask_area_px2(bad)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")


def run_synthetic_tests():
    rows, ok = [], True
    for name, m, exp in synthetic_cases():
        got = mask_area_px2(m)
        ok &= got == exp
        rows.append([f"synthetic_{name}", exp, got, abs(got - exp), "synthetic mask, analytic area"])
    for fn in (test_synthetic_areas, test_per_instance_not_union_not_bbox, test_rejects_bad_shapes):
        try:
            fn(); print(f"PASS {fn.__name__}")
        except AssertionError as e:
            ok = False; print(f"FAIL {fn.__name__}: {e}")
    return rows, ok


# ----------------------------------------------------------------------------- real COCO masks
def _clean(o):
    if isinstance(o, Decimal): return float(o)
    if isinstance(o, list): return [_clean(x) for x in o]
    if isinstance(o, dict): return {k: _clean(v) for k, v in o.items()}
    return o


def _items(path, prefix):
    try:
        import ijson
        use = ijson.backend != "python"
    except ImportError:
        ijson, use = None, False
    if use:
        with open(path, "rb") as f:
            for it in ijson.items(f, prefix + ".item"):
                yield _clean(it)
    else:
        import json
        with open(path) as f:
            for it in json.load(f).get(prefix, []):
                yield it


def real_coco_rows(coco_json, image_dir=None, n=3, wb_ids=None):
    """Use the first n non-crowd polygon WB annotations of the COCO file as real masks."""
    norm = lambda s: "".join(c for c in str(s).lower() if c.isalnum())
    cats = list(_items(coco_json, "categories"))
    if wb_ids is None:
        wb_ids = {c["id"] for c in cats if norm(c.get("name", "")) in WB_KEYS}
    if not wb_ids:
        raise RuntimeError(f"WB category not found; categories={cats}")
    imgs = {i["id"]: i for i in _items(coco_json, "images")}
    rows, found = [], 0
    for a in _items(coco_json, "annotations"):
        seg = a.get("segmentation")
        if a.get("category_id") not in wb_ids or a.get("iscrowd", 0) or not isinstance(seg, list) or not seg:
            continue
        seg = [r for r in seg if isinstance(r, list) and len(r) >= 6]
        im = imgs.get(a["image_id"])
        if not seg or im is None:
            continue
        h, w = int(im["height"]), int(im["width"])
        size_note = "image file not checked"
        if image_dir is not None:
            p = Path(image_dir) / im["file_name"]
            if not p.exists():
                p = Path(image_dir) / Path(im["file_name"]).name
            if p.exists():
                from PIL import Image
                with Image.open(p) as I:
                    size_note = "image size matches COCO" if I.size == (w, h) else f"SIZE MISMATCH file={I.size} coco={(w, h)}"
        mask = polygon_to_mask(seg, h, w)
        measured = mask_area_px2(mask)
        src = f"COCO ann_id={a['id']} image_id={a['image_id']} {w}x{h}; {size_note}"
        try:
            from pycocotools import mask as mu
            exp = int(mu.area(mu.merge(mu.frPyObjects(seg, h, w))))
            rows.append([f"real_coco_ann{a['id']}_pycocotools", exp, measured, abs(measured - exp),
                         src + "; expected=pycocotools RLE area of same polygon"])
        except ImportError:
            rows.append([f"real_coco_ann{a['id']}", "NOT_VERIFIED", measured, "NOT_VERIFIED", src + "; pycocotools missing"])
        try:
            import cv2
            m2 = np.zeros((h, w), np.uint8)
            for r in seg:
                cv2.fillPoly(m2, [np.round(np.asarray(r, float).reshape(-1, 2)).astype(np.int32)], 1)
            if rows[-1][1] != "NOT_VERIFIED":
                m = mask_area_px2(m2)
                rows.append([f"real_coco_ann{a['id']}_cv2_crosscheck", rows[-1][1], m, abs(m - rows[-1][1]),
                             src + "; independent cv2.fillPoly rasterisation (non-zero error = rasterisation-rule difference, not a function bug)"])
        except ImportError:
            pass
        found += 1
        if found >= n:
            break
    if not rows:
        raise RuntimeError("no usable non-crowd WB polygon annotation found")
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--coco-json")
    ap.add_argument("--image-dir")
    ap.add_argument("--out-csv", default="09_results/metrics/wb_area_sanity.csv")
    ap.add_argument("--n-real", type=int, default=3)
    a = ap.parse_args(argv)
    rows, ok = run_synthetic_tests()
    if a.coco_json:
        try:
            rows += real_coco_rows(a.coco_json, a.image_dir, a.n_real)
        except Exception as e:  # keep synthetic results, flag real as not verified
            rows.append(["real_coco_mask", "NOT_VERIFIED", "NOT_VERIFIED", "NOT_VERIFIED", f"FAILED: {type(e).__name__}: {e}"])
            ok = False
    else:
        rows.append(["real_coco_mask", "NOT_VERIFIED", "NOT_VERIFIED", "NOT_VERIFIED", "--coco-json not given"])
    out = Path(a.out_csv); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case", "expected_area_px2", "measured_area_px2", "absolute_error_px2", "source"])
        w.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows); unit = px^2")
    for r in rows: print(r[:4])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
