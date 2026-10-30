# C03 Final Feasibility Decision — WP-04B

## Decision

# `CONDITIONAL_GO`

C03 được giữ làm **ứng viên ưu tiên cho work package đóng evidence**, nhưng **không được chọn chính thức và không được train**.

## Cơ sở

### Điểm đạt

- Source identity, versioned Zenodo record và CC BY 4.0 deposit đã được trace trong WP-04.[S1]
- 9.403/9.403 JPEG decode; không exact SHA duplicates; ba illumination và năm folder classes usable về kỹ thuật.
- White subset counts khớp paper 3.195 ảnh ở cả năm lớp.[S2]
- Paper là baseline có ý nghĩa, nhưng chỉ partial reproduction.
- Một protocol mới, group-aware/cross-illumination có thể thiết kế về mặt phương pháp.

### Blockers

1. biological specimen grouping/farm/session mapping `NOT_VERIFIED`;
2. equal-ordinal shortcut thất bại trong bounded review;
3. `kw → Cobweb` chỉ `PROVISIONAL_PARTIALLY_SUPPORTED`;
4. không có historical split/code/checkpoint; validation paper bị reuse;
5. research gap chỉ là bounded evidence gap, chưa validated.

## Điều kiện bắt buộc

Trước bất kỳ training authorization nào:

1. nhận authoritative specimen/acquisition manifest từ tác giả **hoặc** hoàn thành complete, approved human grouping audit;
2. 100% ảnh có group assignment/exclusion reason và zero group crossing trong split candidate;
3. xác nhận `kw` data dictionary hoặc phê duyệt label-uncertainty policy;
4. freeze immutable group-aware split/protocol, sealed test và metric definitions;
5. thực hiện literature review mở rộng có search log để đánh giá gap;
6. independent review ký chấp thuận data/protocol gates.

## Stop criterion

Nếu không thể thiết lập complete dependency grouping hoặc một estimand trung thực không đòi biological independence trong work package kế tiếp, chuyển C03 thành `NO_GO_FOR_PRIMARY_GENERALIZATION` và đánh giá C04/ứng viên khác; không mở thêm unrestricted QC cycle.

## Authorization state

- Dataset selected: `NO / PENDING`
- Training authorized: `NO`
- Split execution authorized: `NO`
- Research gap validated: `NO`
- C03 priority retained: `YES, CONDITIONAL`

## Sources

- **[S1]** Zenodo record 20260929, https://zenodo.org/records/20260929.
- **[S2]** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226.
