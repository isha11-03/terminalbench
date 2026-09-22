from decimal import Decimal


def expected_create(order_id, customer, total):
    if not order_id or not customer:
        raise ValueError("order_id and customer are required")
    amount = Decimal(str(total))
    if amount <= 0:
        raise ValueError("total must be positive")
    return {"order_id": order_id, "customer": customer, "total": amount.quantize(Decimal("0.01")), "status": "created"}


def expected_cancel(order):
    if order["status"] == "cancelled":
        return order
    if order["status"] != "created":
        raise ValueError("only created orders can be cancelled")
    return {**order, "status": "cancelled"}
