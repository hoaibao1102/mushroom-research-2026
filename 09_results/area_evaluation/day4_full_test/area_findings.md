# Day 4 - Đánh giá diện tích mask dự đoán trên toàn bộ test (450 ảnh)

## 1. Mẫu và cách đo
- **Mẫu:** toàn bộ 450 ảnh của split test M18K V2 (không lấy mẫu con). Danh sách ảnh nằm trong `area_per_image.csv` (một dòng mỗi ảnh). Số annotation WB làm tham chiếu là 70.192, bằng đúng số annotation WB của test trong COCO; không có annotation nào bị loại (không `iscrowd`, không mask diện tích 0).
- **Mô hình:** checkpoint WB-only YOLOv8n-seg đã có (hash trong `area_metrics.json`). Chỉ chạy inference.
- **Inference:** `imgsz=640` (lấy từ checkpoint), `conf=0.25`, NMS IoU `0.7`, `max_det=1000`, `retina_masks=True`; mọi mask dự đoán có cùng kích thước với ảnh COCO. Script ghi thiết bị đã dùng là `cpu`. Các tham số giống hệt đợt 30 ảnh và không được chỉnh lại.
- **Ghép cặp:** một-một theo mask IoU ≥ 0,50 (greedy, IoU cao nhất trước). GT là polygon COCO raster bằng `pycocotools` ở độ phân giải gốc.
- **Diện tích:** `A_px2 = sum(mask > 0)` cho từng instance, đơn vị **px²** (không phải mm²). `relative_error_pct = 100 × |pred − GT| / GT`.

## 2. Kết quả tổng

| đại lượng | giá trị |
|---|---|
| Ảnh đánh giá | 450 |
| GT / dự đoán | 70.192 / 72.182 |
| **Ghép được** | **68.794** |
| Dự đoán không khớp | 3.388 (4,7% số dự đoán) |
| GT không có dự đoán khớp | 1.398 (2,0% số GT) |
| Match coverage (ghép được / GT) | 98,01% |
| Ghép được / số dự đoán | 95,31% |
| MAE | 211,4 px² |
| Sai số tương đối trung bình / trung vị | 8,81% / 7,31% |
| Mask IoU trung bình / trung vị (cặp ghép) | 0,890 / 0,902 |
| Sai số có dấu trung bình (pred − GT) | +165,5 px² |
| Cặp có dự đoán lớn hơn GT | 86,1% |
| Tổng diện tích dự đoán / GT (cặp ghép) | 1,046 |
| Tỉ số tổng diện tích dự đoán / GT trên mỗi ảnh | trung bình 1,068 (từ 1,010 đến 1,262) |

MAE và sai số tương đối chỉ tính trên các cặp ghép được; object không khớp được báo riêng. Tỉ số tổng diện tích trên mỗi ảnh gồm cả dự đoán không khớp và chưa trừ phần chồng nhau. Ảnh có tỉ số cao nhất (1,262) là `004391.png` (42 GT, 51 dự đoán, 40 ghép được); ba ảnh có tỉ số cao nhất (`004170`: 1,233; `004271`: 1,255; `004391`: 1,262) đều có nhiều hơn GT từ 9 đến 12 dự đoán (65 so với 53, 69 so với 57, 51 so với 42). Nguyên nhân của các dự đoán dư đó em chưa xem lại (NOT_VERIFIED).

## 3. Nấm nhỏ so với nấm lớn
Em chia theo phân vị diện tích GT của 70.192 object (ngưỡng 2.093 và 3.904 px²):

| nhóm | n GT | ghép được | coverage | diện tích GT TB (px²) | MAE (px²) | sai số tương đối TB / trung vị | sai số có dấu (px²) | % cặp dự đoán nhỏ hơn GT | mask IoU TB |
|---|---|---|---|---|---|---|---|---|---|
| nhỏ (0–33%) | 23.378 | 22.057 | 94,3% | 1.428 | 206,1 | 15,4% / 14,3% | +202,8 | 1,7 | 0,842 |
| vừa (33–66%) | 23.413 | 23.368 | 99,8% | 2.911 | 221,0 | 7,9% / 7,6% | +205,9 | 6,5 | 0,897 |
| lớn (66–100%) | 23.401 | 23.369 | 99,9% | 6.436 | 206,8 | 3,5% / 2,9% | +89,9 | 32,5 | 0,930 |

Chia mịn hơn thì ở nhóm lớn nhất (đã chia theo phân vị 0–33, 33–66, 66–90, 90–99, 99–100%, ngưỡng 2.081 / 3.849 / 6.984 / 12.603 px²), sai số có dấu trung bình lần lượt là +202,5 / +206,7 / +139,8 / −13,6 / −117,5 px², và tỉ lệ cặp có dự đoán nhỏ hơn GT là 1,7 / 6,3 / 22,6 / 53,6 / 67,7%. Nhóm 99–100% (702 object) có MAE cao nhất, 301,6 px², nhưng sai số tương đối chỉ 2,1%.

**Nhận xét:**
- MAE gần như không đổi giữa các nhóm kích thước (khoảng 206–221 px² ở ba nhóm đầu), nên **sai số tương đối giảm mạnh khi nấm to lên**: 15,4% ở nấm nhỏ so với 3,5% ở nấm lớn.
- Ở nấm nhỏ và vừa, mask dự đoán lớn hơn GT khoảng 200 px² (hầu như mọi cặp đều dự đoán lớn hơn); độ lệch này giảm dần ở nấm lớn rồi **đổi dấu ở nhóm 10% nấm lớn nhất**, nơi hơn một nửa số cặp dự đoán nhỏ hơn GT.
- Phần lớn các GT bị bỏ sót là nấm nhỏ: 1.321 trong 1.398 GT không khớp (94,5%) thuộc nhóm nhỏ, trong khi nhóm vừa và lớn gần như đều tìm được dự đoán (coverage ≥ 99,8%).
- Mask IoU tăng theo kích thước (0,842 → 0,930), tức là mask của nấm nhỏ trùng với GT kém hơn.
- Vì nấm nhỏ bị bỏ sót nhiều hơn và phép ghép dùng ngưỡng IoU 0,5, sai số của nấm nhỏ trong bảng được tính trên các nấm đã ghép được, nên có thể thấp hơn sai số thực của nhóm này (những mask kém nhất không được ghép nên không vào MAE).

Em chưa kiểm tra nguyên nhân của độ lệch dương (NOT_VERIFIED): nó có thể do mô hình, do cách gán nhãn polygon, hoặc do cả hai.

## 4. So sánh với đợt 30 ảnh trước

| | 30 ảnh (trước) | 450 ảnh |
|---|---|---|
| GT / dự đoán | 4.970 / 5.146 | 70.192 / 72.182 |
| Ghép được | 4.900 | 68.794 |
| Match coverage | 98,59% | 98,01% |
| Dự đoán không khớp (% số dự đoán) | 246 (4,8%) | 3.388 (4,7%) |
| MAE (px²) | 207,4 | 211,4 |
| Sai số tương đối TB / trung vị | 8,80% / 7,34% | 8,81% / 7,31% |
| Mask IoU TB | 0,890 | 0,890 |
| Sai số có dấu TB (px²) | +160,8 | +165,5 |
| Cặp dự đoán lớn hơn GT | 85,6% | 86,1% |
| Tổng diện tích dự đoán / GT (cặp ghép) | 1,045 | 1,046 |

- Kết quả của 30 ảnh được tính lại bên trong lần chạy 450 ảnh cho ra đúng các số của lần trước (4.970 / 5.146 / 4.900 / 246 / 70 và MAE 207,4), nên phép đo tái lập được dù phiên bản `ultralytics` khác (8.4.199 trước, 8.4.202 nay).
- Các chỉ số của 450 ảnh sát các chỉ số của 30 ảnh (MAE chênh khoảng 2%, sai số tương đối và IoU gần như trùng), nên mẫu 30 ảnh khá đại diện. Xu hướng theo kích thước cũng khớp đợt 30 ảnh (nhóm nhỏ nhất cùng +202,5 px²; nhóm lớn nhất đảo chiều). Match coverage thấp hơn một chút ở 450 ảnh (98,01% so với 98,59%).
- Điều mới ở 450 ảnh là các bảng theo kích thước có số mẫu lớn hơn nhiều (ví dụ 702 object ở nhóm lớn nhất, so với 49 ở đợt 30 ảnh).

## 5. Hình trong `figures/`
- `error_by_size.png` (đã xem): ba biểu đồ cột theo năm nhóm diện tích GT. Sai số tương đối giảm từ khoảng 15% (nhóm 0–33%) xuống khoảng 2% (nhóm 99–100%); sai số có dấu dương, khoảng +200 px² ở hai nhóm nhỏ nhất, giảm ở nhóm 66–90% rồi âm nhẹ ở hai nhóm lớn nhất; match coverage chỉ thấp hơn 100% rõ rệt ở nhóm nhỏ nhất (khoảng 94%). Hình khớp với bảng ở mục 3.
- `worst_mae_004252.png` (đã xem): đây là ảnh có MAE lớn nhất (632,2 px²) nhưng **không phải ảnh điển hình**. Cảnh chụp một khoảng sàn có chân người, một giá đỡ ba chân và một luống nấm ở xa ở góc trên bên phải; khác hẳn các ảnh nấm dày đặc thông thường. Ảnh chỉ có 5 GT và 6 dự đoán, cả 5 GT đều được ghép. Phần lớn GT (màu xanh) là các vùng lớn nằm trên sàn và gần quần/giày, không thấy mũ nấm nào ở đó, chỉ có một chấm trắng nhỏ ở góc trên bên phải trùng với một mask GT; mô hình cũng dự đoán gần như đúng các vùng lớn đó (các vùng đỏ). Các nhãn trong ô phóng to cho thấy diện tích GT và dự đoán cùng cỡ (ví dụ khoảng 6,3 nghìn và 6,6 nghìn px²), và có vài vùng lớn hàng chục nghìn px². Vì vậy MAE cao ở ảnh này chủ yếu do các object rất lớn chứ không do ghép sai nhiều object. Các vùng lớn đó là gì (nhãn sai, nấm bị che hay thứ khác) thì em chưa xác định được (NOT_VERIFIED). Ô phóng to còn có một khung đỏ hình chữ nhật góc vuông (mask dự đoán có cạnh thẳng), giống quan sát ở đợt 30 ảnh; nguyên nhân chưa kiểm tra.
- `median_mae_004153.png`, `most_unmatched_004250.png`: tạo từ chính kết quả inference của lần chạy này nhưng em chưa xem nên không mô tả. Phần mô tả lỗi trên hình cho đợt 30 ảnh nằm trong `area_findings.md` của `09_results/area_evaluation/`.

## 6. Hạn chế
- GT là polygon COCO raster hóa, không phải mask chính xác từng pixel; chưa tách được phần sai lệch do mô hình và phần do cách gán nhãn.
- Kết quả phụ thuộc tham số inference cố định (`conf`, NMS IoU, `imgsz`) và ngưỡng ghép IoU 0,5; đổi chúng sẽ đổi số object không khớp và có thể đổi diện tích.
- MAE và sai số tương đối chỉ tính trên cặp ghép được; object không khớp (3.388 dự đoán, 1.398 GT) không vào các số này. Bản chất của các dự đoán không khớp trên toàn bộ 450 ảnh chưa được phân tích (đợt 30 ảnh có nhận xét riêng).
- Diện tích tính bằng px², không quy đổi sang mm² và không nói gì về chất lượng nấm. Tổng diện tích mỗi ảnh là tổng từng instance, chưa loại phần chồng nhau.
- Ảnh `worst_mae` được chọn theo MAE cao nhất là một khung không điển hình (ít GT, các vùng lớn trên sàn); đây là ảnh ngoại lệ duy nhất theo số GT: số GT mỗi ảnh có trung bình 156, trung vị 167, từ 5 đến 222, và ảnh có ít GT nhất sau nó đã có 36 GT. Vì vậy không nên lấy ảnh này làm đại diện cho lỗi thường gặp.
- Đây là một mô hình, một checkpoint, một split; không so sánh giữa các mô hình.
