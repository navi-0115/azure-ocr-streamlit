from sqlalchemy import Column, Integer, String, Text, Float, Date, TIMESTAMP, JSON
from sqlalchemy.sql import func
from models.database_config import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    invoice_type_id = Column(Integer, foreign_key=True, nullable=True)
    unified_number = Column(String(50), nullable=True)
    issue_date = Column(Date, nullable=True)
    items_id = Column(Integer, foreign_key=True)
    total_before_tax = Column(Float, nullable=True)
    tax = Column(Float, nullable=True)
    total_after_tax = Column(Float, nullable= True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

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
    
    
    class InvoiceType(Base):
        __tablename__ = "invoice_types"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String(50), nullable=False)
        created_at = Column(TIMESTAMP, nullable=False, default=func.now())
        updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())