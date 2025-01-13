from sqlalchemy import Column, Integer, String, Float, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.database_config import Base

class InvoiceItemsAssociation(Base):
    __tablename__ = "invoice_items_association"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    invoice_item_id = Column(Integer, ForeignKey("invoice_items.id"), nullable=False)

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    invoice_type_id = Column(Integer, nullable=True)
    unified_number = Column(String(50), nullable=True)
    issue_date = Column(Date, nullable=True)
    total_before_tax = Column(Float, nullable=True)
    tax = Column(Float, nullable=True)
    total_after_tax = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

    # Define the relationship with InvoiceItems
    invoice_items = relationship(
        "InvoiceItems",
        secondary="invoice_items_association",
        back_populates="invoices"
    )

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

    # Define the relationship back to Invoice
    invoices = relationship(
        "Invoice",
        secondary="invoice_items_association",
        back_populates="invoice_items"
    )
