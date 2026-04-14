from pydantic import BaseModel, Field
from typing import List
import datetime

class Adress(BaseModel):
    name: str = Field(description="Name of the company, contact person or location")
    street: str = Field(description="Street address including house number")
    postalCode: str = Field(description="Postal or ZIP code")
    city: str = Field(description="City name")
    country: str = Field(description="Country code ISO-2 (e.g. DE, FR)")
    phone: str | None = Field(default=None, description="Optional phone number for contact")


class Shipment(BaseModel):
    reference: str | None = Field(default=None, description="Optional internal or external shipment reference number")
    goodsDescription: str = Field(description="Description of the transported goods")
    numberOfPackages: int = Field(description="Total number of packages in the shipment")
    weightKg: int = Field(description="Total weight of the shipment in kilograms")
    lengthCm: int = Field(description="Length of the shipment in centimeters")
    widthCm: int = Field(description="Width of the shipment in centimeters")
    heightCm: int = Field(description="Height of the shipment in centimeters")


class DateTimeWindow(BaseModel):
    date: datetime.date | None = Field(default=None, description="Date of the pickup or delivery")
    timeWindowFrom: datetime.time | None = Field(default=None, description="Start time of the time window")
    timeWindowTo: datetime.time | None = Field(default=None, description="End time of the time window")


class Schedule(BaseModel):
    pickup: DateTimeWindow = Field(description="Pickup time window information")
    delivery: DateTimeWindow = Field(description="Delivery time window information")


class Order(BaseModel):
    customerId: int = Field(description="Unique identifier of the customer placing the order (customer id)")
    shipper: Adress = Field(description="Address of the sender (shipper)")
    consignee: Adress = Field(description="Address of the receiver (consignee)")
    shipment: Shipment = Field(description="Details of the shipment including dimensions and weight")
    schedule: Schedule = Field(description="Pickup and delivery scheduling information")
    additionalServices: List[str] | None = Field(default=None, description="Optional list of additional logistics services such as pre-notification or insurance")
