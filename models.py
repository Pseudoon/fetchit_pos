import uuid
from datetime import datetime, date

from sqlalchemy import Column, String, Integer, Float, DateTime, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base  # assumes fetch.it already has database.py with Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("order_date", "daily_number", name="uq_order_date_daily_number"),)

    id = Column(Integer, primary_key=True, index=True)  # internal DB id, never shown to customer

    order_date = Column(Date, default=date.today, index=True)
    daily_number = Column(Integer, nullable=False)  # the simple "1, 2, 3..." id, resets each day

    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    delivery_spot = Column(String, nullable=False, default="Hostel Circle")
    time_slot = Column(String, nullable=False, default="12:00 PM – 2:00 PM")

    subtotal = Column(Float, nullable=False, default=0.0)
    delivery_charge = Column(Float, nullable=False, default=20.0)  # flat ₹20 per order
    total = Column(Float, nullable=False, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)  # price per unit

    order = relationship("Order", back_populates="items")