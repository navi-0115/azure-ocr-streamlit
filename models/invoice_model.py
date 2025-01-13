from sqlalchemy import Column, Integer, String, Text, Float, Date, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.database_init import Base
from models.invoice_items_association import InvoiceItemsAssociation

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    invoice_type_id = Column(Integer, ForeignKey("invoice_types.id"), nullable=True)
    unified_number = Column(String(50), nullable=True)
    issue_date = Column(Date, nullable=True)
    invoice_items_id = Column(Integer, foreign_key=True)
    total_before_tax = Column(Float, nullable=True)
    tax = Column(Float, nullable=True)
    total_after_tax = Column(Float, nullable= True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    
    #relationship
    invoice_type = relationship("InvoiceTypes", back_populates="invoices")
    invoice_items = relationship("InvoiceItems", secondary=InvoiceItemsAssociation, back_populates="invoices")

