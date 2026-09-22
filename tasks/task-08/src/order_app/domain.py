from dataclasses import dataclass
from decimal import Decimal


class OrderError(ValueError):
    pass


@dataclass(frozen=True)
class Order:
    order_id: str
    customer: str
    total: Decimal
    status: str = "created"


def create_order(order_id: str, customer: str, total: Decimal) -> Order:
    if not order_id or not customer:
        raise OrderError("order_id and customer are required")
    if total <= 0:
        raise OrderError("total must be positive")
    return Order(order_id, customer, total.quantize(Decimal("0.01")))


def cancel(order: Order) -> Order:
    if order.status == "cancelled":
        return order
    if order.status != "created":
        raise OrderError("only created orders can be cancelled")
    return Order(order.order_id, order.customer, order.total, "cancelled")
