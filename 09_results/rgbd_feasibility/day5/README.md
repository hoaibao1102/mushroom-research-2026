# Day 5 RGB-D feasibility results

Thịnh checked whether the supplied depth maps can support physical mushroom-area measurement. The work covered 30 test images and 4,970 WB masks, plus a depth-file type inventory across all 450 test images.

The result is a feasibility assessment, not a physical measurement. Depth scale and camera intrinsics are not verified, RGB-depth alignment is uncertain, and some masks have incomplete depth. No mm² values were calculated. The current project measurements remain in px².

Read `findings.md` for the English summary and `findings_vi.md` for the original submission. The scripts are in `07_source_code/features/day5_rgbd_feasibility/`.
