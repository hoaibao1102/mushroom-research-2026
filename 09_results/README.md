# Results and daily reports

| Day | Work | Daily report | Main files |
|---|---|---|---|
| 1 — 30 Oct | M18K V2 EDA | [M18K V2 EDA](reports/M18K_V2_EDA_2026-10-30.md) | `metrics/v2_eda_*` |
| 2 — 2 Nov | YOLOv8n-seg runs and dataset/mask checks | [Model runs](reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md) · [Dataset and masks](reports/Day2_WB_Dataset_and_Mask_Validation_2026-11-02.md) | `metrics/Day2_*`, `12_reproducibility/logs/` |
| 3 — 3 Nov | Prediction review and mask-area analysis | [Area and error analysis](reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md) · [Qualitative review](reports/Day3_WB_Qualitative_Review_2026-11-03.md) | `area_evaluation/`, `wb_error_analysis/` |
| 4 — 4 Nov | Full-test area, inference MVP and Otsu baseline | [Full-test area and MVP](reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md) · [QC interpretation](reports/Day4_QC_Interpretation_2026-11-04.md) | `area_evaluation/day4_full_test/`, `inference_demo/`, `otsu_baseline/` |
| 5 — 5 Nov | NMS comparison, RGB-D check and Gradio demo | [Research development](reports/Day5_Research_Development_2026-11-05.md) | `dense_counting/day5_nms/`, `rgbd_feasibility/day5/`, `gradio_demo/` |
| 6 — 8 Nov | Charisis, MushR and Wang paper/source review | [Paper and source review](reports/Day6_Paper_Source_Review_2026-11-08.md) | `../03_dataset_discovery/source_verification/CHARISIS_AND_MUSHR_PAPER_SOURCES_2026-11-09.md` |
| 7 — 9 Nov | Charisis and MushR notebook preparation | [Notebook preparation](reports/Day7_Notebook_Preparation_2026-11-09.md) | `../08_experiments/notebooks/` |
| 8 — 10 Nov | Local application prototype and research handoff | [Application prototype](reports/Day8_Local_Application_Prototype_2026-11-10.md) | `../13_local_application/` (reference snapshot) |

## Notes on the results

- Day 2 scores are results on M18K V2, not a numerical reproduction of the original M18K paper.
- Day 3 area and qualitative checks use selected samples. Day 4 area results cover all 450 WB test images and matched masks only.
- Day 5's lower-NMS result uses eight selected dense images; the full test set has not been evaluated at that setting.
- The RGB-D export has no verified depth scale, camera intrinsics or RGB-depth alignment. No mm² measurements were made.
- The Day 6 work was source screening. Day 7 recorded notebook preparation; notebook files and real-data training evidence are not included in this source archive.
- Day 8 records a local application prototype. Its seven unit tests pass, but the bundled model registry has no checkpoint, so the archive does not establish trained-model inference quality or AMD acceleration.
