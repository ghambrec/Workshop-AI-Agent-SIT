import os
from dotenv import load_dotenv

# 1. LOAD THE ENV BEFORE ANYTHING ELSE HAPPENS!
load_dotenv()

from pathlib import Path
# from langfuse import get_client
from pydantic_ai import Agent
from app.models.order import Order
from app.services.database import (
    get_all_product_data,
    execute_order,
    update_product_price,
    apply_category_discount,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROMPT_DIR = BASE_DIR / "app/prompts"
SOUL_MD = PROMPT_DIR / "soul.md"


# langfuse = get_client()

# # Verify connection
# if langfuse.auth_check():
#     print("Langfuse client is authenticated and ready!")
# else:
#     print("Authentication failed. Please check your credentials and host.")

# Agent.instrument_all()


# ---------------------------------------------------------
# 2. DEFINE TOOLS FIRST (No decorators needed!)
# ---------------------------------------------------------


# def fetch_store_data() -> dict:
#     """Gets the current catalog, including stock, sales, and returns."""
#     return get_all_product_data()


# def place_restock_order(product_id: str, quantity: int) -> str:
#     """Places an order to restock a specific product."""
#     success = execute_order(product_id, quantity)
#     return f"Ordered {quantity} units" if success else "Failed to order"


# def adjust_price(product_id: str, new_price: float) -> str:
#     """Updates the price of a single product."""
#     success = update_product_price(product_id, new_price)
#     return f"Price updated to ${new_price}" if success else "Product not found"


# def discount_category(category: str, percentage: int) -> str:
#     """Applies a discount to an entire category (e.g., 'electronics')."""
#     items = apply_category_discount(category, percentage)
#     return (
#         f"Applied {percentage}% discount to: {', '.join(items)}"
#         if items
#         else "No items found in category"
#     )


# ---------------------------------------------------------
# 3. INITIALIZE THE AGENT
# ---------------------------------------------------------

soul_prompt = Path(SOUL_MD).read_text(encoding="utf-8")

order_agent = Agent(
    "vertexai:gemini-2.5-flash",
    output_type=Order,
    # instrument=True,
    # tools=[fetch_store_data, place_restock_order, adjust_price, discount_category],
    system_prompt=soul_prompt,
)
