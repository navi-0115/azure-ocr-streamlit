from models.database import get_db_session
from models.invoice import Invoice

def store_invoice_data(data):
    session = get_db_session()
    try:
        invoice = Invoice(
            invoice_number=data["invoice_number"],
            date=data["date"],
            items=str(data["items"])  # Store as JSON or text
        )
        session.add(invoice)
        session.commit()
    finally:
        session.close()
