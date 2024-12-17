from sqlalchemy import Column, Integer, String, Text, Float, Date, TIMESTAMP, JSON
from sqlalchemy.sql import func
from models.database_config import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    buyer_name = Column(String(255), nullable=False)
    buyer_address = Column(Text, nullable=True)
    issue_date = Column(Date, nullable=True)
    order_id = Column(String(50), nullable=True)
    items = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    subtotal = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    shipping_cost = Column(Float, nullable=True)
    outstanding_balance = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

