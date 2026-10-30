# C03 Research Gap Prescreen — WP-04B

**Cutoff:** 2026-10-30  
**Loại review:** `BOUNDED_PRESCREEN_NOT_SYSTEMATIC`  
**Gap status:** `UNVALIDATED`; không tuyên bố novelty.

## Source registry rút gọn

| Source | Quan hệ | Điều nguồn thiết lập | Access scope |
|---|---|---|---|
| Dataset paper 2024 [S1] | ORIGINAL_DATASET_PUBLICATION | A. bisporus disease dataset, multi-illumination/multi-view author description | ABSTRACT |
| Agronomy 2025 [S2] | ORIGINAL WHITE-LIGHT BASELINE | 20 CNNs trên 3.195 ảnh White | FULL TEXT |
| Zenodo 2026 [S3] | ORIGINAL_DATASET_RELEASE | 5 lớp, White/UV/Mixed, DOI relation với paper | RECORD + local payload |
| SqueezeNet/color spaces 2026 [S4] | SAME TASK, DATASET RELATION UNCERTAIN | ảnh A. bisporus và color-space comparison | ABSTRACT/XML |
| VNIR blotch 2010 [S5] | ADJACENT SAME SPECIES | spectral discrimination of blotch | ABSTRACT |
| Lab-to-field UDA 2023 [S6] | TRANSFERRED METHOD | controlled→wild domain adaptation | bibliographic/abstract |
| Cross-domain reliability 2026 [S7] | TRANSFERRED EVALUATION | domain shift, parent-aware evaluation, calibration | structured abstract |
| Leaf identity/group split 2026 [S8] | TRANSFERRED EVALUATION | random vs identity-grouped split sensitivity | full text/XML |
| Mango leakage-aware 2026 [S9] | TRANSFERRED METHOD | near-duplicate grouping + GroupKFold | structured abstract |
| Sugarcane leakage-aware 2026 [S10] | TRANSFERRED METHOD | duplicate audit before augmentation ablation | abstract |

Crossref xác minh DOI/title/year của các nguồn trên ngày 2026-10-30. Không xác nhận được independent direct reuse của Zenodo 20260929 trong phạm vi prescreen.

## Điều đã có

- Baseline A. bisporus white-light và release đa nguồn sáng đã tồn tại.[S1][S2][S3]
- Color-space processing trên cùng domain rộng đã được nghiên cứu, nhưng không tương đương unseen-illumination evaluation.[S4]
- Văn liệu ngoài Agaricus đã xử lý domain shift, identity-aware split và leakage-aware agricultural classification.[S6]–[S10]

## Evidence gaps trong coverage đã rà soát

Chưa tìm được nguồn primary đủ bằng chứng cho:

1. benchmark A. bisporus đầy đủ White→UV, White→Mixed và leave-one-illumination-out;
2. split giữ ba nguồn sáng của cùng specimen trong cùng partition bằng ID authoritative;
3. independent farm/session/device/time holdout cho C03;
4. independent confirmed reuse của version Zenodo 20260929;
5. đánh giá đồng thời group leakage, cross-light robustness và calibration trên C03.

Đây là **evidence gap within reviewed coverage**, không phải “không có nghiên cứu nào”. Gap khoa học vẫn `UNVALIDATED` cho tới literature review có protocol/search log rộng hơn và grouping evidence được đóng.

## Câu hỏi nghiên cứu bounded có thể kiểm tra sau này

- Group-aware performance khác random-image diagnostic bao nhiêu?
- Mức giảm macro-F1/calibration khi chuyển sang unseen illumination là bao nhiêu?
- Train trên hai light có cải thiện held-out third-light không?
- Hiệu ứng còn giữ khi holdout farm/session, nếu metadata cho phép?

## Sources

- **[S1]** https://doi.org/10.30708/mantar.1452976
- **[S2]** https://doi.org/10.3390/agronomy15010226
- **[S3]** https://zenodo.org/records/20260929
- **[S4]** https://doi.org/10.3897/ejfa.2026.169921
- **[S5]** https://doi.org/10.1255/jnirs.894
- **[S6]** https://doi.org/10.34133/plantphenomics.0038
- **[S7]** https://doi.org/10.3389/fpls.2026.1826962
- **[S8]** https://doi.org/10.3389/fcomp.2026.1946705
- **[S9]** https://doi.org/10.3390/app16146989
- **[S10]** https://doi.org/10.63158/journalisi.v8i5.1896
