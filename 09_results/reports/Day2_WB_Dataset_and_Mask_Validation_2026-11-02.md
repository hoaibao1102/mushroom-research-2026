# WB dataset preparation and mask-area measurement

## Findings (from executed scripts)
| split | images | EDA WB | raw WB (COCO) | iscrowd excluded | skipped | converted | empty label files | non-WB omitted |
|---|---|---|---|---|---|---|---|---|
| train | 3596 | 558859 | 558859 | 0 | 6 | 558853 | 0 | 686 |
| val | 449 | 70680 | 70680 | 0 | 0 | 70680 | 0 | 75 |
| test | 450 | 70192 | 70192 | 0 | 0 | 70192 | 0 | 97 |

Image memberships match the original split sizes: True (expected 3,596/449/450).
Verification after build: ok=True, YAML nc=1, names={'0': 'WB'}, problems=[].

### Reconciliation with EDA counts
- train: raw WB equals EDA count; converted = raw - iscrowd - skipped (558859 - 0 - 6 = 558853)
- val: raw WB equals EDA count; converted = raw - iscrowd - skipped (70680 - 0 - 0 = 70680)
- test: raw WB equals EDA count; converted = raw - iscrowd - skipped (70192 - 0 - 0 = 70192)

## Conversion policy
- Source: original COCO `annotations_coco.json` streamed per split; COCO JSON and two-class `YOLO_ROOT` untouched; cached YOLO labels not reused (provenance/loss NOT_VERIFIED).
- Output `WB_ROOT=/content/M18K_V2_work/yolo_v2_wb`; only annotations whose COCO category maps to WB are written, remapped to YOLO class `0`.
- BB policy: All non-WB annotations (BB and any other category) are omitted from the WB labels. They are NOT target labels: omitted BB objects are unlabeled background in this WB-only dataset. Images are kept (original split membership) even when they contain only BB; such images get empty label files.
- `iscrowd=1` WB annotations are excluded and counted; RLE/missing/degenerate segmentations are skipped and counted.
- Polygon geometry is preserved (normalised by image width/height) except for multi-component annotations, where YOLO-seg allows one polygon per line, so only the **largest component** is kept (approximation):
- **train**: 0 multi-component WB annotations; 0 extra components discarded (largest-component-only); discarded area 0.0 px² = 0.0000% of total polygon area; invalid rings dropped 0; clipped to image 0; skipped reasons {'degenerate_after_clip': 6}.
- **val**: 0 multi-component WB annotations; 0 extra components discarded (largest-component-only); discarded area 0.0 px² = 0.0000% of total polygon area; invalid rings dropped 0; clipped to image 0; skipped reasons {}.
- **test**: 0 multi-component WB annotations; 0 extra components discarded (largest-component-only); discarded area 0.0 px² = 0.0000% of total polygon area; invalid rings dropped 0; clipped to image 0; skipped reasons {}.

## Mask area
`A_px2 = sum(binary_mask > 0)` computed per instance on the original-resolution mask (not bounding box). Unit **px²**; mm² is NOT_VERIFIED (no verified physical calibration).

| case | expected px² | measured px² | abs. error px² |
|---|---|---|---|
| synthetic_empty_mask | 0 | 0 | 0 |
| synthetic_single_pixel | 1 | 1 | 0 |
| synthetic_rect_10x20_uint8 | 200 | 200 | 0 |
| synthetic_rect_value_255 | 200 | 200 | 0 |
| synthetic_rect_bool | 200 | 200 | 0 |
| synthetic_rect_float_0.5 | 200 | 200 | 0 |
| synthetic_full_frame_1080x1920 | 2073600 | 2073600 | 0 |
| synthetic_two_disjoint_components | 225 | 225 | 0 |
| synthetic_staircase_not_bbox | 55 | 55 | 0 |
| synthetic_checkerboard_half | 800 | 800 | 0 |
| real_coco_ann0_pycocotools | 8156 | 8156 | 0 |
| real_coco_ann0_cv2_crosscheck | 8156 | 8325 | 169 |
| real_coco_ann1_pycocotools | 6972 | 6972 | 0 |
| real_coco_ann1_cv2_crosscheck | 6972 | 7112 | 140 |
| real_coco_ann2_pycocotools | 4508 | 4508 | 0 |
| real_coco_ann2_cv2_crosscheck | 4508 | 4641 | 133 |

## Limitations
- Areas are polygon-rasterised COCO masks, i.e. annotation-visible area; occlusion/annotation noise not assessed.
- Largest-component-only is the conversion rule for multi-part polygons, but no multi-component WB polygon exists in any split, so nothing was discarded; area measurement from COCO polygons uses all components.
- The cv2 cross-check differs from pycocotools by rasterisation rule only.
- No physical calibration; no model training or EDA performed.

## Additional notes (from executed scripts)
- COCO categories: 0 `Mushrooms` (declared, 0 annotations in all splits), 1 `BB` (omitted: 686 train / 75 val / 97 test), 2 `WB` (kept, remapped to YOLO class 0).
- Train: 6 WB annotations skipped (ann_id 65633, 68399, 151483, 398470, 528181, 543586). Each is a single 12-point polygon with COCO `area = 0.0`. The build summary shows 0 annotations clipped to the image in train, so these polygons were degenerate before clipping; the script labels the reason `degenerate_after_clip`. Their images still contain other WB instances (0 empty label files).
- No `iscrowd` WB annotations and no multi-component WB polygons in any split; largest-component-only discarded nothing.
- Area test: the 3 real masks are COCO ann_id 0, 1, 2, all from image_id 0 (1280x720; file size checked equal to COCO size for that image only). pycocotools rows use the RLE area of the same polygon as expected, so they validate the pixel-counting function, not the rasterisation rule. The cv2.fillPoly cross-check differs by 133-169 px2 (rasterisation-rule difference).
- Fresh-runtime rebuild: `--mode rebuild` returned REBUILD OK (09_results/metrics/wb_rebuild_verification.json).
