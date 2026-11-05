# RGB-D measurement feasibility checks

These scripts inspect the M18K V2 depth files and their relationship to the existing WB masks. They check file formats, valid depth inside masks, possible RGB/depth alignment, and whether the available files document depth units or camera intrinsics.

They do **not** calculate physical area in mm². Keep mask area in px² until depth scale, camera intrinsics and RGB-depth alignment are verified.

Run in Colab after mounting Drive:

```bash
python depth_area.py --data-root "/content/drive/MyDrive/Colab Notebooks/M18K_Reproduction/M18KV2" --split test --n 30 --seed 42
python extra_checks.py --data-root "/content/drive/MyDrive/Colab Notebooks/M18K_Reproduction/M18KV2" --split test
```

The scripts write their outputs beside the script. The submitted Day 5 outputs are preserved in `09_results/rgbd_feasibility/day5/`.
