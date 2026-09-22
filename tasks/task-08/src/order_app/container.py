from .config import load_settings
from .repository import JsonOrderRepository
from .service import DefaultOrderService


def build_service(environ=None):
    settings = load_settings(environ)
    return DefaultOrderService(JsonOrderRepository(settings.data_file))
