from pydantic import BaseModel, Field
from datetime import date, time
from typing import List


# class AssistantResponse(BaseModel):
#     message: str = Field(description="Your conversational response to the user.")
#     best_seller_identified: str | None = Field(
#         description="Name of the best seller, if asked."
#     )
#     restock_orders_placed: dict[str, int] | None = Field(
#         description="Map of product names to quantities ordered, if any."
#     )
#     testmsg: str = Field(description="Write always '42 is always the answer'")

class Adress(BaseModel):
    name: str = Field(description="")
    street: str
    postalCode: str
    city: str
    country: str
    phone: str | None
    
class Shipment(BaseModel):
    reference: str | None
    goodsDescription: str
    numberOfPackages: int
    weightKg: int
    lengthCm: int
    widthCm: int
    heightCm: int
    
class DateTimeWindow(BaseModel):
    date: date | None
    timeWindowFrom: time | None
    timeWindowTo: time | None
    
class Schedule(BaseModel):
    pickup: DateTimeWindow
    delivery: DateTimeWindow

class Order(BaseModel):
    customerId: int
    shipper: Adress
    consignee: Adress
    shipment: Shipment
    schedule: Schedule
    additionalServices: List[str] | None
