import os
from dotenv import load_dotenv

# 1. LOAD THE ENV BEFORE ANYTHING ELSE HAPPENS!
load_dotenv()

from langfuse import get_client
from pydantic_ai import Agent
from app.models.retail import AssistantResponse
from app.services.database import (
    get_all_product_data,
    execute_order,
    update_product_price,
    apply_category_discount,
)


langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")


Agent.instrument_all()

# ---------------------------------------------------------
# 2. DEFINE TOOLS FIRST (No decorators needed!)
# ---------------------------------------------------------


def fetch_store_data() -> dict:
    """Gets the current catalog, including stock, sales, and returns."""
    return get_all_product_data()


def place_restock_order(product_id: str, quantity: int) -> str:
    """Places an order to restock a specific product."""
    success = execute_order(product_id, quantity)
    return f"Ordered {quantity} units" if success else "Failed to order"


def adjust_price(product_id: str, new_price: float) -> str:
    """Updates the price of a single product."""
    success = update_product_price(product_id, new_price)
    return f"Price updated to ${new_price}" if success else "Product not found"


def discount_category(category: str, percentage: int) -> str:
    """Applies a discount to an entire category (e.g., 'electronics')."""
    items = apply_category_discount(category, percentage)
    return (
        f"Applied {percentage}% discount to: {', '.join(items)}"
        if items
        else "No items found in category"
    )


# ---------------------------------------------------------
# 3. INITIALIZE THE AGENT
# ---------------------------------------------------------

retail_agent = Agent(
    "vertexai:gemini-2.5-flash",
    output_type=AssistantResponse,
    instrument=True,
    tools=[fetch_store_data, place_restock_order, adjust_price, discount_category],
    system_prompt=(
        "You are a helpful, conversational retail assistant. You answer questions about our products "
        "and help manage the store using the following rules:\n"
        "1. BEST SELLER: The best-selling product is the one with the highest sales number.\n"
        "2. RESTOCKING: If an item's stock is below 5, you must restock it.\n"
        "3. ORDER QUANTITY: When restocking, order a quantity equal to exactly 10% of that item's total sales.\n"
        "4. COMMUNICATION STYLE: Always reply in a friendly, natural tone. If you place restock orders, "
        "you MUST explain your reasoning to the user in the message. Detail exactly which items you ordered, "
        "why you chose them (e.g., low stock), and explain the math behind the specific amount you ordered."
    ),
)
