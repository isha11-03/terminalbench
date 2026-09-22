import json
from decimal import Decimal
from pathlib import Path
from .domain import Order


class JsonOrderRepository:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self):
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text())

    def get(self, order_id):
        item = self._read().get(order_id)
        if item is None:
            return None
        return Order(item["order_id"], item["customer"], Decimal(item["total"]), item["status"])

    def save(self, order):
        records = self._read()
        records[order.order_id] = {
            "order_id": order.order_id,
            "customer": order.customer,
            "total": str(order.total),
            "status": order.status,
        }
        self.path.write_text(json.dumps(records, sort_keys=True, indent=2) + "\n")
