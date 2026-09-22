import json
import os
from decimal import Decimal
from pathlib import Path

DATA_FILE = os.environ.get("ORDER_DATA_FILE", "data/orders.json")
ORDERS = {}


def _load():
    global ORDERS
    path = Path(DATA_FILE)
    if path.exists():
        ORDERS = json.loads(path.read_text())


def _save():
    path = Path(DATA_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ORDERS, sort_keys=True, indent=2) + "\n")


def create_order(order_id, customer, total):
    if not order_id or not customer or Decimal(str(total)) <= 0:
        raise ValueError("invalid order")
    _load()
    order = {"order_id": order_id, "customer": customer, "total": str(Decimal(str(total))), "status": "created"}
    ORDERS[order_id] = order
    _save()
    return order


def get_order(order_id):
    _load()
    if order_id not in ORDERS:
        raise KeyError(order_id)
    return ORDERS[order_id]


def cancel_order(order_id):
    order = get_order(order_id)
    if order["status"] != "created":
        raise ValueError("cannot cancel")
    order["status"] = "cancelled"
    _save()
    return order
