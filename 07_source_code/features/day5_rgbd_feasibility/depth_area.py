#!/usr/bin/env python3
"""Day 5: can M18K V2 RGB-D support calibrated physical (projected) mushroom size estimates?

This script only INSPECTS and CHECKS; it never outputs mm^2. It
  1. inventories the dataset folder and searches the shipped files for depth-unit / intrinsics / alignment documentation,
  2. checks the depth file format (dtype, channels, size vs RGB/COCO),
  3. measures depth validity inside the existing WB masks (COCO polygons rasterised at original resolution),
  4. tests RGB/depth alignment empirically (depth discontinuities should sit on mask boundaries; scan small shifts),
  5. gives a unit-plausibility check against the nominal 15 cm camera height (NOT a calibration),
  6. writes depth_inspection.json, results.csv (px^2 + raw depth units, mm^2 = NOT_VERIFIED) and <=3 figures.
Area stays in px^2. Physical area needs verified depth units AND camera intrinsics (see findings.md).
"""
from __future__ import annotations
import argparse, csv, json, os, random, re, sys
from collections import Counter
from decimal import Decimal
from pathlib import Path
import numpy as np

WB_KEYS = {"wb", "whitebutton"}
norm = lambda s: "".join(c for c in str(s).lower() if c.isalnum())
DEPTH_EXTS = (".png", ".tif", ".tiff", ".npy", ".npz", ".exr", ".jpg", ".jpeg", ".bmp")
DOC_EXTS = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".pdf", ".xml", ".cfg", ".ini", ".docx", ".rst"}
KEYWORDS = re.compile(r"intrinsic|focal|\bfx\b|\bfy\b|\bcx\b|\bcy\b|calib|depth[_ ]?scale|depth unit|millimet|metre|meter|align|registered|baseline|realsense|d405|camera_info|\bfov\b", re.I)


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
        with open(path) as f:
            for it in json.load(f).get(prefix, []): yield it


def polygon_to_mask(seg, h, w):
    from pycocotools import mask as mu
    return mu.decode(mu.merge(mu.frPyObjects(seg, h, w)))


def mask_area_px2(m):  # same formula as the verified mask_area.py
    a = np.asarray(m)
    assert a.ndim == 2
    return int(np.count_nonzero(a > 0))


# ----------------------------------------------------------------------------- 1. inventory / documentation
def inventory(root, splits):
    inv = dict(root=str(root), top_level=[], splits={}, doc_files=[], keyword_hits=[])
    inv["top_level"] = sorted(p.name + ("/" if p.is_dir() else "") for p in root.iterdir())
    for s in splits:
        d = root / s
        if not d.is_dir(): inv["splits"][s] = "MISSING"; continue
        info = {}
        for sub in sorted(d.iterdir()):
            if sub.is_dir():
                ext = Counter(Path(f).suffix.lower() for f in os.listdir(sub))
                info[sub.name + "/"] = dict(n_files=sum(ext.values()), extensions=dict(ext))
            else:
                info[sub.name] = dict(bytes=sub.stat().st_size)
        inv["splits"][s] = info
    for dp, dn, fn in os.walk(root):
        depth = len(Path(dp).relative_to(root).parts)
        dn[:] = [x for x in dn if x.lower() not in ("rgb", "depth", "images", "labels")] if depth < 4 else []
        for f in fn:
            if Path(f).suffix.lower() in DOC_EXTS or re.search(r"intrinsic|calib|camera|readme|license", f, re.I):
                p = Path(dp) / f
                inv["doc_files"].append(dict(path=str(p.relative_to(root)), bytes=p.stat().st_size))
    for d in inv["doc_files"]:
        p = root / d["path"]
        if p.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".csv", ".xml", ".cfg", ".ini", ".rst", ".json"} and d["bytes"] < 2_000_000:
            try: text = p.read_text(errors="ignore")
            except Exception: continue
            d["head"] = text[:600] if d["bytes"] < 20_000 else None
            for ln in text.splitlines()[:5000]:
                if KEYWORDS.search(ln): inv["keyword_hits"].append(dict(file=d["path"], line=ln.strip()[:200]))
            if len(inv["keyword_hits"]) > 60: break
    return inv


def coco_schema(path):
    """Top-level keys, `info`, and the set of keys present in image / annotation / category entries."""
    out = dict(top_level_keys=[], info=None, image_keys=Counter(), annotation_keys=Counter(), n_images=0)
    try:
        import ijson
        if ijson.backend == "python": raise ImportError
        with open(path, "rb") as f:
            cur = None
            for prefix, ev, val in ijson.parse(f):
                if ev == "map_key" and prefix == "": out["top_level_keys"].append(val)
                elif ev == "map_key" and prefix == "images.item": out["image_keys"][val] += 1
                elif ev == "map_key" and prefix == "annotations.item": out["annotation_keys"][val] += 1
                elif ev == "end_map" and prefix == "images.item": out["n_images"] += 1
    except ImportError:
        with open(path) as f: d = json.load(f)
        out["top_level_keys"] = list(d.keys()); out["n_images"] = len(d.get("images", []))
        for im in d.get("images", []): out["image_keys"].update(im.keys())
        for a in d.get("annotations", [])[:5000]: out["annotation_keys"].update(a.keys())
    for k in ("info", "licenses"):
        if k in out["top_level_keys"]:
            for it in _items(path, k): out.setdefault(k + "_sample", it); break
    try:
        with open(path) as f:
            head = f.read(4000)
        m = re.search(r'"info"\s*:\s*(\{.*?\})', head, re.S)
        if m: out["info_head"] = m.group(1)[:600]
    except Exception: pass
    out["image_keys"] = dict(out["image_keys"]); out["annotation_keys"] = dict(out["annotation_keys"])
    return out


# ----------------------------------------------------------------------------- 2. depth reading
def find_depth(split_dir, rgb_name, depth_dir=None):
    stem = Path(rgb_name).stem
    dirs = [Path(depth_dir)] if depth_dir else [d for d in sorted(split_dir.iterdir()) if d.is_dir() and "depth" in d.name.lower()]
    for d in dirs:
        for e in DEPTH_EXTS:
            p = d / f"{stem}{e}"
            if p.exists(): return p
    for d in dirs:
        hits = sorted(d.glob(stem + "*"))
        if hits: return hits[0]
    return None


def read_depth(p):
    e = p.suffix.lower()
    if e == ".npy": return np.load(p)
    if e == ".npz":
        z = np.load(p); return z[list(z.keys())[0]]
    import cv2
    return cv2.imread(str(p), cv2.IMREAD_UNCHANGED)


def depth_format(a):
    if a is None: return dict(readable=False)
    scalar = a.ndim == 2 and a.dtype.kind in "uif" and a.dtype.itemsize >= 2
    v = a[np.isfinite(a)] if a.dtype.kind == "f" else a
    nz = v[v > 0] if scalar else v
    return dict(readable=True, shape=list(a.shape), dtype=str(a.dtype), channels=(a.shape[2] if a.ndim == 3 else 1),
                looks_like_scalar_depth=bool(scalar), min=float(v.min()), max=float(v.max()),
                frac_zero=float((v == 0).mean()) if scalar else None, n_unique=int(len(np.unique(v[::7]))),
                nonzero_percentiles_1_50_99=[float(x) for x in np.percentile(nz, [1, 50, 99])] if scalar and nz.size else None,
                note=None if scalar else "NOT a scalar depth map (8-bit / multi-channel): looks like a colourised visualisation")


# ----------------------------------------------------------------------------- 4. alignment
def boundary_points(masks):
    import cv2
    H, W = masks[0].shape; b = np.zeros((H, W), np.uint8); k = np.ones((3, 3), np.uint8)
    for m in masks:
        m8 = m.astype(np.uint8); b |= (m8 - cv2.erode(m8, k))
    return np.argwhere(b > 0)


def align_scan(depth, pts, rng_px=16, step=2, margin=20):
    """Mean depth-gradient at mask-boundary pixels as the depth map is shifted. Peak near (0,0) supports alignment."""
    import cv2
    d = depth.astype(np.float32); valid = (d > 0).astype(np.float32)
    k = (7, 7); num = cv2.GaussianBlur(d * valid, k, 0); den = cv2.GaussianBlur(valid, k, 0)
    ds = np.where(den > 0.5, num / np.maximum(den, 1e-6), 0).astype(np.float32)
    gx = cv2.Sobel(ds, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(ds, cv2.CV_32F, 0, 1, ksize=3)
    gm = np.hypot(gx, gy); ok = den > 0.9
    H, W = d.shape
    inner = np.zeros_like(ok); inner[margin:H - margin, margin:W - margin] = True
    base = float(gm[ok & inner].mean()) if (ok & inner).any() else float("nan")
    p = pts[(pts[:, 0] >= margin) & (pts[:, 0] < H - margin) & (pts[:, 1] >= margin) & (pts[:, 1] < W - margin)]
    shifts = list(range(-rng_px, rng_px + 1, step)); grid = np.full((len(shifts), len(shifts)), np.nan)
    for i, dy in enumerate(shifts):
        for j, dx in enumerate(shifts):
            yy, xx = p[:, 0] + dy, p[:, 1] + dx
            m = ok[yy, xx]
            grid[i, j] = gm[yy, xx][m].mean() if m.any() else np.nan
    i0 = shifts.index(0); bi = np.unravel_index(np.nanargmax(grid), grid.shape)
    return dict(baseline_mean_gradient=base, score_at_zero=float(grid[i0, i0]), ratio_at_zero=float(grid[i0, i0] / base),
                best_shift_dy_dx=[shifts[bi[0]], shifts[bi[1]]], best_ratio=float(grid[bi] / base), n_boundary_points=int(len(p))), grid, shifts


# ----------------------------------------------------------------------------- figures
def fig_example(path, rgb, depth, masks, tag, grid=None, shifts=None):
    import cv2, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    valid = depth > 0; lo, hi = np.percentile(depth[valid], [2, 98]) if valid.any() else (0, 1)
    cont = rgb.copy()
    for m in masks[:400]:
        cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(cont, cs, -1, (0, 255, 0), 1)
    dshow = np.where(valid, np.clip(depth.astype(np.float32), lo, hi), np.nan)
    inv = np.zeros(depth.shape + (4,), np.float32); inv[~valid] = (1, 0, 0, 0.8)
    n = 4 if grid is not None else 3
    fig, ax = plt.subplots(1, n, figsize=(4.2 * n, 3.4))
    ax[0].imshow(cont); ax[0].set_title("RGB + WB mask contours", fontsize=8)
    im = ax[1].imshow(dshow, cmap="viridis"); ax[1].set_title("raw depth (units NOT_VERIFIED)", fontsize=8); fig.colorbar(im, ax=ax[1], fraction=0.046)
    ax[2].imshow(rgb); ax[2].imshow(inv); ax[2].set_title("invalid depth (=0) in red", fontsize=8)
    if grid is not None:
        h = ax[3].imshow(grid, extent=(shifts[0] - 1, shifts[-1] + 1, shifts[-1] + 1, shifts[0] - 1), cmap="magma")
        ax[3].set_title("boundary gradient vs depth shift (px)", fontsize=8); ax[3].set_xlabel("dx"); ax[3].set_ylabel("dy"); fig.colorbar(h, ax=ax[3], fraction=0.046)
    for a in ax[:3]: a.axis("off")
    fig.suptitle(tag, fontsize=9); fig.tight_layout(); fig.savefig(path, dpi=70); plt.close(fig)


def fig_summary(path, inst_valid, pooled_depth):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
    ax[0].hist(inst_valid, bins=40, color="#4c78a8"); ax[0].set_yscale("log"); ax[0].set_xlabel("fraction of mask pixels with depth > 0"); ax[0].set_title("Depth validity per WB instance", fontsize=9)
    ax[1].hist(pooled_depth, bins=80, color="#f58518"); ax[1].set_xlabel("raw depth value inside masks (units NOT_VERIFIED)"); ax[1].set_title("Pooled raw depth in WB masks", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=70); plt.close(fig)


# ----------------------------------------------------------------------------- main
def run(a):
    import cv2
    out = Path(a.out_dir); (out / "figures").mkdir(parents=True, exist_ok=True)
    root = Path(a.data_root); splits = ["train", "valid", "test"]
    rep = dict(script="depth_area.py", unit_of_area="px2 (physical area NOT computed)")
    rep["inventory"] = inventory(root, splits)
    print("TOP LEVEL:", rep["inventory"]["top_level"])
    for s, v in rep["inventory"]["splits"].items(): print(f"[{s}]", json.dumps(v)[:400])
    print("DOC FILES:", [d["path"] for d in rep["inventory"]["doc_files"]][:40])
    print("KEYWORD HITS (calibration / unit / alignment text in shipped files):", len(rep["inventory"]["keyword_hits"]))
    for h in rep["inventory"]["keyword_hits"][:25]: print("  ", h["file"], "|", h["line"])

    sd = root / a.split; coco = sd / "annotations_coco.json"
    rep["coco_schema"] = coco_schema(coco)
    print("COCO top-level keys:", rep["coco_schema"]["top_level_keys"])
    print("COCO image keys:", rep["coco_schema"]["image_keys"])
    print("COCO annotation keys:", rep["coco_schema"]["annotation_keys"])
    if rep["coco_schema"].get("info_sample") or rep["coco_schema"].get("info_head"): print("COCO info:", rep["coco_schema"].get("info_sample") or rep["coco_schema"].get("info_head"))
    cats = list(_items(coco, "categories"))
    wb_ids = {c["id"] for c in cats if norm(c.get("name", "")) in WB_KEYS}
    images = sorted(_items(coco, "images"), key=lambda i: i["file_name"])
    idx = sorted(random.Random(a.seed).sample(range(len(images)), min(a.n, len(images))))
    sel = [images[i] for i in idx]; sel_ids = {i["id"] for i in sel}
    anns = {}
    for an in _items(coco, "annotations"):
        if an.get("category_id") in wb_ids and an["image_id"] in sel_ids and not an.get("iscrowd", 0) and isinstance(an.get("segmentation"), list):
            anns.setdefault(an["image_id"], []).append(an)

    depth_dirs = [d.name for d in sorted(sd.iterdir()) if d.is_dir() and "depth" in d.name.lower()] if not a.depth_dir else [a.depth_dir]
    rep["depth_dirs_found"] = depth_dirs; print("DEPTH DIRS in", sd.name, ":", depth_dirs)
    first = find_depth(sd, sel[0]["file_name"], a.depth_dir)
    if first is None:
        rep["status"] = "BLOCKED: no depth file found for the RGB images (see inventory)"; (out / "depth_inspection.json").write_text(json.dumps(rep, indent=2, default=str))
        print(rep["status"]); return 2
    rep["depth_naming_example"] = dict(rgb=sel[0]["file_name"], depth=str(first.relative_to(root)))
    fmts = []
    for im in sel[:5]:
        p = find_depth(sd, im["file_name"], a.depth_dir)
        fm = depth_format(read_depth(p)) if p else dict(readable=False); fm["file"] = p.name if p else None; fmts.append(fm)
    rep["depth_format_first5"] = fmts; print("DEPTH FORMAT (first 5):"); [print("  ", f) for f in fmts]

    rows, inst_valid, pooled, per_img, aligns = [], [], [], [], []
    size_ok = 0; grids = {}; cache = {}
    for k, im in enumerate(sel):
        dp = find_depth(sd, im["file_name"], a.depth_dir)
        if dp is None: print("missing depth for", im["file_name"]); continue
        dep = read_depth(dp)
        rgbp = sd / "rgb" / im["file_name"]
        rgb = cv2.cvtColor(cv2.imread(str(rgbp)), cv2.COLOR_BGR2RGB); H, W = rgb.shape[:2]
        if dep.ndim != 2: dep = dep[..., 0]
        same = dep.shape == (H, W) and (W, H) == (im["width"], im["height"]); size_ok += int(same)
        ms, areas = [], []
        for an in sorted(anns.get(im["id"], []), key=lambda x: x["id"]):
            rings = [r for r in an["segmentation"] if isinstance(r, list) and len(r) >= 6]
            if not rings: continue
            m = polygon_to_mask(rings, H, W)
            if m.shape != dep.shape: continue
            ar = mask_area_px2(m)
            if ar == 0: continue
            ms.append(m); areas.append(ar)
        vals_all, fr = [], []
        for m in ms:
            v = dep[m > 0]; fv = float((v > 0).mean()); fr.append(fv); inst_valid.append(fv)
            vv = v[v > 0]
            if vv.size: vals_all.append(vv)
        pv = np.concatenate(vals_all) if vals_all else np.zeros(0)
        if pv.size: pooled.append(pv[::5])
        al, grid, shifts = align_scan(dep, boundary_points(ms), a.shift_px) if ms else (None, None, None)
        if al: aligns.append(al); grids[im["id"]] = (grid, shifts)
        row = dict(image_id=im["id"], filename=im["file_name"], n_wb_instances=len(ms), wb_area_px2_total=int(sum(areas)),
                   mean_instance_valid_fraction=float(np.mean(fr)) if fr else None, image_valid_fraction=float((dep > 0).mean()),
                   depth_median_raw_in_masks=float(np.median(pv)) if pv.size else None,
                   depth_p05_raw=float(np.percentile(pv, 5)) if pv.size else None, depth_p95_raw=float(np.percentile(pv, 95)) if pv.size else None,
                   align_ratio_at_zero_shift=al["ratio_at_zero"] if al else None, align_best_shift_dy_dx=str(al["best_shift_dy_dx"]) if al else None,
                   depth_size_matches_rgb_and_coco=bool(same))
        rows.append(row)
        cache[im["id"]] = None
        if (k + 1) % 5 == 0: print(f"{k + 1}/{len(sel)} images", flush=True)
    # aggregate
    iv = np.array(inst_valid); pooled_all = np.concatenate(pooled) if pooled else np.zeros(0)
    rep["depth_validity_in_wb_masks"] = dict(images=len(rows), instances=int(iv.size), mean_valid_fraction=float(iv.mean()),
        median_valid_fraction=float(np.median(iv)), p05_valid_fraction=float(np.percentile(iv, 5)), instances_valid_lt_50pct=int((iv < .5).sum()),
        instances_valid_lt_90pct=int((iv < .9).sum()), instances_zero_valid=int((iv == 0).sum()), depth_size_matches_rgb_and_coco_images=size_ok)
    print("VALIDITY:", rep["depth_validity_in_wb_masks"])
    if pooled_all.size:
        med = float(np.median(pooled_all)); p = [float(x) for x in np.percentile(pooled_all, [1, 5, 50, 95, 99])]
        rep["unit_plausibility"] = dict(raw_depth_in_masks_percentiles_1_5_50_95_99=p, nominal_camera_height_mm=150,
            implied_median_mm_if_unit_1mm=med, implied_median_mm_if_unit_0p1mm=med / 10, implied_median_mm_if_unit_1m=med * 1000,
            note="plausibility only: camera was ~15 cm above the WB beds and caps stand above the bed (so expect roughly 70-150 mm); this does NOT verify units or intrinsics")
        print("UNIT PLAUSIBILITY:", rep["unit_plausibility"])
    if aligns:
        r0 = np.array([x["ratio_at_zero"] for x in aligns]); bs = [tuple(x["best_shift_dy_dx"]) for x in aligns]
        rep["alignment_scan"] = dict(images=len(aligns), mean_ratio_at_zero=float(r0.mean()), min_ratio_at_zero=float(r0.min()),
            best_shift_counts={str(k): v for k, v in Counter(bs).most_common(8)}, images_best_shift_is_zero=sum(1 for b in bs if b == (0, 0)),
            interpretation_guide="ratio>1 = depth discontinuities concentrate on mask boundaries; best shift (0,0) in most images supports pixel alignment of depth to RGB/masks. Consistency evidence only, not a calibration.")
        print("ALIGNMENT:", rep["alignment_scan"])
    rep["intrinsics_or_units_text_found_in_dataset_files"] = bool(rep["inventory"]["keyword_hits"])
    rep["calibration_verified"] = False
    rep["calibration_note"] = "Set to False by design: verified calibration requires documented depth units AND camera intrinsics (and depth-to-colour alignment). Review keyword_hits / doc_files manually."

    # outputs
    with open(out / "results.csv", "w", newline="") as f:
        cols = list(rows[0]) + ["wb_area_mm2", "area_units_note"]
        w = csv.writer(f); w.writerow(cols)
        for r in rows: w.writerow(list(r.values()) + ["NOT_VERIFIED", "area in px2 (column wb_area_px2_total); depth columns are RAW sensor units, unit NOT_VERIFIED; no mm2"])
    (out / "depth_inspection.json").write_text(json.dumps(rep, indent=2, default=str))
    # figures (<=3)
    fm = sorted([r for r in rows if r["mean_instance_valid_fraction"] is not None], key=lambda r: r["mean_instance_valid_fraction"])
    picks = [("typical", fm[len(fm) // 2])] + ([("lowest_depth_validity", fm[0])] if fm[0]["image_id"] != fm[len(fm) // 2]["image_id"] else [])
    for tag, r in picks:
        im = next(i for i in sel if i["id"] == r["image_id"]); sdp = find_depth(sd, im["file_name"], a.depth_dir)
        rgb = cv2.cvtColor(cv2.imread(str(sd / "rgb" / im["file_name"])), cv2.COLOR_BGR2RGB); dep = read_depth(sdp)
        dep = dep if dep.ndim == 2 else dep[..., 0]; H, W = rgb.shape[:2]
        ms = [polygon_to_mask([x for x in an["segmentation"] if isinstance(x, list) and len(x) >= 6], H, W) for an in anns.get(im["id"], []) if any(isinstance(x, list) and len(x) >= 6 for x in an["segmentation"])]
        g = grids.get(im["id"]); fig_example(out / "figures" / f"{tag}_{Path(im['file_name']).stem}.png", rgb, dep, ms, f"[{tag}] {im['file_name']} (area px², depth raw units)", *(g if tag == "typical" and g else (None, None)))
    if iv.size: fig_summary(out / "figures" / "depth_validity_summary.png", iv, pooled_all)
    print("done; wrote results.csv, depth_inspection.json, figures/")
    return 0


def parse(argv=None):
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-root", required=True, help="folder containing train/ valid/ test/ (M18KV2)")
    ap.add_argument("--out-dir", default=str(here))
    ap.add_argument("--split", default="test")
    ap.add_argument("--depth-dir", default=None, help="override depth folder (default: sibling dir of rgb/ whose name contains 'depth')")
    ap.add_argument("--n", type=int, default=30, help="images (seed 42, same rule as earlier evaluations)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--shift-px", type=int, default=16)
    return ap.parse_args(argv)


if __name__ == "__main__":
    sys.exit(run(parse()))
