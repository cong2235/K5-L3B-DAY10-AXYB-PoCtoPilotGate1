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
|   2 |           Từ Huy Bảo|2A202604021      |     Vận hành và pháp lý|             |
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

## VoTranCong-2A202604026

### Phần việc phụ trách

Trưởng nhóm, vai **Sản phẩm và kinh doanh**. Vòng 1: tiêu chí và ký (câu 1.1–1.6, Phiếu A mục A1–A5, `config/acceptance_criteria.json`), bản đồ dữ liệu và ví dụ drift (câu 2.3, B3), lăng kính kinh doanh của pre-mortem (B6), cổng kinh doanh (câu 2.9, B7.4, mục `business` trong `config/operating_gates.json`), quyết định v1 (B8). Vòng 2: quyết định v2 và ba dòng bắt buộc (C12), gom `submission/`. File: `config/acceptance_criteria.json`, `config/operating_gates.json` (cả mục `operations`, `legal` điền cùng Bảo), `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`.

### Đóng góp cụ thể

- Điền Phiếu A: mục tiêu hệ thống (1.1), thước đo và telemetry (1.3, 1.4), đọc khoảng tin cậy (chọn đáp án (b) ở 1.5), sáu câu tiêu chí "Nếu … thì chúng tôi sẽ …", hai câu ranh giới đầu ra, bốn câu soát và ba ngưỡng `business_ops` (8.000 đ/ticket, ROI ≥ 0,25, 0 ca ùn). Các số lấy từ `data/world.json` (`ops_facts`, `ops_limits`), không chép từ file example.
- Điền `config/acceptance_criteria.json`, chạy `lab10.criteria sign` và push trước lần `eval` đầu tiên (`1ef78f7`). Sau đó bàn đổi ngưỡng `pass_rate_min` và `pass_k_min` rồi ký lại (`cfa378f`); đã hỏi Lab Coach và ghi lý do vào commit `b68d08b`.
- Chạy baseline sau khi ký (`R-base-before-20261119-164917-3971c5`), đối chiếu từng ngưỡng đã ký với kết quả `lab10.gate` và ghi bảng so sánh ở B1: hai chỉ số an toàn chưa đạt (hoàn sai 20.000 đ, lỗi hãng oan 1), cả hai từ một trial `T-002@55`.
- Điền `config/operating_gates.json` (trần hoàn 1.000.000 đ/ngày, ngân sách LLM 1.500 đ/ticket, ROI ≥ 0,25, PIC NV-TUNG, người duyệt NV-HANH, 1 người trực, 6 ca/giờ, chờ tối đa 60 phút, chặn `customer_note`, `recipient_contact`), kiểm lại bộ nền sau khi điền (`R-base-after-20261119-170317-cf1775`: 110/110 đạt, không vượt trần), rồi điền B7.4 kèm lý do có số.
- Soạn runbook 1–3 và mục giờ cao điểm (B7.5, B7.6) khớp các con số trong config, để Bảo rà lại.
- Viết quyết định v1 ở B8 và quyết định v2 ở C12: **Cải tiến thêm** cho cả hai, dựa trên mã lần chạy và nhánh `decision_rule` đã ký; ghi rõ vì sao không chọn Tiếp tục dù ngưỡng đạt (chưa đo riêng phạm vi hai depot, còn nhánh hở ở fault tree).

### Bằng chứng

- Commit: `b5f28b3`, `68d6fb2` (Phiếu A), `1ef78f7` (ký lần đầu), `cfa378f` (ký lại), `b68d08b` (ghi chú lý do ngưỡng, đề xuất cho Lab Coach), `ea97861` (điền `operating_gates.json`), `5090dcb` và `f9601ae` (B3–B6, quyết định v1), `2bf1284` (C12 v2, `submission/`).
- Lần chạy: `R-base-before-20261119-164917-3971c5` (base), `R-base-after-20261119-170317-cf1775` (after, config đã điền), `R-S7-grade-20261119-173057-cf1775` (tự kiểm tra thẻ S7 trước khi sửa).
- Phiếu: A (A1–A5), B1 (bảng so ngưỡng), B3, B7.4, B7.5–B7.6, B8 cột v1, C12 cột v2.
- Còn mở: lịch sử git có hai commit ký tiêu chí (`1ef78f7`, `cfa378f`), nên hàm kiểm lịch sử của lab báo "đã bị commit thêm sau commit ký"; Lab Coach trả lời chỉ kiểm tra đã ký hay chưa nhưng bàn chưa có xác nhận bằng văn bản.

**Dùng AI:** dùng Claude (Claude Code) để đọc code và `data/world.json`, đề xuất ngưỡng và cách viết cho Phiếu A, nháp B7.4, runbook 1–3 và giờ cao điểm, chạy lệnh đo và đối chiếu kết quả, xử lý conflict khi merge. Tôi đã đọc lại, đối chiếu với output thật của `lab10.eval` / `lab10.gate` và chốt các con số; không dùng AI để viết code xử lý riêng theo mã ticket.

### Exit ticket

- Học được: ngưỡng phải viết trước khi đo và giữ nguyên, nếu không dấu vết git và nhật ký lần chạy sẽ phản bội chính bàn; tôi đã phải ký lại một lần và mất thời gian giải thích. Ngoài ra một chỉ số tốt như pass_rate 0,99 có thể che một trial gây thiệt hại thật (hoàn sai, lỗi hãng oan), nên ba ngưỡng an toàn phải đặt riêng bằng 0.
- Còn chưa chắc: ngưỡng chuyển người 0,25 và trần 1.000.000 đ/ngày được chọn từ dữ liệu giả, chưa biết có đúng khi ticket tăng gấp ba hoặc khi chính sách đổi sang REFUND-v4 (hạn mức tự động hạ còn 100.000 đ); và chưa đo riêng phạm vi hai depot nên chưa dám chọn Tiếp tục.

## NguyenDucKhuongLam-2A202604020

### Phần việc phụ trách

Kỹ sư cổng (cùng Đạt), phần **code cổng phòng ngừa và kiểm thử hành vi**: cùng cả bàn thảo luận tiêu chí ở Khối 1 (CP1–CP2), viết 3 cổng phòng ngừa vòng 1 trong `lab10/guards.py` (chốt thành `lab10/guards_round1.py`), lý do kỹ thuật và pháp lý của pre-mortem câu 2.5 (B6), điền Phiếu B mục B0 dòng 2 và B7.1–B7.3 (câu 2.6–2.8); PIC dòng 3 (Bảo mật) và dòng 5 (Hiệu năng, hạ tầng) của checklist B5, PIC dòng 3 (Bảo mật) ở C11; kiểm chứng lại bản sửa vòng 2 trên thẻ S7. File: `lab10/guards.py`, `lab10/guards_round1.py`, `templates/form-b-evaluation-gates.md`.

### Đóng góp cụ thể

- Cài đặt môi trường, kiểm tra bộ test công khai (`unittest` 13/13 OK) và cùng cả bàn thảo luận tiêu chí, nguồn dữ liệu ở Khối 1 (trưởng nhóm tổng hợp vào Phiếu A và ký `config/acceptance_criteria.json`).
- Viết hai lý do "(Lam) ★" cho pre-mortem (B6): lăng kính Kỹ thuật (đổi chính sách sang `REFUND-v4` ngày 01/12/2026 khi cờ `index_active` chưa chuyển) và lăng kính Pháp lý (đơn quà tặng `is_gift: true` và `customer_note` lộ dữ liệu người nhận sang hãng). Hai lý do này thành cổng 1 và cổng 3b ở B7.1.
- Viết 3 cổng phòng ngừa vòng 1 trong `lab10/guards.py` (được chốt thành `lab10/guards_round1.py`, hash `ccbbeabb`), đối chiếu trực tiếp nguồn sự thật DB: `pre_guard` ghim chính sách hiệu lực theo `as_of`; `_gate_issue_refund` chặn hoàn trùng theo `ledger_rows`, không ghi khi `fail_open`, tính lại tiền hoàn từ tracking DB và giữ `payer = "LOGIX"`, kiểm phê duyệt và trần mỗi khách/ngày; `_gate_file_carrier_fault` và `_gate_notify_carrier` kiểm `carrier_at_fault` trên đúng kiện trễ và lọc tin gửi hãng về đúng 4 trường trong `carrier_notice_fields`.
- Đo lại bộ nền sau khi dựng cổng vòng 1 (`R-base-after-20261119-164356-997c3c`): 110/110 trial đạt (`pass_rate` 1.0, `pass_k` 1.0, hoàn sai 0đ, lỗi hãng oan 0, lộ PII 0, 9/9 ngưỡng `[ĐẠT]`), không regression, `unittest` 13/13 OK; kiểm thêm các ca biên ngoài bộ mẫu (đổi ngày sang `REFUND-v4`, lỗi 429 retry/fail-open, phê duyệt sai ticket, đơn đa kiện, thiếu `delay_cause`).
- Điền Phiếu B mục B0 dòng 2, B7.1 (bảng 3 cổng), B7.2 (hai bước tránh rò rỉ dữ liệu) và B7.3 (tính chất hành vi và 2 ticket hiểm chạy bằng `--adhoc` trên `O-1002`/`C-02` và `O-1026`/`C-10`).
- Vòng 2 (thẻ S7): cổng vòng 1 (`guards_round1.py`) và dòng "(Lam) ★" ở B6 đã chặn được toàn bộ 30/30 lần lộ dữ liệu người nhận ngay ở mốc prepared (`pass_rate` 0.25 → 1.0, `pii_leaks` 30 → 0, ghi nhận ở C1); sau khi nhóm nâng cấp `_gate_notify_carrier` vòng 2 và thêm monitor, đã rà lại code và chạy kiểm chứng `lab10.grade --incident S7` (PASS-VISIBLE, cả 5 ô kiểm cục bộ đạt, không hỏng bộ nền) cùng `unittest` 13/13 OK.

### Bằng chứng

- Commit: `9c9c99f` (3 cổng vòng 1 trong `lab10/guards.py`, B0 dòng 2, B7.1–B7.3), `f4a84e7` (hai dòng "(Lam) ★" ở B6 và đồng bộ văn phong Phiếu B).
- Lần chạy: `R-base-after-20261119-164356-997c3c` (base · after, cổng vòng 1), `R-S7-grade-20261119-174327-5c7fa5` (kiểm chứng thẻ S7 sau vòng 2); bản chốt `lab10/guards_round1.py` (`ccbbeabb`, mốc prepared trong `submission/runs/R-S7-prepared-20261119-205555-5c7fa5/report.json` đạt 1.0 và 0 lộ PII).
- Phiếu B: B0 dòng 2; B5 dòng 3 (Bảo mật) và dòng 5 (Hiệu năng, hạ tầng); hai dòng "(Lam) ★" ở B6; B7.1, B7.2, B7.3; kế hoạch đo lại ở B8. Phiếu C: C1 (đối chiếu pre-mortem và mốc prepared), C11 dòng 3 (Bảo mật), kế hoạch đo lại ở C12.
- Còn mở: B5 dòng 5 (Hiệu năng, hạ tầng) ghi "Chưa" vì bộ nền chạy MockLLM không có lỗi 429 (`llm_degraded_rate` = 0) và chưa đo tải giờ cao điểm thật; kế hoạch đo lại phạm vi hai depot HN và HCM theo B8/C12 trước 26/11/2026.

**Dùng AI:** dùng Antigravity để đọc code agent, gợi ý cấu trúc cổng trong `lab10/guards.py`, chạy lệnh đo/kiểm thử và rà câu chữ cho B0, B6, B7.1–B7.3. Tôi đã đọc lại, đối chiếu từng nhánh kiểm tra với `data/world.json`, trace và output thật của `lab10.eval` / `lab10.grade`; không viết luật xử lý riêng theo mã ticket hay câu chữ mẫu.

### Exit ticket

- Học được: muốn thực sự ngăn lỗi trước các cách viết mới ở bộ kiểm tra ẩn thì cổng phải dựng lại dữ liệu từ nguồn sự thật DB (như 4 trường gửi hãng ở vòng 2, hay số ngày trễ trong tracking thay vì số khách khai); dò rồi che theo chuỗi chỉ giảm rủi ro và dễ lọt.
- Còn chưa chắc: khi chạy pilot thật, nếu chính dữ liệu đầu nguồn (tracking DB hoặc trường `district` của đơn) bị nhập sai hay đồng bộ trễ thì cổng đọc từ DB vẫn có thể tin nhầm; cần đo thêm độ sạch dữ liệu nguồn và thử tải lỗi 429 thật trước Gate 2.

## TuHuyBao-2A202604021

### Phần việc phụ trách

Vận hành và pháp lý: người viết Runbook phần 1–3 (Phiếu B mục B7.5) và mục Giờ cao điểm (B7.6); PIC dòng 7 (Vận hành) và dòng 8 (Con người, pháp lý) của checklist B5 và C11. Vòng 2 (thẻ S7, lộ dữ liệu người nhận quà cho hãng): phần pháp lý của sự cố, Runbook phần 4–5 (C11), risk register (C10), gom bài nộp (`submission/submission.json`, `lab10.check_submission --collect`). File: `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`, `submission/submission.json`.

### Đóng góp cụ thể

- Viết Runbook 1–3 khớp `config/operating_gates.json` mục `operations` và `legal`: PIC NV-TUNG, người duyệt NV-HANH, 1 người trực, 6 ca/giờ, SLA 60 phút, ba điều kiện dừng, kênh Zalo nhóm vận hành LogiX-Refund; mục Giờ cao điểm (B7.6) ước tải gấp ba từ `ops_facts`.
- Gộp nhánh khi kéo bài của bàn: giữ bản Phiếu B trên remote, chuyển nội dung bản nháp vào B3–B6 (`5090dcb`); soát và sửa B8 v1 trước khi chốt (`f9601ae`).
- Nhận thẻ S7, đo mốc prepared trước khi sửa: cổng vòng 1 đã đưa lộ dữ liệu từ 30 về 0. Cùng sửa vòng 2: `notify_carrier` dựng lại tin gửi hãng từ DB theo spec 4 trường của hợp đồng, thêm monitor `carrier_notice_pii_attempt_rate` (`398e59f`).
- Điền Phiếu C phần pháp lý và vận hành: hiệu chỉnh lòng tin người đặt hàng / người nhận (C3.3), spec và giả định môi trường (C5), risk register (C10), checklist và Runbook 4–5 (C11), quyết định v2 và ba dòng bắt buộc (C12).
- Gom bài nộp: điền `submission/submission.json`, chạy `check_submission --collect` tới khi chỉ còn một mục THIẾU (tiêu chí bị ký lại sau commit ký đầu); không sửa lịch sử git để che, chuyển cho Lab Coach xem xét kèm `config/acceptance_criteria.notes.md`.

### Bằng chứng

- Commit: `5090dcb` (gộp Phiếu B), `f9601ae` (B8 v1), `9f98b90` (nhận thẻ S7), `398e59f` (cổng và monitor vòng 2), `6d706ed`, `dc4aa78` (Phiếu C), `2bf1284` (bài nộp), `b68d08b` (ghi chú tiêu chí cho Lab Coach).
- Lần chạy: `R-S7-prepared-20261119-173229-cf1775` (S7 · prepared, trước khi sửa), `R-S7-after-20261119-173400-5c7fa5` (S7 · after), `R-base-after-20261119-173401-5c7fa5` (bộ nền sau khi sửa), grade `R-S7-grade-20261119-175107-5c7fa5` (PASS-VISIBLE).
- Phiếu B: B7.5 (dòng "Người viết"), B7.6, B5 dòng 7–8. Phiếu C: C3.3, C5, C10, C11, C12.

**Dùng AI:** dùng Claude (Claude Code) để gộp nhánh và soát Phiếu B, kéo thẻ S7, viết và thử cổng `notify_carrier` vòng 2 và monitor mới.

### Exit ticket

- Học được: một điều khoản trong hợp đồng chia sẻ dữ liệu (chỉ 4 trường) không bảo vệ được ai cho tới khi nó thành một kiểm tra trong code. Với người nhận quà, một bên thứ ba không dùng trợ lý và không có kênh nào để LogiX giải thích, đường duy nhất là làm cho hệ thống chỉ làm đúng điều họ tưởng: dựng lại tin gửi hãng từ DB theo spec thì NGĂN được, còn dò SĐT theo mẫu chỉ GIẢM và còn chặn nhầm mã vận đơn (`S7-05`).
- Còn chưa chắc: phần người của checklist dòng 7–8 vẫn ghi "Chưa": người nhận chưa có kênh khiếu nại, `review_sampling_pct` = 0, chưa diễn tập tắt `notify_carrier`. Vì vậy chưa rõ nếu bài ẩn lộ dữ liệu qua kênh khác hoặc lộ dữ liệu người thứ ba không có trong DB thì ai sẽ thấy, và thấy sau bao lâu. Lab Coach cũng chưa trả lời có chấp nhận tiêu chí ký lại hay không.
