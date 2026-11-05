#!/usr/bin/env python3
"""Day 5 extra checks (supporting findings.md). Run after depth_area.py; prints results only.
  1. dtype census over all depth .npy files of the split
  2. mask-free RGB-vs-depth alignment scan (RGB gradient vs depth gradient correlation) on the same 30 images (seed 42)
  3. where the low-depth-validity WB masks are located horizontally, width of the left invalid band, count of extreme depth values
Usage: python extra_checks.py --data-root <.../M18KV2> [--split test]
"""
import argparse, collections, random, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, str(Path(__file__).resolve().parent))
import depth_area as da


def gm(x):
    x = cv2.GaussianBlur(x.astype(np.float32), (5, 5), 0)
    return np.log1p(np.hypot(cv2.Sobel(x, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(x, cv2.CV_32F, 0, 1, ksize=3)))


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--data-root", required=True); ap.add_argument("--split", default="test")
    a = ap.parse_args(argv)
    split = Path(a.data_root) / a.split; cj = split / "annotations_coco.json"
    cnt = collections.Counter(np.load(p, mmap_mode="r").dtype.name for p in sorted((split / "depth").glob("*.npy")))
    print("dtype of all depth files:", dict(cnt))
    imgs = sorted(da._items(cj, "images"), key=lambda i: i["file_name"])
    sel = [imgs[i] for i in sorted(random.Random(42).sample(range(len(imgs)), 30))]
    res = []
    for im in sel:  # mask-free test: RGB edges vs depth edges
        g = cv2.imread(str(split / "rgb" / im["file_name"]), 0)
        d = np.load(split / "depth" / (Path(im["file_name"]).stem + ".npy")).astype(np.float32); v = (d > 0).astype(np.float32)
        n = cv2.GaussianBlur(d * v, (7, 7), 0); w = cv2.GaussianBlur(v, (7, 7), 0)
        g1, g2, ok = gm(g), gm(np.where(w > 0.5, n / np.maximum(w, 1e-6), 0)), w > 0.9
        H, W = g.shape; M = 30; best = (-9, None)
        for dy in range(-8, 9, 2):
            for dx in range(-24, 25, 2):
                m = ok[M + dy:H - M + dy, M + dx:W - M + dx]
                c = np.corrcoef(g1[M:H - M, M:W - M][m], g2[M + dy:H - M + dy, M + dx:W - M + dx][m])[0, 1]
                if c > best[0]: best = (c, (dy, dx))
        res.append(best[1])
    print("best RGB-depth shift (dy,dx) per image, counts:", collections.Counter(res).most_common(10))
    wb = {c["id"] for c in da._items(cj, "categories") if da.norm(c["name"]) in da.WB_KEYS}
    ids = {i["id"] for i in sel}; anns = {}
    for an in da._items(cj, "annotations"):
        if an["category_id"] in wb and an["image_id"] in ids and not an.get("iscrowd", 0) and isinstance(an["segmentation"], list):
            anns.setdefault(an["image_id"], []).append(an)
    band, low_cx, big, tot = [], [], 0, 0
    for im in sel:
        d = np.load(split / "depth" / (Path(im["file_name"]).stem + ".npy")).astype(np.float32); H, W = d.shape
        band.append(int(np.argmax((d > 0).mean(0) >= 0.5)))
        for an in anns.get(im["id"], []):
            r = [x for x in an["segmentation"] if isinstance(x, list) and len(x) >= 6]
            if not r: continue
            m = da.polygon_to_mask(r, H, W) > 0; v = d[m]
            if v.size == 0: continue
            tot += v.size; big += int((v > 5000).sum())
            if (v > 0).mean() < 0.5:
                xs = np.nonzero(m.any(0))[0]; low_cx.append((xs.min() + xs.max()) / 2 / W)
    low_cx = np.array(low_cx)
    print("left invalid band width in px (min/median/max):", min(band), int(np.median(band)), max(band))
    print("low-validity (<50%) masks:", len(low_cx), "| centre x < 10% of width:", int((low_cx < 0.10).sum()),
          "| 10-90%:", int(((low_cx >= .1) & (low_cx <= .9)).sum()), "| > 90%:", int((low_cx > .9).sum()))
    print("mask pixels with raw depth > 5000:", big, "of", tot, f"({100 * big / tot:.4f}%)")


if __name__ == "__main__":
    main()
