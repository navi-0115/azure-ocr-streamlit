from sqlalchemy import Column, Integer, String, Text, Float, Date, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.database_init import Base

class InvoiceTypes(Base):
    __tablename__ = "invoice_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    
    invoices = relationship("Invoice", back_populates="invoice_type") 