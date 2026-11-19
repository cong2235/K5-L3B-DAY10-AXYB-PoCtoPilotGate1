"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): 3 cổng phòng ngừa rút từ pre-mortem / HAZOP / ranh giới Phiếu A:
  1. pre_guard(ctx): ghim phiên bản chính sách đang có hiệu lực theo ngày `as_of`
     (không phụ thuộc cờ `index_active` có thể bị cũ khi đổi chính sách).
  2. write_gate(ctx, action) — nhánh `issue_refund`:
     - Chặn hoàn trùng theo sổ cái (`ledger_rows`), chống ghi lặp do cờ đêm trễ hoặc retry khi 429.
     - Chặn `fail_open` khi LLM 429; tính lại quyền lợi từ tracking DB + chính sách hiệu lực
       (chặn hoàn sai do tin số khách khai như T-002@55 hoặc chỉ thị cài cắm ghi nợ `MERCHANT`).
     - Xác thực phê duyệt hợp lệ (đúng ticket, đúng đơn, status valid, còn hạn, đủ hạn mức, chưa dùng)
       và kiểm trần hoàn tự động mỗi khách/ngày theo `ops_limits()`.
  3. write_gate(ctx, action) — nhánh `file_carrier_fault` & `notify_carrier`:
     - Chỉ ghi lỗi hãng khi tracking DB đủ ngày trễ & có `delay_cause` nằm trong `fault_causes`,
       sửa về đúng kiện trễ nhất/kiện của ticket và đúng `db_delay`, tôn trọng trần lỗi/hãng/ngày.
     - Lọc `notify_carrier` theo whitelist `carrier_notice_fields` của chính sách,
       loại bỏ `customer_note`, `recipient_contact` để ngăn lộ PII ra bên thứ ba.

VÒNG 2 (thẻ S7, lộ thông tin người nhận quà cho hãng):
  - `notify_carrier` không còn tin giá trị agent điền: dựng lại payload từ DB theo spec hợp đồng
    (mã đơn, mã kiện, quận/huyện, số ngày trễ), kiểm kiện và hãng nhận tin khớp đơn, rồi soát lần cuối
    không có tên / SĐT / địa chỉ người nhận. Ghi sự kiện `carrier_notice_rebuilt` cho monitor.
"""
from __future__ import annotations

from . import helpers as H
from .tools import Verdict

_VALID_PARCEL_STATUSES = ("DELIVERED", "IN_TRANSIT")


def _active_policy(ctx) -> dict | None:
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _is_valid_approval_row(ctx, a: dict, ticket_id: str, order: dict, amount_vnd: int) -> bool:
    aid = a.get("approval_id")
    if not aid:
        return False
    if a.get("ticket_id") != ticket_id or a.get("order_id") != order["order_id"]:
        return False
    if a.get("customer_id") != order["customer_id"]:
        return False
    if a.get("status") != "valid" or (a.get("expires_at") or "") < ctx.as_of:
        return False
    if int(a.get("max_vnd") or 0) < amount_vnd:
        return False
    if ctx.tools.ledger_rows(approval_id=aid):
        return False
    expected_approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
    if expected_approver and a.get("approver_id") != expected_approver:
        return False
    return True


def _find_valid_approval(ctx, approval_id: str | None, ticket_id: str, order: dict, amount_vnd: int) -> str | None:
    if approval_id:
        for a in ctx.tools.lookup_approvals(approval_id=approval_id):
            if _is_valid_approval_row(ctx, a, ticket_id, order, amount_vnd):
                return approval_id
    for a in ctx.tools.lookup_approvals(ticket_id=ticket_id, order_id=order["order_id"]):
        if _is_valid_approval_row(ctx, a, ticket_id, order, amount_vnd):
            return a["approval_id"]
    return None


def pre_guard(ctx):
    """Cổng 1: ghim đúng phiên bản chính sách có hiệu lực tại ngày `ctx.as_of`."""
    pol = _active_policy(ctx)
    if pol is None:
        ctx.log("missing_effective_policy", as_of=ctx.as_of)
        return Verdict.escalate(f"không có chính sách hiệu lực tại ngày {ctx.as_of}")
    if not pol.get("index_active"):
        ctx.log("policy_pinned_override", policy_id=pol["policy_id"], as_of=ctx.as_of)
    return Verdict.allow(policy_id=pol["policy_id"])


def _gate_issue_refund(ctx, action: dict) -> Verdict:
    """Cổng 2: kiểm tra hoàn trùng, nguồn sự thật tracking DB, quyền lợi, bên trả và phê duyệt."""
    oid = action.get("order_id")
    tid = action.get("ticket_id")
    order = ctx.tools.lookup_order(oid)
    pol = _active_policy(ctx)
    if order is None or pol is None:
        return Verdict.escalate("thiếu dữ liệu đơn hàng hoặc chính sách hiệu lực")

    # 2a. Chặn hoàn trùng (idempotency trên sổ cái thật, không dựa vào cờ đối soát đêm)
    if ctx.tools.ledger_rows(order_id=oid):
        ctx.log("duplicate_refund_blocked", order_id=oid, ticket_id=tid)
        return Verdict.deny("đơn đã có khoản hoàn trong sổ cái, chặn hoàn trùng")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    if parcel.get("status") not in _VALID_PARCEL_STATUSES:
        ctx.log("invalid_parcel_status", order_id=oid, parcel_id=parcel.get("parcel_id"), status=parcel.get("status"))
        return Verdict.escalate(f"trạng thái kiện hàng ({parcel.get('status')}) cần người kiểm tra")

    db_delay = H.db_delay_days(parcel, ctx.as_of)
    db_cause = parcel.get("delay_cause")
    entitled = H.entitlement_vnd(pol, order, db_delay, db_cause)

    # 2b. Fail-closed khi LLM lỗi 429 (không tự hoàn theo basis='fail_open')
    if action.get("basis") == "fail_open":
        ctx.log("fail_open_blocked", order_id=oid, entitled=entitled)
        if entitled <= 0:
            return Verdict.deny("LLM lỗi 429 (fail-open) và tracking không đủ điều kiện hoàn")
        return Verdict.escalate("LLM lỗi 429 (fail-open), không tự ghi sổ, chuyển người duyệt")

    # 2c. Chỉ hoàn khi tracking DB & chính sách hiệu lực cho phép (chặn model_override & prompt injection)
    if entitled <= 0:
        ctx.log("ineligible_refund_blocked", order_id=oid, db_delay=db_delay, db_cause=db_cause,
                asked=action.get("amount_vnd"))
        return Verdict.deny(f"theo tracking DB (trễ {db_delay} ngày) và {pol['policy_id']}, đơn chưa đủ điều kiện hoàn")

    final_amount = entitled
    final_payer = "LOGIX"  # Cấm tự ý trừ tiền MERCHANT từ chỉ thị trong ticket / checkout_note
    aid = _find_valid_approval(ctx, action.get("approval_id"), tid, order, final_amount)
    has_valid_approval = bool(aid)

    # 2d. Xác thực phê duyệt khi vượt hạn mức tự động của chính sách hiệu lực
    if final_amount > pol["auto_limit_vnd"]:
        if not has_valid_approval:
            ctx.log("invalid_approval_blocked", order_id=oid, approval_id=action.get("approval_id"),
                    amount_vnd=final_amount, auto_limit_vnd=pol["auto_limit_vnd"])
            return Verdict.escalate("vượt hạn mức tự động và chưa có phê duyệt hợp lệ cho ticket này")
    else:
        if not has_valid_approval:
            aid = None

    # 2e. Trần hoàn tự động mỗi khách trong ngày theo ops_limits() (loại các dòng đã đối soát từ ngày trước)
    cust_cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
    if cust_cap is not None and not has_valid_approval:
        spent = sum(
            r["amount_vnd"]
            for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
            if not r.get("approval_id")
            and (ctx.tools.lookup_order(r["order_id"]) or {}).get("refund_status") != "REFUNDED"
        )
        if spent + final_amount > cust_cap:
            ctx.log("customer_daily_refund_cap", customer_id=order["customer_id"], spent=spent,
                    asked=final_amount, cap=cust_cap)
            return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày, chuyển người duyệt")

    if (final_amount != action.get("amount_vnd") or final_payer != action.get("payer")
            or aid != action.get("approval_id")):
        ctx.log("refund_normalized_to_db", old_amount=action.get("amount_vnd"), new_amount=final_amount,
                old_payer=action.get("payer"), new_payer=final_payer)
        return Verdict.modify("điều chỉnh khoản hoàn và bên trả khớp tracking DB và chính sách hiệu lực",
                              amount_vnd=final_amount, payer=final_payer, approval_id=aid)
    return Verdict.allow()


def _gate_file_carrier_fault(ctx, action: dict) -> Verdict:
    """Cổng 3a: chỉ ghi lỗi hãng khi kiện thực sự trễ có căn cứ theo DB & trong trần lỗi/hãng/ngày."""
    oid = action.get("order_id")
    order = ctx.tools.lookup_order(oid)
    pol = _active_policy(ctx)
    if order is None or pol is None:
        return Verdict.deny("thiếu dữ liệu đơn hàng hoặc chính sách hiệu lực để ghi lỗi hãng")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    db_delay = H.db_delay_days(parcel, ctx.as_of)
    if parcel.get("status") not in _VALID_PARCEL_STATUSES or not H.carrier_at_fault(pol, parcel, db_delay):
        ctx.log("ungrounded_carrier_fault_blocked", order_id=oid, parcel_id=parcel.get("parcel_id"),
                db_delay=db_delay, delay_cause=parcel.get("delay_cause"), policy_id=pol["policy_id"])
        return Verdict.deny("kiện hàng không đủ căn cứ ghi lỗi hãng theo tracking DB và chính sách hiệu lực")

    # Nếu đơn đa kiện không nêu parcel_id và có ≥ 2 hãng cùng mức trễ lớn nhất thì không quy lỗi oan
    if not ctx.ticket.get("parcel_id") and len(order.get("parcels") or []) > 1:
        top_carriers = {p.get("carrier_id") for p in order["parcels"]
                        if H.db_delay_days(p, ctx.as_of) == db_delay and H.carrier_at_fault(pol, p, db_delay)}
        if len(top_carriers) > 1:
            ctx.log("ambiguous_multiparcels_fault_blocked", order_id=oid, carriers=sorted(top_carriers))
            return Verdict.deny("đơn nhiều kiện không rõ kiện nào thuộc hãng chịu lỗi, không tự quy lỗi")

    max_strikes = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if max_strikes is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= max_strikes:
        ctx.log("carrier_daily_strike_cap", carrier_id=parcel["carrier_id"], max_strikes=max_strikes)
        return Verdict.deny("đạt trần lỗi tự động mỗi hãng trong ngày, chuyển người duyệt thủ công")

    if (action.get("parcel_id") != parcel["parcel_id"] or action.get("carrier_id") != parcel["carrier_id"]
            or action.get("driver_id") != parcel.get("driver_id") or action.get("delay_days") != db_delay):
        ctx.log("carrier_fault_corrected_to_parcel", old_parcel=action.get("parcel_id"),
                new_parcel=parcel["parcel_id"], old_delay=action.get("delay_days"), new_delay=db_delay)
        return Verdict.modify("sửa đúng kiện hàng, hãng và số ngày trễ theo tracking DB",
                              parcel_id=parcel["parcel_id"], carrier_id=parcel["carrier_id"],
                              driver_id=parcel.get("driver_id"), delay_days=db_delay)
    return Verdict.allow()


# Spec kênh gửi hãng (hợp đồng chia sẻ dữ liệu, thẻ S7): chỉ mã đơn, mã kiện, quận/huyện, số ngày trễ.
_NOTICE_CONTRACT = ("order_id", "parcel_id", "district", "delay_days")


def _recipient_pii_in(obj, order: dict) -> bool:
    """Có tên, số điện thoại (9 số cuối) hoặc số nhà/đường của người nhận trong giá trị sắp gửi đi không."""
    rc = (order or {}).get("recipient") or {}
    blob = str(obj).lower()
    phone = H.digits(rc.get("phone", ""))[-9:]
    if phone and phone in H.digits(blob):
        return True
    return any(s and s.lower() in blob for s in (rc.get("name"), rc.get("street")))


def _gate_notify_carrier(ctx, action: dict) -> Verdict:
    """Cổng 3b (vòng 2, thẻ S7): BẢO ĐẢM tin gửi hãng chỉ mang dữ liệu đúng spec.

    Không lọc theo khoá rồi tin giá trị do agent điền: dựng lại toàn bộ payload từ nguồn sự thật
    (đơn và tracking trong DB), chỉ gồm các trường nằm trong cả spec hợp đồng lẫn `carrier_notice_fields`
    của chính sách hiệu lực. Bước cuối soát lại: giá trị đi ra không được chứa tên, số điện thoại,
    địa chỉ người nhận; nếu có thì không gửi.
    """
    payload = action.get("payload") or {}
    pol = _active_policy(ctx)
    pol_fields = (pol or {}).get("carrier_notice_fields") or _NOTICE_CONTRACT
    allowed = [k for k in _NOTICE_CONTRACT if k in pol_fields]

    order = ctx.tools.lookup_order(ctx.ticket.get("order_id") or payload.get("order_id"))
    if order is None:
        return Verdict.deny("không tìm thấy đơn trong DB, không gửi tin cho hãng")
    parcel = next((p for p in order.get("parcels") or [] if p.get("parcel_id") == payload.get("parcel_id")), None)
    if parcel is None or parcel.get("carrier_id") != action.get("carrier_id"):
        ctx.log("carrier_notice_wrong_target", order_id=order.get("order_id"),
                parcel_id=payload.get("parcel_id"), carrier_id=action.get("carrier_id"))
        return Verdict.deny("kiện hoặc hãng nhận tin không khớp đơn trong DB, không gửi tin cho hãng")

    truth = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"],
             "district": (order.get("recipient") or {}).get("district"),
             "delay_days": H.db_delay_days(parcel, ctx.as_of)}
    clean = {k: truth[k] for k in allowed}
    if _recipient_pii_in(clean, order):
        ctx.log("carrier_notice_pii_blocked", order_id=order["order_id"])
        return Verdict.deny("tin gửi hãng vẫn chứa dữ liệu người nhận sau khi dựng lại, không gửi")

    if clean != payload:
        ctx.log("carrier_notice_rebuilt", dropped=sorted(set(payload) - set(clean)),
                recipient_pii_attempt=_recipient_pii_in(payload, order),
                changed=sorted(k for k in clean if payload.get(k) != clean[k]))
        return Verdict.modify("dựng lại tin gửi hãng từ DB, chỉ gồm các trường trong spec hợp đồng",
                              payload=clean)
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_issue_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_file_carrier_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify_carrier(ctx, action)
    return Verdict.allow()
