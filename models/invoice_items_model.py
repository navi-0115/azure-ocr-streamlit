from sqlalchemy import Column, Integer, String, Text, Float, Date, TIMESTAMP, JSON
from sqlalchemy.sql import func
from models.database_init import Base

class InvoiceItems(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())