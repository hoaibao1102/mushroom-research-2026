# C03 Proposed Evaluation Protocol — WP-04B

**Loại:** protocol đề xuất, chưa execute.  
**Authorization:** `TRAINING_NOT_AUTHORIZED`; `SPLIT_NOT_CREATED`.  
**Scientific readiness hiện tại:** `BLOCKED_BY_GROUPING_AND_LABEL_PROVENANCE`.

## 1. Estimands tách biệt

1. **White-light historical diagnostic:** so sánh với baseline paper nhưng không gọi exact reproduction.
2. **In-domain multi-illumination:** hiệu năng khi train/evaluate cùng distribution, group-held-out.
3. **Cross-illumination robustness:** train trên một/nhóm lights, test trên unseen light.
4. **Acquisition/farm generalization:** chỉ khi metadata farm/visit/session tồn tại.
5. **Specimen-level generalization:** chỉ khi group specimen authoritative/validated.

Không gộp các estimand trên thành một accuracy duy nhất.

## 2. Gating trước split/training

Bắt buộc trước khi tạo split:

- frozen manifest: path, SHA-256, label token, illumination, provenance version;
- xác nhận hoặc adjudicate `kw` semantics; giữ uncertainty flag;
- authoritative specimen/session/farm IDs, hoặc complete conservative grouping policy được phê duyệt;
- 100% ảnh có group ID hoặc exclusion reason;
- kiểm tra group/class contradictions và exact/near-duplicate crossings;
- định nghĩa target population và deployment unit;
- freeze protocol trước khi xem sealed-test predictions.

Nếu grouping không đóng được, **stop**: không claim independent biological generalization. Có thể chạy random-image diagnostic sau này nhưng phải gắn `DEPENDENCE_NOT_CONTROLLED` và không dùng làm bằng chứng chính.

## 3. Split candidate (chưa tạo)

- Primary: stratified group split theo specimen; nếu farm/session có thật, ưu tiên hierarchy farm/session → specimen.
- Tất cả White/UV/Mixed của cùng group phải ở cùng partition.
- Train/development/sealed test tách riêng; sealed test không dùng chọn architecture/hyperparameters.
- Augmentation và mọi learned preprocessing chỉ fit/apply sau split, trên train.
- Version manifest/split và checksum; không regenerate tùy ý.

## 4. Evaluation matrix

| Scenario | Train | Test | Claim được phép |
|---|---|---|---|
| In-domain | White train | White group-held-out | White-light internal generalization |
| Cross-light | White | UV; Mixed | transfer under unseen illumination |
| Leave-one-light-out | 2 lights | light còn lại | illumination robustness |
| Mixed-domain | all lights train groups | all lights held-out groups | multi-light internal generalization |
| Farm/session holdout | farms/sessions A | unseen farm/session B | chỉ khi metadata authoritative |

## 5. Metrics

Pre-register: macro-F1, macro recall/balanced accuracy, per-class precision/recall/F1, confusion matrix, multiclass AUROC/AP với averaging được ghi rõ, calibration (ECE/Brier), và group-weighted accuracy. Báo mean + uncertainty qua multiple seeds; interval resample group, không resample ảnh độc lập.

Báo riêng theo illumination và class. Không dùng Overall Score của paper làm endpoint duy nhất; có thể báo như secondary compatibility metric với công thức cố định.

## 6. Acceptance criteria

- zero group overlap và zero exact SHA overlap giữa partitions;
- mọi suspected near-duplicate crossing được adjudicate hoặc conservative co-location;
- no sealed-test reuse trong selection;
- labels uncertain được báo riêng/sensitivity analysis;
- results có per-seed, per-class và group-aware uncertainty;
- claim scope không vượt metadata/grouping evidence.

## 7. Stop criteria

Dừng trước training nếu: không có complete grouping coverage; `kw` chưa đủ dùng cho intended claim; split chứa component crossing; preprocessing không thể fit train-only; hoặc sealed test đã bị dùng để thiết kế model. Không mở unrestricted similarity cycle để né blocker—chuyển thành quyết định dataset.

## Methodological context

Group-aware split và leakage-aware evaluation đã được minh họa trong agricultural CV; đây là phương pháp transferable, không phải bằng chứng C03 đã độc lập.[S1][S2]

## Sources

- **[S1]** *Leaf identity and visual group splitting in potato disease classification* (2026), https://doi.org/10.3389/fcomp.2026.1946705.
- **[S2]** *Leakage-Aware Transfer Learning... MangoLeafBD* (2026), https://doi.org/10.3390/app16146989.
- **[S3]** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226.
