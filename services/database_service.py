from datetime import datetime
from models.database_config import get_db_session
from models.invoice_model import Invoice

def store_invoice_data(data):
    session = get_db_session()
    try:
        
        invoice = Invoice(
            invoice_number=data.get("invoice_number"),
            unified_number=data.get("unified_number"),
            issue_date=data.get("issue_date"),
            items=data.get("items"),
            tax=data.get("tax"),
            amount=data.get("amount"),
            total_amount=data.get("total_amount"),
        )
        session.add(invoice)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()