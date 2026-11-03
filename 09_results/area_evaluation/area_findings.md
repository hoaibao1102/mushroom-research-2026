# Đánh giá diện tích mask dự đoán (WB YOLOv8n-seg)

## 1. Thiết lập
- **Dữ liệu:** 30 ảnh chọn xác định từ split test (450 ảnh, 70.192 annotation WB trong COCO). Ảnh được sắp theo tên file rồi lấy mẫu bằng `random.Random(42).sample`; danh sách lưu trong `selected_test_images.csv`. Đây là đợt kiểm tra phép đo, không phải benchmark mô hình.
- **Mô hình:** checkpoint YOLOv8n-seg một class (`0: WB`), SHA-256 `93d993ec6b48c1fca9d59178afe11377ef20afa3ed0c304841e4d6b36d447961`; theo `train_args` trong checkpoint: `imgsz=640`, 10 epoch, `seed=42`. Chỉ chạy inference.
- **Inference:** `imgsz=640`, `conf=0.25`, NMS IoU `0.7`, `max_det=1000`, `retina_masks=True` (mask ở độ phân giải ảnh gốc). Các tham số được cố định trước khi xem kết quả, không tinh chỉnh. Mọi mask dự đoán có cùng kích thước với ảnh COCO.
- **Tham chiếu (GT):** polygon WB của COCO, raster bằng `pycocotools` ở độ phân giải gốc. Cả 4.970 annotation WB của 30 ảnh đều dùng được (không có `iscrowd` hay mask diện tích 0).
- **Ghép cặp:** một-một, greedy theo mask IoU giảm dần, ngưỡng IoU ≥ 0,50.
- **Diện tích:** `A_px2 = sum(mask > 0)` bằng đúng hàm `mask_area_px2` đã kiểm chứng; đơn vị px² (không phải mm²). `relative_error_pct = 100 * |pred − GT| / GT`.

## 2. Kết quả

| đại lượng | giá trị |
|---|---|
| Số GT / số dự đoán | 4.970 / 5.146 |
| Ghép được | 4.900 |
| Dự đoán không khớp | 246 (4,8% số dự đoán) |
| GT không có dự đoán khớp | 70 (1,4% số GT) |
| Match coverage (ghép được / GT) | 98,59% |
| MAE | 207,4 px² (5,84% diện tích GT trung bình 3.552,9 px²) |
| Sai số tương đối trung bình | 8,80% (trung vị 7,34%) |
| Phân vị 75 / 90 / 95 / 99 / max của sai số tương đối | 12,6 / 17,78 / 22,34 / 33,4 / 94,59 % |
| Mask IoU của cặp ghép | trung bình 0,890; nhỏ nhất 0,504 |

Ghi chú: MAE và sai số tương đối chỉ tính trên các cặp ghép được; các object không khớp được báo riêng bên dưới.

### Xu hướng sai lệch
- Mask dự đoán **có xu hướng lớn hơn GT**: 85,6% cặp có diện tích dự đoán lớn hơn GT, 14,3% nhỏ hơn. Sai số có dấu trung bình là +160,75 px², và tổng diện tích dự đoán bằng 1,045 lần tổng diện tích GT trên các cặp ghép.
- Trên cả ảnh (tổng diện tích mọi instance, gồm cả dự đoán không khớp, chưa trừ phần chồng nhau), tỉ số tổng diện tích dự đoán/GT là 1,062 trung bình, từ 1,027 đến 1,107 giữa các ảnh. Nghĩa là diện tích tổng ước lượng cao hơn GT ở cả 30 ảnh.

### Theo kích thước object (chia ba nhóm bằng nhau theo diện tích GT)

| nhóm | n | diện tích GT trung bình (px²) | MAE (px²) | sai số tương đối TB (%) |
|---|---|---|---|---|
| nhỏ | 1.633 | 1.447,8 | 207,9 | 15,2 |
| vừa | 1.633 | 2.892,6 | 214,8 | 7,7 |
| lớn | 1.634 | 6.316,5 | 199,5 | 3,4 |

MAE gần như không đổi giữa ba nhóm (khoảng 200–215 px²) nên sai số tương đối tập trung ở object nhỏ. Việc sai số tuyệt đối gần không đổi cho thấy có thể là lệch ở viền mask, nhưng mình chưa kiểm tra nguyên nhân này (NOT_VERIFIED).

### Sai số có dấu theo kích thước (nhóm theo phân vị diện tích GT của 4.900 cặp ghép)

| nhóm (phân vị diện tích GT) | n | diện tích GT TB (px²) | sai số có dấu TB, pred − GT (px²) | tương ứng (% diện tích GT TB) | % cặp dự đoán nhỏ hơn GT |
|---|---|---|---|---|---|
| 0–33% (nhỏ) | 1.618 | 1.441,6 | +202,5 | +14,0% | 1,8 |
| 33–66% (vừa) | 1.617 | 2.867,9 | +202,6 | +7,1% | 6,9 |
| 66–90% (lớn) | 1.175 | 5.019,3 | +126,6 | +2,5% | 24,6 |
| 90–99% (rất lớn) | 441 | 8.731,7 | −21,0 | −0,2% | 53,7 |
| 99–100% (lớn nhất) | 49 | 14.095,6 | −144,3 | −1,0% | 69,4 |

Độ lệch dương khoảng +200 px² gần như không đổi ở nấm nhỏ và vừa, giảm dần ở nấm lớn, rồi đổi dấu ở 10% nấm lớn nhất, nơi dự đoán nhỏ hơn GT trong hơn một nửa số cặp. Mình chưa kiểm tra nguyên nhân (NOT_VERIFIED). Chỉ số 4.900 cặp đã được ghép, không gồm các object không khớp.

### Object không khớp
- **246 dự đoán không khớp:** diện tích trung vị 1.076 px², độ tin cậy trung vị 0,40. Có 168 dự đoán không chồng lên GT nào đáng kể (IoU tốt nhất < 0,1), 38 dự đoán chồng một phần (IoU 0,1–0,5), và 40 dự đoán còn lại có IoU ≥ 0,5 với một GT đã được ghép với dự đoán khác (suy ra từ phép trừ, nghĩa là dự đoán trùng hoặc chia nhỏ một object). Chưa xác định 168 dự đoán đó là dương tính giả hay object thật chưa được gán nhãn (NOT_VERIFIED).
- **70 GT không khớp:** diện tích trung vị 777 px² (nhỏ hơn diện tích GT trung bình). 50 GT không có dự đoán nào chồng lên (IoU < 0,1, tức bị bỏ sót), 10 chồng một phần, 10 có IoU ≥ 0,5 với một dự đoán đã ghép với GT khác.

## 3. Quan sát từ hình overlay (`area_examples/`)
Bốn hình được tạo từ chính kết quả inference: `best_mae_114_004160.png`, `median_mae_379_004425.png`, `worst_mae_327_004373.png`, `most_unmatched_216_004262.png`.

Đã xem cả 4 hình (`best_mae`, `median_mae`, `worst_mae`, `most_unmatched`). Các điểm dưới đây là quan sát trực tiếp trên hình hoặc đọc từ nhãn diện tích trong ô phóng to; nguyên nhân chỉ là phỏng đoán nếu có ghi rõ. Ô phóng to được đặt quanh cặp có sai số tuyệt đối lớn nhất của ảnh, nên các cặp được gắn nhãn không phải mẫu ngẫu nhiên.

- **Viền mask dự đoán nằm hơi ngoài viền GT.** Ở ô phóng to của cả 3 hình, đường viền đỏ (dự đoán) thường nằm sát và hơi bên ngoài đường viền xanh (GT) một dải mỏng. Nhãn diện tích trong `most_unmatched` và `best_mae` cho thấy mọi cặp được gắn nhãn đều có dự đoán lớn hơn GT, ví dụ 5306 → 5505, 1835 → 2071, 955 → 1142 (`most_unmatched`) và 1881 → 2205, 1652 → 2200 (`best_mae`). Điều này phù hợp với xu hướng dự đoán lớn hơn GT ở mục 2.
- **Object nhỏ chịu ảnh hưởng nhiều hơn.** Cùng một dải viền thừa chiếm tỉ lệ lớn hơn ở object nhỏ, ví dụ 1652 → 2200 (khoảng +33%) và 1339 → 1834 trong hai hình trên, so với khoảng +4% ở mushroom lớn 5306 → 5505. Đây là quan sát trên một số object, phù hợp với bảng sai số theo nhóm kích thước nhưng không thay thế bảng đó.
- **Hình `worst_mae` (sai số trung bình ảnh lớn nhất, 274,9 px²) cho thấy sai số theo cả hai hướng.** Ảnh này có nhiều nấm lớn xếp sát nhau. Một số nấm lớn có dự đoán nhỏ hơn GT, ví dụ 10298 → 8039 (khoảng −22%) và 9658 → 9019, trong khi nấm nhỏ hơn bên cạnh bị dự đoán lớn hơn, ví dụ 2542 → 3583 (khoảng +41%) và 1155 → 1572. Ranh giới giữa các mũ nấm chạm nhau là chỗ hai đường viền lệch nhau rõ nhất. Mình không xác định được nguyên nhân (có thể do ranh giới mũ nấm dính nhau khó tách, hoặc do cách vẽ polygon GT).
- **Hình `median_mae` (ảnh có MAE trung vị, 208,9 px²) cho cùng kiểu sai số.** Các nấm nhỏ và vừa trong ô phóng to đều bị dự đoán lớn hơn GT, ví dụ 1008 → 1273 (khoảng +26%), 2394 → 2779, 2371 → 2733, 1486 → 1697, 2312 → 2491. Ba nấm lớn nhất được gắn nhãn thì dự đoán nhỏ hơn GT một chút: 12892 → 11940 (khoảng −7%), 8749 → 8471, 7070 → 6797. Cùng với `worst_mae`, các nấm lớn được gắn nhãn đôi khi bị dự đoán nhỏ hơn, nhưng đây chỉ là các ví dụ trong ô phóng to; bảng sai số có dấu theo nhóm kích thước ở mục 2 xác nhận xu hướng này trên toàn bộ 4.900 cặp ghép (nhóm lớn nhất bị dự đoán nhỏ hơn GT).
- **Một số mask dự đoán có cạnh thẳng, hình chữ nhật.** Ở ô phóng to của `best_mae` có các khung đỏ góc vuông nằm trong mũ nấm, và trong `most_unmatched` có vài đoạn viền đỏ thẳng, góc cạnh. Vài dự đoán không khớp (màu tím) cũng có dạng khối chữ nhật. Có thể mask bị cắt theo bounding box, nhưng chưa kiểm tra (NOT_VERIFIED).
- **Dự đoán không khớp (màu tím) tập trung ở mép ảnh và là các mảng nhỏ.** Trong 3 hình, các mảng tím chủ yếu nằm sát mép khung hình hoặc là mảng nhỏ chen giữa các mũ nấm. Ở hình `most_unmatched`, bảng GT còn để lộ vài nấm trắng nhỏ không được phủ xanh, nên một số dự đoán tím có thể rơi vào những nấm nhỏ chưa được gán nhãn. Điều này chưa được xác nhận bằng cách so từng dự đoán với ảnh gốc.
- **GT không khớp (màu vàng) rất ít và nằm ở mép ảnh.** Trong cả 3 hình chỉ thấy vài đa giác vàng nhỏ sát mép khung hình, có vẻ là nấm bị cắt ngang bởi khung ảnh.

## 4. Kết luận
- Với các object ghép được, diện tích dự đoán sát GT: sai số trung vị 7,3%, MAE 207 px² (khoảng 5,8% diện tích GT trung bình), mask IoU trung bình 0,89.
- Model **ước lượng diện tích hơi cao hơn** GT (khoảng +4,5% trên cặp ghép, +6,2% trên toàn ảnh). Mức này nhất quán ở cả 30 ảnh theo tỉ số tổng diện tích. Thiên lệch dương đến từ nấm nhỏ, vừa và lớn (dưới phân vị 90 của diện tích GT); với 10% nấm lớn nhất, sai số có dấu trung bình gần 0 hoặc âm (−21 px² và −144 px²).
- Sai số tương đối lớn hơn nhiều ở object nhỏ (15,2%) so với object lớn (3,4%).
- Số object không khớp nhỏ nhưng không bằng 0 (246 dự đoán, 70 GT); đây là phần ảnh hưởng đến diện tích tổng cần đọc cùng với MAE, vì MAE không tính chúng.

## 5. Hạn chế
- Mẫu chỉ có 30 ảnh (4.970 GT), đây là kiểm tra phép đo, không phải đánh giá tổng quát cho mô hình.
- GT là polygon COCO được raster hóa, không phải mask chính xác từng pixel; xu hướng dự đoán lớn hơn có thể đến từ cách gán nhãn polygon, từ mô hình, hoặc từ cả hai, và đợt đo này chưa tách được hai nguyên nhân.
- Kết quả phụ thuộc vào các tham số inference cố định (`conf=0,25`, NMS IoU 0,7, `imgsz=640`, `retina_masks=True`); đổi chúng sẽ đổi số object và có thể đổi diện tích mask.
- Diện tích tính bằng px², không quy đổi sang mm² và không nói gì về chất lượng nấm.
- Nhận xét ở mục 3 dựa trên 4 hình được xem, không phải toàn bộ 30 ảnh; các nguyên nhân nêu ở đó chưa được kiểm chứng.
- Thiết bị dùng khi inference không được ghi trong summary (`device: None`, để Ultralytics tự chọn); `pycocotools` hiện `NOT_VERIFIED` ở mục phiên bản vì thư viện này không có thuộc tính `__version__`, nhưng nó đã được dùng để raster GT và tính IoU.
- Tổng diện tích mỗi ảnh là tổng diện tích từng instance, chưa loại phần chồng nhau.
