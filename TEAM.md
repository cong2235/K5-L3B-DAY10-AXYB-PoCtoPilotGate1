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

Kỹ sư cổng (cùng Lam), phần **đo, trace và chỉ số theo dõi** ở vòng 1: câu 2.1, 2.2 (Phiếu B mục B0, B1, B2), lý do kỹ thuật của pre-mortem câu 2.5 (B6), đo kiểm cổng vòng 1 và config trên bộ nền, chốt cổng vòng 1 và đo mốc prepared (B0 dòng 3–4, số liệu cho B8); PIC dòng 1 (Chất lượng) và dòng 4 (Quyền hạn) của checklist B5. File: `lab10/monitors.py`, `templates/form-b-evaluation-gates.md`.

### Đóng góp cụ thể

- Chạy mốc base ngay sau khi tiêu chí đã ký, đọc gate, khối kinh doanh/vận hành và khối theo kho/hãng; viết lý lẽ tự chặn / người duyệt và khuyến nghị "kết hợp" (B1).
- Dò trace `T-002@55`, điền bảng soát lỗi 2 lỗi chìm: hoàn 20.000đ theo số khách khai 5 ngày (DB 2 ngày) và ghi lỗi oan cho hãng VNX (B2).
- Viết 12 chỉ số mới trong `lab10/monitors.py` (`model_override_rate`, `instruction_obeyed_rate`, `llm_degraded_rate`, `fail_open_refund_rate`, `duplicate_refund_rate`, `merchant_payer_rate`, `fault_without_recorded_cause_rate`, `fault_not_delayed_parcel_rate`, `carrier_pii_rate`, `refund_vnd_per_ticket`, `cost_vnd_per_ticket`, `queue_stuck_rate`), chỉ đọc trace / sổ cái / tin gửi đi, không đọc nhãn. Viết từ vòng 1, trước khi biết thẻ; ở thẻ S7, `carrier_pii_rate` sáng đèn ngay ở mốc base (0.625) và được dùng trong Phiếu C (C2, C8, C11).
- Viết hai lý do kỹ thuật "(Đạt) ★" cho pre-mortem (B6): model tin số khách khai; lỗi 429 dẫn tới hoàn fail-open và hoàn trùng. Cả hai thành cổng 2 và 3 ở B7.1.
- Đo lại bộ nền sau cổng vòng 1 của Lam (110/110 đạt, không regression) và sau khi Công điền `config/operating_gates.json` (kiểm config hợp lệ, 110/110 đạt, không vượt trần).
- Chạy `lab10.checkpoint` chốt cổng vòng 1 (hash `ccbbeabb`), đo mốc prepared, điền B0 dòng 3–4 và chuyển mã lần chạy, kho/hãng xấu nhất cho Công điền B8.
- Phát hiện và xử lý lỗi hash tiêu chí lệch trên Windows do Git tự đổi LF→CRLF (`core.autocrlf false`).

### Bằng chứng

- Commit: `e08eb6c` (monitors + B0, B1, B2), `c49463a` (cập nhật B1 theo tiêu chí ký lại), `76d429d` (B6 + mục cá nhân), `34fc2f3` (chốt cổng vòng 1, mốc prepared, B0 dòng 3–4), `62134db` (cập nhật mục cá nhân).
- Lần chạy: `runs/R-base-before-20261119-161459-3971c5` (base · base), `runs/R-base-after-20261119-164605-997c3c` (base · after, cổng vòng 1), `runs/R-base-after-20261119-171411-cf1775` (base · after, cổng + config), `runs/R-base-prepared-20261119-171512-cf1775` (base · prepared).
- Phiếu B: B0 dòng 1, 3, 4; B1; B2; hai dòng "(Đạt) ★" ở B6; B5 dòng 1. Phiếu C: `carrier_pii_rate` ở C2, C8, C11.
- Còn mở: B5 dòng 4 (Quyền hạn) ghi "Chưa", chưa thử tắt thao tác ghi bằng `config/switches.json`.

**Dùng AI:** dùng Claude (Claude Code) để đọc code agent, chạy lệnh đo/trace/checkpoint, gợi ý chỉ số theo dõi và nháp câu chữ cho B1, B2, B6; đã đọc lại và đối chiếu với output thật.

### Exit ticket

- Học được: một lỗi chìm như `T-002@55` chỉ chiếm 1/110 trial nhưng đủ làm trượt ngưỡng an toàn; pass_rate cao không nói lên thiệt hại cho bên thứ ba, phải đo riêng tiền hoàn sai và lỗi oan.
- Còn chưa chắc: chỉ số chỉ đọc kết quả đã ghi (như `carrier_pii_rate`, `model_override_rate`) sẽ về 0 hoặc đứng yên khi cổng chặn đúng, nên không cho thấy áp lực đang đè lên cổng; cần thêm chỉ số đo "lần thử" như `carrier_notice_pii_attempt_rate` của vòng 2.

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
