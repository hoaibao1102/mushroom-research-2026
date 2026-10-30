# V2 dataset metadata — notebook-derived

**Observed 2026-10-30** in `analysis/M18K_V2_Research_EDA_Executed_2026-10-30.ipynb`.

| Split | RGB | Depth files listed | Annotations | BB | WB |
| --- | ---: | ---: | ---: | ---: | ---: |
| Train | 3,596 | 3,596 | 559,545 | 686 | 558,859 |
| Validation | 449 | 449 | 70,755 | 75 | 70,680 |
| Test | 450 | 450 | 70,289 | 97 | 70,192 |
| Total | 4,495 | 4,495 | 700,589 | 858 | 699,731 |

Image-depth pairing was verified using file stems within each split; that is **not** a metric depth calibration or geometric alignment test. COCO category IDs 1 and 2 were mapped from source names BB and WB. Image identity across splits was checked **by filename only**. Do not interpret these as complete dataset QC.

Files are stored externally on Drive. No image/depth/annotation payload was included in this Git workspace.
