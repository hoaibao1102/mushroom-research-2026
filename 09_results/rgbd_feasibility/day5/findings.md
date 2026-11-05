# Day 5 — RGB-D feasibility for physical mushroom-area measurement

## Conclusion

The current M18K V2 export does not provide enough verified calibration information to report mushroom area in mm². The team therefore kept area measurements in px² and did not calculate physical area. This is the correct decision: a numerical conversion without a verified depth scale and camera calibration would not be a defensible physical measurement.

## What was checked

- Thirty randomly selected test images (seed 42) and 4,970 WB ground-truth masks were inspected.
- All 30 depth maps had the same 1280 × 720 dimensions as their RGB/COCO images.
- The depth folder for the full 450-image test split contained 340 `float32` files and 110 `uint16` files. The reason for the mixed types is not documented in the supplied export.
- The dataset files inspected did not provide a verified depth scale or camera intrinsics (`fx`, `fy`, `cx`, `cy`). The paper identifies an Intel RealSense D405 camera, but that alone does not establish the units or calibration of these exported `.npy` maps.

## Depth values inside WB masks

Across the 4,970 masks, the mean valid-depth fraction was 93.1%, the median was 99.76%, and the fifth percentile was 26.3%. A total of 301 masks (6.1%) had less than 50% valid depth, 452 (9.1%) had less than 90%, and 132 (2.7%) had no valid depth pixels.

The low-validity masks were concentrated near image edges: 199 mask centres were in the leftmost 10% of the image and 102 were in the rightmost 10%; none were in the central 80%. The median width of the left-side invalid-depth band was 49 pixels (range 0–61 pixels). The reason for the right-edge cases was not established.

## Alignment and units

Two exploratory image-gradient checks suggested that the strongest RGB/depth correspondence was often found at a non-zero horizontal shift. The estimated shifts varied in direction and the correlation peaks were broad. These tests are not precise enough to establish a fixed offset or prove that the depth maps are misaligned. RGB-depth alignment remains **unverified**.

The raw depth median inside WB masks was 2,399 units. Interpreting that as millimetres would imply about 2.4 m, which conflicts with the nominal camera height described in the paper. Interpreting it as 0.1 mm per unit gives about 240 mm, which is more plausible but still does not match the nominal 150 mm setup. This is only a plausibility check; it does not verify the unit.

## What is needed to continue

A defensible physical-area estimate would require: (1) the depth scale and a clear explanation of the mixed `float32`/`uint16` files; (2) the intrinsics for the depth image at its actual resolution; (3) documentation or calibration confirming depth-to-RGB alignment; and (4) an independent check against an object of known size or manual mushroom measurements. Even with these, the projected area would not be the true surface area of a curved mushroom cap.

Until that information is available, the project should continue reporting mask area in px² only.

## Files

- `depth_inspection.json`: dataset inventory and 30-image depth checks.
- `results.csv`: per-image depth and mask summaries; `wb_area_mm2` is `NOT_VERIFIED`.
- `extra_checks_summary.json`: supporting results from the additional 450-file dtype and spatial checks.
- `findings_vi.md`: original Vietnamese submission.
- `figures/`: submitted depth-validity and example visualizations.
