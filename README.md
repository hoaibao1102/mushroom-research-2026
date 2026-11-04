# Mushroom Research 2026 — Team 10

Repository for the **M18K V2 mushroom detection and instance-segmentation reproduction study**. We preserve the shared `00`–`12` research organization.

**Current research record (2026-11-04): Day 4 inference MVP and course experiments documented.** The YOLOv8n-seg reproduction workflow on M18K V2 is operational: two models trained/evaluated on the held-out test split, then WB-only predicted-mask area and qualitative error analysis performed. This is **not** an exact replication of the original 2025 M18K benchmark or a claim of numerical superiority. Formal source/license approval, full image leakage audit and some annotation checks remain unresolved. A demo video and final presentation are still pending.

## Day-by-day progression

| Day | Work | Evidence |
| --- | --- | --- |
| **Day 1 — EDA** (recorded 2026-10-30) | M18K V2 source inventory, RGB-depth stem pairing, annotation/class audit and figures | [`09_results/reports/M18K_V2_EDA_2026-10-30.md`](09_results/reports/M18K_V2_EDA_2026-10-30.md) |
| **Day 2 — Paper approach reproduction** (2026-11-02) | Two-class and WB-only YOLOv8n-seg training and held-out test | [`Day 2 results`](09_results/reports/Day2_YOLOv8n_Seg_Reproduction_2026-11-02.md) |
| **Day 3 — Additional analysis** (2026-11-03) | WB-only mask-area error on 30 images; 12 qualitative prediction comparisons and review | [`Day 3 results`](09_results/reports/Day3_Prediction_Area_and_Error_Analysis_2026-11-03.md) |
| **Day 4 — MVP and course evaluation** (2026-11-04) | Full 450-image area evaluation, executed inference demo, scratch Otsu comparison and ablation; English course-report draft | [`Day 4 results`](09_results/reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md) |

## Dataset

M18K V2 working copy: **4,495 indexed RGB images** (3,596 train / 449 val / 450 test), **700,589 original COCO annotations** (858 Baby Bella, 699,731 White Button). All 4,495 RGB files have filename-matched depth files. This does not verify physical depth calibration, image-content independence, or original dataset license. The upstream V2 count of 4,652 versus our 4,495 indexed images remains unexplained.

## Main results (held-out test)

| Model/result | Mask AP@50 | Mask AP@50:95 |
| --- | ---: | ---: |
| Two-class **overall, macro-mean BB+WB** | 0.4995 | 0.3963 |
| Two-class **WB only, class metric** | 0.9890 | 0.7870 |
| Two-class **BB only, class metric** | 0.0095 | 0.00571 |
| Independently trained **WB-only model** | **0.9906** | **0.7974** |

Day 3 diagnostic on a **random 30-image subset** measured mean absolute pixel-area error **207.4 px²** (4,900 matched masks). **Day 4 expands this to all 450 test images:** **68,794 matched WB masks**, mean absolute area error **211.41 px²** and mean relative absolute error **8.81%**. These are **projected mask areas in px², not physical mm²**; errors are conditional on matching.

Day 4 also completed a **WB-only inference MVP** (10 random test images; 1,551 predicted instances) and a **10-image Otsu baseline/ablation**. Scratch Otsu matched OpenCV on all 10; YOLO had higher foreground-union IoU and far lower counting error. These illustrative comparisons are separate from full-test instance AP.

## Where to find the work

- Experiment configs, CSV registry and saved notebooks (including Day 4 inference and Otsu): [`08_experiments`](08_experiments/README.md)
- Scripts for WB labels and area measurement: [`07_source_code`](07_source_code/README.md)
- Metrics, qualitative review, area data: [`09_results`](09_results/README.md)
- English course-project Word/PDF report draft: [`10_research_paper/drafts`](10_research_paper/drafts/README.md)
- Reproduction logs and provenance: [`12_reproducibility`](12_reproducibility/CLOUD_EXECUTION_GUIDE.md)
- Open QC/approval items: [`00_project_management/RESEARCH_STATUS.md`](00_project_management/RESEARCH_STATUS.md)

The trained weights (`best.pt`), full V2 RGB-D dataset, raw multi-gigabyte COCO JSON and WB-label ZIP are **not committed**. They remain external in the team's Drive. Model outputs do not imply confirmed scene-level split independence.

Reference: Zakeri et al. (2025), *M18K: A Multi-Purpose Real-World Dataset for Mushroom Detection, 3D Pose Estimation, and Growth Monitoring*, *Computers* 14(5), 199. https://doi.org/10.3390/computers14050199

## Day 4 course-project MVP — quick start

1. Run [`Day4_WB_Only_Final_Inference_Executed.ipynb`](08_experiments/notebooks/Day4_WB_Only_Final_Inference_Executed.ipynb) in **Google Colab** with the dataset test RGB directory and existing WB-only checkpoint (downloaded by the notebook). It displays predictions and exports count/area CSVs and a ZIP. No training required.
2. Run [`Day4_Otsu_Baseline_Ablation_Executed.ipynb`](08_experiments/notebooks/Day4_Otsu_Baseline_Ablation_Executed.ipynb) for the scratch Otsu/OpenCV verification, 10-image comparison, and ablations. Requires the COCO test JSON and checkpoint.
3. Read [`Day4_Full_Test_Area_And_MVP_2026-11-04.md`](09_results/reports/Day4_Full_Test_Area_And_MVP_2026-11-04.md) and edit the [`course report`](10_research_paper/drafts/README.md). Install dependencies for Python/Colab from [`requirements.txt`](requirements.txt) where needed.

This is an **MVP**, not a fully validated production system. Foreground-union IoU is distinct from YOLO instance AP; the 10-image Otsu experiment is illustrative only. Day 4 QC submitted results do **not** clear the originally flagged dHash pairs. The demo video, slide deck and syllabus-specific course-lesson mapping still need finalization. 
