import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    data_file: str


def load_settings(environ=None) -> Settings:
    values = os.environ if environ is None else environ
    return Settings(values.get("ORDER_DATA_FILE", "data/orders.json"))
