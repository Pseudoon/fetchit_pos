from typing import List, Literal
from datetime import date, datetime
from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    item_name: str
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)


class OrderItemOut(BaseModel):
    item_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True


class DailySummaryOut(BaseModel):
    date: date
    total_orders: int
    total_subtotal: float
    total_delivery_charges: float
    total_revenue: float


class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    delivery_spot: Literal["Admin Circle", "Hostel Circle"]
    time_slot: Literal["7:00 PM – 8:00 PM", "10:00 PM – 11:00 PM"]
    items: List[OrderItemCreate]


class OrderOut(BaseModel):
    daily_number: int
    order_date: date
    customer_name: str
    customer_phone: str
    delivery_spot: str
    time_slot: str
    subtotal: float
    delivery_charge: float
    total: float
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True