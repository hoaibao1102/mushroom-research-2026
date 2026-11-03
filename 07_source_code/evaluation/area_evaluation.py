#!/usr/bin/env python3
"""Predicted-mask area evaluation on a deterministic 30-image subset of the M18K V2 test split.

Inference only (existing WB-only YOLOv8n-seg checkpoint). Reference = original COCO WB polygons
rasterised with pycocotools at original resolution. One-to-one matching by mask IoU >= 0.5
(greedy, highest IoU first). Area = verified mask_area.mask_area_px2 (sum(mask > 0)), unit px^2.
Outputs go to <repo>/09_results/area_evaluation/.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, platform, random, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mask_area import mask_area_px2, polygon_to_mask, _items  # verified counting method, unchanged

WB_KEYS = {"wb", "whitebutton"}
norm = lambda s: "".join(c for c in str(s).lower() if c.isalnum())


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def find_image(img_dir, file_name):
    for c in (img_dir / file_name, img_dir / Path(file_name).name):
        if c.exists():
            return c
    raise FileNotFoundError(f"{file_name} not under {img_dir}")


def match_greedy(iou, thr):
    """One-to-one: take pairs with IoU>=thr in descending IoU order (ties: lower indices first)."""
    if iou.size == 0:
        return []
    cand = sorted(np.argwhere(iou >= thr).tolist(), key=lambda p: (-iou[p[0], p[1]], p[0], p[1]))
    up, ug, out = set(), set(), []
    for p, g in cand:
        if p not in up and g not in ug:
            up.add(p); ug.add(g); out.append((p, g, float(iou[p, g])))
    return out


def yolo_predict(model, path, a, classes):
    """Binary instance masks at ORIGINAL resolution: uint8 (N,H,W) + confidences."""
    r = model.predict(source=str(path), imgsz=a.imgsz, conf=a.conf, iou=a.iou, max_det=a.max_det,
                      retina_masks=True, classes=classes, device=a.device, verbose=False)[0]
    H, W = r.orig_shape
    if r.masks is None or len(r.masks) == 0:
        return np.zeros((0, H, W), np.uint8), np.zeros(0)
    m = (r.masks.data.cpu().numpy() > 0.5).astype(np.uint8)
    return m, r.boxes.conf.cpu().numpy()


# ----------------------------------------------------------------------------- figures
def render_example(path_png, img_path, tag, rec, H, W, mu):
    import cv2, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt, matplotlib.patheffects as pe
    rgb = cv2.cvtColor(cv2.imread(str(img_path)), cv2.COLOR_BGR2RGB)
    mp = {m["p"] for m in rec["matches"]}; mg = {m["g"] for m in rec["matches"]}
    def overlay(items, matched_set, c_m, c_u):
        im = rgb.copy(); lay = im.copy()
        for i, rle in enumerate(items):
            m = mu.decode(rle).astype(np.uint8); col = c_m if i in matched_set else c_u
            lay[m > 0] = col
        im = cv2.addWeighted(lay, 0.35, im, 0.65, 0)
        for i, rle in enumerate(items):
            m = mu.decode(rle).astype(np.uint8); col = c_m if i in matched_set else c_u
            cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(im, cs, -1, col, 1)
        return im
    gt_img = overlay(rec["gt_rle"], mg, (0, 255, 0), (255, 255, 0))
    pr_img = overlay(rec["pred_rle"], mp, (255, 0, 0), (255, 0, 255))
    # zoom: centred on the matched pair with the largest absolute error (else image centre)
    cw, ch = max(W // 3, 64), max(H // 3, 64)
    if rec["matches"]:
        w = max(rec["matches"], key=lambda m: m["abs"]); x, y, bw, bh = mu.toBbox(rec["gt_rle"][w["g"]])
        cx, cy = x + bw / 2, y + bh / 2
    else:
        cx, cy = W / 2, H / 2
    x0 = int(min(max(cx - cw / 2, 0), W - cw)); y0 = int(min(max(cy - ch / 2, 0), H - ch))
    zoom = rgb.copy()
    for rles, col in ((rec["gt_rle"], (0, 255, 0)), (rec["pred_rle"], (255, 0, 0))):
        for rle in rles:
            x, y, bw, bh = mu.toBbox(rle)
            if x > x0 + cw or x + bw < x0 or y > y0 + ch or y + bh < y0: continue
            cs, _ = cv2.findContours(mu.decode(rle).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(zoom, cs, -1, col, 1)
    fig, ax = plt.subplots(2, 2, figsize=(16, 9.5))
    ax[0, 0].imshow(rgb); ax[0, 0].set_title("RGB (original resolution)")
    ax[0, 1].imshow(gt_img); ax[0, 1].set_title(f"GT masks (COCO polygons): {len(rec['gt_rle'])}  [green matched, yellow unmatched]")
    ax[1, 0].imshow(pr_img); ax[1, 0].set_title(f"Predicted masks: {len(rec['pred_rle'])}  [red matched, magenta unmatched]")
    ax[1, 1].imshow(zoom[y0:y0 + ch, x0:x0 + cw], extent=(x0, x0 + cw, y0 + ch, y0)); ax[1, 1].set_title("Zoom: GT (green) vs pred (red) contours; labels = GT / pred area px²")
    shown = 0
    for m in sorted(rec["matches"], key=lambda m: m["abs"], reverse=True):
        x, y, bw, bh = mu.toBbox(rec["gt_rle"][m["g"]]); tx, ty = x + bw / 2, y + bh / 2
        if x0 <= tx <= x0 + cw and y0 <= ty <= y0 + ch and shown < 14:
            ax[1, 1].text(tx, ty, f"G {m['gt']}\nP {m['pred']}", color="white", fontsize=6, ha="center", va="center",
                          path_effects=[pe.withStroke(linewidth=1.5, foreground="black")]); shown += 1
    for a_ in ax.ravel(): a_.axis("off")
    mae = np.mean([m["abs"] for m in rec["matches"]]) if rec["matches"] else float("nan")
    fig.suptitle(f"[{tag}] {rec['filename']}  |  GT {len(rec['gt_rle'])}, pred {len(rec['pred_rle'])}, matched {len(rec['matches'])}, "
                 f"image MAE {mae:.1f} px²  (areas in px², not mm²)", fontsize=11)
    fig.tight_layout(); fig.savefig(path_png, dpi=130); plt.close(fig)


# ----------------------------------------------------------------------------- main run
def run(a, model=None, predictor=None):
    from pycocotools import mask as mu
    from PIL import Image
    out = Path(a.out_dir); (out / "area_examples").mkdir(parents=True, exist_ok=True)
    coco = Path(a.data_root) / a.test_dir / "annotations_coco.json"
    img_dir = Path(a.data_root) / a.test_dir / "rgb"
    cats = list(_items(coco, "categories"))
    wb_ids = set(a.wb_category_ids) if a.wb_category_ids else {c["id"] for c in cats if norm(c.get("name", "")) in WB_KEYS}
    if not wb_ids: sys.exit(f"WB category not found: {cats}")
    images = sorted(_items(coco, "images"), key=lambda i: i["file_name"])
    idx = sorted(random.Random(a.seed).sample(range(len(images)), a.n))
    sel = [images[i] for i in idx]
    with open(out / "selected_test_images.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["image_id", "filename", "selection_seed"])
        for im in sel: w.writerow([im["id"], im["file_name"], a.seed])
    sel_ids = {i["id"] for i in sel}; gt_by = defaultdict(list); wb_total = 0
    for ann in _items(coco, "annotations"):
        if ann.get("category_id") in wb_ids:
            wb_total += 1
            if ann["image_id"] in sel_ids: gt_by[ann["image_id"]].append(ann)
    print(f"test images={len(images)}  WB annotations (incl. crowd)={wb_total}  selected={len(sel)}")

    # model
    ck = Path(a.checkpoint)
    if model is None:
        from ultralytics import YOLO
        import ultralytics, torch
        model = YOLO(str(ck))
    names = dict(model.names)
    one = [k for k, v in names.items() if norm(v) in WB_KEYS]
    classes = None if len(names) == 1 else (one or sys.exit(f"no WB class in model names {names}"))
    train_args = getattr(model, "ckpt", None) or {}
    train_args = train_args.get("train_args", {}) if isinstance(train_args, dict) else {}
    if a.imgsz is None:
        a.imgsz = int(train_args.get("imgsz", 640)) if str(train_args.get("imgsz", "")).isdigit() or isinstance(train_args.get("imgsz"), int) else 640
        imgsz_src = "checkpoint train_args" if "imgsz" in train_args else "default 640 (train imgsz NOT_VERIFIED)"
    else:
        imgsz_src = "command line"
    predictor = predictor or (lambda p: yolo_predict(model, p, a, classes))

    rows, un_p, un_g, per_img, recs = [], [], [], [], {}
    tot = Counter(); excl_all = Counter()
    for im in sel:
        path = find_image(img_dir, im["file_name"])
        with Image.open(path) as I: W, H = I.size
        size_ok = (W, H) == (im["width"], im["height"])
        masks, confs = predictor(path)
        assert masks.shape[1:] == (H, W), f"pred mask {masks.shape} != image {(H, W)}"
        gts, excl = [], Counter()
        for ann in sorted(gt_by[im["id"]], key=lambda x: x["id"]):
            seg = ann.get("segmentation")
            if ann.get("iscrowd", 0): excl["iscrowd"] += 1; continue
            if not isinstance(seg, list): excl["non_polygon"] += 1; continue
            rings = [r for r in seg if isinstance(r, list) and len(r) >= 6 and len(r) % 2 == 0]
            if not rings: excl["no_valid_ring"] += 1; continue
            m = polygon_to_mask(rings, H, W); ar = mask_area_px2(m)
            if ar == 0: excl["zero_area_mask"] += 1; continue
            gts.append(dict(id=ann["id"], area=ar, rle=mu.encode(np.asfortranarray(m))))
        excl_all.update(excl)
        preds = []
        for i in range(len(masks)):
            preds.append(dict(area=mask_area_px2(masks[i]), rle=mu.encode(np.asfortranarray(masks[i])), conf=float(confs[i])))
        iou = np.asarray(mu.iou([p["rle"] for p in preds], [g["rle"] for g in gts], [0] * len(gts))) if preds and gts else np.zeros((len(preds), len(gts)))
        pairs = match_greedy(iou, a.iou_thr)
        mp, mg = {p for p, _, _ in pairs}, {g for _, g, _ in pairs}
        ms = []
        for p, g, v in pairs:
            ae = abs(preds[p]["area"] - gts[g]["area"]); rel = 100.0 * ae / gts[g]["area"]
            rows.append([im["id"], gts[g]["id"], p, round(v, 6), gts[g]["area"], preds[p]["area"], ae, round(rel, 6)])
            ms.append(dict(p=p, g=g, abs=ae, gt=gts[g]["area"], pred=preds[p]["area"]))
        for p in range(len(preds)):
            if p not in mp: un_p.append([im["id"], p, round(preds[p]["conf"], 4), preds[p]["area"], round(float(iou[p].max()), 4) if iou.shape[1] else 0.0])
        for g in range(len(gts)):
            if g not in mg: un_g.append([im["id"], gts[g]["id"], gts[g]["area"], round(float(iou[:, g].max()), 4) if iou.shape[0] else 0.0])
        mae = float(np.mean([m["abs"] for m in ms])) if ms else None
        per_img.append(dict(image_id=im["id"], filename=im["file_name"], width=W, height=H, size_matches_coco=size_ok,
                            gt_raw=len(gt_by[im["id"]]), gt_reference=len(gts), pred=len(preds), matched=len(pairs),
                            unmatched_pred=len(preds) - len(pairs), unmatched_gt=len(gts) - len(pairs), mae_px2=mae,
                            gt_total_area_px2=sum(g["area"] for g in gts), pred_total_area_px2=sum(p["area"] for p in preds)))
        recs[im["id"]] = dict(filename=im["file_name"], path=path, H=H, W=W, matches=ms,
                              gt_rle=[g["rle"] for g in gts], pred_rle=[p["rle"] for p in preds])
        print(f"{im['file_name']}: gt={len(gts)} pred={len(preds)} matched={len(pairs)} MAE={mae}")

    def wcsv(name, head, data):
        with open(out / name, "w", newline="") as f: w = csv.writer(f); w.writerow(head); w.writerows(data)
    wcsv("mask_area_matches.csv", ["image_id", "gt_annotation_id", "pred_instance_index", "mask_iou", "gt_area_px2", "pred_area_px2", "abs_error_px2", "relative_error_pct"], rows)
    wcsv("unmatched_predictions.csv", ["image_id", "pred_instance_index", "pred_conf", "pred_area_px2", "best_iou_with_any_gt"], un_p)
    wcsv("unmatched_gt.csv", ["image_id", "gt_annotation_id", "gt_area_px2", "best_iou_with_any_pred"], un_g)
    wcsv("per_image_summary.csv", list(per_img[0]), [list(d.values()) for d in per_img])

    ae = np.array([r[6] for r in rows], float); rel = np.array([r[7] for r in rows], float)
    sg = np.array([r[5] - r[4] for r in rows], float)
    n_gt = sum(d["gt_reference"] for d in per_img); n_pr = sum(d["pred"] for d in per_img); n_m = len(rows)
    summary = dict(
        sample_size_images=len(sel), selection=f"images sorted by filename; random.Random({a.seed}).sample(range({len(images)}), {a.n}); listed in filename order",
        test_images_total=len(images), test_wb_annotations_total_in_coco=wb_total, subset_wb_annotations_raw=sum(d["gt_raw"] for d in per_img),
        gt_reference_instances=n_gt, gt_excluded=dict(excl_all), predicted_instances=n_pr, matched=n_m,
        unmatched_predictions=n_pr - n_m, unmatched_gt=n_gt - n_m,
        match_coverage_matched_over_gt=n_m / n_gt if n_gt else None, matched_over_predictions=n_m / n_pr if n_pr else None,
        match_rule=f"one-to-one greedy by descending mask IoU, IoU >= {a.iou_thr}; masks at original resolution; GT=pycocotools-rasterised COCO polygons (non-crowd, non-zero area)",
        area_definition="A_px2 = sum(mask > 0) via mask_area.mask_area_px2; unit px2 (not mm2)",
        mae_px2=float(ae.mean()) if n_m else "NOT_VERIFIED", mean_relative_error_pct=float(rel.mean()) if n_m else "NOT_VERIFIED",
        extra=dict(median_relative_error_pct=float(np.median(rel)) if n_m else None, mean_signed_error_px2_pred_minus_gt=float(sg.mean()) if n_m else None,
                   matched_pred_over_gt_area_ratio=float(sum(r[5] for r in rows) / sum(r[4] for r in rows)) if n_m else None),
        all_pred_sizes_match_coco_image_size=all(d["size_matches_coco"] for d in per_img),
        model=dict(path=str(ck), sha256=sha256(ck) if ck.exists() else "NOT_VERIFIED", names=names, train_args={k: str(train_args.get(k)) for k in ("imgsz", "epochs", "data", "model", "seed") if k in train_args}),
        inference=dict(imgsz=a.imgsz, imgsz_source=imgsz_src, conf=a.conf, nms_iou=a.iou, max_det=a.max_det, retina_masks=True, classes=classes, device=str(a.device),
                       note="inference settings fixed before looking at results; not tuned"),
        versions=dict(python=platform.python_version(), numpy=np.__version__, **{k: v for k, v in _vers().items()}))
    (out / "mask_area_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    # example figures: best / median / worst image MAE + most unmatched
    ok = [d for d in per_img if d["mae_px2"] is not None]
    ok.sort(key=lambda d: d["mae_px2"])
    picks = [("best_mae", ok[0]), ("median_mae", ok[len(ok) // 2]), ("worst_mae", ok[-1]),
             ("most_unmatched", max(per_img, key=lambda d: d["unmatched_pred"] + d["unmatched_gt"]))] if ok else []
    seen, idx_rows = set(), []
    for tag, d in picks:
        if d["image_id"] in seen: continue
        seen.add(d["image_id"]); r = recs[d["image_id"]]
        fn = out / "area_examples" / f"{tag}_{d['image_id']}_{Path(d['filename']).stem}.png"
        render_example(fn, r["path"], tag, r, r["H"], r["W"], mu); idx_rows.append([tag, d["image_id"], d["filename"], fn.name]); print("figure", fn.name)
    wcsv("area_examples/examples_index.csv", ["criterion", "image_id", "filename", "png"], idx_rows)
    write_findings(out, summary, per_img)
    print(json.dumps({k: summary[k] for k in ("gt_reference_instances", "predicted_instances", "matched", "unmatched_predictions", "unmatched_gt", "match_coverage_matched_over_gt", "mae_px2", "mean_relative_error_pct")}, indent=2))
    return 0


def _vers():
    v = {}
    for m in ("ultralytics", "torch", "pycocotools", "cv2"):
        try: v[m] = __import__(m).__version__
        except Exception: v[m] = "NOT_VERIFIED"
    return v


def write_findings(out, s, per_img):
    f = lambda x, d=2: f"{x:.{d}f}" if isinstance(x, (int, float)) else str(x)
    e = s["extra"]
    (out / "area_findings.md").write_text(f"""# Predicted-mask area evaluation (draft generated from executed results)

Subset: {s['sample_size_images']} test images (seed {s['selection'].split('Random(')[1].split(')')[0]}), model sha256 `{str(s['model']['sha256'])[:16]}...`, inference {s['inference']}.

| quantity | value |
|---|---|
| reference GT instances | {s['gt_reference_instances']} (excluded: {s['gt_excluded']}) |
| predicted instances | {s['predicted_instances']} |
| matched (IoU >= 0.5, one-to-one) | {s['matched']} |
| unmatched predictions / unmatched GT | {s['unmatched_predictions']} / {s['unmatched_gt']} |
| match coverage (matched / GT) | {f(100 * s['match_coverage_matched_over_gt'], 1) if s['match_coverage_matched_over_gt'] is not None else 'NOT_VERIFIED'} % |
| MAE | {f(s['mae_px2'])} px² |
| mean relative error | {f(s['mean_relative_error_pct'])} % (median {f(e['median_relative_error_pct'])} %) |
| mean signed error (pred - GT) | {f(e['mean_signed_error_px2_pred_minus_gt'])} px² |

## Conclusions
TODO: write after reading the figures in `area_examples/` and `per_image_summary.csv`.

## Limitations
- 30-image measurement audit, not a model benchmark; errors are over matched instances only (unmatched objects are reported separately and not in MAE).
- Reference masks are rasterised COCO polygons, not pixel-perfect ground truth; areas are px², not mm², and say nothing about quality.
- Inference settings (conf, NMS IoU, imgsz) affect which instances exist and their masks; they were fixed, not tuned.
""")


def parse(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-root", required=True, help="folder containing train/ valid/ test/ (M18KV2)")
    ap.add_argument("--repo-root", required=True, help="wb_task_repo (outputs to 09_results/area_evaluation)")
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--test-dir", default="test")
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--iou", type=float, default=0.7, help="NMS IoU")
    ap.add_argument("--imgsz", type=int, default=None, help="default: checkpoint train imgsz, else 640")
    ap.add_argument("--max-det", type=int, default=1000)
    ap.add_argument("--device", default=None)
    ap.add_argument("--iou-thr", type=float, default=0.5, help="matching mask IoU threshold")
    ap.add_argument("--wb-category-ids", type=int, nargs="*", default=None)
    a = ap.parse_args(argv)
    a.out_dir = a.out_dir or str(Path(a.repo_root) / "09_results" / "area_evaluation")
    return a


if __name__ == "__main__":
    sys.exit(run(parse()))
