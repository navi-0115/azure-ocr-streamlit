from sqlalchemy import Column, Integer, String, Text, Float, Date, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.database_init import Base

class InvoiceItemsAssociation(Base):
    __tablename__ = "invoice_items_association"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"),nullable=False)
    invoice_item_id = Column(Integer, ForeignKey("invoice_items.id"),nullable=False)