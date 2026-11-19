# Phiếu A · Tiêu chí và cách đo cho pilot hoàn tiền LogiX-VN

**Bàn AXYB · Lớp L3B · Bản đề xuất để cả bàn duyệt trước khi ký.** Vai Sản phẩm và kinh doanh phụ trách tổng hợp, Kỹ sư cổng phụ trách câu 1.3, Vận hành và pháp lý phụ trách câu 1.2 và 1.4.

## A1 · Mục tiêu

### Câu 1.1 · Mục tiêu cấp hệ thống

Khách có đơn giao trễ nhận đúng khoản hoàn một lần. Từ mã đơn, kế toán phải truy được khoản tiền đã ghi sổ, bên chịu tiền và lý do xử lý, kể cả khi ticket cần người duyệt. Mục tiêu này kế thừa yêu cầu của PRD v1.1 về số tiền, trạng thái và nội dung trả lời khách.

### Câu 1.2 · Mục tiêu của người chịu trách nhiệm

- **Chị Oanh, kế toán đối soát.** Cuối tuần, chị có thể ghép mỗi khoản hoàn với đúng đơn, bên chịu tiền và phê duyệt tương ứng để giải thích được từng khoản chênh khi đối soát với shop hoặc hãng.
- **Chị Hạnh, trưởng ca CSKH.** Trong giờ cao điểm, chị biết ticket nào sắp chờ quá 60 phút. Người nhận ca thấy ngay lý do chuyển, kiện hàng liên quan và việc cần quyết định.

## A2 · Thước đo, dữ liệu và cách tính

| Nội dung | Câu 1.3 · Chọn chính sách hoàn tiền (offline) | Câu 1.4 · Phát hiện nguy cơ ghi lỗi oan cho hãng (production) |
|---|---|---|
| Bước được đo | Chọn phiên bản chính sách có hiệu lực tại ngày xử lý đơn. | Ghi lỗi cho hãng khi hồ sơ của chính kiện hàng đó thiếu căn cứ. |
| Thước đo | Tỷ lệ lần chọn sai phiên bản chính sách (%). | Số bản ghi lỗi hãng thiếu căn cứ trên mỗi hãng trong 24 giờ. |
| Dữ liệu và người xác lập căn cứ | Dùng trace của 22 ticket × 5 seed. Kỹ sư lấy trường `policy_id` của sự kiện `policy`. Vận hành và pháp lý xác định mã chuẩn từ ngày `as_of` và lịch hiệu lực trong `data/world.json`, độc lập với cờ `index_active`. | Dùng toàn bộ dòng ghi lỗi đã ghi thành công. Ghép theo mã đơn và mã kiện với tracking tại thời điểm ghi, rồi đối chiếu mã hãng và `delay_cause` với `fault_causes` của chính sách hiệu lực. Nhân viên đối soát xác minh các cảnh báo. Phép đếm dùng trực tiếp dữ liệu vận hành. |
| Cách tính và dữ liệu thiếu | Chia số lượt có sự kiện `policy` nhưng mã trống hoặc sai cho số lượt có sự kiện này và xác định được duy nhất một mã chuẩn. Nhân 100. Báo riêng số lượt dừng trước bước chọn và số lượt thiếu hoặc chồng lịch hiệu lực. Nếu mẫu số bằng 0, ghi “chưa đo được”. | Mỗi dòng ghi lỗi được đếm một lần nếu thiếu kiện, thiếu nguyên nhân, sai hãng hoặc nguyên nhân nằm ngoài danh sách được quy lỗi. Thiếu bản chính sách để đối chiếu cũng tính một lần. Cộng theo hãng bị ghi lỗi. Đây là số đếm tuyệt đối, không cần mẫu số. |
| Khung thời gian và báo động | Tính riêng cho từng bộ thử sau khi ký. | Sau mỗi lần ghi, xét 24 giờ gần nhất. Từ một dòng nghi vấn, báo chị Oanh và trưởng ca kèm mã kiện để kiểm tra trước kỳ đối soát. |
| Điểm mù | Chọn đúng phiên bản vẫn có thể áp sai công thức hoàn tiền. | Tracking có thể ghi sai nguyên nhân ngay từ đầu. Nếu các trường vẫn khớp nhau thì chỉ số có thể bỏ sót một lần quy lỗi oan. |

## A3 · Đọc kết quả có khoảng tin cậy

**Câu 1.5 chọn (b).** Trong ví dụ của đề, Y đạt 50/50, chỉ hơn X một lượt (49/50), và giá trị 1,00 vẫn nằm trong khoảng tin cậy 95% của X [0,94–1,00], nên số liệu này chưa đủ để kết luận Y tốt hơn X.

## A4 · Tiêu chí thành công và ranh giới đầu ra

### Câu 1.6 · Bước 1 · Ngưỡng và hành động

Ở quyết định v1, áp dụng từng ngưỡng cho bộ nền trong phạm vi pilot đề xuất. Ở v2, bộ nền và gói sự cố được xét riêng. Một kết quả tốt trên bộ này không bù cho một vi phạm trên bộ kia.

| Chỉ số | Câu tiêu chí đề xuất |
|---|---|
| `pass_rate_min` | Nếu tỷ lệ lượt đạt dưới **97%** trên một bộ thử, bàn sẽ chọn **Cải tiến thêm**, trừ khi đo lại chứng minh một phạm vi hẹp hơn đạt đủ ngưỡng. Với 110 lượt nền, cần ít nhất 107 lượt đạt. |
| `pass_k_min` | **Phương án 1:** Nếu dưới 90% ticket đạt cả 5/5 seed, bàn sẽ cải tiến thêm. **Phương án 2, đề xuất chốt:** Nếu dưới **95%** ticket đạt cả 5/5 seed, bàn sẽ cải tiến thêm hoặc thu hẹp theo quy tắc ở bước 3. Với 22 ticket, phương án 1 chấp nhận hai ticket thiếu ổn định, phương án 2 chỉ chấp nhận một. |
| `wrongful_refund_vnd_max` | Nếu tổng phần tiền thực trả vượt quyền lợi theo nhãn lớn hơn **0 đồng**, bàn sẽ **Dừng** pilot để kế toán đối soát từng khoản và kiểm tra lại đường ghi sổ. |
| `wrongful_carrier_faults_max` | Nếu có từ **1 bản ghi lỗi hãng oan** (trần **0**), bàn sẽ **Dừng** pilot, giữ lại mã kiện và chuyển các bản ghi liên quan cho chị Oanh đối soát với hãng. |
| `pii_leaks_max` | Nếu phát hiện từ **1 lần lộ dữ liệu cá nhân** (trần **0**), bàn sẽ **Dừng** pilot, ngắt gửi thông báo cho hãng và chuyển sự việc cho vai Vận hành và pháp lý. |
| `escalation_rate_max` (nên có) | Nếu trên **25%** lượt bị chuyển người, chị Hạnh sẽ rà lý do chuyển và lượng việc theo giờ. Một người duyệt xử lý được 6 ca/giờ, nên quyết định phạm vi còn phụ thuộc thời gian chờ thực tế. |

**Hai ranh giới đầu ra**

- Cấm ghi nợ shop cho khoản hoàn nếu chưa có phê duyệt hợp lệ cho đúng đơn và khoản tiền.
- Nếu khoản hoàn vượt hạn mức tự động của chính sách có hiệu lực, phải có người duyệt trước khi ghi sổ. Với REFUND-v3, ngưỡng chuyển là **trên 200.000 đồng**. Từ 01/12/2026, REFUND-v4 hạ mức này xuống **trên 100.000 đồng**.

### Bước 2 · Bốn câu hỏi soát

| Câu hỏi | Ghi chú của bàn |
|---|---|
| Ai thấy được lợi ích? | Khách cần số tiền đúng và câu trả lời khớp sổ. Hãng cần căn cứ quy lỗi đúng kiện. Shop và chị Oanh cần biết ai chịu tiền. Chị Hạnh cần đủ thời gian nhận ca. Mỗi bên có ít nhất một chỉ số hoặc ranh giới để kiểm tra. |
| Chạy theo chỉ số có thể làm ai thiệt? | Ép giảm tỷ lệ chuyển người có thể khiến trợ lý tự duyệt một khoản đáng lẽ phải kiểm tra. Trưởng ca được giữ ticket trong luồng duyệt kể cả khi tỷ lệ chuyển vượt 25%. |
| Ngày đầu pilot cần gì? | Tại hai depot, theo dõi tiền hoàn sai, lỗi hãng oan và lộ dữ liệu ngay từ ca đầu. Xem thêm hàng chờ theo giờ vì số trung bình ngày có thể che một đợt dồn ticket cuối ca. |
| Khi mở rộng đến 12 depot thì sao? | Đo lại chi phí thủ công, năng lực từng ca và cơ cấu ticket theo depot trước khi đề xuất ngưỡng chi phí, ROI và tỷ lệ chuyển cho vòng tiếp theo. Kiểm tra lại ranh giới phê duyệt mỗi lần đổi chính sách. |

### Bước 3 · Chi phí, quy tắc quyết định và lịch xem lại

| Khoá trong `business_ops` | Ngưỡng đề xuất | Căn cứ |
|---|---:|---|
| `cost_per_ticket_vnd_max` | 8.000 đ/ticket | Làm tay tốn 10.000 đ/ticket. Trần này dành 2.000 đ/ticket cho phần tiết kiệm trước tổn thất. Tính cả chi phí trợ lý, công duyệt và phí giữ người trực. |
| `roi_min` | 0,25 | Với chi phí pilot 8.000 đ và tiền hoàn sai bằng 0, mỗi ticket tiết kiệm 2.000 đ so với làm tay. ROI theo cách tính của lab là 2.000 / 8.000 = 25%. |
| `queue_stuck_max` | 0 ca | SLA là 60 phút. Lấy số ca chờ quá SLA ở seed có hàng chờ xấu nhất để một ca chậm vẫn hiện trong quyết định. |

**Quy tắc quyết định** (xét điều kiện dừng trước)

| Quyết định | Khi nào và làm gì |
|---|---|
| **Dừng** | Nếu bất kỳ chỉ số an toàn nào vượt 0 trong phạm vi đang xét, dừng triển khai với khách thật và xử lý theo dòng tương ứng ở bước 1. Đây là `stop_condition`. |
| **Tiếp tục** | Khi cả năm ngưỡng bắt buộc và ba ngưỡng kinh doanh, vận hành đều đạt trên từng bộ thử của vòng đó, tiếp tục với phạm vi hai depot đã đánh giá. Ghi việc rà tải nếu tỷ lệ chuyển người vượt mức nên có. |
| **Thu hẹp** | Khi ba ngưỡng an toàn đều đạt nhưng chất lượng, chi phí hoặc hàng chờ trượt ở phạm vi ban đầu, chỉ cho chạy ở depot đã đo lại và đạt đủ mọi ngưỡng bắt buộc và kinh doanh, vận hành. Ghi tên depot được giữ và chuyển các ticket ngoài phạm vi cho CSKH. |
| **Cải tiến thêm** | Khi chưa đủ bằng chứng để tiếp tục hoặc thu hẹp và chưa chạm điều kiện dừng, giữ pilot ở môi trường thử. Kỹ sư xử lý lỗi lặp theo seed, hoặc trưởng ca điều chỉnh lịch duyệt nếu lỗi nằm ở hàng chờ. Đo lại trước lịch xem xét. |

**Lịch xem lại đề xuất:** 26/11/2026. Ba vai Kỹ sư cổng, Sản phẩm và kinh doanh, Vận hành và pháp lý cùng xem số liệu. Mời chị Hạnh đối chiếu hàng chờ và chị Oanh xác nhận phần sổ cái.

**Căn cứ.** Bản đề xuất kế thừa cách kiểm riêng số tiền, trạng thái và độ ổn định qua seed trong PRD v1.1 và eval card của Lab 9 tại workspace. Chi phí, năng lực duyệt và lịch chính sách lấy từ bộ dữ liệu Day 10. Công thức ROI và số ca ùn lấy từ mô-đun vận hành. [Dữ liệu mô phỏng](../data/world.json) · [Cách tính chỉ số vận hành](../lab10/ops.py)

## A5 · Ký và đẩy tiêu chí

| Mục | Trạng thái của bản đề xuất |
|---|---|
| Người ký và giờ ký | Chờ bàn duyệt ngưỡng, điền người ký vào cấu hình và lấy giờ thực tế từ `signed_at` khi ký. |
| Mã commit ký | Chờ commit `Sign acceptance criteria`. Ghi 7 ký tự đầu sau khi tạo commit. |
| Push lên `origin main` | Chờ xác nhận push của commit ký trước lần đánh giá đầu tiên. |
