# C03 Specimen Grouping Audit — WP-04B

**Ngày audit:** 2026-10-30  
**Trạng thái:** `BIOLOGICAL_INDEPENDENCE_NOT_VERIFIED`  
**Phạm vi:** audit bounded, không train, không tạo split, không sửa ảnh gốc.

## 1. Bằng chứng trực tiếp

- `DATASET_OBSERVED`: 9.403 JPEG, đều 912×912 RGB và decode được; White 3.195, UV 3.143, Mixed 3.065.
- Cấu trúc gồm 15 thư mục `illumination × class`; tên file là prefix nguồn sáng/lớp + ordinal liên tục.
- Không có EXIF, specimen ID, camera ID, farm, visit, session, flush hoặc manifest cross-illumination trong payload.
- Không có duplicate SHA-256. Điều này chỉ loại exact-byte duplicates.
- `AUTHOR_REPORTED`: ảnh được chụp ở nhiều góc/giai đoạn, trong nhiều lần thăm nhiều farm trong 12 tháng.[S1]
- Bản ghi dữ liệu mô tả ba nguồn sáng và năm lớp.[S2]

## 2. Bounded candidate matching

Procedure `C03_BOUNDED_V1` tạo đúng 120 cặp, không chạy all-pairs:

- 15 strata = 5 lớp × 3 cặp nguồn sáng.
- Mỗi stratum: 6 equal-ordinal suggestions + 2 shifted-ordinal controls.
- Tổng: 90 equal ordinal, 30 controls.
- Score lưu riêng: dHash Hamming, gray correlation, edge cosine, HSV-histogram cosine, ORB ratio matches và homography inliers.
- 15 plate chứa native L/R và luminance-normalized L/R; filename, ordinal và arm bị ẩn khỏi first-pass AI screening.

## 3. Kết quả screening

| Arm | SAME | LIKELY | DIFFERENT | UNCERTAIN | Tổng |
|---|---:|---:|---:|---:|---:|
| Equal ordinal | 16 | 23 | 48 | 3 | 90 |
| Shifted control | 4 | 5 | 15 | 6 | 30 |
| Toàn bộ | 20 | 28 | 63 | 9 | 120 |

Các giá trị trên là `AI_SCREENING`, **không phải human adjudication**. Trường reviewer/adjudicated trong CSV vẫn để trống. Không edge grouping nào được tạo.

## 4. Diễn giải

- Equal ordinal thất bại rõ: 48/90 bị screen là `DIFFERENT_SPECIMEN`; controls vẫn có 4/30 `SAME_VISIBLE_SPECIMEN`.
- Do đó ordinal không phải khóa ghép specimen đáng tin cậy. Tương đồng ảnh/score cũng không đủ để nâng thành biological identity.
- Audit mẫu 120 cặp không cung cấp complete grouping coverage cho 9.403 ảnh.
- `SAME_VISIBLE_SPECIMEN` chỉ nói về vật thể nhìn thấy trong hai ảnh, không chứng minh farm/session hoặc độc lập giữa components.

## 5. Kết luận và stop gate

**Kết luận:** `BIOLOGICAL_INDEPENDENCE = NOT_VERIFIED`; C03 chưa sẵn sàng cho tuyên bố specimen-level generalization.

Không được:

1. ghép toàn corpus bằng ordinal;
2. gọi random image split là independent biological validation;
3. tạo authoritative specimen ID từ similarity;
4. mở rộng thành unrestricted all-pairs QC.

Bước đóng blocker phải là một trong hai: (a) manifest authoritative từ tác giả; hoặc (b) audit grouping bao phủ toàn bộ, được phê duyệt riêng và có human adjudication. Bounded sample hiện tại chỉ đủ bác bỏ shortcut ordinal.

## Artifacts

- `04_dataset_candidates/C03_agaricus_disease/qc/wp04b_readiness/bounded_similarity_review.csv`
- `.../image_review_index.csv`
- `.../ai_screening_summary.csv`
- `.../bounded_review_manifest.json`
- `.../review_plates/plate_01...plate_15.jpg`

## Sources

- **[S1]** Albayrak et al. (2025), *Classification and Analysis of Agaricus bisporus Diseases with Pre-Trained Deep Learning Models*, https://doi.org/10.3390/agronomy15010226 (Methods §§2.2–2.4).
- **[S2]** Zenodo record 20260929, https://zenodo.org/records/20260929.
