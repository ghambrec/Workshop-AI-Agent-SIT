from pydantic import BaseModel, Field


class AssistantResponse(BaseModel):
    message: str = Field(description="Your conversational response to the user.")
    best_seller_identified: str | None = Field(
        description="Name of the best seller, if asked."
    )
    restock_orders_placed: dict[str, int] | None = Field(
        description="Map of product names to quantities ordered, if any."
    )
