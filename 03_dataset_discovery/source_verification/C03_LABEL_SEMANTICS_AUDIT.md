# C03 Label Semantics Audit — WP-04B

**Trạng thái:** `PARTIALLY_SUPPORTED`; không đổi tên/relabel dữ liệu.

## Mapping được kiểm tra

| Folder code | Class diễn giải | Trạng thái | Bằng chứng |
|---|---|---|---|
| `hl` | Healthy | `SUPPORTED` | White count 731 khớp chính xác paper Healthy 731; paper figure dùng `w0hl`.[S1] |
| `bb` | Bacterial Blotch | `SUPPORTED` | White count 576 khớp paper; figure dùng `w b b`.[S1] |
| `db` | Dry Bubble | `SUPPORTED` | White count 665 khớp paper; figure dùng `w d b`.[S1] |
| `kw` | Cobweb | `PROVISIONAL_PARTIALLY_SUPPORTED` | White count 664 khớp chính xác Cobweb 664 và đây là folder bệnh thứ tư; paper figure lại ghi `w c w`, không trực tiếp giải thích token `kw`.[S1] |
| `wb` | Wet Bubble | `SUPPORTED` | White count 559 khớp paper; figure dùng `w w b`.[S1] |

Zenodo nêu năm lớp Healthy, Bacterial Blotch, Dry Bubble, Cobweb và Wet Bubble, dưới White/UV/Mixed.[S2] Tuy nhiên record không cung cấp data dictionary giải thích trực tiếp `kw`.

## Label provenance

- `AUTHOR_REPORTED`: expert mycologists thực hiện manual annotation; panel specialists cross-validate và xử lý ambiguities.[S1]
- `NOT_FOUND_IN_REVIEWED_METHODS`: nuôi cấy, isolation, microscopy, PCR hoặc xét nghiệm lab theo từng ảnh.
- Vì vậy nhãn là **expert visual diagnosis reported by authors**, không phải laboratory-confirmed ground truth.
- Paper báo Dry Bubble/Cobweb có visual similarity; đây là rủi ro confusion có thật theo tác giả.[S1]

## Quyết định

- Giữ nguyên raw folder token `kw` trong mọi manifest.
- Trong báo cáo có thể dùng `kw (provisional: Cobweb)`.
- Không âm thầm đổi `kw` thành `cw/cb/Cobweb`.
- Điều kiện nâng lên `CONFIRMED`: README/data dictionary hoặc xác nhận tác giả liên kết trực tiếp `kw` với Cobweb, kèm provenance của diagnosis.

## Sources

- **[S1]** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226, Methods §§2.2–2.4 và captions Figures 7–8.
- **[S2]** Zenodo record 20260929, https://zenodo.org/records/20260929.
