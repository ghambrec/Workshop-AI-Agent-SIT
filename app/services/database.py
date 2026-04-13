import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SEED_FILE = DATA_DIR / "initial_store.json"
DB_FILE = DATA_DIR / "store.json"


def reset_database():
    """Copies the pristine seed file over the working database file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if SEED_FILE.exists():
        shutil.copy(SEED_FILE, DB_FILE)
        print("🧹 Database reset from initial_store.json!")
    else:
        print("⚠️ Warning: initial_store.json not found!")


def get_all_product_data() -> dict:
    if not DB_FILE.exists():
        reset_database()

    with open(DB_FILE, "r") as file:
        return json.load(file)


def execute_order(product_id: str, quantity: int) -> bool:
    if not DB_FILE.exists():
        return False

    with open(DB_FILE, "r") as file:
        store_db = json.load(file)

    if product_id in store_db:
        store_db[product_id]["stock_level"] += quantity
        with open(DB_FILE, "w") as file:
            json.dump(store_db, file, indent=4)
        return True

    return False


def update_product_price(product_id: str, new_price: float) -> bool:
    """Permanently updates a product's price in the JSON database."""
    with open(DB_FILE, "r") as file:
        store_db = json.load(file)

    if product_id in store_db:
        store_db[product_id]["price"] = round(new_price, 2)
        with open(DB_FILE, "w") as file:
            json.dump(store_db, file, indent=4)
        return True
    return False


def apply_category_discount(category: str, percentage: int) -> list[str]:
    """Applies a percentage discount to all items in a specific category."""
    with open(DB_FILE, "r") as file:
        store_db = json.load(file)

    updated_items = []
    multiplier = (100 - percentage) / 100

    for pid, details in store_db.items():
        if details.get("category") == category:
            details["price"] = round(details["price"] * multiplier, 2)
            updated_items.append(details["name"])

    with open(DB_FILE, "w") as file:
        json.dump(store_db, file, indent=4)
    return updated_items
