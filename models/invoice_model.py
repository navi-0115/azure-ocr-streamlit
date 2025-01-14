from sqlalchemy import Column, Integer, String, Float, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.database_config import Base

class InvoiceItemsAssociation(Base):
    __tablename__ = "invoice_items_association"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    invoice_item_id = Column(Integer, ForeignKey("invoice_items.id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    
    invoice = relationship("Invoice", back_populates="invoice_items_association")
    invoice_item = relationship("InvoiceItem", back_populates="invoice_items_association")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), nullable=False)
    invoice_type_id = Column(Integer, ForeignKey("invoice_types.id", ondelete="CASCADE"), nullable=True)
    unified_number = Column(String(50), nullable=True)
    issue_date = Column(Date, nullable=True)
    total_before_tax = Column(Float, nullable=True)
    tax = Column(Float, nullable=True)
    total_after_tax = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

    # Define the relationship
    invoice_types = relationship("InvoiceTypes", back_populates="invoices")
    
    invoice_items_association = relationship("InvoiceItemsAssociation", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

    invoice_items_association = relationship("InvoiceItemsAssociation", back_populates="invoice_item")

class InvoiceTypes(Base):
    __tablename__ = "invoice_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
        
    invoices = relationship("Invoice", back_populates="invoice_types")
