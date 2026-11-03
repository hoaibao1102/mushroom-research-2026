#!/usr/bin/env python3
"""WB-only YOLO-segmentation dataset builder / Colab reconstruction (M18K V2).

Modes
  build    stream the original COCO JSONs, write WB-only labels (class 0), manifest, build
           metadata, conversion summary, and Drive zip `derived_datasets/wb_yolo_labels.zip`.
  rebuild  fresh runtime: unzip labels+manifest from Drive, recreate runtime image symlinks to
           the Drive RGB files, write data.yaml, verify (one class `0: WB`, split counts, labels).
  report   write 09_results/reports/wb_dataset_measurement.md from real summary/CSV outputs.

Conventions copied from the EDA notebook (README): SEED=42, DRIVE_ROOT, DATA_ROOT, WORK_ROOT,
REPORT_DIR, SPLIT_DIRS = {'train':'train','valid':'val','test':'test'} (original dir -> YOLO split).
Original COCO JSON and the two-class YOLO_ROOT are never modified. Cached YOLO labels are NOT
reused (provenance/conversion loss unknown) -> labels come directly from the COCO JSON.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, hashlib, json, os, platform, shutil, sys, zipfile
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

SCRIPT_VERSION = "1.0.0"
SEED = 42
DRIVE_ROOT = Path("/content/drive/MyDrive/M18K_Reproduction")
WORK_ROOT = Path("/content/M18K_V2_work")
SPLIT_DIRS = {"train": "train", "valid": "val", "test": "test"}  # original dir -> yolo split
EXPECTED_IMAGES = {"train": 3596, "val": 449, "test": 450}
EXPECTED_WB_EDA = {"train": 558859, "val": 70680, "test": 70192}
WB_KEYS, BB_KEYS = {"wb", "whitebutton"}, {"bb", "brownbutton"}
BB_POLICY = ("All non-WB annotations (BB and any other category) are omitted from the WB labels. "
             "They are NOT target labels: omitted BB objects are unlabeled background in this WB-only dataset. "
             "Images are kept (original split membership) even when they contain only BB; such images get empty label files.")
YAML_TEMPLATE = ("# WB-only, one-class schema (White Button).\n"
                 "# __WB_ROOT__ is resolved at runtime by 07_source_code/data/build_wb_dataset.py\n"
                 "path: __WB_ROOT__\ntrain: images/train\nval: images/val\ntest: images/test\nnc: 1\nnames:\n  0: WB\n")


# ------------------------------------------------------------------ paths
def resolve(a):
    drive = Path(a.drive_root)
    P = argparse.Namespace()
    P.drive = drive
    P.data = Path(a.data_root) if a.data_root else drive / "M18K_V2_data" / "M18KV2"
    P.work = Path(a.work_root)
    P.report_dir = drive / "reports" / "v2_eda"
    P.yolo = P.work / "yolo_v2"
    P.wb = P.work / "yolo_v2_wb"
    P.repo = Path(a.repo_root) if a.repo_root else drive / "wb_task_repo"
    P.zip = Path(a.zip_path) if a.zip_path else drive / "derived_datasets" / "wb_yolo_labels.zip"
    P.metrics = P.repo / "09_results" / "metrics"
    P.reports = P.repo / "09_results" / "reports"
    P.config = P.repo / "08_experiments" / "configs" / "wb_dataset.yaml"
    if P.wb.resolve() == P.yolo.resolve():
        sys.exit("refusing: WB_ROOT must differ from the original two-class YOLO_ROOT")
    return P


def sha256(p, chunk=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------ COCO streaming
def _clean(o):
    if isinstance(o, Decimal): return float(o)
    if isinstance(o, list): return [_clean(x) for x in o]
    if isinstance(o, dict): return {k: _clean(v) for k, v in o.items()}
    return o


class CocoStream:
    """Streams categories/images/annotations (ijson with a C backend; json.load otherwise)."""
    def __init__(self, path):
        self.path, self._data = Path(path), None
        try:
            import ijson
            self.ijson = ijson if ijson.backend != "python" else None
        except ImportError:
            self.ijson = None
        self.mode = f"ijson[{self.ijson.backend}]" if self.ijson else "json.load"

    def items(self, key):
        if self.ijson:
            with open(self.path, "rb") as f:
                for it in self.ijson.items(f, key + ".item"):
                    yield _clean(it)
        else:
            if self._data is None:
                with open(self.path) as f:
                    self._data = json.load(f)
            yield from self._data.get(key, [])


def find_coco(data_root, orig):
    for c in (data_root / orig / "annotations_coco.json", data_root / "annotations" / f"{orig}_coco.json"):
        if c.exists(): return c
    hits = sorted((data_root / orig).rglob("annotations_coco.json")) if (data_root / orig).exists() else []
    if hits: return hits[0]
    raise FileNotFoundError(f"annotations_coco.json not found under {data_root/orig}")


def map_categories(cats, wb_ids=None):
    norm = lambda s: "".join(c for c in str(s).lower() if c.isalnum())
    roles = {}
    for c in cats:
        k = norm(c.get("name", ""))
        if wb_ids is not None: roles[c["id"]] = "WB" if c["id"] in wb_ids else ("BB" if k in BB_KEYS else "OTHER")
        else: roles[c["id"]] = "WB" if k in WB_KEYS else ("BB" if k in BB_KEYS else "OTHER")
    if "WB" not in roles.values():
        raise RuntimeError(f"No category mapped to WB. COCO categories: {cats}. Re-run with --wb-category-ids.")
    return roles


# ------------------------------------------------------------------ geometry
def ring_area(r):
    xs, ys, n, s = r[0::2], r[1::2], len(r) // 2, 0.0
    for i in range(n):
        j = (i + 1) % n
        s += xs[i] * ys[j] - xs[j] * ys[i]
    return abs(s) / 2.0


def convert_wb(ann, w, h, st):
    """Return a YOLO-seg line for one WB annotation (class 0) or None; every outcome is counted."""
    st["wb_raw"] += 1
    if ann.get("iscrowd", 0):
        st["wb_iscrowd_excluded"] += 1; return None
    seg = ann.get("segmentation")
    if not seg: st["skipped"]["missing_segmentation"] += 1; return None
    if isinstance(seg, dict): st["skipped"]["rle_non_polygon"] += 1; return None
    if w <= 0 or h <= 0: st["skipped"]["bad_image_size"] += 1; return None
    rings = []
    for r in seg:
        if isinstance(r, (list, tuple)) and len(r) >= 6 and len(r) % 2 == 0: rings.append(list(r))
        else: st["invalid_rings_dropped"] += 1       # <3 points / odd length
    if not rings: st["skipped"]["no_valid_ring"] += 1; return None
    areas = [ring_area(r) for r in rings]
    k = max(range(len(rings)), key=areas.__getitem__)
    st["all_component_area_px2"] += sum(areas)
    st["kept_component_area_px2"] += areas[k]
    if len(rings) > 1:                                # largest-component-only approximation
        st["multi_component_annotations"] += 1
        st["extra_components_discarded"] += len(rings) - 1
        st["discarded_component_area_px2"] += sum(areas) - areas[k]
    r = rings[k]; out, clipped = [], False
    for i in range(0, len(r), 2):
        x, y = min(max(r[i], 0.0), w), min(max(r[i + 1], 0.0), h)
        clipped |= (x != r[i]) or (y != r[i + 1])
        out += [x / w, y / h]
    if clipped: st["annotations_clipped_to_image"] += 1
    if ring_area(out) <= 0: st["skipped"]["degenerate_after_clip"] += 1; return None
    st["wb_converted"] += 1
    return "0 " + " ".join(f"{v:.6f}" for v in out)


def new_stats():
    return dict(images=0, annotations_total=0, wb_raw=0, wb_iscrowd_excluded=0, wb_converted=0,
                skipped=Counter(), invalid_rings_dropped=0, multi_component_annotations=0,
                extra_components_discarded=0, all_component_area_px2=0.0, kept_component_area_px2=0.0,
                discarded_component_area_px2=0.0, annotations_clipped_to_image=0, non_wb_omitted=0,
                ann_by_role=Counter(), ann_by_category_id=Counter(), orphan_annotations=0,
                images_with_wb=0, empty_label_files=0, missing_source_images=0, wb_instances_written=0)


# ------------------------------------------------------------------ build
def build(a, P):
    if P.wb.exists():
        shutil.rmtree(P.wb / "labels", ignore_errors=True)
    (P.wb / "labels").mkdir(parents=True, exist_ok=True)
    summary = dict(script_version=SCRIPT_VERSION, seed=SEED, bb_policy=BB_POLICY, splits={}, source_category_mapping={},
                   cached_yolo_labels_reused=False,
                   note_cached="Cached YOLO labels not reused: provenance/conversion loss NOT_VERIFIED; labels streamed from COCO JSON.")
    manifest, meta_src = [], {}
    for orig, split in SPLIT_DIRS.items():
        coco_path = find_coco(P.data, orig)
        cs = CocoStream(coco_path)
        cats = list(cs.items("categories"))
        roles = map_categories(cats, set(a.wb_category_ids) if a.wb_category_ids else None)
        summary["source_category_mapping"][orig] = [dict(id=c["id"], name=c.get("name"), role=roles[c["id"]]) for c in cats]
        st = new_stats()
        imgs = {}
        for im in cs.items("images"):
            imgs[im["id"]] = im
        st["images"] = len(imgs)
        stems = Counter(Path(i["file_name"]).stem for i in imgs.values())
        dup = [s for s, n in stems.items() if n > 1]
        if dup: raise RuntimeError(f"[{orig}] duplicate image stems -> label collision: {dup[:5]}")
        lines = defaultdict(list)
        for ann in cs.items("annotations"):
            st["annotations_total"] += 1
            role = roles.get(ann.get("category_id"), "UNMAPPED")
            st["ann_by_role"][role] += 1; st["ann_by_category_id"][str(ann.get("category_id"))] += 1
            im = imgs.get(ann.get("image_id"))
            if im is None: st["orphan_annotations"] += 1; continue
            if role != "WB": st["non_wb_omitted"] += 1; continue
            ln = convert_wb(ann, im["width"], im["height"], st)
            if ln: lines[im["id"]].append(ln)
        ldir = P.wb / "labels" / split; ldir.mkdir(parents=True, exist_ok=True)
        for iid in sorted(imgs):
            im = imgs[iid]; name = Path(im["file_name"]).name; stem = Path(name).stem
            body = lines.get(iid, [])
            lp = ldir / f"{stem}.txt"
            lp.write_text("\n".join(body) + ("\n" if body else ""))
            n = len(body); st["wb_instances_written"] += n
            st["images_with_wb"] += n > 0; st["empty_label_files"] += n == 0
            rel = f"{orig}/rgb/{im['file_name']}"
            if not (P.data / rel).exists():
                alt = f"{orig}/rgb/{name}"
                if (P.data / alt).exists(): rel = alt
                else: st["missing_source_images"] += 1
            manifest.append(dict(split=split, source_split=orig, image_id=iid, file_name=im["file_name"],
                                 source_rel_path=rel, width=im["width"], height=im["height"], wb_instances=n,
                                 label_rel_path=f"labels/{split}/{stem}.txt", label_sha256=sha256(lp),
                                 source_image_exists=(P.data / rel).exists()))
        meta_src[orig] = dict(coco_json=str(coco_path), coco_bytes=coco_path.stat().st_size,
                              coco_sha256=sha256(coco_path), reader=cs.mode)
        eda, skipped = EXPECTED_WB_EDA[split], sum(st["skipped"].values())
        assert st["wb_raw"] == st["wb_iscrowd_excluded"] + skipped + st["wb_converted"], "count identity broken"
        assert st["wb_converted"] == st["wb_instances_written"]
        raw_diff = st["wb_raw"] - eda
        d = {k: (dict(v) if isinstance(v, Counter) else v) for k, v in st.items()}
        d.update(wb_skipped_total=skipped, expected_images=EXPECTED_IMAGES[split],
                 images_match_expected=st["images"] == EXPECTED_IMAGES[split],
                 eda_wb_annotations=eda, raw_wb_minus_eda=raw_diff,
                 converted_minus_eda=st["wb_converted"] - eda,
                 discarded_area_fraction=(st["discarded_component_area_px2"] / st["all_component_area_px2"]
                                          if st["all_component_area_px2"] else 0.0),
                 reconciliation=("raw WB equals EDA count; converted = raw - iscrowd - skipped "
                                 f"({st['wb_raw']} - {st['wb_iscrowd_excluded']} - {skipped} = {st['wb_converted']})"
                                 if raw_diff == 0 else
                                 f"raw WB differs from EDA by {raw_diff:+d}; cause NOT_VERIFIED (compare with the notebook's counting rule)"))
        summary["splits"][split] = d
        print(f"[{split}] images={st['images']} raw_WB={st['wb_raw']} converted={st['wb_converted']} "
              f"crowd={st['wb_iscrowd_excluded']} skipped={skipped} multi_component={st['multi_component_annotations']} "
              f"empty_labels={st['empty_label_files']} (EDA {eda}, diff {raw_diff:+d})")
    # artifacts
    write_yaml(P)
    if not P.config.exists():
        P.config.parent.mkdir(parents=True, exist_ok=True); P.config.write_text(YAML_TEMPLATE)
    mp = P.wb / "manifest.csv"
    with open(mp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0])); w.writeheader(); w.writerows(manifest)
    meta = dict(script_version=SCRIPT_VERSION, seed=SEED, created_utc=dt.datetime.utcnow().isoformat() + "Z",
                python=platform.python_version(), platform=platform.platform(), split_dirs=SPLIT_DIRS,
                paths=dict(DATA_ROOT=str(P.data), WORK_ROOT=str(P.work), WB_ROOT=str(P.wb), YOLO_ROOT_untouched=str(P.yolo)),
                sources=meta_src, class_names={0: "WB"}, bb_policy=BB_POLICY)
    (P.wb / "build_metadata.json").write_text(json.dumps(meta, indent=2))
    ver = make_links_and_verify(P, manifest)
    summary["verification"] = ver
    P.metrics.mkdir(parents=True, exist_ok=True)
    (P.wb / "wb_conversion_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    (P.metrics / "wb_conversion_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    make_zip(P)
    print("verification ok:", ver["ok"], ver["problems"][:5])
    return 0 if ver["ok"] else 2


def write_yaml(P):
    tpl = P.config.read_text() if P.config.exists() else YAML_TEMPLATE
    (P.wb / "data.yaml").write_text(tpl.replace("__WB_ROOT__", str(P.wb)))


def make_zip(P):
    P.zip.parent.mkdir(parents=True, exist_ok=True)
    if P.zip.exists():
        P.zip.rename(P.zip.with_name(P.zip.stem + f".bak_{dt.datetime.utcnow():%Y%m%dT%H%M%S}.zip"))
    with zipfile.ZipFile(P.zip, "w", zipfile.ZIP_DEFLATED) as z:      # labels + manifest + metadata ONLY
        for f in sorted((P.wb / "labels").rglob("*.txt")): z.write(f, f.relative_to(P.wb).as_posix())
        for n in ("manifest.csv", "build_metadata.json", "wb_conversion_summary.json"):
            if (P.wb / n).exists(): z.write(P.wb / n, n)
    print(f"zip: {P.zip} ({P.zip.stat().st_size/1e6:.1f} MB)")


# ------------------------------------------------------------------ links + verification
def make_links_and_verify(P, manifest):
    for sp in SPLIT_DIRS.values(): shutil.rmtree(P.wb / "images" / sp, ignore_errors=True); (P.wb / "images" / sp).mkdir(parents=True)
    for r in manifest:
        link = P.wb / "images" / r["split"] / Path(r["file_name"]).name
        if os.path.lexists(link): os.remove(link)
        os.symlink(P.data / r["source_rel_path"], link)
    write_yaml(P)
    return verify(P)


def verify(P):
    res = dict(ok=True, problems=[], splits={})
    def bad(m): res["ok"] = False; res["problems"].append(m)
    try:
        import yaml; d = yaml.safe_load((P.wb / "data.yaml").read_text())
    except ImportError:
        txt = (P.wb / "data.yaml").read_text(); d = dict(nc=1 if "nc: 1" in txt else None, names={0: "WB"} if "0: WB" in txt else None)
    res["yaml_nc"], res["yaml_names"] = d.get("nc"), d.get("names")
    if d.get("nc") != 1 or d.get("names") != {0: "WB"}: bad(f"yaml not one-class '0: WB': {d.get('nc')}, {d.get('names')}")
    for sp in SPLIT_DIRS.values():
        idir, ldir = P.wb / "images" / sp, P.wb / "labels" / sp
        imgs = sorted(idir.iterdir()) if idir.exists() else []
        labs = sorted(ldir.glob("*.txt")) if ldir.exists() else []
        broken = [p.name for p in imgs if not p.exists()]
        s = dict(images=len(imgs), labels=len(labs), broken_links=len(broken), nonempty=0, empty=0, instances=0, bad_lines=0)
        for lp in labs:
            t = [l for l in lp.read_text().splitlines() if l.strip()]
            s["nonempty"] += bool(t); s["empty"] += not t
            for l in t:
                p = l.split(); ok = p[0] == "0" and len(p) >= 7 and len(p) % 2 == 1
                try: ok = ok and all(0.0 <= float(v) <= 1.0 for v in p[1:])
                except ValueError: ok = False
                s["instances"] += 1; s["bad_lines"] += not ok
        if s["images"] != EXPECTED_IMAGES[sp]: bad(f"{sp}: images {s['images']} != {EXPECTED_IMAGES[sp]}")
        if s["labels"] != s["images"]: bad(f"{sp}: labels {s['labels']} != images {s['images']}")
        if {p.stem for p in imgs} != {p.stem for p in labs}: bad(f"{sp}: image/label stems differ")
        if broken: bad(f"{sp}: {len(broken)} broken symlinks, e.g. {broken[:3]}")
        if s["bad_lines"]: bad(f"{sp}: {s['bad_lines']} malformed/non-class-0 lines")
        res["splits"][sp] = s
    return res


def rebuild(a, P):
    if not P.zip.exists(): sys.exit(f"BLOCKED: {P.zip} missing")
    if not P.data.exists(): sys.exit(f"BLOCKED: DATA_ROOT missing: {P.data}")
    shutil.rmtree(P.wb, ignore_errors=True); P.wb.mkdir(parents=True)
    with zipfile.ZipFile(P.zip) as z:
        for n in z.namelist():
            if n.startswith(("/", "..")) or ".." in Path(n).parts: sys.exit(f"unsafe zip member {n}")
            if not (n.startswith("labels/") or n in ("manifest.csv", "build_metadata.json", "wb_conversion_summary.json")):
                sys.exit(f"unexpected zip member {n} (zip must contain labels/manifest/metadata only)")
        z.extractall(P.wb)
    with open(P.wb / "manifest.csv") as f: manifest = list(csv.DictReader(f))
    ver = make_links_and_verify(P, manifest)
    P.metrics.mkdir(parents=True, exist_ok=True)
    (P.metrics / "wb_rebuild_verification.json").write_text(json.dumps(ver, indent=2))
    print(json.dumps(ver, indent=2)); print("REBUILD", "OK" if ver["ok"] else "FAILED")
    return 0 if ver["ok"] else 2


# ------------------------------------------------------------------ report
def report(a, P):
    S = json.loads((P.metrics / "wb_conversion_summary.json").read_text())
    csvp = P.metrics / "wb_area_sanity.csv"
    area = list(csv.DictReader(open(csvp))) if csvp.exists() else []
    rows = ""
    for sp, d in S["splits"].items():
        rows += (f"| {sp} | {d['images']} | {d['eda_wb_annotations']} | {d['wb_raw']} | {d['wb_iscrowd_excluded']} | "
                 f"{d['wb_skipped_total']} | {d['wb_converted']} | {d['empty_label_files']} | {d['non_wb_omitted']} |\n")
    poly = ""
    for sp, d in S["splits"].items():
        poly += (f"- **{sp}**: {d['multi_component_annotations']} multi-component WB annotations; {d['extra_components_discarded']} extra components "
                 f"discarded (largest-component-only); discarded area {d['discarded_component_area_px2']:.1f} px² "
                 f"= {100*d['discarded_area_fraction']:.4f}% of total polygon area; invalid rings dropped {d['invalid_rings_dropped']}; "
                 f"clipped to image {d['annotations_clipped_to_image']}; skipped reasons {d['skipped']}.\n")
    rec = "\n".join(f"- {sp}: {d['reconciliation']}" for sp, d in S["splits"].items())
    ar = "\n".join(f"| {r['case']} | {r['expected_area_px2']} | {r['measured_area_px2']} | {r['absolute_error_px2']} |" for r in area) or "| NOT_VERIFIED | | | |"
    v = S.get("verification", {})
    md = f"""# WB dataset preparation and mask-area measurement

## Findings (from executed scripts)
| split | images | EDA WB | raw WB (COCO) | iscrowd excluded | skipped | converted | empty label files | non-WB omitted |
|---|---|---|---|---|---|---|---|---|
{rows}
Image memberships match the original split sizes: {all(d['images_match_expected'] for d in S['splits'].values())} (expected 3,596/449/450).
Verification after build: ok={v.get('ok')}, YAML nc={v.get('yaml_nc')}, names={v.get('yaml_names')}, problems={v.get('problems')}.

### Reconciliation with EDA counts
{rec}

## Conversion policy
- Source: original COCO `annotations_coco.json` streamed per split; COCO JSON and two-class `YOLO_ROOT` untouched; cached YOLO labels not reused (provenance/loss NOT_VERIFIED).
- Output `WB_ROOT=/content/M18K_V2_work/yolo_v2_wb`; only annotations whose COCO category maps to WB are written, remapped to YOLO class `0`.
- BB policy: {S['bb_policy']}
- `iscrowd=1` WB annotations are excluded and counted; RLE/missing/degenerate segmentations are skipped and counted.
- Polygon geometry is preserved (normalised by image width/height) except for multi-component annotations, where YOLO-seg allows one polygon per line, so only the **largest component** is kept (approximation):
{poly}
## Mask area
`A_px2 = sum(binary_mask > 0)` computed per instance on the original-resolution mask (not bounding box). Unit **px²**; mm² is NOT_VERIFIED (no verified physical calibration).

| case | expected px² | measured px² | abs. error px² |
|---|---|---|---|
{ar}

## Limitations
- Areas are polygon-rasterised COCO masks, i.e. annotation-visible area; occlusion/annotation noise not assessed.
- Largest-component-only labels slightly understate multi-part instances (see losses above); area measurement from COCO polygons uses all components.
- The cv2 cross-check differs from pycocotools by rasterisation rule only.
- No physical calibration; no model training or EDA performed.
"""
    P.reports.mkdir(parents=True, exist_ok=True)
    (P.reports / "wb_dataset_measurement.md").write_text(md); print("wrote", P.reports / "wb_dataset_measurement.md")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["build", "rebuild", "report"], default="build")
    ap.add_argument("--drive-root", default=str(DRIVE_ROOT))
    ap.add_argument("--data-root", default=None, help="default DRIVE_ROOT/M18K_V2_data/M18KV2")
    ap.add_argument("--work-root", default=str(WORK_ROOT))
    ap.add_argument("--repo-root", default=None, help="where 07_/08_/09_ outputs go (default DRIVE_ROOT/wb_task_repo)")
    ap.add_argument("--zip-path", default=None)
    ap.add_argument("--wb-category-ids", type=int, nargs="*", default=None, help="override WB category ids")
    a = ap.parse_args(argv); P = resolve(a)
    return {"build": build, "rebuild": rebuild, "report": report}[a.mode](a, P)


if __name__ == "__main__":
    sys.exit(main())
