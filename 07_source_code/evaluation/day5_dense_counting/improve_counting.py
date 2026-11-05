
import os
import csv
import json
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict

import cv2
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ultralytics
from ultralytics import YOLO
from pycocotools.coco import COCO

# =========================================================
# 1. CONFIGURATION
# =========================================================

BASE = Path('/content/drive/MyDrive/M18K_Reproduction')
OUT = BASE / 'Day5_Dense_Counting'
FIG = OUT / 'figures'

OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

IMG_SIZE = 640
CONF = 0.25
MAX_DET = 3000
MATCH_IOU = 0.50

# Only experimental change:
BASELINE_NMS_IOU = 0.70
MODIFIED_NMS_IOU = 0.50

SAMPLE_SIZE = 8

# =========================================================
# 2. FIND INPUT FILES
# =========================================================

def find_first(paths):
    for p in paths:
        p = Path(p)
        if p.exists():
            return p
    return None

checkpoint = find_first([
    BASE / 'best.pt',
    BASE / 'model_runs/khang_wb_heldout_test/weights/best.pt'
])

data_yaml = find_first([
    BASE / 'data.yaml',
    BASE / 'M18K_V2_data/data.yaml',
    BASE / 'M18K_V2_data/M18KV2/data.yaml'
])

test_candidates = [
    BASE / 'M18K_V2_data/M18KV2/test',
    BASE / 'M18K_V2_data/test'
]

test_dir = next(
    (p for p in test_candidates if (p / 'rgb').is_dir()),
    None
)

if checkpoint is None:
    matches = list(BASE.rglob('best.pt'))
    if len(matches) == 1:
        checkpoint = matches[0]

if data_yaml is None:
    matches = list(BASE.rglob('data.yaml'))
    if len(matches) == 1:
        data_yaml = matches[0]

if test_dir is None:
    matches = list(BASE.rglob('test/rgb'))
    if len(matches) == 1:
        test_dir = matches[0].parent

if checkpoint is None:
    raise FileNotFoundError('Không tìm thấy best.pt trong M18K_Reproduction')

if data_yaml is None:
    raise FileNotFoundError('Không tìm thấy data.yaml')

if test_dir is None:
    raise FileNotFoundError('Không tìm thấy test/rgb')

rgb_dir = test_dir / 'rgb'

ann_candidates = [
    test_dir / 'annotations_coco.json',
    test_dir.parent / 'annotations_coco.json',
    BASE / 'M18K_V2_data/annotations_coco.json'
]

ann_path = next(
    (p for p in ann_candidates if p.is_file()),
    None
)

if ann_path is None:
    search_root = BASE / 'M18K_V2_data'
    matches = list(search_root.rglob('annotations_coco.json'))
    if len(matches) == 1:
        ann_path = matches[0]

if ann_path is None:
    raise FileNotFoundError('Không tìm thấy annotations_coco.json')

# Verify WB-only class.
with open(data_yaml, encoding='utf-8') as f:
    cfg = yaml.safe_load(f)

names = cfg.get('names', {})
class_zero = names[0] if isinstance(names, list) else names.get(0, names.get('0'))

if cfg.get('nc') != 1 or str(class_zero).upper() != 'WB':
    raise ValueError(f'Dataset không đúng WB-only: nc={cfg.get("nc")}, names={names}')

print('Checkpoint:', checkpoint)
print('Test images:', rgb_dir)
print('COCO annotation:', ann_path)

# =========================================================
# 3. LOAD COCO AND IDENTIFY WB
# =========================================================

coco = COCO(str(ann_path))

categories = coco.dataset.get('categories', [])

wb_categories = [
    c for c in categories
    if str(c.get('name', '')).strip().lower() in
    ['wb', 'white button', 'white button mushroom']
]

if len(wb_categories) == 1:
    cat_id = int(wb_categories[0]['id'])
elif len(categories) == 1:
    cat_id = int(categories[0]['id'])
else:
    raise ValueError(f'Không xác định được WB category: {categories}')

anns_by_image = defaultdict(list)

for ann in coco.dataset['annotations']:
    if int(ann['category_id']) == cat_id:
        anns_by_image[int(ann['image_id'])].append(ann)

# Match COCO filenames to actual RGB files.
files_by_name = defaultdict(list)

for p in rgb_dir.rglob('*'):
    if p.is_file() and p.suffix.lower() in [
        '.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'
    ]:
        files_by_name[p.name].append(p)

# =========================================================
# 4. SELECT 8 FIXED DENSE / CROWDED IMAGES
# =========================================================

def bbox_iou(a, b):
    ax, ay, aw, ah = map(float, a[:4])
    bx, by, bw, bh = map(float, b[:4])

    x1 = max(ax, bx)
    y1 = max(ay, by)
    x2 = min(ax + aw, bx + bw)
    y2 = min(ay + ah, by + bh)

    inter = max(0, x2-x1) * max(0, y2-y1)
    union = aw*ah + bw*bh - inter

    return inter / union if union > 0 else 0


records = []

for image in coco.dataset['images']:

    image_id = int(image['id'])
    filename = Path(image['file_name']).name

    candidates = files_by_name.get(filename, [])

    if not candidates:
        continue

    if len(candidates) > 1:
        raise RuntimeError(f'Tên ảnh trùng nhau: {filename}')

    anns = anns_by_image[image_id]
    boxes = [a['bbox'] for a in anns]

    overlaps = []

    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            overlaps.append(bbox_iou(boxes[i], boxes[j]))

    records.append({
        'image_id': image_id,
        'filename': filename,
        'path': str(candidates[0]),
        'gt': len(anns),
        'overlap': max(overlaps) if overlaps else 0
    })

if len(records) < 2:
    raise RuntimeError('Không đủ ảnh hợp lệ để thực hiện so sánh.')

selection_file = OUT / 'selected_images.csv'

# Reuse previous selection when rerunning.
if selection_file.exists():
    old = pd.read_csv(selection_file)
    ids = old['image_id'].astype(int).tolist()
    record_map = {r['image_id']: r for r in records}

    if any(i not in record_map for i in ids):
        raise RuntimeError('Danh sách ảnh cũ không khớp COCO hiện tại.')

    selected = [record_map[i] for i in ids]

else:
    nonzero = [r for r in records if r['gt'] > 0]

    median_count = np.median([r['gt'] for r in nonzero])
    candidates = [r for r in nonzero if r['gt'] >= median_count]

    if len(candidates) < min(SAMPLE_SIZE, len(nonzero)):
        candidates = nonzero

    count_sorted = sorted(candidates, key=lambda x: x['gt'])
    overlap_sorted = sorted(candidates, key=lambda x: x['overlap'])

    n = max(1, len(candidates)-1)

    count_rank = {
        r['image_id']: i/n
        for i, r in enumerate(count_sorted)
    }

    overlap_rank = {
        r['image_id']: i/n
        for i, r in enumerate(overlap_sorted)
    }

    for r in candidates:
        r['score'] = (
            0.5 * count_rank[r['image_id']]
            + 0.5 * overlap_rank[r['image_id']]
        )

    selected = sorted(
        candidates,
        key=lambda x: (-x['score'], x['image_id'])
    )[:SAMPLE_SIZE]

    pd.DataFrame([
        {
            'image_id': r['image_id'],
            'filename': r['filename'],
            'gt_count': r['gt'],
            'max_bbox_overlap': r['overlap'],
            'selection_rule': 'Top 50% count rank + 50% bbox overlap rank',
            'visual_confirmation': 'PENDING'
        }
        for r in selected
    ]).to_csv(selection_file, index=False, encoding='utf-8-sig')

print('\nSelected images:')

for r in selected:
    print(r['image_id'], r['filename'], 'GT:', r['gt'])

# =========================================================
# 5. MODEL AND MATCHING FUNCTIONS
# =========================================================

model = YOLO(str(checkpoint))

device = 0 if __import__('torch').cuda.is_available() else 'cpu'

def predict(image_path, nms_iou):
    return model.predict(
        source=str(image_path),
        imgsz=IMG_SIZE,
        conf=CONF,
        iou=nms_iou,
        max_det=MAX_DET,
        classes=[0],
        retina_masks=True,
        agnostic_nms=False,
        device=device,
        save=False,
        verbose=False
    )[0]


def get_masks(result, h, w):

    if result.masks is None:
        return []

    output = []

    for raw in result.masks.data.cpu().numpy():
        m = (raw > 0.5).astype(np.uint8)

        if m.shape != (h, w):
            m = cv2.resize(
                m, (w, h),
                interpolation=cv2.INTER_NEAREST
            )

        output.append(m.astype(bool))

    return output


def get_gt_masks(image_id, h, w):

    output = []

    for ann in anns_by_image[image_id]:
        try:
            m = coco.annToMask(ann).astype(np.uint8)

            if m.shape != (h, w):
                m = cv2.resize(
                    m, (w, h),
                    interpolation=cv2.INTER_NEAREST
                )

            if m.any():
                output.append(m.astype(bool))

        except Exception:
            return []

    return output


def mask_iou(a, b):

    inter = np.logical_and(a, b).sum()
    union = np.logical_or(a, b).sum()

    return inter / union if union else 0


def greedy_match(matrix):

    if matrix.size == 0:
        return 0, matrix.shape[0], matrix.shape[1]

    used_gt = set()
    used_pred = set()
    tp = 0

    while True:

        temp = matrix.copy()

        if used_gt:
            temp[list(used_gt), :] = -1

        if used_pred:
            temp[:, list(used_pred)] = -1

        i, j = np.unravel_index(np.argmax(temp), temp.shape)
        best = temp[i, j]

        if best < MATCH_IOU:
            break

        used_gt.add(i)
        used_pred.add(j)
        tp += 1

    return tp, matrix.shape[0]-tp, matrix.shape[1]-tp


def bbox_xyxy_iou(a, b):

    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])

    inter = max(0, x2-x1) * max(0, y2-y1)

    aa = max(0, a[2]-a[0]) * max(0, a[3]-a[1])
    ab = max(0, b[2]-b[0]) * max(0, b[3]-b[1])

    union = aa + ab - inter

    return inter/union if union > 0 else 0


def matching_stats(image_id, result, h, w):

    gt_masks = get_gt_masks(image_id, h, w)
    pred_masks = get_masks(result, h, w)

    # Prefer segmentation-mask matching.
    if gt_masks and len(gt_masks) == len(anns_by_image[image_id]):

        matrix = np.zeros(
            (len(gt_masks), len(pred_masks)),
            dtype=np.float32
        )

        for i, gm in enumerate(gt_masks):
            for j, pm in enumerate(pred_masks):
                matrix[i, j] = mask_iou(gm, pm)

        tp, fn, fp = greedy_match(matrix)

        return tp, fn, fp, 'mask_IoU'

    # Bbox fallback if COCO masks are unavailable.
    gt_boxes = []

    for a in anns_by_image[image_id]:
        x, y, bw, bh = map(float, a['bbox'])
        gt_boxes.append([x, y, x+bw, y+bh])

    if result.boxes is None:
        pred_boxes = []
    else:
        pred_boxes = result.boxes.xyxy.cpu().numpy().tolist()

    matrix = np.zeros(
        (len(gt_boxes), len(pred_boxes)),
        dtype=np.float32
    )

    for i, a in enumerate(gt_boxes):
        for j, b in enumerate(pred_boxes):
            matrix[i, j] = bbox_xyxy_iou(a, b)

    tp, fn, fp = greedy_match(matrix)

    return tp, fn, fp, 'bbox_IoU_fallback'


def overlay(rgb, masks, color):

    out = rgb.copy()

    for mask in masks:

        out[mask] = (
            0.55 * out[mask].astype(float)
            + 0.45 * np.array(color)
        ).astype(np.uint8)

        contours, _ = cv2.findContours(
            mask.astype(np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        cv2.drawContours(out, contours, -1, color, 1)

    return out

# =========================================================
# 6. BASELINE VS MODIFIED INFERENCE
# =========================================================

rows = []
figure_cache = []

for i, item in enumerate(selected, 1):

    image_path = Path(item['path'])
    bgr = cv2.imread(str(image_path))

    if bgr is None:
        raise RuntimeError(f'Cannot read {image_path}')

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]

    image_id = int(item['image_id'])
    gt_count = int(item['gt'])

    # Exact same image and model, only NMS IoU changes.
    baseline = predict(image_path, BASELINE_NMS_IOU)
    modified = predict(image_path, MODIFIED_NMS_IOU)

    baseline_count = len(baseline.boxes) if baseline.boxes is not None else 0
    modified_count = len(modified.boxes) if modified.boxes is not None else 0

    btp, bfn, bfp, bmethod = matching_stats(
        image_id, baseline, h, w
    )

    mtp, mfn, mfp, mmethod = matching_stats(
        image_id, modified, h, w
    )

    row = {
        'image_id': image_id,
        'filename': item['filename'],
        'gt_count': gt_count,
        'baseline_count': baseline_count,
        'modified_count': modified_count,
        'baseline_signed_error': baseline_count-gt_count,
        'modified_signed_error': modified_count-gt_count,
        'baseline_abs_error': abs(baseline_count-gt_count),
        'modified_abs_error': abs(modified_count-gt_count),
        'baseline_matched_tp': btp,
        'baseline_unmatched_gt_fn': bfn,
        'baseline_unmatched_pred_fp': bfp,
        'baseline_match_method': bmethod,
        'modified_matched_tp': mtp,
        'modified_unmatched_gt_fn': mfn,
        'modified_unmatched_pred_fp': mfp,
        'modified_match_method': mmethod
    }

    rows.append(row)

    figure_cache.append({
        'row': row,
        'rgb': rgb,
        'gt': get_gt_masks(image_id, h, w),
        'baseline': get_masks(baseline, h, w),
        'modified': get_masks(modified, h, w)
    })

    print(
        f'[{i}/{len(selected)}] {item["filename"]}: '
        f'GT={gt_count}, base={baseline_count}, '
        f'mod={modified_count}'
    )

# =========================================================
# 7. COMPARISON CSV AND MAE
# =========================================================

df = pd.DataFrame(rows)

df.to_csv(
    OUT / 'comparison.csv',
    index=False,
    encoding='utf-8-sig'
)

baseline_mae = df['baseline_abs_error'].mean()
modified_mae = df['modified_abs_error'].mean()

delta = modified_mae - baseline_mae

improved = int(
    (df['modified_abs_error'] < df['baseline_abs_error']).sum()
)

worsened = int(
    (df['modified_abs_error'] > df['baseline_abs_error']).sum()
)

unchanged = len(df) - improved - worsened

# =========================================================
# 8. SAVE UP TO 4 FIGURES
# =========================================================

deltas = (
    df['baseline_abs_error'] - df['modified_abs_error']
).to_numpy()

indexes = [
    int(np.argmax(deltas)),
    int(np.argmin(deltas)),
    int(np.argmax(df['baseline_abs_error'].to_numpy()))
]

indexes = list(dict.fromkeys(indexes))[:4]

for number, idx in enumerate(indexes, 1):

    item = figure_cache[idx]
    r = item['row']

    gt_img = overlay(item['rgb'], item['gt'], (40, 190, 80))
    base_img = overlay(item['rgb'], item['baseline'], (240, 130, 40))
    mod_img = overlay(item['rgb'], item['modified'], (70, 130, 240))

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(gt_img)
    axes[0].set_title(f'Ground Truth: {r["gt_count"]}')

    axes[1].imshow(base_img)
    axes[1].set_title(
        f'Baseline NMS={BASELINE_NMS_IOU}: '
        f'{r["baseline_count"]} | AE={r["baseline_abs_error"]}'
    )

    axes[2].imshow(mod_img)
    axes[2].set_title(
        f'Modified NMS={MODIFIED_NMS_IOU}: '
        f'{r["modified_count"]} | AE={r["modified_abs_error"]}'
    )

    for ax in axes:
        ax.axis('off')

    fig.suptitle(r['filename'])
    fig.tight_layout()

    fig.savefig(
        FIG / f'comparison_{number:02d}_{Path(r["filename"]).stem}.jpg',
        dpi=110,
        bbox_inches='tight'
    )

    plt.close(fig)

# =========================================================
# 9. CONFIG, README AND FINDINGS
# =========================================================

sha = hashlib.sha256(checkpoint.read_bytes()).hexdigest()

config_data = {
    'checkpoint': str(checkpoint),
    'checkpoint_sha256': sha,
    'data_yaml': str(data_yaml),
    'test_rgb': str(rgb_dir),
    'annotation': str(ann_path),
    'ultralytics_version': ultralytics.__version__,
    'device': str(device),
    'imgsz': IMG_SIZE,
    'confidence': CONF,
    'baseline_nms_iou': BASELINE_NMS_IOU,
    'modified_nms_iou': MODIFIED_NMS_IOU,
    'max_det': MAX_DET,
    'selected_images': len(selected),
    'only_change': 'NMS IoU 0.70 -> 0.50'
}

with open(OUT / 'run_config.json', 'w', encoding='utf-8') as f:
    json.dump(config_data, f, indent=2, ensure_ascii=False)

if delta < 0:
    outcome = 'MAE improved on selected sample'
elif delta > 0:
    outcome = 'MAE worsened on selected sample'
else:
    outcome = 'MAE unchanged on selected sample'

findings = f"""
# Day 5 — Dense Mushroom Segmentation & Counting

## 1. Scope

- Model: existing WB-only YOLOv8n-seg checkpoint.
- Checkpoint: `{checkpoint.name}`
- Test sample: {len(selected)} fixed M18K V2 test images.
- Retraining: No.
- Full 450-image evaluation: Not rerun.

## 2. Failure hypothesis

The targeted hypothesis is duplicate or highly overlapping detections
that can cause over-counting in crowded scenes.

This is a hypothesis to test; it must be checked against the figures.

## 3. One targeted change

NMS IoU threshold:

- Baseline: {BASELINE_NMS_IOU}
- Modified: {MODIFIED_NMS_IOU}

All other inference settings remain the same:

- imgsz = {IMG_SIZE}
- conf = {CONF}
- class = WB (0)
- same checkpoint and same images

Lower NMS IoU suppresses overlapping boxes more aggressively. It may
reduce duplicates but may also suppress nearby real mushrooms.

## 4. Counting results

- Baseline counting MAE: **{baseline_mae:.4f}**
- Modified counting MAE: **{modified_mae:.4f}**
- Difference (modified - baseline): **{delta:+.4f}**
- Images improved: {improved}
- Images worsened: {worsened}
- Images unchanged: {unchanged}

MAE = mean(abs(predicted instance count - COCO GT instance count)).

**Outcome:** {outcome}.

## 5. Matched-instance diagnostics

The CSV includes one-to-one matching at IoU >= {MATCH_IOU}.
Mask IoU is used when valid COCO segmentation masks are available;
otherwise bbox IoU is used and identified as a fallback.

Unmatched predictions are only FP candidates. They are not automatically
confirmed duplicates. Unmatched GT masks are only FN candidates.

## 6. Limitations

- Only {len(selected)} selected dense/crowded candidates were tested.
- Selection uses COCO instance count and bbox overlap heuristics.
- Bbox overlap does not prove physical touching or occlusion.
- The result does not establish general improvement on the full test set.
- No model retraining or full-test mAP evaluation was performed.
"""

(OUT / 'findings.md').write_text(findings, encoding='utf-8')

readme = """
# Day 5 — Dense Mushroom Segmentation & Counting

Run `improve_counting.py` in Google Colab after mounting Drive.
Required packages: ultralytics>=8.3,<9, pycocotools, pyyaml.

The experiment compares the same WB-only checkpoint on the same fixed
test images. The only change is NMS IoU from 0.70 to 0.50.
Image size (640), confidence (0.25), class filter (WB class 0), model,
and dataset images are held constant.

The script selects 8 dense/crowded candidate images on first run and
freezes them in selected_images.csv. Selection uses GT WB instance
count and maximum pairwise COCO bbox IoU. Review figures because bbox
overlap is only a heuristic for crowded scenes.

Outputs:
- selected_images.csv
- comparison.csv
- findings.md
- run_config.json
- figures/ (up to 4 compressed before/after examples)

Counting MAE is the mean per-image absolute count error.
Matched-instance diagnostics use IoU >= 0.50 and are supplementary,
not official mAP. No retraining or full-test evaluation is performed.
"""

(OUT / 'README.md').write_text(readme.strip() + '\n', encoding='utf-8')

# Include a copy of the running script in submission folder.
try:
    shutil.copy2(__file__, OUT / 'improve_counting.py')
except Exception:
    pass

print('\n===================================')
print('DAY 5 COMPLETED')
print('Baseline MAE:', round(float(baseline_mae), 4))
print('Modified MAE:', round(float(modified_mae), 4))
print('Delta:', round(float(delta), 4))
print('Outcome:', outcome)
print('Output folder:', OUT)
print('===================================')
