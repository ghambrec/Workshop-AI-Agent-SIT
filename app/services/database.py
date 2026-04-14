import json
# import shutil
from pathlib import Path
from app.models.order import Order

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
JSON_FILE = DATA_DIR / "order.json"

def write_order(order: Order):
    order_json = order.model_dump_json(indent=4)
    with open(JSON_FILE, "w") as file:
        file.write(order_json)
