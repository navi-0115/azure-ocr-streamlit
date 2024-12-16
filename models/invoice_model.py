from sqlalchemy import Column, Integer, String, Text
from models.database_config import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, index=True)
    date = Column(String, index=True)
    items = Column(Text)  # Store item details as a JSON string or plain text
