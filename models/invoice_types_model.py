from sqlalchemy import Column, Integer, String, Text, Float, Date, TIMESTAMP, JSON
from sqlalchemy.sql import func
from models.database_init import Base

class InvoiceType(Base):
    __tablename__ = "invoice_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())