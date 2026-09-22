import ast
import json
from decimal import Decimal

import pytest

from order_app import cancel_order, create_order, get_order, reset
from order_app.domain import OrderError
from order_app.repository import JsonOrderRepository
from order_app.service import DefaultOrderService, NotFoundError


def test_public_api_and_persistence(tmp_path, monkeypatch):
    path = tmp_path / "orders.json"
    monkeypatch.setenv("ORDER_DATA_FILE", str(path))
    reset()
    order = create_order("o-1", "Ada", "12.5")
    assert order.total == Decimal("12.50")
    assert get_order("o-1") == order
    reset()
    assert get_order("o-1") == order
    assert json.loads(path.read_text())["o-1"]["status"] == "created"


def test_cancel_is_idempotent_and_missing_is_clear(tmp_path):
    service = DefaultOrderService(JsonOrderRepository(str(tmp_path / "orders.json")))
    service.create("o-2", "Lin", "3")
    assert service.cancel("o-2").status == "cancelled"
    assert service.cancel("o-2").status == "cancelled"
    with pytest.raises(NotFoundError):
        service.get("missing")


@pytest.mark.parametrize("args", [("", "Ada", "1"), ("x", "", "1"), ("x", "Ada", "0"), ("x", "Ada", "bad")])
def test_invalid_orders(args):
    service = DefaultOrderService(JsonOrderRepository("/tmp/task08-test-orders.json"))
    with pytest.raises((ValueError, OrderError)):
        service.create(*args)


def test_fake_repository_is_enough_for_service():
    class Fake:
        def __init__(self): self.items = {}
        def get(self, key): return self.items.get(key)
        def save(self, order): self.items[order.order_id] = order

    fake = Fake()
    service = DefaultOrderService(fake)
    assert service.create("o-3", "Grace", "4.00").customer == "Grace"
    assert service.get("o-3").total == Decimal("4.00")


def test_dependency_direction_has_no_infrastructure_imports_in_core():
    for name in ("domain.py", "ports.py", "service.py"):
        tree = ast.parse((__import__("pathlib").Path(__file__).parents[1] / "src" / "order_app" / name).read_text())
        imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
        imported = {n.module for n in imports if isinstance(n, ast.ImportFrom)}
        imported.update(alias.name for n in imports if isinstance(n, ast.Import) for alias in n.names)
        assert not {"order_app.repository", "json", "os"} & imported


def test_cli_entrypoint(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("ORDER_DATA_FILE", str(tmp_path / "orders.json"))
    reset()
    from order_app.cli import main
    assert main(["create", "o-4", "Turing", "2.25"]) == 0
    assert capsys.readouterr().out.strip() == "o-4 Turing 2.25 created"
