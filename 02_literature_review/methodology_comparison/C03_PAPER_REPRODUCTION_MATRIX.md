# C03 Paper Reproduction Matrix — WP-04B

**Paper:** Albayrak et al. (2025), DOI 10.3390/agronomy15010226.[S1]  
**Kết luận:** `EXACT_REPRODUCTION_FEASIBLE = NO`; `PARTIAL_REIMPLEMENTATION = YES`; thí nghiệm khoa học mới phải gắn nhãn `NEW_PROTOCOL_REQUIRED`.

| Thành phần | Paper báo cáo | Trạng thái tái lập | Blocker |
|---|---|---|---|
| Dataset | 3.195 ảnh White; HL 731, BB 576, DB 665, Cobweb 664, WB 559 | PARTIAL | Không có historical manifest/checksum trong paper; Zenodo 2026 rộng hơn (9.403 ảnh/3 lights).[S2] |
| Split | 80% train / 20% validation; không test độc lập | PARTIAL | Thiếu file list, seed, stratification và grouping unit |
| Preprocess | resize theo input, thường 224², giữ aspect ratio; [0,1]; background cleaning; không augmentation | PARTIAL | Thiếu padding/crop/interpolation và thuật toán background cleaning |
| Models | 20 pretrained CNNs | PARTIAL | Thiếu exact checkpoint/hash/API versions |
| Training | batch 11; LR .001; SGD momentum .9; 8 epochs; no early stop | PARTIAL | Thiếu loss, weight decay, scheduler, freeze/unfreeze, classifier init |
| Software | MATLAB R2023b chính; Python 3.9 cho analysis/visualization | PARTIAL | Thiếu toolbox/library versions và bridge implementation |
| Metrics | accuracy, precision, recall, F1, AUC, AP, specificity; weighted Overall Score | PARTIAL | Thiếu macro/micro/weighted, OVR/OVO, AP interpolation, class-absence convention |
| Model selection | ResNet-50 Overall Score 99,70% | EXACT_AS_REPORTED | Dùng cùng validation để tuning, so 20 models và báo kết quả |
| Repeated runs | Không báo seed/run count/uncertainty | INSUFFICIENT | Không tái tạo variability |
| Code/checkpoint | Không tìm thấy trong nguồn reviewed | INSUFFICIENT | Exact implementation không có |

### 20 kiến trúc được báo cáo

ResNet-50, DenseNet-201, DarkNet-53, Inception-v3, VGG-16, VGG-19, MobileNet-v2, EfficientNet-b0, NasNet-Large, NasNet-Mobile, ShuffleNet, SqueezeNet, Xception, GoogLeNet, AlexNet, ResNet-18, ResNet-101, Inception-ResNet-v2, DarkNet-19 và Places365-GoogLeNet.

## Validation reuse và leakage risk

- Validation 20% được paper mô tả vừa dùng trong training/fine-tuning/hyperparameter tuning vừa dùng đánh giá; không có final held-out test.[S1]
- Chọn winner trong 20 architectures trên cùng validation tạo selection bias (`REVIEWER_INFERENCE`).
- Paper báo nhiều góc/giai đoạn, nhiều visits/farms nhưng không báo specimen/farm split; leakage thật sự chưa được chứng minh, song không thể loại trừ.

## Mâu thuẫn nội bộ đáng kể

1. Results nói VGG-16 bị loại vì overfitting, nhưng đoạn sau nói không overfit và Table 2 vẫn có kết quả.
2. Một số prose dùng 99,70% như accuracy; Table 2 cho accuracy 99,66%, Overall Score 99,70%.
3. Conclusion nhấn mạnh DenseNet-201 trong khi công thức/Table 2 xếp ResNet-50 đầu.
4. Validation được gọi “unbiased” dù cùng đoạn nói dùng để tuning.

## Phân loại cuối

- **EXACT_REPRODUCTION_FEASIBLE:** `NO`.
- **PARTIAL_REPRODUCTION_FEASIBLE:** `YES`, chỉ ở mức khung chung nếu xác minh đúng corpus.
- **NEW_PROTOCOL_REQUIRED:** `YES` cho mọi split/preprocess/metric tự chọn.
- **INSUFFICIENT_EVIDENCE:** historical split, grouping, exact fine-tuning, exact metrics và code.

Không chạy model trong WP-04B.

## Sources

- **[S1]** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226; local full text locators `paper_agronomy_fulltext.txt:49–76, 78–85, 107–120`, Table 1/2 trong XML.
- **[S2]** Zenodo record 20260929, https://zenodo.org/records/20260929.
