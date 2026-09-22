from decimal import Decimal, InvalidOperation
from .domain import OrderError, cancel, create_order
from .ports import OrderRepository


class NotFoundError(LookupError):
    pass


class DefaultOrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create(self, order_id: str, customer: str, total: str):
        try:
            amount = Decimal(str(total))
        except (InvalidOperation, ValueError):
            raise OrderError("total must be numeric") from None
        order = create_order(order_id, customer, amount)
        self.repository.save(order)
        return order

    def get(self, order_id: str):
        order = self.repository.get(order_id)
        if order is None:
            raise NotFoundError(f"order {order_id} not found")
        return order

    def cancel(self, order_id: str):
        order = cancel(self.get(order_id))
        self.repository.save(order)
        return order
