# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): AXYB
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-AXYB-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S7

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Võ Trần Công | 2A202604026 |     Sản phẩm và kinh doanh| ✔ |
|   2 |           Trần Huy Bảo|2A202604021      |     Vận hành và pháp lý|             |
|   3 |           Hà Văn Khánh Đạt|     2A202604074 |Kỹ sư cổng     |             |
|   4 |           Nguyễn Đức Khương Lam |      2A202604020|     Kỹ sư cổng|             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HaVanKhanhDat-2A202604074

### Phần việc phụ trách

Kỹ sư cổng (cùng Lam), phần **đo, trace và chỉ số theo dõi**: câu 2.1, 2.2 (Phiếu B mục B0, B1, B2), lý do kỹ thuật của pre-mortem câu 2.5 (B6), đo kiểm cổng vòng 1 trên bộ nền; vòng 2: câu 3.0, 3.1 (C0, C2) và câu 3.6 chỉ số theo dõi (C8). File: `lab10/monitors.py`, `templates/form-b-evaluation-gates.md`.

### Đóng góp cụ thể

- Chạy mốc base sau khi tiêu chí đã ký, đọc gate và khối kinh doanh/vận hành, theo kho/hãng; viết lý lẽ tự chặn / người duyệt và khuyến nghị "kết hợp" (B1).
- Dò trace `T-002@55`, điền bảng soát lỗi 2 lỗi chìm: hoàn 20.000đ theo số khách khai 5 ngày (DB 2 ngày) và ghi lỗi oan cho hãng VNX (B2).
- Viết 12 chỉ số mới trong `lab10/monitors.py` (`model_override_rate`, `instruction_obeyed_rate`, `llm_degraded_rate`, `fail_open_refund_rate`, `duplicate_refund_rate`, `merchant_payer_rate`, `fault_without_recorded_cause_rate`, `fault_not_delayed_parcel_rate`, `carrier_pii_rate`, `refund_vnd_per_ticket`, `cost_vnd_per_ticket`, `queue_stuck_rate`), chỉ đọc trace / sổ cái / tin gửi đi, không đọc nhãn.
- Đo lại bộ nền với cổng vòng 1 của Lam: 110/110 đạt, không regression.
- Phát hiện và xử lý lỗi hash tiêu chí lệch trên Windows do Git tự đổi LF→CRLF (`core.autocrlf false`).

### Bằng chứng

- Commit: `e08eb6c` (monitors + B0, B1, B2), `c49463a` (cập nhật B1 theo tiêu chí ký lại).
- Lần chạy: `runs/R-base-before-20261119-161459-3971c5` (base · base), `runs/R-base-after-20261119-164605-997c3c` (base · after, cổng vòng 1).
- Phiếu B: B0 dòng 1, B1, B2, hai dòng "(Đạt)" ở B6.

**Dùng AI:** dùng Claude (Claude Code) để đọc code agent, chạy lệnh đo/trace, gợi ý chỉ số theo dõi và nháp câu chữ cho B1, B2, B6; đã đọc lại và đối chiếu với output thật.

### Exit ticket

- Học được: một lỗi chìm như `T-002@55` chỉ chiếm 1/110 trial nhưng đủ làm trượt ngưỡng an toàn; pass_rate cao không nói lên thiệt hại cho bên thứ ba, phải đo riêng tiền hoàn sai và lỗi oan.
- Còn chưa chắc: chỉ số nào trong 12 chỉ số sẽ "sáng đèn" với thẻ sự cố, và `model_override_rate` vẫn 0.045 sau khi có cổng (model vẫn tin số khai, cổng chỉ chặn ở bước ghi), có nên coi là cảnh báo khi pilot không.

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
