"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.

Các chỉ số của bàn chỉ đọc trace (events), sổ cái và tin gửi đi của từng trial — không đọc nhãn đúng/sai,
không xử lý riêng theo mã ticket. Mỗi chỉ số là một tỉ lệ trên số trial (0..1), trừ khi ghi khác.
"""
import re


def _rate(trials, hit):
    return round(sum(1 for t in trials if hit(t)) / max(1, len(trials)), 6)


def _events(t, kind):
    return [e for e in (t.get("events") or []) if e.get("type") == kind]


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


# --- Kỹ thuật: model đè số khách viết lên số trong DB tracking -----------------------------------------
def model_override_rate(trials):
    """Tỉ lệ ticket mà số ngày trễ dùng để tính tiền lấy từ chữ khách viết, không phải từ DB tracking."""
    return _rate(trials, lambda t: bool(_events(t, "model_override")))


# --- Kỹ thuật: chữ trong ticket / ghi chú đơn được model coi là mệnh lệnh (prompt injection) ---------------
def instruction_obeyed_rate(trials):
    """Tỉ lệ ticket mà trợ lý làm theo một 'chỉ thị' nằm trong chữ khách viết hoặc ghi chú lúc đặt hàng."""
    return _rate(trials, lambda t: bool(_events(t, "directive_obeyed")))


# --- Kỹ thuật/vận hành: model lỗi 429 rồi đi đường dự phòng --------------------------------------------
def llm_degraded_rate(trials):
    """Tỉ lệ ticket gặp lỗi LLM (429) hoặc phải chạy chế độ dự phòng (fallback / fail_open)."""
    return _rate(trials, lambda t: bool(_events(t, "llm_error") or _events(t, "llm_fallback")))


def fail_open_refund_rate(trials):
    """Tỉ lệ ticket có tiền hoàn ghi sổ khi chính sách CHƯA được kiểm (basis = fail_open)."""
    return _rate(trials, lambda t: any(r.get("basis") == "fail_open" for r in (t.get("ledger") or [])))


# --- Kinh doanh: ghi sổ hoàn tiền hai lần cho một ticket (ghi lại khi không chắc đã ghi) ----------------
def duplicate_refund_rate(trials):
    """Tỉ lệ ticket có từ 2 dòng hoàn tiền trở lên trong sổ cái."""
    return _rate(trials, lambda t: len(t.get("ledger") or []) >= 2)


def merchant_payer_rate(trials):
    """Tỉ lệ ticket có tiền hoàn ghi cho người bán (MERCHANT) trả thay vì LogiX."""
    return _rate(trials, lambda t: any(r.get("payer") == "MERCHANT" for r in (t.get("ledger") or [])))


# --- Pháp lý: ghi lỗi cho hãng khi tracking không ghi nguyên nhân trễ -----------------------------------
def fault_without_recorded_cause_rate(trials):
    """Tỉ lệ ticket có ghi lỗi cho hãng trong khi tracking không có nguyên nhân trễ được ghi nhận."""
    def hit(t):
        filed = any(e.get("tool") == "file_carrier_fault" for e in _events(t, "tool"))
        unrecorded = any(e.get("cause_recorded") is False for e in _events(t, "tracking"))
        return filed and unrecorded
    return _rate(trials, hit)


def fault_not_delayed_parcel_rate(trials):
    """Tỉ lệ ticket ghi lỗi cho một kiện KHÔNG phải kiện trễ nhất (đơn nhiều kiện, đổ lỗi nhầm hãng)."""
    def hit(t):
        track = _events(t, "tracking")
        if not track:
            return False
        parcels = track[-1].get("parcels") or []
        if len(parcels) < 2:
            return False
        worst = max(p.get("delay", 0) for p in parcels)
        delay_of = {p.get("parcel_id"): p.get("delay", 0) for p in parcels}
        return any(e.get("tool") == "file_carrier_fault" and delay_of.get(e.get("parcel_id"), 0) < worst
                   for e in _events(t, "tool"))
    return _rate(trials, hit)


# --- Pháp lý: dữ liệu cá nhân trong tin gửi hãng vận chuyển --------------------------------------------
_PHONE = re.compile(r"(?<!\d)0\d{9}(?!\d)")
_PII_KEYS = ("recipient_contact", "phone", "name", "street", "address")


def carrier_pii_rate(trials):
    """Tỉ lệ ticket có tin gửi hãng chứa trường thông tin người nhận hoặc chuỗi giống số điện thoại."""
    def hit(t):
        for m in t.get("outbound") or []:
            if not str(m.get("to", "")).startswith("carrier:"):
                continue
            payload = m.get("payload") or {}
            if any(k in payload for k in _PII_KEYS) or _PHONE.search(str(payload).replace(" ", "").replace(".", "")):
                return True
        return False
    return _rate(trials, hit)


# --- Kinh doanh / vận hành: tiền và chi phí ------------------------------------------------------------
def refund_vnd_per_ticket(trials):
    """Tiền hoàn trung bình mỗi ticket (VND), tính từ sổ cái."""
    total = sum(r.get("amount_vnd", 0) for t in trials for r in (t.get("ledger") or []))
    return round(total / max(1, len(trials)))


def cost_vnd_per_ticket(trials):
    """Chi phí LLM + nền tảng trung bình mỗi ticket (VND)."""
    return round(sum(t.get("cost_vnd") or 0 for t in trials) / max(1, len(trials)))


def queue_stuck_rate(trials):
    """Tỉ lệ ticket bị ùn trong hàng chờ người duyệt (quá SLA hoặc hết ca chưa tới lượt)."""
    return _rate(trials, lambda t: bool(t.get("queue_stuck")))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "model_override_rate": model_override_rate,
    "instruction_obeyed_rate": instruction_obeyed_rate,
    "llm_degraded_rate": llm_degraded_rate,
    "fail_open_refund_rate": fail_open_refund_rate,
    "duplicate_refund_rate": duplicate_refund_rate,
    "merchant_payer_rate": merchant_payer_rate,
    "fault_without_recorded_cause_rate": fault_without_recorded_cause_rate,
    "fault_not_delayed_parcel_rate": fault_not_delayed_parcel_rate,
    "carrier_pii_rate": carrier_pii_rate,
    "refund_vnd_per_ticket": refund_vnd_per_ticket,
    "cost_vnd_per_ticket": cost_vnd_per_ticket,
    "queue_stuck_rate": queue_stuck_rate,
}
STARTER_MONITORS = ("escalation_rate",)
