#!/usr/bin/env python3
"""Day 4: predicted-mask area evaluation of the WB-only YOLOv8n-seg model on ALL M18K V2 test images.

Inference only. Reference = original COCO WB polygons rasterised with pycocotools at original resolution.
One-to-one matching by mask IoU >= 0.50 (greedy, highest IoU first). Area = sum(mask > 0) in px^2 per instance
(same formula as the previously verified mask_area.mask_area_px2, copied below so this script is standalone).
Outputs are written next to this script (or --out-dir):
  area_metrics.json, area_per_image.csv, area_matches.csv.gz, figures/*.png, README.md
Progress is cached in --work-dir so an interrupted run resumes.
"""
from __future__ import annotations
import argparse, csv, gzip, hashlib, json, platform, random, sys, time
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
import numpy as np

WB_KEYS = {"wb", "whitebutton"}
norm = lambda s: "".join(c for c in str(s).lower() if c.isalnum())

# Results of the previous 30-image evaluation (copied from its executed outputs, for comparison only)
PREV30 = dict(images=30, gt_reference=4970, predicted=5146, matched=4900, unmatched_predictions=246, unmatched_gt=70,
              match_coverage=0.9859154929577465, mae_px2=207.4, mean_relative_error_pct=8.799715146122448,
              median_relative_error_pct=7.344207, mean_mask_iou=0.890, mean_signed_error_px2=160.75020408163266,
              matched_pred_over_gt_area_ratio=1.0452452860925296)


# ----------------------------------------------------------------------------- area (verified formula)
def mask_area_px2(mask) -> int:
    """Area of one instance mask in px^2 = number of pixels with value > 0 (identical to mask_area.py)."""
    a = np.asarray(mask)
    if a.ndim != 2:
        raise ValueError(f"mask must be 2-D (H, W), got shape {a.shape}")
    return int(np.count_nonzero(a > 0))


def polygon_to_mask(segmentation, height, width):
    from pycocotools import mask as mu
    return mu.decode(mu.merge(mu.frPyObjects(segmentation, height, width)))


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
            for it in json.load(f).get(prefix, []):
                yield it


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def find_image(img_dir, file_name):
    for c in (img_dir / file_name, img_dir / Path(file_name).name):
        if c.exists(): return c
    raise FileNotFoundError(f"{file_name} not under {img_dir}")


def match_greedy(iou, thr):
    if iou.size == 0: return []
    cand = sorted(np.argwhere(iou >= thr).tolist(), key=lambda p: (-iou[p[0], p[1]], p[0], p[1]))
    up, ug, out = set(), set(), []
    for p, g in cand:
        if p not in up and g not in ug:
            up.add(p); ug.add(g); out.append((p, g, float(iou[p, g])))
    return out


def yolo_predict(model, path, a, classes):
    r = model.predict(source=str(path), imgsz=a.imgsz, conf=a.conf, iou=a.iou, max_det=a.max_det,
                      retina_masks=True, classes=classes, device=a.device, verbose=False)[0]
    H, W = r.orig_shape
    if r.masks is None or len(r.masks) == 0:
        return np.zeros((0, H, W), np.uint8), np.zeros(0)
    return (r.masks.data.cpu().numpy() > 0.5).astype(np.uint8), r.boxes.conf.cpu().numpy()


# ----------------------------------------------------------------------------- per-image processing
def process_image(im, gt_anns, img_dir, predictor, a, mu):
    from PIL import Image
    path = find_image(img_dir, im["file_name"])
    with Image.open(path) as I: W, H = I.size
    masks, confs = predictor(path)
    assert masks.shape[1:] == (H, W), f"pred mask {masks.shape} != image {(H, W)}"
    gts, excl = [], Counter()
    for ann in sorted(gt_anns, key=lambda x: x["id"]):
        seg = ann.get("segmentation")
        if ann.get("iscrowd", 0): excl["iscrowd"] += 1; continue
        if not isinstance(seg, list): excl["non_polygon"] += 1; continue
        rings = [r for r in seg if isinstance(r, list) and len(r) >= 6 and len(r) % 2 == 0]
        if not rings: excl["no_valid_ring"] += 1; continue
        m = polygon_to_mask(rings, H, W); ar = mask_area_px2(m)
        if ar == 0: excl["zero_area_mask"] += 1; continue
        gts.append(dict(id=ann["id"], area=ar, rle=mu.encode(np.asfortranarray(m))))
    preds = [dict(area=mask_area_px2(masks[i]), rle=mu.encode(np.asfortranarray(masks[i])), conf=float(confs[i]))
             for i in range(len(masks))]
    iou = (np.asarray(mu.iou([p["rle"] for p in preds], [g["rle"] for g in gts], [0] * len(gts)))
           if preds and gts else np.zeros((len(preds), len(gts))))
    pairs = match_greedy(iou, a.iou_thr)
    mp, mg = {p for p, _, _ in pairs}, {g for _, g, _ in pairs}
    rows, ms = [], []
    for p, g, v in pairs:
        ae = abs(preds[p]["area"] - gts[g]["area"]); rel = 100.0 * ae / gts[g]["area"]
        rows.append([im["id"], gts[g]["id"], p, round(v, 6), gts[g]["area"], preds[p]["area"], ae, round(rel, 6)])
        ms.append(dict(p=p, g=g, abs=ae, gt=gts[g]["area"], pred=preds[p]["area"]))
    un_p = [[im["id"], p, round(preds[p]["conf"], 4), preds[p]["area"], round(float(iou[p].max()), 4) if iou.shape[1] else 0.0]
            for p in range(len(preds)) if p not in mp]
    un_g = [[im["id"], gts[g]["id"], gts[g]["area"], round(float(iou[:, g].max()), 4) if iou.shape[0] else 0.0]
            for g in range(len(gts)) if g not in mg]
    gt_rows = [[gts[g]["id"], gts[g]["area"], int(g in mg)] for g in range(len(gts))]
    summ = dict(image_id=im["id"], filename=im["file_name"], width=W, height=H,
                size_matches_coco=(W, H) == (im["width"], im["height"]), gt_raw=len(gt_anns), gt_reference=len(gts),
                pred=len(preds), matched=len(pairs), unmatched_pred=len(preds) - len(pairs), unmatched_gt=len(gts) - len(pairs),
                mae_px2=float(np.mean([r[6] for r in rows])) if rows else None,
                mean_relative_error_pct=float(np.mean([r[7] for r in rows])) if rows else None,
                mean_mask_iou=float(np.mean([r[3] for r in rows])) if rows else None,
                gt_total_area_px2=sum(g["area"] for g in gts), pred_total_area_px2=sum(p["area"] for p in preds))
    rec = dict(filename=im["file_name"], path=path, H=H, W=W, matches=ms,
               gt_rle=[g["rle"] for g in gts], pred_rle=[p["rle"] for p in preds])
    return dict(summ=summ, rows=rows, un_p=un_p, un_g=un_g, gt_rows=gt_rows, excl=dict(excl)), rec


# ----------------------------------------------------------------------------- tables / figures
def bin_table(ms, gt_all, thresholds, labels):
    """ms: matched rows; gt_all: [ann_id, area, matched]; bins by GT area thresholds (px^2)."""
    out = []
    ga = np.array([g[1] for g in gt_all], float); gm = np.array([g[2] for g in gt_all], int)
    gb = np.searchsorted(thresholds, ga, side="right")
    ma = np.array([r[4] for r in ms], float); mb = np.searchsorted(thresholds, ma, side="right")
    pr = np.array([r[5] for r in ms], float); ae = np.array([r[6] for r in ms], float)
    rel = np.array([r[7] for r in ms], float); iu = np.array([r[3] for r in ms], float)
    for i, lab in enumerate(labels):
        s = mb == i; sg = pr[s] - ma[s]; ng = int((gb == i).sum()); nm = int(s.sum())
        out.append(dict(label=lab, gt_area_range_px2=[float(thresholds[i - 1]) if i > 0 else 0.0, float(thresholds[i]) if i < len(thresholds) else None],
                        n_gt=ng, n_matched=nm, match_coverage=(nm / ng if ng else None),
                        gt_area_mean_px2=float(ma[s].mean()) if nm else None, mae_px2=float(ae[s].mean()) if nm else None,
                        mean_relative_error_pct=float(rel[s].mean()) if nm else None,
                        median_relative_error_pct=float(np.median(rel[s])) if nm else None,
                        mean_signed_error_px2=float(sg.mean()) if nm else None,
                        pct_pred_smaller_than_gt=float(100 * (sg < 0).mean()) if nm else None,
                        mean_mask_iou=float(iu[s].mean()) if nm else None))
    return out


def size_plot(path, bins):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    L = [b["label"] for b in bins]; fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.6))
    ax[0].bar(L, [b["mean_relative_error_pct"] or 0 for b in bins], color="#4c78a8"); ax[0].set_title("Mean relative area error (%)")
    ax[1].bar(L, [b["mean_signed_error_px2"] or 0 for b in bins], color="#f58518"); ax[1].axhline(0, color="k", lw=.8)
    ax[1].set_title("Mean signed error, pred − GT (px²)")
    ax[2].bar(L, [100 * (b["match_coverage"] or 0) for b in bins], color="#54a24b"); ax[2].set_ylim(0, 100)
    ax[2].set_title("Match coverage (% of GT matched)")
    for x in ax: x.set_xlabel("GT area percentile bin"); x.tick_params(axis="x", labelsize=8)
    fig.suptitle("Area error vs mushroom size (GT area bins; px², not mm²)", fontsize=10)
    fig.tight_layout(); fig.savefig(path, dpi=80); plt.close(fig)


def render_example(path_png, tag, rec, mu):
    import cv2, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt, matplotlib.patheffects as pe
    H, W = rec["H"], rec["W"]
    rgb = cv2.cvtColor(cv2.imread(str(rec["path"])), cv2.COLOR_BGR2RGB)
    mp = {m["p"] for m in rec["matches"]}; mg = {m["g"] for m in rec["matches"]}
    def overlay(items, matched, c_m, c_u):
        im = rgb.copy(); lay = im.copy()
        dec = [mu.decode(r).astype(np.uint8) for r in items]
        for i, m in enumerate(dec): lay[m > 0] = c_m if i in matched else c_u
        im = cv2.addWeighted(lay, 0.35, im, 0.65, 0)
        for i, m in enumerate(dec):
            cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(im, cs, -1, c_m if i in matched else c_u, 1)
        return im
    gt_img = overlay(rec["gt_rle"], mg, (0, 255, 0), (255, 255, 0)); pr_img = overlay(rec["pred_rle"], mp, (255, 0, 0), (255, 0, 255))
    cw, ch = max(W // 3, 64), max(H // 3, 64)
    if rec["matches"]:
        w = max(rec["matches"], key=lambda m: m["abs"]); x, y, bw, bh = mu.toBbox(rec["gt_rle"][w["g"]]); cx, cy = x + bw / 2, y + bh / 2
    else: cx, cy = W / 2, H / 2
    x0 = int(min(max(cx - cw / 2, 0), W - cw)); y0 = int(min(max(cy - ch / 2, 0), H - ch)); zoom = rgb.copy()
    for rles, col in ((rec["gt_rle"], (0, 255, 0)), (rec["pred_rle"], (255, 0, 0))):
        for rle in rles:
            x, y, bw, bh = mu.toBbox(rle)
            if x > x0 + cw or x + bw < x0 or y > y0 + ch or y + bh < y0: continue
            cs, _ = cv2.findContours(mu.decode(rle).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(zoom, cs, -1, col, 1)
    fig, ax = plt.subplots(2, 2, figsize=(14, 8))
    ax[0, 0].imshow(rgb); ax[0, 0].set_title("RGB")
    ax[0, 1].imshow(gt_img); ax[0, 1].set_title(f"GT masks: {len(rec['gt_rle'])} [green matched, yellow unmatched]", fontsize=9)
    ax[1, 0].imshow(pr_img); ax[1, 0].set_title(f"Predicted masks: {len(rec['pred_rle'])} [red matched, magenta unmatched]", fontsize=9)
    ax[1, 1].imshow(zoom[y0:y0 + ch, x0:x0 + cw], extent=(x0, x0 + cw, y0 + ch, y0)); ax[1, 1].set_title("Zoom: GT (green) vs pred (red); G/P = areas px²", fontsize=9)
    shown = 0
    for m in sorted(rec["matches"], key=lambda m: m["abs"], reverse=True):
        x, y, bw, bh = mu.toBbox(rec["gt_rle"][m["g"]]); tx, ty = x + bw / 2, y + bh / 2
        if x0 <= tx <= x0 + cw and y0 <= ty <= y0 + ch and shown < 14:
            ax[1, 1].text(tx, ty, f"G {m['gt']}\nP {m['pred']}", color="white", fontsize=6, ha="center", va="center",
                          path_effects=[pe.withStroke(linewidth=1.5, foreground="black")]); shown += 1
    for a_ in ax.ravel(): a_.axis("off")
    mae = np.mean([m["abs"] for m in rec["matches"]]) if rec["matches"] else float("nan")
    fig.suptitle(f"[{tag}] {rec['filename']} | GT {len(rec['gt_rle'])}, pred {len(rec['pred_rle'])}, matched {len(rec['matches'])}, image MAE {mae:.1f} px²", fontsize=10)
    fig.tight_layout(); fig.savefig(path_png, dpi=70); plt.close(fig)


# ----------------------------------------------------------------------------- main
def run(a, model=None, predictor=None):
    from pycocotools import mask as mu
    out = Path(a.out_dir); (out / "figures").mkdir(parents=True, exist_ok=True)
    work = Path(a.work_dir); work.mkdir(parents=True, exist_ok=True)
    coco = Path(a.data_root) / a.test_dir / "annotations_coco.json"; img_dir = Path(a.data_root) / a.test_dir / "rgb"
    cats = list(_items(coco, "categories"))
    wb_ids = set(a.wb_category_ids) if a.wb_category_ids else {c["id"] for c in cats if norm(c.get("name", "")) in WB_KEYS}
    if not wb_ids: sys.exit(f"WB category not found: {cats}")
    images = sorted(_items(coco, "images"), key=lambda i: i["file_name"])
    prev30 = {images[i]["id"] for i in sorted(random.Random(42).sample(range(len(images)), 30))}  # same rule as the 30-image run
    sel = images if a.n in (0, None) else [images[i] for i in sorted(random.Random(a.seed).sample(range(len(images)), a.n))]
    sel_ids = {i["id"] for i in sel}; gt_by = defaultdict(list); wb_total = 0
    for ann in _items(coco, "annotations"):
        if ann.get("category_id") in wb_ids:
            wb_total += 1
            if ann["image_id"] in sel_ids: gt_by[ann["image_id"]].append(ann)
    print(f"test images={len(images)}  WB annotations (incl. crowd)={wb_total}  evaluating={len(sel)}", flush=True)

    ck = Path(a.checkpoint)
    if model is None:
        from ultralytics import YOLO
        model = YOLO(str(ck))
    names = dict(model.names)
    one = [k for k, v in names.items() if norm(v) in WB_KEYS]
    classes = None if len(names) == 1 else (one or sys.exit(f"no WB class in model names {names}"))
    targs = getattr(model, "ckpt", None) or {}
    targs = targs.get("train_args", {}) if isinstance(targs, dict) else {}
    if a.imgsz is None:
        a.imgsz = int(targs["imgsz"]) if "imgsz" in targs else 640
        imgsz_src = "checkpoint train_args" if "imgsz" in targs else "default 640 (train imgsz NOT_VERIFIED)"
    else: imgsz_src = "command line"
    predictor = predictor or (lambda p: yolo_predict(model, p, a, classes))
    ck_hash = sha256(ck) if ck.exists() else "NOT_VERIFIED"

    sig = hashlib.sha256(json.dumps([ck_hash, a.imgsz, a.conf, a.iou, a.max_det, a.iou_thr, [i["id"] for i in sel]]).encode()).hexdigest()
    prog = work / "progress.jsonl"; done = {}
    if prog.exists() and not a.no_resume:
        with open(prog) as f:
            first = f.readline()
            if first.strip() == sig:
                for ln in f:
                    try: d = json.loads(ln); done[d["summ"]["image_id"]] = d
                    except Exception: break
            else: print("progress file has different settings; starting fresh")
    if not done:
        open(prog, "w").write(sig + "\n")
    print(f"resuming with {len(done)} cached images" if done else "starting fresh", flush=True)

    recs, results, t0 = {}, {}, time.time()
    for k, im in enumerate(sel):
        if im["id"] in done: results[im["id"]] = done[im["id"]]; continue
        res, rec = process_image(im, gt_by[im["id"]], img_dir, predictor, a, mu)
        results[im["id"]] = res; recs[im["id"]] = rec
        with open(prog, "a") as f: f.write(json.dumps(res) + "\n")
        if (k + 1) % 25 == 0 or k + 1 == len(sel):
            print(f"{k + 1}/{len(sel)} images  ({time.time() - t0:.0f}s)", flush=True)
    order = [results[i["id"]] for i in sel]
    try:
        dev = str(next(model.model.parameters()).device)
    except Exception: dev = "NOT_VERIFIED"

    rows = [r for d in order for r in d["rows"]]; un_p = [r for d in order for r in d["un_p"]]; un_g = [r for d in order for r in d["un_g"]]
    gt_all = [r for d in order for r in d["gt_rows"]]; excl = Counter()
    for d in order: excl.update(d["excl"])
    summ = [d["summ"] for d in order]

    def wcsv(path, head, data, opener=open):
        with opener(path, "wt", newline="") as f: w = csv.writer(f); w.writerow(head); w.writerows(data)
    cols = ["image_id", "filename", "width", "height", "size_matches_coco", "gt_raw", "gt_reference", "pred", "matched", "unmatched_pred",
            "unmatched_gt", "mae_px2", "mean_relative_error_pct", "mean_mask_iou", "gt_total_area_px2", "pred_total_area_px2", "in_previous_30"]
    wcsv(out / "area_per_image.csv", cols, [[s.get(c) if c != "in_previous_30" else int(s["image_id"] in prev30) for c in cols] for s in summ])
    wcsv(out / "area_matches.csv.gz", ["image_id", "gt_annotation_id", "pred_instance_index", "mask_iou", "gt_area_px2", "pred_area_px2", "abs_error_px2", "relative_error_pct"], rows,
         opener=lambda p, m, newline="": gzip.open(p, "wt", newline=newline))
    wcsv(work / "unmatched_predictions.csv", ["image_id", "pred_instance_index", "pred_conf", "pred_area_px2", "best_iou_with_any_gt"], un_p)
    wcsv(work / "unmatched_gt.csv", ["image_id", "gt_annotation_id", "gt_area_px2", "best_iou_with_any_pred"], un_g)

    def agg(rs, n_gt, n_pr, n_img):
        n_m = len(rs)
        if not n_m: return dict(images=n_img, gt_reference=n_gt, predicted=n_pr, matched=0)
        ae = np.array([r[6] for r in rs], float); rel = np.array([r[7] for r in rs], float); sg = np.array([r[5] - r[4] for r in rs], float)
        return dict(images=n_img, gt_reference=n_gt, predicted=n_pr, matched=n_m, unmatched_predictions=n_pr - n_m, unmatched_gt=n_gt - n_m,
                    match_coverage=n_m / n_gt if n_gt else None, matched_over_predictions=n_m / n_pr if n_pr else None,
                    mae_px2=float(ae.mean()), mean_relative_error_pct=float(rel.mean()), median_relative_error_pct=float(np.median(rel)),
                    mean_mask_iou=float(np.mean([r[3] for r in rs])), median_mask_iou=float(np.median([r[3] for r in rs])),
                    mean_signed_error_px2=float(sg.mean()), pct_pred_larger_than_gt=float(100 * (sg > 0).mean()),
                    matched_pred_over_gt_area_ratio=float(sum(r[5] for r in rs) / sum(r[4] for r in rs)))
    overall = agg(rows, sum(s["gt_reference"] for s in summ), sum(s["pred"] for s in summ), len(sel))
    p30 = {s["image_id"] for s in summ} & prev30
    r30 = [r for r in rows if r[0] in p30]
    sub30 = agg(r30, sum(s["gt_reference"] for s in summ if s["image_id"] in p30), sum(s["pred"] for s in summ if s["image_id"] in p30), len(p30))
    ga = np.array([g[1] for g in gt_all], float)
    th3 = [float(np.quantile(ga, q)) for q in (1 / 3, 2 / 3)]; th5 = [float(np.quantile(ga, q)) for q in (.33, .66, .90, .99)]
    by3 = bin_table(rows, gt_all, th3, ["small (0-33%)", "medium (33-66%)", "large (66-100%)"])
    by5 = bin_table(rows, gt_all, th5, ["0-33%", "33-66%", "66-90%", "90-99%", "99-100%"])
    tot_ratio = [s["pred_total_area_px2"] / s["gt_total_area_px2"] for s in summ if s["gt_total_area_px2"]]
    metrics = dict(
        sample=dict(images_evaluated=len(sel), test_images_total=len(images), all_test_images=len(sel) == len(images),
                    test_wb_annotations_in_coco=wb_total, image_list="see area_per_image.csv (one row per evaluated image, sorted by filename)",
                    gt_reference_instances=overall["gt_reference"], gt_excluded=dict(excl)),
        match_rule=f"one-to-one greedy by descending mask IoU, IoU >= {a.iou_thr}; masks at original resolution; GT = pycocotools-rasterised COCO polygons (non-crowd, non-zero area)",
        area_definition="A_px2 = sum(mask > 0) per instance; unit px2 (not mm2); relative_error_pct = 100*|pred-GT|/GT",
        overall=overall, image_level_total_area_ratio_pred_over_gt=dict(mean=float(np.mean(tot_ratio)), min=float(np.min(tot_ratio)), max=float(np.max(tot_ratio)),
                                                                          note="sum of per-instance areas incl. unmatched predictions; overlaps not removed"),
        by_size_terciles=dict(gt_area_thresholds_px2=th3, bins=by3), by_size_percentile_bins=dict(gt_area_thresholds_px2=th5, bins=by5),
        previous_30_image_evaluation=PREV30, previous_30_images_recomputed_in_this_run=sub30,
        all_pred_sizes_match_coco_image_size=all(s["size_matches_coco"] for s in summ),
        model=dict(path=str(ck), sha256=ck_hash, names={str(k): v for k, v in names.items()},
                   train_args={k: str(targs.get(k)) for k in ("imgsz", "epochs", "data", "model", "seed") if k in targs}),
        inference=dict(imgsz=a.imgsz, imgsz_source=imgsz_src, conf=a.conf, nms_iou=a.iou, max_det=a.max_det, retina_masks=True, classes=classes,
                       device_requested=str(a.device), device_used=dev, note="settings identical to the 30-image evaluation; not tuned"),
        versions=_vers())
    (out / "area_metrics.json").write_text(json.dumps(metrics, indent=2, default=str))

    # figures: 3 overlays + size plot (4 total, small)
    ok = sorted([s for s in summ if s["mae_px2"] is not None], key=lambda s: s["mae_px2"])
    picks = [("median_mae", ok[len(ok) // 2]), ("worst_mae", ok[-1]), ("most_unmatched", max(summ, key=lambda s: s["unmatched_pred"] + s["unmatched_gt"]))]
    seen = set()
    by_id = {i["id"]: i for i in sel}
    for tag, s in picks:
        if s["image_id"] in seen: continue
        seen.add(s["image_id"])
        rec = recs.get(s["image_id"]) or process_image(by_id[s["image_id"]], gt_by[s["image_id"]], img_dir, predictor, a, mu)[1]
        render_example(out / "figures" / f"{tag}_{Path(s['filename']).stem}.png", tag, rec, mu); print("figure", tag, s["filename"])
    size_plot(out / "figures" / "error_by_size.png", by5)
    write_readme(out, a, metrics, ck)
    o = overall
    print(json.dumps({k: o.get(k) for k in ("images", "gt_reference", "predicted", "matched", "unmatched_predictions", "unmatched_gt", "match_coverage",
                                            "mae_px2", "mean_relative_error_pct", "median_relative_error_pct", "mean_mask_iou")}, indent=2))
    return 0


def _vers():
    from importlib import metadata
    v = {"python": platform.python_version(), "numpy": np.__version__}
    for m in ("ultralytics", "torch", "pycocotools", "opencv-python", "matplotlib"):
        try: v[m] = metadata.version(m)
        except Exception: v[m] = "NOT_VERIFIED"
    return v


def write_readme(out, a, m, ck):
    inf = m["inference"]
    (out / "README.md").write_text(f"""# Day 4 - Predicted mask-area evaluation (all M18K V2 test images)

Evaluates the existing WB-only YOLOv8n-seg checkpoint: how close is the area (px²) of each predicted instance mask to the area of
the matching COCO ground-truth WB polygon mask. Inference only; no training, no EDA. Area is in **px²**, not mm².

## References (not copied here)
- Checkpoint: https://drive.google.com/file/d/1Q5iq_-j-RwOTkyiiXyTOc80Cf_xwk7K-/view  (sha256 `{m['model']['sha256']}`)
- Dataset: M18K V2, split `{a.test_dir}` (`<data_root>/{a.test_dir}/rgb/` and `annotations_coco.json`); WB-only labels were built earlier (`wb_yolo_labels.zip`).

## Run (Colab)
```python
from google.colab import drive; drive.mount("/content/drive")
!pip -q install ultralytics gdown pycocotools ijson
import gdown; gdown.download(id="1Q5iq_-j-RwOTkyiiXyTOc80Cf_xwk7K-", output="/content/wb_yolov8n_seg.pt")
!python area_evaluation.py --data-root <.../M18KV2> --checkpoint /content/wb_yolov8n_seg.pt
```
Default: all {m['sample']['test_images_total']} test images (`--n 30` etc. for a random subset, seed 42). Outputs are written next to the script;
an interrupted run resumes from `--work-dir` (default `/content/day4_work`).

## Settings
- imgsz {inf['imgsz']} ({inf['imgsz_source']}), conf {inf['conf']}, NMS IoU {inf['nms_iou']}, max_det {inf['max_det']}, retina_masks=True (masks at original resolution); device used: {inf['device_used']}.
- Matching: {m['match_rule']}.
- Area: {m['area_definition']}.

## Files
`area_metrics.json` (summary, size bins, comparison with the 30-image run), `area_per_image.csv` (one row per image, `in_previous_30` flags the earlier subset),
`area_matches.csv.gz` (all matched pairs; optional, lets the size analysis and medians be recomputed), `figures/`, `area_findings.md`.
""")


def parse(argv=None):
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-root", required=True, help="folder containing train/ valid/ test/ (M18KV2)")
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--out-dir", default=str(here))
    ap.add_argument("--work-dir", default="/content/day4_work")
    ap.add_argument("--test-dir", default="test")
    ap.add_argument("--n", type=int, default=0, help="0 = all test images; otherwise a random subset (seed)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--iou", type=float, default=0.7, help="NMS IoU")
    ap.add_argument("--imgsz", type=int, default=None)
    ap.add_argument("--max-det", type=int, default=1000)
    ap.add_argument("--device", default=None)
    ap.add_argument("--iou-thr", type=float, default=0.5)
    ap.add_argument("--wb-category-ids", type=int, nargs="*", default=None)
    ap.add_argument("--no-resume", action="store_true")
    return ap.parse_args(argv)


if __name__ == "__main__":
    sys.exit(run(parse()))
