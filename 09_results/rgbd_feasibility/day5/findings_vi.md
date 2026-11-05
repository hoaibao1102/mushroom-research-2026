# Day 5 - Có ước lượng được kích thước vật lý của nấm từ ảnh RGB-D M18K V2 không?

## 1. Kết luận
**Hiện tại chưa thể ước lượng diện tích chiếu vật lý (mm²) một cách có hiệu chuẩn.** Dataset thiếu hai thông tin bắt buộc là **đơn vị của depth** và **thông số nội tại của camera (intrinsics)**, và các kiểm tra trên dữ liệu thật còn cho thấy **depth chưa chắc căn chỉnh đúng với RGB/mask** và **không có depth hợp lệ ở một phần các mask**. Vì vậy em dừng ở kết quả khả thi (feasibility): diện tích vẫn giữ ở **px²**, em không tính và không báo cáo mm². Một con số mm² tính khi chưa hiệu chuẩn thì không phải một phép đo vật lý hợp lệ.

## 2. Bằng chứng về hiệu chuẩn

| yêu cầu | tình trạng | bằng chứng |
|---|---|---|
| Camera | Intel RealSense D405 (chỉ từ bài báo, chưa kiểm chứng trên dữ liệu) | bài báo M18K V2 (Computers 2025) và bản V1 trên arXiv |
| Độ phân giải RGB và depth | **Đã kiểm chứng** | bài báo ghi 1280×720; 30/30 ảnh được kiểm tra có depth 720×1280, bằng kích thước RGB và COCO |
| Căn chỉnh RGB-depth | **NOT_VERIFIED** | bài báo nói không cần căn chỉnh, nhưng chưa có tài liệu hay kiểm tra độc lập; phép thử của em gợi ý có lệch (mục 5) |
| Đơn vị depth | **NOT_VERIFIED** | không có tài liệu đi kèm dữ liệu; giá trị thô không khớp giả thuyết 1 mm (mục 6) |
| Intrinsics (fx, fy, cx, cy, méo ảnh) | **Không tìm thấy** | 0 dòng nhắc intrinsics/depth scale/calibration trong file đi kèm; các khóa trong COCO JSON chỉ là `id, license, file_name, height, width, date_captured` (ảnh) và `id, image_id, category_id, bbox, area, segmentation, iscrowd` (annotation); phần văn bản bài báo em đọc cũng không nêu |
| Nguồn gốc file depth | **Chưa rõ** | file depth là `.npy`; trong 450 file depth của split test, **340 file là `float32` và 110 file là `uint16`** (kiểu dữ liệu không đồng nhất); trường `info` của COCO ghi "Auto-labeled with Ultralytics YOLO segmentation (shuffled+renamed)" và ngày tạo 2025-11-08, nên đây có vẻ là một bản xuất lại đã xử lý, chưa có tài liệu liên kết với dữ liệu cảm biến gốc |

Cấu trúc dữ liệu kiểm tra: mỗi split (`train`, `valid`, `test`) có `rgb/` (PNG), `depth/` (NPY, mỗi ảnh một file cùng tên), `labels/` (TXT) và `annotations_coco.json`; không có README, file calibration hay file metadata camera nào.

## 3. Phương pháp kiểm tra
Script `depth_area.py` chạy trên 30 ảnh test (chọn theo seed 42, cùng quy tắc với các đợt trước), tức 4.970 mask WB (polygon COCO được raster hóa ở độ phân giải gốc, diện tích tính bằng đúng công thức `sum(mask > 0)` đã kiểm chứng). Với mỗi mask, em đếm tỉ lệ pixel có depth > 0, thống kê giá trị depth thô, so sánh với cấu hình camera danh nghĩa, và thử độ căn chỉnh depth với biên mask. Chỉ có kết quả đã chạy mới được ghi ở đây. Việc kiểm tra kiểu dữ liệu được chạy trên cả 450 file depth của split test.

## 4. Depth hợp lệ trong mask WB
- Trong 4.970 mask: tỉ lệ pixel depth hợp lệ trung bình 0,931, trung vị 0,998, phân vị 5% là 0,263.
- **301 mask (6,1%) có dưới 50% pixel hợp lệ; 452 mask (9,1%) dưới 90%; 132 mask (2,7%) không có pixel depth hợp lệ nào.**
- Toàn ảnh có khoảng 4,8–6,4% pixel bằng 0 (5 ảnh đầu).
- Hình `depth_validity_summary.png`: biểu đồ độ hợp lệ theo từng mask (trục y log) có một đỉnh rất cao gần 1,0 (khoảng 4.000 mask) và một đỉnh nhỏ ở 0 (khoảng 150 mask ở bin đầu), với phần đuôi thấp, phẳng ở giữa. Biểu đồ giá trị depth gộp trong mask có trục x kéo đến khoảng 45.000–47.000 trong khi phân vị 99% là 2.781, tức có một số pixel trong mask mang giá trị lớn gấp khoảng 15 lần giá trị điển hình; trong 17.481.201 pixel của các mask chỉ có 588 pixel (0,0034%) có giá trị lớn hơn 5000 (ngưỡng chọn tùy ý), nên giá trị ngoại lai rất hiếm nhưng có tồn tại.
- Hình `typical_004103.png` và `lowest_depth_validity_004058.png`: ở cả hai ảnh, pixel depth bằng 0 (màu đỏ) chủ yếu là một dải dọc sát mép trái ảnh; tỉ lệ 4,8–6,4% pixel bằng 0 phù hợp với một dải như vậy. Ảnh `004058` còn có vài đốm depth bằng 0 nhỏ trên một số mũ nấm ở nửa phải. Kiểm tra bổ sung trên 30 ảnh (`extra_checks.py`): dải mép trái không có depth rộng trung vị 49 px (từ 0 đến 61 px, khoảng 3,8% bề rộng 1280 px). Trong 301 mask có dưới 50% pixel hợp lệ, **199 mask (66%) có tâm nằm ở 10% bề rộng bên trái, 102 mask (34%) có tâm nằm ở 10% bề rộng bên phải, và không mask nào ở khoảng giữa (10–90%)**. Vậy việc thiếu depth trong mask là hiệu ứng ở mép ảnh: bên trái khớp với dải đã thấy trong hình, còn nguyên nhân ở mép phải em chưa xem. Mọi mask có tâm ở khoảng giữa đều có ít nhất 50% pixel hợp lệ.
- Vậy phần lớn mask có depth dùng được; nếu sau này có hiệu chuẩn, một quy tắc đơn giản là loại hoặc đánh dấu các mask sát mép trái và mép phải, và việc đó cần được nêu rõ.

## 5. Căn chỉnh RGB và depth
Em dùng hai phép thử, đều dịch bản đồ depth trong khoảng ±16–24 px và tìm vị trí cho độ tương hợp cao nhất. Nếu RGB, mask và depth thẳng hàng thì đỉnh phải ở dịch (0, 0).
- **Phép thử 1 (dùng biên mask):** gradient của depth tại biên mask, trên 30 ảnh. Tỉ số so với trung bình ảnh ở dịch 0 là 1,30 (trung bình), thấp nhất 0,45. Không ảnh nào có đỉnh ở (0, 0). Trong 18 ảnh thuộc 8 nhóm dịch phổ biến nhất, 16 ảnh có đỉnh ở dx từ +4 đến +10 px (riêng dx = +8 có 11 ảnh) và 2 ảnh ở dx = −10.
- **Phép thử 2 (không dùng mask):** tương quan giữa gradient của ảnh xám RGB và gradient của depth, trên cùng 30 ảnh. Trong 18 ảnh thuộc 10 nhóm dịch phổ biến nhất, không nhóm nào là (0, 0); 13 ảnh có đỉnh ở dx từ +6 đến +10 px và 5 ảnh ở dx từ −10 đến −8 px (dịch dọc dy từ −6 đến +4 px).
- Hai phép thử cho kết quả cùng chiều (không có đỉnh ở (0, 0), độ lớn dịch khoảng 6–10 px), nhưng **dấu của dịch không nhất quán** (một số ảnh dương, một số âm). Bản đồ nhiệt trong `typical_004103.png` cho thấy đỉnh rất rộng (độ tương hợp giảm chậm trong khoảng vài chục px), tức phép thử có độ phân giải thấp so với độ lớn dịch cần phát hiện.
- Kết luận: **không thể khẳng định depth thẳng hàng với RGB**, và cũng không thể khẳng định lệch một lượng cố định. Căn chỉnh vẫn là **NOT_VERIFIED**. Để biết chắc cần tài liệu về căn chỉnh (hoặc ngoại tham số depth-sang-màu).

## 6. Đơn vị depth (kiểm tra mức hợp lý, không phải xác minh)
Giá trị depth thô trong mask WB có phân vị 1/5/50/95/99% lần lượt là 2044 / 2141 / 2399 / 2676 / 2781.
- Nếu đơn vị là **1 mm**: độ sâu trung vị là 2,4 m. Điều này mâu thuẫn với cấu hình ghi trong bài báo (camera cách luống nấm WB khoảng 15 cm) và với khoảng cách làm việc gần của D405, nên giả thuyết này rất khó đúng.
- Nếu đơn vị là **0,1 mm**: trung vị là 240 mm (24 cm). Hình học tương đối cũng hợp lý hơn: trong `lowest_depth_validity_004058.png` mũ nấm hiện màu gần hơn mặt luống khoảng 300 đơn vị thô (đọc từ thang màu), tức cỡ 3 cm nếu đơn vị 0,1 mm (hợp lý với chiều cao mũ nấm) nhưng cỡ 30 cm nếu đơn vị 1 mm (không hợp lý). Tuy vậy trung vị 24 cm **vẫn lớn hơn khoảng 90 mm** so với 15 cm danh nghĩa, trong khi mũ nấm nằm cao hơn mặt luống nên lẽ ra phải gần camera hơn. Em không giải thích được chênh lệch này.
- Vì vậy đơn vị depth là **NOT_VERIFIED**; giả thuyết 0,1 mm hợp lý hơn nhưng chưa được chứng minh, và các giá trị depth em báo cáo luôn là "đơn vị thô của file".

## 7. Quyết định và thông tin cần bổ sung
Em không cài đặt bộ ước lượng mm² vì điều kiện hiệu chuẩn chưa đạt. Để có diện tích chiếu vật lý cần:
1. **Đơn vị depth** (depth scale, tức mét hoặc mm trên mỗi đơn vị giá trị) từ cấu hình RealSense của tác giả hoặc tài liệu dataset, kèm xác nhận kiểu dữ liệu nào (`uint16` hay `float32`) là bản gốc và vì sao hai kiểu cùng tồn tại.
2. **Intrinsics của luồng depth dùng cho ảnh này**: fx, fy, cx, cy (và hệ số méo nếu có), cùng thông tin độ phân giải gốc, có cắt/resize hay không.
3. **Xác nhận depth đã được căn chỉnh với RGB** (hoặc ngoại tham số depth-sang-màu để tự căn chỉnh), và quy tắc xử lý pixel depth bằng 0.
4. **Một phép kiểm chứng độc lập**: ví dụ một vật có kích thước đã biết trong ảnh, hoặc vài mũ nấm được đo tay bằng thước.

Nếu đủ các thông tin trên, phương pháp dự kiến là: diện tích chiếu của một pixel ở độ sâu Z là `(Z/fx) × (Z/fy)`, nên với mask M, diện tích chiếu ≈ `Σ_{p∈M, Z_p hợp lệ} Z_p² / (fx·fy)`, quy đổi đúng đơn vị của Z. Đây là diện tích chiếu lên mặt phẳng ảnh, **không phải diện tích bề mặt thật của mũ nấm cong**. Phương pháp này chưa được chạy trên dữ liệu.

## 8. Hạn chế
- Chỉ 30 ảnh test (4.970 mask) được kiểm tra; các số về độ hợp lệ, đơn vị và căn chỉnh có thể thay đổi nếu mở rộng ra cả 450 ảnh và các split khác.
- Phép thử căn chỉnh phụ thuộc vào chất lượng mask; kết quả chỉ là bằng chứng gợi ý.
- Em chưa mở được repo GitHub của dataset (`abdollahzakeri/m18k`), nên chưa biết ở đó có ghi đơn vị depth hay intrinsics không (NOT_VERIFIED). Nếu có, kết luận ở mục 1 có thể thay đổi.
- Các hình trong `figures/` do script tạo ra; findings chỉ mô tả các điểm đọc được trên 3 hình đã xem (`typical_004103`, `lowest_depth_validity_004058`, `depth_validity_summary`).
- Hai phép thử căn chỉnh dùng gradient đã làm mờ và có độ phân giải thấp so với độ lớn dịch (vài đến khoảng 10 px).

## 9. File
`depth_area.py` (kiểm tra chính), `extra_checks.py` (kiểu dữ liệu của 450 file depth, phép thử căn chỉnh không dùng mask, kiểm tra độ hợp lệ theo vị trí; kết quả ở mục 2, 4, 5), `results.csv` (một dòng mỗi ảnh: số mask, tổng diện tích px², thống kê depth thô, độ hợp lệ, kết quả căn chỉnh; cột `wb_area_mm2` ghi `NOT_VERIFIED`), `depth_inspection.json` (toàn bộ kết quả kiểm tra), `figures/`.

Tài liệu tham khảo: Zakeri et al., *M18K: A Comprehensive RGB-D Dataset and Benchmark for Mushroom Detection and Instance Segmentation* (arXiv:2407.11275); Zakeri et al., *M18K: A Multi-Purpose Real-World Dataset for Mushroom Detection, 3D Pose Estimation, and Growth Monitoring*, Computers 2025, 14(5), 199.
