from .container import build_service

_service = None


def _get_service():
    global _service
    if _service is None:
        _service = build_service()
    return _service


def reset():
    global _service
    _service = None


def create_order(order_id, customer, total):
    return _get_service().create(order_id, customer, total)


def get_order(order_id):
    return _get_service().get(order_id)


def cancel_order(order_id):
    return _get_service().cancel(order_id)
